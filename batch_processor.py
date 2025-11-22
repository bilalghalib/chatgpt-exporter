#!/usr/bin/env python3
"""
Incremental Theory of Mind Builder with Knowledge Graph Preparation
Processes conversations in batches, extracting SAREC beliefs, values cards, and book material
All outputs are graph-ready with complete provenance tracking
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import hashlib
from anthropic import Anthropic
import time


class GraphReadyAnalysis:
    """
    Structures all analysis outputs for future knowledge graph ingestion
    Every entity, belief, and relationship tracked with provenance
    """

    def __init__(self, output_dir: str = "/home/user/chatgpt-exporter/analysis_batches"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Master registries (prevent duplication)
        self.processed_conversations = set()
        self.belief_registry = {}  # belief_id → canonical belief
        self.values_card_registry = {}  # card_id → canonical card
        self.tag_registry = {}  # tag → metadata

        # Knowledge graph preparation
        self.nodes = []  # All entities (beliefs, values, concepts)
        self.edges = []  # All relationships

        # Load existing state if resuming
        self.load_state()

    def load_state(self):
        """Load existing analysis state to avoid duplication"""
        state_file = self.output_dir / "master_state.json"
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
                self.processed_conversations = set(state.get('processed_conversations', []))
                self.belief_registry = state.get('belief_registry', {})
                self.values_card_registry = state.get('values_card_registry', {})
                self.tag_registry = state.get('tag_registry', {})
                self.nodes = state.get('nodes', [])
                self.edges = state.get('edges', [])

    def save_state(self):
        """Save current state"""
        state = {
            'processed_conversations': list(self.processed_conversations),
            'belief_registry': self.belief_registry,
            'values_card_registry': self.values_card_registry,
            'tag_registry': self.tag_registry,
            'nodes': self.nodes,
            'edges': self.edges,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.output_dir / "master_state.json", 'w') as f:
            json.dump(state, f, indent=2)


class BatchSelector:
    """
    Selects conversations for processing using smart algorithm:
    - Prioritize recent (recency bias)
    - Prioritize high depth (substance bias)
    - Include random samples (diversity)
    """

    def __init__(self, conversations_dir: Path):
        self.conversations_dir = conversations_dir
        self.metadata_cache = {}

    def load_metadata(self, conversation_file: Path) -> Dict:
        """Load or generate metadata for a conversation"""
        # Check if organized conversation exists
        conv_id = conversation_file.stem
        organized_meta = self.conversations_dir.parent / "conversations" / conv_id / "metadata.json"

        if organized_meta.exists():
            with open(organized_meta, 'r') as f:
                return json.load(f)

        # Otherwise, calculate on the fly
        with open(conversation_file, 'r') as f:
            data = json.load(f)

        filename = conversation_file.name
        parts = filename.split("_")

        message_count = 0
        if "messages" in data:
            message_count = len(data["messages"])
        elif "mapping" in data:
            message_count = len(data["mapping"])

        return {
            "id": conv_id,
            "date": parts[0],
            "depth_score": message_count / 10,
            "file_path": str(conversation_file)
        }

    def select_batch(self,
                     batch_size: int = 50,
                     processed_ids: set = None,
                     weights: Dict = None) -> List[Dict]:
        """
        Select conversations for next batch

        weights: {
            'recent': 0.4,     # Favor recent conversations
            'depth': 0.4,      # Favor substantive conversations
            'random': 0.2      # Include diversity
        }
        """
        if weights is None:
            weights = {'recent': 0.4, 'depth': 0.4, 'random': 0.2}

        if processed_ids is None:
            processed_ids = set()

        # Get all conversations
        all_convos = list(self.conversations_dir.glob("*.json"))

        # Load metadata for all
        print(f"📊 Loading metadata for {len(all_convos)} conversations...")
        scored_convos = []

        for conv_file in all_convos:
            conv_id = conv_file.stem

            # Skip if already processed
            if conv_id in processed_ids:
                continue

            meta = self.load_metadata(conv_file)

            # Calculate composite score
            recency_score = self.calculate_recency_score(meta['date'])
            depth_score = meta['depth_score']
            random_score = hash(conv_id) % 100 / 100  # Deterministic randomness

            composite_score = (
                recency_score * weights['recent'] +
                depth_score * weights['depth'] +
                random_score * weights['random']
            )

            scored_convos.append({
                **meta,
                'recency_score': recency_score,
                'composite_score': composite_score
            })

        # Sort by composite score and take top N
        scored_convos.sort(key=lambda x: x['composite_score'], reverse=True)
        selected = scored_convos[:batch_size]

        print(f"✓ Selected {len(selected)} conversations for batch")
        print(f"  Avg recency: {sum(c['recency_score'] for c in selected) / len(selected):.2f}")
        print(f"  Avg depth: {sum(c['depth_score'] for c in selected) / len(selected):.2f}")

        return selected

    def calculate_recency_score(self, date_str: str) -> float:
        """Convert date to recency score (0-1, where 1 is most recent)"""
        try:
            # Parse date
            date = datetime.strptime(date_str, "%Y-%m-%d")
            now = datetime.now()

            # Days ago
            days_ago = (now - date).days

            # Score: 1.0 for today, decays to 0 over ~3 years
            score = max(0, 1 - (days_ago / 1095))  # 1095 days = 3 years
            return score
        except:
            return 0.5  # Default for unparseable dates


class ProvenanceTracker:
    """
    Tracks exact source of every piece of data
    Enables: "Where did this belief come from?" queries
    """

    @staticmethod
    def create_provenance(
        conversation_id: str,
        message_index: int = None,
        quote: str = None,
        batch_number: int = None
    ) -> Dict:
        """Create provenance record"""

        prov = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "batch": batch_number
        }

        if message_index is not None:
            prov["message_index"] = message_index
            prov["loc"] = f"messages[{message_index}]"

        if quote:
            prov["quote"] = quote[:200]  # Truncate long quotes
            prov["quote_hash"] = hashlib.sha256(quote.encode()).hexdigest()[:16]

        return prov


class SARECBeliefExtractor:
    """
    Extract SAREC-formatted beliefs from conversations
    Knowledge, Values, Goals, Needs
    """

    SAREC_PROMPT = """You are analyzing a conversation to build a Theory of Mind about Bilal Ghalib.

Your task: Extract SAREC assessments (Structured Assessment, Reasoning, Evidence, Confidence) about:
1. What Bilal KNOWS (knowledge, skills, expertise)
2. What Bilal CARES ABOUT (values, priorities, passions)
3. What Bilal IS TRYING TO DO (goals, projects, aspirations)
4. What Bilal NEEDS (gaps, challenges, support)

CONVERSATION:
{conversation}

INSTRUCTIONS:
Analyze the conversation and extract beliefs. For each belief:
- belief_id: unique ID (e.g., "bilal.knowledge.solar_iraq_training")
- category: "knowledge", "values", "goals", or "needs"
- subcategory: specific domain (e.g., "solar_energy", "spiritual_integration")
- claim: clear statement (e.g., "Bilal has expertise in designing solar training for conflict zones")
- score: 0.0-1.0 (strength of this belief based on this conversation)
- reasoning: WHY you believe this (2-3 sentences)
- evidence: array of specific quotes from the conversation that support this
- confidence: 0.0-1.0 (how certain you are)
- book_worthy: true/false (is this compelling book material?)

IMPORTANT:
- Only extract beliefs with STRONG evidence in THIS conversation
- Quote EXACT snippets from the conversation (not summaries)
- Focus on what BILAL said (user messages), not AI responses
- Each evidence quote should be 50-200 chars
- Only include high-confidence beliefs (>0.5)
- Mark book_worthy=true for especially compelling insights, frameworks, or stories

Return JSON array of beliefs:
[
  {{
    "belief_id": "bilal.knowledge.domain",
    "category": "knowledge|values|goals|needs",
    "subcategory": "specific_domain",
    "claim": "Clear statement",
    "score": 0.8,
    "reasoning": "Why you believe this",
    "evidence": [
      {{"quote": "exact quote from conversation", "speaker": "user|assistant"}},
      {{"quote": "another quote", "speaker": "user"}}
    ],
    "confidence": 0.85,
    "book_worthy": false
  }}
]

Return ONLY valid JSON array, no other text."""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.cost_tracker = {"input_tokens": 0, "output_tokens": 0, "total_cost": 0.0}

    def extract_message_content(self, message: dict) -> str:
        """Extract text from various message formats"""
        content = message.get("content", "")

        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            if "parts" in content:
                parts = content["parts"]
                if isinstance(parts, list):
                    return " ".join(str(p) for p in parts)
                return str(parts)
            elif "text" in content:
                return content["text"]
        elif isinstance(content, list):
            return " ".join(
                str(part.get("text", part.get("content", "")))
                for part in content if isinstance(part, dict)
            )

        return str(content)

    def extract_conversation_content(self, conversation_data: dict) -> str:
        """Convert conversation to readable format for LLM"""

        lines = []
        lines.append(f"TITLE: {conversation_data.get('title', 'Untitled')}")
        lines.append(f"DATE: {conversation_data.get('created_at', 'Unknown')}")
        lines.append("")

        if "messages" in conversation_data:
            for msg in conversation_data["messages"]:
                role = msg.get("role", "unknown")
                content = self.extract_message_content(msg)

                if content.strip():
                    speaker = "BILAL" if role in ["user", "human"] else "AI"
                    lines.append(f"[{speaker}]: {content.strip()}")
                    lines.append("")

        return "\n".join(lines)

    def extract_beliefs_from_conversation(self, conversation_data: Dict, conversation_id: str) -> Dict:
        """
        Use Claude API to extract SAREC-formatted beliefs
        """

        # Convert conversation to readable format
        conversation_content = self.extract_conversation_content(conversation_data)

        # Skip very short conversations
        if len(conversation_content) < 200:
            return {
                "conversation_id": conversation_id,
                "beliefs": {"knowledge": [], "values": [], "goals": [], "needs": []},
                "extraction_metadata": {
                    "method": "llm_analysis",
                    "model": "claude-sonnet-4-20250514",
                    "timestamp": datetime.now().isoformat(),
                    "skipped": "too_short"
                }
            }

        try:
            prompt = self.SAREC_PROMPT.format(conversation=conversation_content[:100000])  # Limit to 100k chars

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.0,  # Deterministic for analysis
                messages=[{"role": "user", "content": prompt}]
            )

            # Track cost
            self.cost_tracker["input_tokens"] += response.usage.input_tokens
            self.cost_tracker["output_tokens"] += response.usage.output_tokens
            self.cost_tracker["total_cost"] += (
                response.usage.input_tokens * 0.003 / 1000 +  # $3 per million
                response.usage.output_tokens * 0.015 / 1000   # $15 per million
            )

            # Parse response
            content = response.content[0].text

            # Try to extract JSON (sometimes model adds explanation)
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                beliefs_list = json.loads(json_str)

                # Group by category
                beliefs_by_category = {"knowledge": [], "values": [], "goals": [], "needs": []}
                for belief in beliefs_list:
                    category = belief.get("category", "knowledge")
                    beliefs_by_category[category].append(belief)

                return {
                    "conversation_id": conversation_id,
                    "beliefs": beliefs_by_category,
                    "extraction_metadata": {
                        "method": "llm_analysis",
                        "model": "claude-sonnet-4-20250514",
                        "timestamp": datetime.now().isoformat(),
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                        "cost": self.cost_tracker["total_cost"]
                    }
                }
            else:
                print(f"   ⚠️  No JSON found in response for {conversation_id}")
                return {
                    "conversation_id": conversation_id,
                    "beliefs": {"knowledge": [], "values": [], "goals": [], "needs": []},
                    "extraction_metadata": {
                        "method": "llm_analysis",
                        "model": "claude-sonnet-4-20250514",
                        "timestamp": datetime.now().isoformat(),
                        "error": "no_json_in_response"
                    }
                }

        except Exception as e:
            print(f"   ⚠️  Error analyzing {conversation_id}: {e}")
            return {
                "conversation_id": conversation_id,
                "beliefs": {"knowledge": [], "values": [], "goals": [], "needs": []},
                "extraction_metadata": {
                    "method": "llm_analysis",
                    "model": "claude-sonnet-4-20250514",
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e)
                }
            }


class ValuesCardGenerator:
    """
    Generate Come Alive values cards from conversations
    Track attention policies and sources of meaning
    """

    VALUES_PROMPT = """You are analyzing a conversation to identify sources of meaning for Bilal Ghalib using the Come Alive framework.

Come Alive Framework:
- **CAPs** (Constitutive Actions): Activities that feel intrinsically meaningful, energizing, "coming alive"
- **IAPs** (Instrumental Actions): Activities done as means to an end
- **Attention Policies**: What Bilal consistently pays attention to, what draws his focus
- **Tensions as Guides**: Contradictions and tensions reveal what matters most

CONVERSATION:
{conversation}

INSTRUCTIONS:
Identify values cards - distinct sources of meaning. For each card:
- title: short name for this source of meaning (e.g., "Integrating Spiritual Practice with Tech Work")
- cap_indicators: quotes showing CAP behavior (feeling alive, intrinsic motivation)
- attention_policies: what Bilal consistently notices/cares about in this domain
- ground_truth: specific quotes, stories, or examples
- tensions: contradictions or challenges that reveal values
- energy_level: 0.0-1.0 (how energized Bilal seems about this)

IMPORTANT:
- Look for what makes Bilal feel ALIVE, not just what he's good at
- Identify TENSIONS - they reveal what matters
- Quote exact text from Bilal (user messages)
- Focus on recurring patterns of attention
- Mark energy_level based on enthusiasm, depth, engagement

Return JSON array of values cards:
[
  {{
    "title": "Source of meaning",
    "cap_indicators": ["quote showing intrinsic motivation", "quote showing feeling alive"],
    "attention_policies": ["what consistently draws attention", "what Bilal notices/cares about"],
    "ground_truth": {{
      "quotes": ["exact quote 1", "exact quote 2"],
      "stories": ["brief summary of story/example"],
      "recurring_themes": ["pattern 1", "pattern 2"]
    }},
    "tensions": ["contradiction or challenge that reveals values"],
    "energy_level": 0.8
  }}
]

Return ONLY valid JSON array, no other text."""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.cost_tracker = {"input_tokens": 0, "output_tokens": 0, "total_cost": 0.0}

    def extract_message_content(self, message: dict) -> str:
        """Extract text from various message formats"""
        content = message.get("content", "")

        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            if "parts" in content:
                parts = content["parts"]
                if isinstance(parts, list):
                    return " ".join(str(p) for p in parts)
                return str(parts)
            elif "text" in content:
                return content["text"]
        elif isinstance(content, list):
            return " ".join(
                str(part.get("text", part.get("content", "")))
                for part in content if isinstance(part, dict)
            )

        return str(content)

    def extract_conversation_content(self, conversation_data: dict) -> str:
        """Convert conversation to readable format for LLM"""

        lines = []
        lines.append(f"TITLE: {conversation_data.get('title', 'Untitled')}")
        lines.append(f"DATE: {conversation_data.get('created_at', 'Unknown')}")
        lines.append("")

        if "messages" in conversation_data:
            for msg in conversation_data["messages"]:
                role = msg.get("role", "unknown")
                content = self.extract_message_content(msg)

                if content.strip():
                    speaker = "BILAL" if role in ["user", "human"] else "AI"
                    lines.append(f"[{speaker}]: {content.strip()}")
                    lines.append("")

        return "\n".join(lines)

    def generate_values_cards(
        self,
        conversation_data: Dict,
        conversation_id: str
    ) -> List[Dict]:
        """
        Extract values cards using Come Alive framework
        """

        # Convert conversation to readable format
        conversation_content = self.extract_conversation_content(conversation_data)

        # Skip very short conversations
        if len(conversation_content) < 200:
            return []

        try:
            prompt = self.VALUES_PROMPT.format(conversation=conversation_content[:100000])

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}]
            )

            # Track cost
            self.cost_tracker["input_tokens"] += response.usage.input_tokens
            self.cost_tracker["output_tokens"] += response.usage.output_tokens
            self.cost_tracker["total_cost"] += (
                response.usage.input_tokens * 0.003 / 1000 +
                response.usage.output_tokens * 0.015 / 1000
            )

            # Parse response
            content = response.content[0].text

            # Extract JSON
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                values_cards = json.loads(json_str)

                # Add metadata to each card
                for card in values_cards:
                    card_id = f"vc_{hashlib.sha256(card['title'].encode()).hexdigest()[:8]}"
                    card["id"] = card_id
                    card["conversation_id"] = conversation_id
                    card["first_noticed"] = datetime.now().isoformat()
                    card["status"] = "emerging"
                    card["node_type"] = "values_card"

                return values_cards
            else:
                print(f"   ⚠️  No JSON found in values card response for {conversation_id}")
                return []

        except Exception as e:
            print(f"   ⚠️  Error generating values cards for {conversation_id}: {e}")
            return []


class KnowledgeGraphPrep:
    """
    Prepare all data for knowledge graph ingestion
    Nodes: beliefs, values, concepts, conversations
    Edges: supports, contradicts, evolves_to, related_to
    """

    @staticmethod
    def create_node(
        node_id: str,
        node_type: str,
        properties: Dict,
        provenance: List[Dict]
    ) -> Dict:
        """Create a graph node"""

        return {
            "id": node_id,
            "type": node_type,
            "properties": properties,
            "provenance": provenance,
            "created_at": datetime.now().isoformat()
        }

    @staticmethod
    def create_edge(
        from_id: str,
        to_id: str,
        relationship: str,
        properties: Dict = None,
        provenance: List[Dict] = None
    ) -> Dict:
        """Create a graph edge"""

        return {
            "from": from_id,
            "to": to_id,
            "relationship": relationship,
            "properties": properties or {},
            "provenance": provenance or [],
            "created_at": datetime.now().isoformat()
        }


class BatchProcessor:
    """
    Main orchestrator for processing batches
    """

    def __init__(self, conversations_dir: Path, output_dir: Path, api_key: str = None):
        self.conversations_dir = conversations_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

        self.selector = BatchSelector(conversations_dir)
        self.analysis = GraphReadyAnalysis(output_dir)
        self.current_batch = None

        # Initialize LLM extractors (only if API key provided)
        self.api_key = api_key
        if api_key:
            self.belief_extractor = SARECBeliefExtractor(api_key)
            self.values_generator = ValuesCardGenerator(api_key)
        else:
            self.belief_extractor = None
            self.values_generator = None

    def process_batch(self, batch_number: int, batch_size: int = 50):
        """Process a batch of conversations"""

        print(f"\n{'='*80}")
        print(f"BATCH {batch_number} - Processing {batch_size} conversations")
        print(f"{'='*80}\n")

        # Select conversations
        selected = self.selector.select_batch(
            batch_size=batch_size,
            processed_ids=self.analysis.processed_conversations
        )

        if not selected:
            print("✓ No more conversations to process!")
            return

        # Create batch directory
        batch_dir = self.output_dir / f"batch_{batch_number:03d}"
        batch_dir.mkdir(exist_ok=True)

        # Save batch manifest
        manifest = {
            "batch_number": batch_number,
            "conversation_count": len(selected),
            "conversations": [c['id'] for c in selected],
            "started_at": datetime.now().isoformat()
        }

        with open(batch_dir / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"📁 Batch directory: {batch_dir}")
        print(f"📝 Processing {len(selected)} conversations...")

        # Process each conversation
        batch_results = {
            "beliefs": [],
            "values_cards": [],
            "book_material": [],
            "nodes": [],
            "edges": []
        }

        for i, conv_meta in enumerate(selected, 1):
            conv_id = conv_meta['id']
            print(f"\n[{i}/{len(selected)}] {conv_id[:60]}...")

            # Load conversation
            conv_file = Path(conv_meta['file_path'])
            with open(conv_file, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)

            # Extract SAREC beliefs (if API key provided)
            if self.belief_extractor:
                print(f"   → Extracting SAREC beliefs...")
                beliefs_result = self.belief_extractor.extract_beliefs_from_conversation(
                    conversation_data,
                    conv_id
                )
                batch_results["beliefs"].append(beliefs_result)

                # Identify book material
                for category in ["knowledge", "values", "goals", "needs"]:
                    for belief in beliefs_result["beliefs"].get(category, []):
                        if belief.get("book_worthy", False):
                            batch_results["book_material"].append({
                                "conversation_id": conv_id,
                                "belief_id": belief["belief_id"],
                                "category": category,
                                "claim": belief["claim"],
                                "evidence": belief["evidence"],
                                "confidence": belief["confidence"]
                            })

                # Create graph nodes for beliefs
                for category in ["knowledge", "values", "goals", "needs"]:
                    for belief in beliefs_result["beliefs"].get(category, []):
                        node = KnowledgeGraphPrep.create_node(
                            node_id=belief["belief_id"],
                            node_type=f"belief_{category}",
                            properties=belief,
                            provenance=[ProvenanceTracker.create_provenance(
                                conv_id,
                                batch_number=batch_number,
                                quote=belief.get("evidence", [{}])[0].get("quote", "") if belief.get("evidence") else ""
                            )]
                        )
                        batch_results["nodes"].append(node)

                print(f"   ✓ Extracted {sum(len(beliefs_result['beliefs'][cat]) for cat in ['knowledge', 'values', 'goals', 'needs'])} beliefs")

            # Generate values cards (if API key provided)
            if self.values_generator:
                print(f"   → Generating values cards...")
                values_cards = self.values_generator.generate_values_cards(
                    conversation_data,
                    conv_id
                )
                batch_results["values_cards"].extend(values_cards)

                # Create graph nodes for values cards
                for card in values_cards:
                    node = KnowledgeGraphPrep.create_node(
                        node_id=card["id"],
                        node_type="values_card",
                        properties=card,
                        provenance=[ProvenanceTracker.create_provenance(
                            conv_id,
                            batch_number=batch_number
                        )]
                    )
                    batch_results["nodes"].append(node)

                print(f"   ✓ Generated {len(values_cards)} values cards")

            # Mark as processed
            self.analysis.processed_conversations.add(conv_id)

            # Rate limiting (Claude has 50 req/min limit)
            if self.api_key and i % 40 == 0:
                print(f"\n   ⏸️  Rate limit pause...")
                time.sleep(5)

        # Save batch results
        with open(batch_dir / "results.json", 'w') as f:
            json.dump(batch_results, f, indent=2)

        # Update master state
        self.analysis.save_state()

        # Generate batch report
        self.generate_batch_report(batch_number, batch_dir, batch_results)

        print(f"\n✓ Batch {batch_number} complete!")
        print(f"  Processed: {len(selected)} conversations")
        print(f"  Total processed: {len(self.analysis.processed_conversations)}")

    def generate_batch_report(self, batch_number: int, batch_dir: Path, results: Dict):
        """Generate human-readable batch report"""

        # Calculate statistics
        total_beliefs = sum(
            len(b.get('beliefs', {}).get(cat, []))
            for b in results.get('beliefs', [])
            for cat in ['knowledge', 'values', 'goals', 'needs']
        )

        beliefs_by_category = {
            "knowledge": sum(len(b.get('beliefs', {}).get('knowledge', [])) for b in results.get('beliefs', [])),
            "values": sum(len(b.get('beliefs', {}).get('values', [])) for b in results.get('beliefs', [])),
            "goals": sum(len(b.get('beliefs', {}).get('goals', [])) for b in results.get('beliefs', [])),
            "needs": sum(len(b.get('beliefs', {}).get('needs', [])) for b in results.get('beliefs', []))
        }

        # Cost tracking
        total_cost = 0.0
        if self.belief_extractor:
            total_cost += self.belief_extractor.cost_tracker.get("total_cost", 0.0)
        if self.values_generator:
            total_cost += self.values_generator.cost_tracker.get("total_cost", 0.0)

        report = f"""# Batch {batch_number} Analysis Report

## Summary
- **Conversations processed**: {len(results.get('beliefs', []))}
- **Total beliefs extracted**: {total_beliefs}
  - Knowledge: {beliefs_by_category['knowledge']}
  - Values: {beliefs_by_category['values']}
  - Goals: {beliefs_by_category['goals']}
  - Needs: {beliefs_by_category['needs']}
- **Values cards generated**: {len(results.get('values_cards', []))}
- **Book material flagged**: {len(results.get('book_material', []))}

## Knowledge Graph Additions
- **New nodes**: {len(results.get('nodes', []))}
- **New edges**: {len(results.get('edges', []))}

## Cost Analysis
- **Total API cost**: ${total_cost:.3f}
- **Avg cost per conversation**: ${total_cost / max(len(results.get('beliefs', [])), 1):.3f}

## Book Material Highlights

{self._format_book_material(results.get('book_material', []))}

## Values Cards Discovered

{self._format_values_cards(results.get('values_cards', []))}

## Next Steps
1. Review extracted beliefs for accuracy
2. Validate values cards
3. Assess book material readiness
4. Plan next batch (incremental processing)

---
Generated: {datetime.now().isoformat()}
"""

        with open(batch_dir / "REPORT.md", 'w') as f:
            f.write(report)

    def _format_book_material(self, book_material: List[Dict], top_n: int = 10) -> str:
        """Format top book material for report"""
        if not book_material:
            return "No book material flagged in this batch."

        sorted_material = sorted(book_material, key=lambda x: x.get("confidence", 0), reverse=True)
        lines = []

        for i, item in enumerate(sorted_material[:top_n], 1):
            lines.append(f"{i}. **{item['claim']}** (confidence: {item.get('confidence', 0):.2f})")
            lines.append(f"   - Category: {item['category']}")
            lines.append(f"   - Conversation: {item['conversation_id'][:60]}...")
            lines.append("")

        return "\n".join(lines)

    def _format_values_cards(self, values_cards: List[Dict], top_n: int = 10) -> str:
        """Format top values cards for report"""
        if not values_cards:
            return "No values cards generated in this batch."

        sorted_cards = sorted(values_cards, key=lambda x: x.get("energy_level", 0), reverse=True)
        lines = []

        for i, card in enumerate(sorted_cards[:top_n], 1):
            lines.append(f"{i}. **{card.get('title', 'Untitled')}** (energy: {card.get('energy_level', 0):.2f})")
            lines.append(f"   - Conversation: {card.get('conversation_id', 'unknown')[:60]}...")
            if card.get('tensions'):
                lines.append(f"   - Key tension: {card['tensions'][0] if card['tensions'] else 'N/A'}")
            lines.append("")

        return "\n".join(lines)


def main():
    """Run batch processing"""

    import sys

    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python3 batch_processor.py <ANTHROPIC_API_KEY> [batch_number] [batch_size]")
        print("\nExample: python3 batch_processor.py sk-ant-... 1 50")
        print("  (processes batch 1 with 50 conversations)")
        print("\nTo test without API (dry run):")
        print("  python3 batch_processor.py test 1 5")
        sys.exit(1)

    api_key = sys.argv[1] if sys.argv[1] != "test" else None
    batch_number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    conversations_dir = Path("/home/user/chatgpt-exporter/exported_conversations")
    output_dir = Path("/home/user/chatgpt-exporter/analysis_batches")

    print(f"\n{'='*80}")
    print(f"BATCH PROCESSOR - Incremental Theory of Mind Builder")
    print(f"{'='*80}")
    if api_key:
        print(f"✓ API key provided - LLM analysis enabled")
    else:
        print(f"⚠️  No API key (test mode) - Will create structure without LLM analysis")
    print(f"Batch: {batch_number}, Size: {batch_size}")
    print(f"{'='*80}\n")

    processor = BatchProcessor(conversations_dir, output_dir, api_key=api_key)

    # Process batch
    processor.process_batch(batch_number=batch_number, batch_size=batch_size)

    print(f"\n{'='*80}")
    print(f"BATCH {batch_number} COMPLETE - System ready for incremental processing")
    print(f"{'='*80}")
    print(f"\nOutputs saved to: {output_dir}/batch_{batch_number:03d}/")
    print(f"Master state: {output_dir}/master_state.json")

    if api_key and processor.belief_extractor:
        total_cost = processor.belief_extractor.cost_tracker.get("total_cost", 0.0)
        if processor.values_generator:
            total_cost += processor.values_generator.cost_tracker.get("total_cost", 0.0)
        print(f"\nTotal cost: ${total_cost:.3f}")
        print(f"Avg cost per conversation: ${total_cost / max(batch_size, 1):.3f}")

    print(f"\nTo process next batch:")
    print(f"  python3 batch_processor.py {sys.argv[1]} {batch_number + 1} {batch_size}")


if __name__ == "__main__":
    main()
