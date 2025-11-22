#!/usr/bin/env python3
"""
Unified Knowledge Graph Extraction - Window-Based Orchestrator

Implements 6-phase extraction pipeline:
1. Metadata & Structure
2. Thematic Analysis
3. Pattern-Based Extraction
4. LLM-Powered Analysis (Adaptive)
5. Knowledge Graph Construction
6. Checkpointing & Export
"""

import json
import os
import re
import glob
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import time
import uuid

# Optional anthropic import
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  anthropic module not installed - LLM analysis disabled")

# Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
CONVERSATIONS_DIR = './exported_conversations'
OUTPUT_DIR = './unified_extraction_output'
CHECKPOINT_DIR = f'{OUTPUT_DIR}/checkpoints'
BATCH_SIZE = 20
RATE_LIMIT_DELAY = 1.5  # seconds between API calls

# Window configuration (passed as argument)
WINDOW_CONFIG = {
    1: {'name': 'top-down', 'range': (0, 1172), 'description': 'Chronologically earliest'},
    2: {'name': 'bottom-up', 'range': (2345, 3516), 'description': 'Chronologically latest'},
    3: {'name': 'random', 'range': 'random_1173', 'description': 'Random sample from middle'}
}

# Node and Relationship Types (from CONSOLIDATION_DESIGN.md)
NODE_TYPES = [
    'conversation', 'idea', 'project', 'concept', 'technology', 'value',
    'insight', 'question', 'person', 'tag', 'decision', 'assumption',
    'problem', 'solution', 'pattern', 'goal'
]

RELATIONSHIP_TYPES = [
    'solves', 'challenges', 'questions', 'supports', 'contradicts', 'validates',
    'refutes', 'derives_from', 'leads_to', 'evolves_into', 'supersedes',
    'implements', 'answers', 'exemplifies', 'categorizes', 'broader_than',
    'narrower_than', 'related_to', 'bridges', 'mentions', 'creates',
    'depends_on', 'inspired_by', 'strengthens'
]

# Deep Themes - 6 Dimensions
DEEP_THEMES = {
    'work_domains': {
        'bloom': ['bloom', 'education technology', 'pedagogical', 'student', 'teacher'],
        'solar': ['solar', 'photovoltaic', 'pv', 'renewable', 'energy'],
        'education': ['learning', 'curriculum', 'pedagogy', 'assessment'],
        'technology': ['software', 'web', 'app', 'development', 'programming'],
        'personal': ['personal', 'reflection', 'growth', 'spiritual']
    },
    'activity_types': {
        'problem_solving': ['debug', 'fix', 'error', 'issue', 'troubleshoot'],
        'creation': ['create', 'build', 'design', 'develop', 'implement'],
        'analysis': ['analyze', 'evaluate', 'assess', 'review', 'examine'],
        'strategy': ['plan', 'strategy', 'roadmap', 'vision', 'goal'],
        'learning': ['learn', 'understand', 'explore', 'study', 'research']
    },
    'technical_stack': {
        'web': ['html', 'css', 'javascript', 'react', 'vue', 'frontend'],
        'backend': ['python', 'node', 'api', 'database', 'server'],
        'ai_ml': ['ai', 'machine learning', 'gpt', 'claude', 'llm', 'neural'],
        'data': ['data', 'analytics', 'visualization', 'chart', 'graph'],
        'devops': ['docker', 'kubernetes', 'deployment', 'ci/cd', 'aws']
    },
    'personal_professional': {
        'career': ['job', 'career', 'interview', 'resume', 'professional'],
        'growth': ['improve', 'skill', 'learn', 'development', 'practice'],
        'spiritual': ['spiritual', 'faith', 'prayer', 'islam', 'reflection'],
        'health': ['health', 'fitness', 'exercise', 'diet', 'wellbeing'],
        'relationships': ['family', 'friend', 'relationship', 'social']
    },
    'geographic_cultural': {
        'lebanon': ['lebanon', 'lebanese', 'beirut', 'arabic'],
        'mena': ['mena', 'middle east', 'arab', 'regional'],
        'uk': ['uk', 'london', 'british', 'england'],
        'global': ['international', 'global', 'worldwide']
    },
    'communication_medium': {
        'writing': ['write', 'blog', 'article', 'documentation', 'content'],
        'code': ['code', 'programming', 'script', 'function', 'algorithm'],
        'visual': ['design', 'image', 'visualization', 'ui', 'graphic'],
        'teaching': ['teach', 'explain', 'tutorial', 'guide', 'lesson']
    }
}

# SAREC Framework patterns
SAREC_PATTERNS = {
    'knowledge': {
        'solar_energy': ['solar', 'pv', 'photovoltaic', 'renewable energy', 'mppt'],
        'web_development': ['react', 'javascript', 'html', 'css', 'frontend', 'backend'],
        'ai_ml': ['gpt', 'claude', 'llm', 'machine learning', 'neural network'],
        'data_visualization': ['chart', 'graph', 'd3', 'visualization', 'plotly'],
        'education_pedagogy': ['pedagogical', 'curriculum', 'assessment', 'bloom taxonomy']
    },
    'values': {
        'impact_over_profit': ['impact', 'social good', 'community', 'help'],
        'spiritual_integration': ['spiritual', 'faith', 'prayer', 'islam', 'reflection'],
        'education_empowerment': ['empower', 'student agency', 'learner-centered'],
        'quality_excellence': ['quality', 'excellence', 'best practice', 'rigorous'],
        'cultural_sensitivity': ['cultural', 'context', 'local', 'appropriate']
    }
}


class KnowledgeGraphExtractor:
    """Unified extraction orchestrator"""

    def __init__(self, window: int):
        self.window = window
        self.config = WINDOW_CONFIG[window]
        self.client = None
        if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
            self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Knowledge graph state
        self.graph = {
            'nodes': {},
            'relationships': [],
            'temporal_chains': [],
            'indexes': {
                'by_type': defaultdict(list),
                'by_conversation': defaultdict(list),
                'by_date': defaultdict(list),
                'by_tag': defaultdict(list),
                'by_concept': defaultdict(list)
            }
        }

        # Tracking
        self.stats = {
            'conversations_processed': 0,
            'batches_completed': 0,
            'nodes_created': 0,
            'nodes_merged': 0,
            'relationships_created': 0,
            'api_calls': 0,
            'cost_usd': 0.0,
            'start_time': datetime.now().isoformat()
        }

        # Ensure output directories exist
        Path(OUTPUT_DIR).mkdir(exist_ok=True)
        Path(CHECKPOINT_DIR).mkdir(exist_ok=True)
        Path(f'{OUTPUT_DIR}/analytics').mkdir(exist_ok=True)
        Path(f'{OUTPUT_DIR}/provenance').mkdir(exist_ok=True)

    def get_conversation_files(self) -> List[str]:
        """Get conversation files for this window"""
        all_files = sorted(glob.glob(f'{CONVERSATIONS_DIR}/*.json'))

        if self.window == 3:  # Random sample
            # TODO: Implement random sampling from middle range
            import random
            random.seed(42)  # Reproducible
            middle = all_files[1173:2345]
            return sorted(random.sample(middle, 1173))
        else:
            start, end = self.config['range']
            return all_files[start:end+1]

    def load_checkpoint(self) -> Optional[int]:
        """Load checkpoint if exists, return last completed batch number"""
        checkpoint_file = f'{CHECKPOINT_DIR}/window{self.window}_checkpoint.json'
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                self.graph = checkpoint['graph']
                self.stats = checkpoint['stats']
                print(f"✅ Resumed from checkpoint: batch {checkpoint['last_batch']}")
                return checkpoint['last_batch']
        return None

    def save_checkpoint(self, batch_num: int, last_conv_id: str):
        """Save checkpoint"""
        checkpoint = {
            'window': self.window,
            'last_batch': batch_num,
            'last_conversation_id': last_conv_id,
            'timestamp': datetime.now().isoformat(),
            'graph': self.graph,
            'stats': self.stats
        }
        checkpoint_file = f'{CHECKPOINT_DIR}/window{self.window}_checkpoint.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    # PHASE 1: Metadata & Structure
    def extract_metadata(self, conv: Dict) -> Dict:
        """Extract conversation metadata"""
        messages = conv.get('messages', [])
        user_msgs = [m for m in messages if m.get('role') == 'user']
        assistant_msgs = [m for m in messages if m.get('role') == 'assistant']

        return {
            'id': conv.get('id'),
            'title': conv.get('title', 'Untitled'),
            'source': conv.get('source', 'unknown'),
            'created_at': conv.get('created_at'),
            'updated_at': conv.get('updated_at'),
            'message_count': len(messages),
            'user_message_count': len(user_msgs),
            'assistant_message_count': len(assistant_msgs),
            'avg_user_message_length': sum(len(m.get('content', '')) for m in user_msgs) / max(len(user_msgs), 1),
            'avg_assistant_message_length': sum(len(m.get('content', '')) for m in assistant_msgs) / max(len(assistant_msgs), 1),
            'total_characters': sum(len(m.get('content', '')) for m in messages)
        }

    # PHASE 2: Thematic Analysis
    def analyze_themes(self, conv: Dict, metadata: Dict) -> Dict[str, List[str]]:
        """Apply multi-dimensional thematic categorization"""
        text = f"{metadata['title']} {' '.join(m.get('content', '') for m in conv.get('messages', []))}"
        text_lower = text.lower()

        themes = {}
        for dimension, categories in DEEP_THEMES.items():
            themes[dimension] = []
            for category, keywords in categories.items():
                if any(kw in text_lower for kw in keywords):
                    themes[dimension].append(category)

        return themes

    # PHASE 3: Pattern-Based Extraction (SAREC)
    def extract_patterns(self, conv: Dict, metadata: Dict) -> Dict:
        """Pattern-based entity and belief extraction"""
        text = ' '.join(m.get('content', '') for m in conv.get('messages', []) if m.get('role') == 'user')
        text_lower = text.lower()

        knowledge = {}
        for domain, keywords in SAREC_PATTERNS['knowledge'].items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                knowledge[domain] = {
                    'score': score,
                    'confidence': min(score / 5.0, 1.0)
                }

        values = {}
        for value, keywords in SAREC_PATTERNS['values'].items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                values[value] = {
                    'score': score,
                    'confidence': min(score / 3.0, 1.0)
                }

        return {
            'knowledge': knowledge,
            'values': values
        }

    # PHASE 4: LLM Analysis (Adaptive - called only when needed)
    def llm_extract_entities(self, conv: Dict, metadata: Dict) -> Optional[Dict]:
        """LLM-powered entity extraction (adaptive - only for substantial conversations)"""
        if not self.client:
            return None

        # Adaptive rule: Only run on conversations with >10 messages or >2000 chars
        if metadata['message_count'] < 10 and metadata['total_characters'] < 2000:
            return None

        # Build conversation text
        conv_text = f"Title: {metadata['title']}\n\n"
        for msg in conv.get('messages', [])[:20]:  # Limit to first 20 messages for cost
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')[:500]  # Limit message length
            conv_text += f"{role.upper()}: {content}\n\n"

        prompt = f"""Analyze this conversation and extract knowledge graph entities.

{conv_text}

Extract:
1. **Ideas**: Seed ideas, proposals, hypotheses mentioned
2. **Concepts**: Abstract concepts discussed (max 5)
3. **Technologies**: Specific tools, frameworks, platforms mentioned
4. **Questions**: Important questions asked
5. **Insights**: Key realizations or aha moments
6. **Decisions**: Decisions made or choices considered
7. **Problems**: Problems identified
8. **Solutions**: Solutions proposed

For each entity, provide:
- type: (idea, concept, technology, question, insight, decision, problem, solution)
- label: Short descriptive label (2-5 words)
- description: Brief description (1 sentence)
- confidence: 0-1 score
- evidence_quote: Direct quote from conversation (if available)

Return as JSON:
{{
  "entities": [
    {{"type": "concept", "label": "Solar energy optimization", "description": "...", "confidence": 0.9, "evidence_quote": "..."}},
    ...
  ],
  "relationships": [
    {{"source_label": "...", "target_label": "...", "type": "solves", "confidence": 0.8}},
    ...
  ]
}}

Focus on quality over quantity. Only extract entities with confidence > 0.6."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",  # Using Haiku for cost efficiency
                max_tokens=2000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            self.stats['api_calls'] += 1
            self.stats['cost_usd'] += 0.002  # Approximate Haiku cost

            # Parse JSON from response
            content = response.content[0].text
            # Extract JSON from markdown code blocks if present
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            return json.loads(content)

        except Exception as e:
            print(f"⚠️  LLM extraction error: {e}")
            return None

    # PHASE 5: Knowledge Graph Construction
    def create_node(self, node_type: str, label: str, properties: Dict, conversation_id: str) -> str:
        """Create or merge a node in the knowledge graph"""
        # Generate deterministic ID based on type + label
        node_id = f"node_{hashlib.md5(f'{node_type}:{label.lower()}'.encode()).hexdigest()[:12]}"

        if node_id in self.graph['nodes']:
            # Merge with existing node
            existing = self.graph['nodes'][node_id]
            existing['properties']['confidence'] = max(
                existing['properties'].get('confidence', 0),
                properties.get('confidence', 0)
            )
            existing['provenance']['source_conversations'].append(conversation_id)
            existing['provenance']['source_conversations'] = list(set(existing['provenance']['source_conversations']))
            self.stats['nodes_merged'] += 1
        else:
            # Create new node
            self.graph['nodes'][node_id] = {
                'id': node_id,
                'type': node_type,
                'label': label,
                'properties': properties,
                'provenance': {
                    'source_conversations': [conversation_id],
                    'extracted_by': f"window{self.window}",
                    'created_at': datetime.now().isoformat()
                }
            }
            self.stats['nodes_created'] += 1
            self.graph['indexes']['by_type'][node_type].append(node_id)

        # Update indexes
        self.graph['indexes']['by_conversation'][conversation_id].append(node_id)

        return node_id

    def create_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Dict):
        """Create or strengthen a relationship"""
        # Check if relationship exists
        existing = None
        for rel in self.graph['relationships']:
            if (rel['source'] == source_id and
                rel['target'] == target_id and
                rel['type'] == rel_type):
                existing = rel
                break

        if existing:
            # Strengthen existing relationship
            existing['weight'] += 1
            existing['properties']['strengthened_count'] = existing.get('weight', 1)
        else:
            # Create new relationship
            rel_id = f"rel_{uuid.uuid4().hex[:12]}"
            self.graph['relationships'].append({
                'id': rel_id,
                'type': rel_type,
                'source': source_id,
                'target': target_id,
                'weight': 1,
                'properties': properties
            })
            self.stats['relationships_created'] += 1

    def process_conversation(self, conv: Dict, batch_id: str) -> Dict:
        """Process a single conversation through all 6 phases"""
        # Phase 1: Metadata
        metadata = self.extract_metadata(conv)

        # Phase 2: Themes
        themes = self.analyze_themes(conv, metadata)

        # Phase 3: Pattern extraction
        patterns = self.extract_patterns(conv, metadata)

        # Phase 4: LLM extraction (adaptive)
        llm_entities = self.llm_extract_entities(conv, metadata)

        # Phase 5: Knowledge graph construction
        conv_id = metadata['id']

        # Create conversation node
        conv_node_id = self.create_node(
            'conversation',
            metadata['title'],
            {
                'source': metadata['source'],
                'created_at': metadata['created_at'],
                'message_count': metadata['message_count'],
                'themes': themes,
                'confidence': 1.0
            },
            conv_id
        )

        # Create nodes from pattern extraction
        for domain, data in patterns['knowledge'].items():
            if data['confidence'] > 0.6:
                tech_node_id = self.create_node(
                    'technology',
                    domain.replace('_', ' ').title(),
                    {
                        'domain': domain,
                        'confidence': data['confidence'],
                        'extraction_method': 'pattern'
                    },
                    conv_id
                )
                self.create_relationship(
                    conv_node_id,
                    tech_node_id,
                    'mentions',
                    {'confidence': data['confidence']}
                )

        for value, data in patterns['values'].items():
            if data['confidence'] > 0.6:
                value_node_id = self.create_node(
                    'value',
                    value.replace('_', ' ').title(),
                    {
                        'category': value,
                        'confidence': data['confidence'],
                        'extraction_method': 'pattern'
                    },
                    conv_id
                )
                self.create_relationship(
                    conv_node_id,
                    value_node_id,
                    'mentions',
                    {'confidence': data['confidence']}
                )

        # Create nodes from LLM extraction
        if llm_entities:
            for entity in llm_entities.get('entities', []):
                if entity.get('confidence', 0) > 0.6:
                    entity_node_id = self.create_node(
                        entity['type'],
                        entity['label'],
                        {
                            'description': entity.get('description', ''),
                            'confidence': entity['confidence'],
                            'evidence_quote': entity.get('evidence_quote', ''),
                            'extraction_method': 'llm'
                        },
                        conv_id
                    )
                    self.create_relationship(
                        conv_node_id,
                        entity_node_id,
                        'creates',
                        {'confidence': entity['confidence']}
                    )

            # Create relationships from LLM extraction
            for rel in llm_entities.get('relationships', []):
                if rel.get('confidence', 0) > 0.6:
                    # Find node IDs by label (simplified - would need better matching)
                    source_label = rel['source_label']
                    target_label = rel['target_label']
                    # This is simplified - in production would need fuzzy matching
                    source_id = f"node_{hashlib.md5(source_label.lower().encode()).hexdigest()[:12]}"
                    target_id = f"node_{hashlib.md5(target_label.lower().encode()).hexdigest()[:12]}"

                    if source_id in self.graph['nodes'] and target_id in self.graph['nodes']:
                        self.create_relationship(
                            source_id,
                            target_id,
                            rel['type'],
                            {'confidence': rel['confidence']}
                        )

        return {
            'conversation_id': conv_id,
            'nodes_contributed': len(self.graph['indexes']['by_conversation'][conv_id]),
            'metadata': metadata
        }

    def process_batch(self, batch_files: List[str], batch_num: int) -> Dict:
        """Process a batch of conversations"""
        batch_id = f"w{self.window}_batch_{batch_num:03d}"
        batch_start = time.time()

        print(f"\n{'='*60}")
        print(f"📦 BATCH {batch_num} - Window {self.window} ({self.config['name']})")
        print(f"{'='*60}")
        print(f"Processing {len(batch_files)} conversations...")

        batch_results = []
        for i, filepath in enumerate(batch_files):
            try:
                with open(filepath, 'r') as f:
                    conv = json.load(f)

                result = self.process_conversation(conv, batch_id)
                batch_results.append(result)
                self.stats['conversations_processed'] += 1

                print(f"  [{i+1}/{len(batch_files)}] ✓ {result['metadata']['title'][:50]}")

                # Rate limiting
                if self.client:
                    time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                import traceback
                conv_title = conv.get('title', 'Unknown') if 'conv' in locals() else 'Unknown'
                print(f"  [{i+1}/{len(batch_files)}] ✗ Error processing {conv_title[:30]}: {type(e).__name__}: {str(e)[:100]}")
                if i == 0:  # Only print traceback for first error in batch
                    traceback.print_exc()

        batch_time = time.time() - batch_start
        self.stats['batches_completed'] += 1

        # Batch summary
        print(f"\n📊 Batch {batch_num} Summary:")
        print(f"  ├─ Conversations: {len(batch_results)}")
        print(f"  ├─ Total nodes: {len(self.graph['nodes'])}")
        print(f"  ├─ Total relationships: {len(self.graph['relationships'])}")
        print(f"  ├─ API calls: {self.stats['api_calls']}")
        print(f"  ├─ Cost: ${self.stats['cost_usd']:.2f}")
        print(f"  ├─ Time: {batch_time:.1f}s")
        print(f"  └─ Avg: {batch_time/len(batch_files):.1f}s/conv")

        # Phase 6: Checkpoint
        last_conv_id = batch_results[-1]['conversation_id'] if batch_results else None
        self.save_checkpoint(batch_num, last_conv_id)
        print(f"💾 Checkpoint saved")

        return {
            'batch_id': batch_id,
            'batch_num': batch_num,
            'results': batch_results,
            'time_seconds': batch_time
        }

    def export_final_graph(self):
        """Export final knowledge graph"""
        output_file = f'{OUTPUT_DIR}/window{self.window}_knowledge_graph.json'

        final_output = {
            'window': self.window,
            'config': self.config,
            'knowledge_graph': self.graph,
            'statistics': self.stats,
            'metadata': {
                'total_nodes': len(self.graph['nodes']),
                'total_relationships': len(self.graph['relationships']),
                'nodes_by_type': {
                    ntype: len(self.graph['indexes']['by_type'].get(ntype, []))
                    for ntype in NODE_TYPES
                },
                'exported_at': datetime.now().isoformat()
            }
        }

        with open(output_file, 'w') as f:
            json.dump(final_output, f, indent=2)

        print(f"\n✅ Final graph exported to: {output_file}")
        return output_file

    def run(self):
        """Main extraction pipeline"""
        print(f"\n{'='*60}")
        print(f"🚀 UNIFIED EXTRACTION - WINDOW {self.window}")
        print(f"{'='*60}")
        print(f"Name: {self.config['name']}")
        print(f"Description: {self.config['description']}")
        print(f"Range: {self.config['range']}")
        print(f"Batch size: {BATCH_SIZE}")

        # Get conversation files
        conv_files = self.get_conversation_files()
        total_convs = len(conv_files)
        total_batches = (total_convs + BATCH_SIZE - 1) // BATCH_SIZE

        print(f"Total conversations: {total_convs}")
        print(f"Total batches: {total_batches}")

        # Check for checkpoint
        last_batch = self.load_checkpoint()
        start_batch = (last_batch + 1) if last_batch is not None else 1

        if start_batch > 1:
            print(f"Resuming from batch {start_batch}")
            conv_files = conv_files[(start_batch-1) * BATCH_SIZE:]

        # Process batches
        for batch_num in range(start_batch, total_batches + 1):
            batch_start_idx = (batch_num - 1) * BATCH_SIZE - ((start_batch - 1) * BATCH_SIZE)
            batch_end_idx = min(batch_start_idx + BATCH_SIZE, len(conv_files))
            batch_files = conv_files[batch_start_idx:batch_end_idx]

            if not batch_files:
                break

            self.process_batch(batch_files, batch_num)

        # Export final graph
        self.export_final_graph()

        # Final summary
        print(f"\n{'='*60}")
        print(f"✅ EXTRACTION COMPLETE - Window {self.window}")
        print(f"{'='*60}")
        print(f"Conversations processed: {self.stats['conversations_processed']}")
        print(f"Batches completed: {self.stats['batches_completed']}")
        print(f"Nodes created: {self.stats['nodes_created']}")
        print(f"Nodes merged: {self.stats['nodes_merged']}")
        print(f"Relationships created: {self.stats['relationships_created']}")
        print(f"API calls: {self.stats['api_calls']}")
        print(f"Total cost: ${self.stats['cost_usd']:.2f}")
        print(f"{'='*60}\n")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python unified_extraction.py <window_number>")
        print("  window_number: 1 (top-down), 2 (bottom-up), 3 (random)")
        sys.exit(1)

    window = int(sys.argv[1])
    if window not in [1, 2, 3]:
        print("Error: window_number must be 1, 2, or 3")
        sys.exit(1)

    extractor = KnowledgeGraphExtractor(window)
    extractor.run()
