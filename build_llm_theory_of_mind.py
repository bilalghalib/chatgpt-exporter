#!/usr/bin/env python3
"""
LLM-Based Theory of Mind Builder
Uses Claude API to deeply analyze conversations and build SAREC assessments
"""

import json
import os
from pathlib import Path
from anthropic import Anthropic
import time
from typing import Dict, List
import hashlib

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

IMPORTANT:
- Only extract beliefs with STRONG evidence in THIS conversation
- Quote EXACT snippets from the conversation (not summaries)
- Focus on what BILAL said (user messages), not AI responses
- Each evidence quote should be 50-200 chars
- Only include high-confidence beliefs (>0.5)

Return JSON array of beliefs:
[
  {
    "belief_id": "bilal.knowledge.domain",
    "category": "knowledge|values|goals|needs",
    "subcategory": "specific_domain",
    "claim": "Clear statement",
    "score": 0.8,
    "reasoning": "Why you believe this",
    "evidence": [
      {"quote": "exact quote from conversation", "speaker": "user|assistant"},
      {"quote": "another quote", "speaker": "user"}
    ],
    "confidence": 0.85
  }
]

Return ONLY valid JSON array, no other text.
"""


class LLMTheoryOfMindBuilder:
    """Build Theory of Mind using LLM analysis of each conversation"""

    def __init__(self, api_key: str, output_dir: str = "/home/user/chatgpt-exporter/llm_theory_of_mind"):
        self.client = Anthropic(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Storage
        self.beliefs = {}  # belief_id -> aggregated belief
        self.provenance = {}  # conversation_id -> beliefs extracted
        self.cost_tracker = {"input_tokens": 0, "output_tokens": 0, "total_cost": 0.0}

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

    def analyze_conversation_with_llm(self, conversation_id: str, conversation_content: str) -> List[Dict]:
        """Use Claude to analyze conversation and extract SAREC beliefs"""

        try:
            prompt = SAREC_PROMPT.format(conversation=conversation_content[:100000])  # Limit to 100k chars

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
                beliefs = json.loads(json_str)
                return beliefs
            else:
                print(f"   ⚠️  No JSON found in response for {conversation_id}")
                return []

        except Exception as e:
            print(f"   ⚠️  Error analyzing {conversation_id}: {e}")
            return []

    def aggregate_belief(self, new_belief: dict, conversation_id: str):
        """Aggregate new belief with existing beliefs"""

        belief_id = new_belief["belief_id"]

        if belief_id not in self.beliefs:
            # New belief
            self.beliefs[belief_id] = {
                **new_belief,
                "conversation_count": 1,
                "conversations": [conversation_id],
                "all_evidence": new_belief["evidence"],
                "score_history": [{"conversation": conversation_id, "score": new_belief["score"]}]
            }
        else:
            # Update existing belief
            existing = self.beliefs[belief_id]

            # Weighted average of scores (more recent = higher weight)
            old_score = existing["score"]
            new_score = new_belief["score"]
            existing["score"] = (old_score * 0.7 + new_score * 0.3)

            # Aggregate confidence (take max)
            existing["confidence"] = max(existing["confidence"], new_belief["confidence"])

            # Merge evidence
            existing["all_evidence"].extend(new_belief["evidence"])

            # Track conversations
            existing["conversation_count"] += 1
            existing["conversations"].append(conversation_id)
            existing["score_history"].append({"conversation": conversation_id, "score": new_score})

    def process_all_conversations(self, export_dir: Path, limit: int = None):
        """Process conversations one by one with LLM analysis"""

        conversation_files = list(export_dir.glob("*.json"))
        total = limit if limit else len(conversation_files)

        print(f"🧠 LLM-Based Theory of Mind Builder")
        print(f"Processing {total} conversations with Claude Sonnet 4.5")
        print("=" * 80)

        for i, filepath in enumerate(conversation_files[:total], 1):
            try:
                # Read conversation
                with open(filepath, 'r', encoding='utf-8') as f:
                    conversation_data = json.load(f)

                conversation_id = filepath.stem

                # Convert to readable format
                conversation_content = self.extract_conversation_content(conversation_data)

                # Skip very short conversations
                if len(conversation_content) < 200:
                    continue

                print(f"\n[{i}/{total}] {conversation_id[:60]}...")

                # Analyze with LLM
                beliefs = self.analyze_conversation_with_llm(conversation_id, conversation_content)

                print(f"   → Extracted {len(beliefs)} beliefs")
                print(f"   → Cost so far: ${self.cost_tracker['total_cost']:.3f}")

                # Store provenance
                self.provenance[conversation_id] = {
                    "title": conversation_data.get("title", "Untitled"),
                    "date": filepath.name.split("_")[0],
                    "beliefs_extracted": len(beliefs),
                    "belief_ids": [b["belief_id"] for b in beliefs]
                }

                # Aggregate beliefs
                for belief in beliefs:
                    self.aggregate_belief(belief, conversation_id)

                # Rate limiting (Claude has 50 req/min limit)
                if i % 40 == 0:
                    print(f"\n   ⏸️  Rate limit pause (40 requests)...")
                    time.sleep(5)

                # Checkpoint every 20 conversations
                if i % 20 == 0:
                    self.save_checkpoint()

            except Exception as e:
                print(f"   ⚠️  Error processing {filepath.name}: {e}")

        print("\n" + "=" * 80)
        print("✅ Processing complete!")
        print(f"Total beliefs: {len(self.beliefs)}")
        print(f"Total cost: ${self.cost_tracker['total_cost']:.2f}")

    def save_checkpoint(self):
        """Save current state"""

        checkpoint = {
            "beliefs": self.beliefs,
            "provenance": self.provenance,
            "cost_tracker": self.cost_tracker
        }

        with open(self.output_dir / "checkpoint.json", 'w') as f:
            json.dump(checkpoint, f, indent=2)

    def generate_outputs(self):
        """Generate organized outputs"""

        # Group by category
        by_category = {"knowledge": {}, "values": {}, "goals": {}, "needs": {}}

        for belief_id, belief in self.beliefs.items():
            category = belief["category"]
            by_category[category][belief_id] = belief

        # Save by category
        for category, beliefs in by_category.items():
            cat_dir = self.output_dir / category
            cat_dir.mkdir(exist_ok=True)

            with open(cat_dir / "all.json", 'w') as f:
                json.dump(beliefs, f, indent=2)

        # Generate README
        readme = f"""# LLM-Based Theory of Mind: Bilal Ghalib

**Generated using Claude Sonnet 4.5 analysis**

## Summary

- **Total beliefs extracted**: {len(self.beliefs)}
- **Conversations analyzed**: {len(self.provenance)}
- **Total cost**: ${self.cost_tracker['total_cost']:.2f}

## Beliefs by Category

### Knowledge ({len(by_category['knowledge'])} beliefs)
{self._format_top_beliefs(by_category['knowledge'])}

### Values ({len(by_category['values'])} beliefs)
{self._format_top_beliefs(by_category['values'])}

### Goals ({len(by_category['goals'])} beliefs)
{self._format_top_beliefs(by_category['goals'])}

### Needs ({len(by_category['needs'])} beliefs)
{self._format_top_beliefs(by_category['needs'])}

## Provenance

All beliefs include:
- Exact quotes from conversations
- Conversation IDs
- LLM reasoning
- Confidence scores

See individual category files for full details.
"""

        with open(self.output_dir / "README.md", 'w') as f:
            f.write(readme)

        # Save provenance
        with open(self.output_dir / "provenance.json", 'w') as f:
            json.dump(self.provenance, f, indent=2)

        # Save cost tracker
        with open(self.output_dir / "cost_report.json", 'w') as f:
            json.dump(self.cost_tracker, f, indent=2)

    def _format_top_beliefs(self, beliefs: dict, top_n: int = 10) -> str:
        """Format top beliefs for README"""

        sorted_beliefs = sorted(beliefs.values(), key=lambda x: x["score"], reverse=True)
        lines = []

        for belief in sorted_beliefs[:top_n]:
            lines.append(f"- **{belief['claim']}** (score: {belief['score']:.2f}, {belief['conversation_count']} convos, confidence: {belief['confidence']:.2f})")

        return "\n".join(lines)


def main():
    """Run LLM-based Theory of Mind builder"""

    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 build_llm_theory_of_mind.py <ANTHROPIC_API_KEY> [limit]")
        print("\nExample: python3 build_llm_theory_of_mind.py sk-ant-... 50")
        print("  (processes 50 conversations)")
        sys.exit(1)

    api_key = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

    export_dir = Path("/home/user/chatgpt-exporter/exported_conversations")
    builder = LLMTheoryOfMindBuilder(api_key)

    # Process conversations
    builder.process_all_conversations(export_dir, limit=limit)

    # Generate outputs
    builder.generate_outputs()

    print(f"\n✅ Outputs saved to: {builder.output_dir}")
    print(f"   - README.md: Summary and top beliefs")
    print(f"   - knowledge/all.json: All knowledge beliefs")
    print(f"   - values/all.json: All value beliefs")
    print(f"   - goals/all.json: All goal beliefs")
    print(f"   - needs/all.json: All need beliefs")
    print(f"   - provenance.json: Which conversations contributed what")
    print(f"   - cost_report.json: API usage and costs")


if __name__ == "__main__":
    main()
