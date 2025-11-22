# Batch Processor Usage Guide

**Incremental Theory of Mind Builder with Knowledge Graph Preparation**

## Overview

The batch processor analyzes conversations incrementally (50 at a time) to extract:
- **SAREC Beliefs**: Knowledge, Values, Goals, Needs with evidence
- **Values Cards**: Come Alive framework - sources of meaning, attention policies, tensions
- **Book Material**: Flagged content suitable for publications
- **Knowledge Graph Nodes**: Graph-ready data with provenance tracking

## Quick Start

### Prerequisites

1. **Anthropic API Key** - Get from https://console.anthropic.com/
2. **Python 3.7+** with packages:
   ```bash
   pip install anthropic
   ```

### Run Your First Batch

```bash
# Process batch 1 (50 conversations) with LLM analysis
python3 batch_processor.py YOUR_API_KEY 1 50

# Test with smaller batch (5 conversations)
python3 batch_processor.py YOUR_API_KEY 1 5

# Dry run without API (structure only, no LLM)
python3 batch_processor.py test 1 5
```

### What Gets Generated

After running, you'll find:

```
analysis_batches/
├── batch_001/
│   ├── manifest.json           # Conversations in this batch
│   ├── results.json            # All extracted data
│   └── REPORT.md               # Human-readable summary
├── master_state.json           # Tracks processed conversations
└── (future batches...)
```

## Understanding the Outputs

### 1. SAREC Beliefs (`results.json` → `beliefs`)

Each conversation generates beliefs in 4 categories:

**Example Knowledge Belief:**
```json
{
  "belief_id": "bilal.knowledge.solar_iraq_training",
  "category": "knowledge",
  "subcategory": "solar_energy",
  "claim": "Bilal has expertise in designing solar training for conflict zones",
  "score": 0.85,
  "reasoning": "Bilal describes specific methodologies...",
  "evidence": [
    {"quote": "We adapted the curriculum for...", "speaker": "user"}
  ],
  "confidence": 0.9,
  "book_worthy": true
}
```

**Categories:**
- **knowledge**: Skills, expertise, capabilities
- **values**: Priorities, passions, what Bilal cares about
- **goals**: Projects, aspirations, what Bilal is trying to do
- **needs**: Gaps, challenges, support needed

### 2. Values Cards (`results.json` → `values_cards`)

Come Alive framework - sources of meaning:

**Example Values Card:**
```json
{
  "id": "vc_a1b2c3d4",
  "title": "Integrating Spiritual Practice with Tech Work",
  "cap_indicators": [
    "I feel most alive when I can bring dhikr into debugging sessions"
  ],
  "attention_policies": [
    "Notices opportunities for spiritual integration",
    "Pays attention to tension between efficiency and presence"
  ],
  "ground_truth": {
    "quotes": ["..."],
    "stories": ["..."],
    "recurring_themes": ["spiritual integration", "presence in work"]
  },
  "tensions": [
    "Wanting to move fast vs. wanting to be fully present"
  ],
  "energy_level": 0.85,
  "status": "emerging"
}
```

### 3. Book Material (`results.json` → `book_material`)

Beliefs flagged as `book_worthy: true`:
- Compelling insights
- Unique frameworks
- Powerful stories
- Novel methodologies

### 4. Knowledge Graph Nodes (`results.json` → `nodes`)

Each belief and values card becomes a graph node with:
- **node_id**: Unique identifier
- **node_type**: belief_knowledge, belief_values, values_card, etc.
- **properties**: All belief/card data
- **provenance**: Exact source (conversation, quote, batch)

## Batch Selection Algorithm

The processor uses **composite scoring** to select which 50 conversations to process:

- **40% Recency**: Favor recent conversations (2025 > 2024 > 2023)
- **40% Depth**: Favor substantive conversations (more messages = higher depth)
- **20% Random**: Include diversity, explore unexpected areas

This ensures you get:
1. Latest thinking (recent)
2. Rich conversations (depth)
3. Serendipitous discoveries (random)

## Incremental Processing Workflow

### Process First 50 Conversations
```bash
python3 batch_processor.py YOUR_API_KEY 1 50
```

**Expected:**
- Time: ~15-20 minutes
- Cost: ~$25-30
- Output: `analysis_batches/batch_001/`

### Review Results

```bash
# Read the report
cat analysis_batches/batch_001/REPORT.md

# Explore beliefs
cat analysis_batches/batch_001/results.json | jq '.beliefs[0]'

# See values cards
cat analysis_batches/batch_001/results.json | jq '.values_cards'

# Check book material
cat analysis_batches/batch_001/results.json | jq '.book_material'
```

### Process Next Batch

```bash
python3 batch_processor.py YOUR_API_KEY 2 50
```

The processor automatically:
- Tracks which conversations are already processed
- Selects next 50 unprocessed conversations
- Prevents duplication
- Updates master state

### Continue Until Complete

```bash
# Batch 3
python3 batch_processor.py YOUR_API_KEY 3 50

# Batch 4
python3 batch_processor.py YOUR_API_KEY 4 50

# ... and so on
```

For 3,517 conversations: ~71 batches × $25 = ~$1,775 total

## Cost Management

### Estimated Costs (Claude Sonnet 4.5)

- **Per conversation**: ~$0.50
- **Per batch (50)**: ~$25
- **All 3,517**: ~$1,750

### Budget-Conscious Strategy

**Week 1**: Priority batch (50 conversations) - $25
- Recent solar work (July 2025)
- Bloom methodology
- Spiritual integration

**Week 2**: Next tier (50) - $25
- MENA/Iraq projects
- AI integration
- Education design

**Weeks 3-8**: Incremental (50/week × 6) - $150
- Total: 400 conversations for ~$200

**Result**: 80% of value for ~11% of cost

## Master State Tracking

`master_state.json` tracks:
- Which conversations are processed
- Belief registry (prevents duplication)
- Values card registry
- Tag registry
- All nodes and edges

**Never delete this file** - it ensures you don't reprocess conversations.

## Resuming After Interruption

If processing stops mid-batch:

```bash
# The master_state.json tracks what's done
# Just run the next batch number
python3 batch_processor.py YOUR_API_KEY 2 50
```

The system automatically skips already-processed conversations.

## Advanced Usage

### Custom Batch Size

```bash
# Process 100 at once
python3 batch_processor.py YOUR_API_KEY 1 100

# Process just 10 (testing)
python3 batch_processor.py YOUR_API_KEY 1 10
```

### Accessing Results Programmatically

```python
import json
from pathlib import Path

# Load batch results
with open("analysis_batches/batch_001/results.json") as f:
    data = json.load(f)

# Get all book-worthy beliefs
book_material = data["book_material"]
print(f"Found {len(book_material)} book-worthy insights")

# Get values cards with high energy
high_energy_cards = [
    card for card in data["values_cards"]
    if card.get("energy_level", 0) > 0.7
]
```

### Querying Across Batches

```bash
# Find all book material across batches
cat analysis_batches/batch_*/results.json | jq '.book_material[]'

# Count total beliefs extracted
cat analysis_batches/batch_*/results.json | jq '[.beliefs[].beliefs | to_entries[].value | length] | add'

# Find high-energy values cards
cat analysis_batches/batch_*/results.json | jq '.values_cards[] | select(.energy_level > 0.8)'
```

## Integration with Other Tools

### 1. Populate Organized Conversations

```bash
# First organize all conversations
python3 organize_conversations.py

# Then run batch processor
# Results can populate theory_of_mind.json in each folder
```

### 2. Build Knowledge Graph

After processing batches, use the nodes/edges to build a graph:
- Import into Neo4j, NetworkX, or other graph DB
- Query relationships between beliefs
- Track belief evolution over time

### 3. Generate Deliverables

Use extracted data to create:
- Portfolio knowledge cards
- Blog posts from book material
- Grant proposals with evidence
- Thematic compilations

## Troubleshooting

### "No API key provided"
```bash
# Check you're passing the API key
python3 batch_processor.py YOUR_ACTUAL_KEY 1 50
```

### "Rate limit exceeded"
The processor includes automatic rate limiting (pauses every 40 requests). If you still hit limits, reduce batch size:
```bash
python3 batch_processor.py YOUR_API_KEY 1 25
```

### "JSON parsing error"
Sometimes Claude's response includes extra text. The processor handles this automatically by extracting the JSON array. If errors persist, check the conversation content length (should be < 100k chars).

### "Out of memory"
Processing 50 conversations loads all data into memory. If running on limited RAM:
```bash
# Reduce batch size
python3 batch_processor.py YOUR_API_KEY 1 25
```

## Next Steps After Processing

1. **Review Quality**: Read `batch_001/REPORT.md` to check extraction quality
2. **Adjust Prompts**: If beliefs aren't accurate, modify SAREC_PROMPT or VALUES_PROMPT
3. **Continue Batches**: Process incrementally (50/week recommended)
4. **Aggregate Results**: Build master knowledge graph from all batches
5. **Generate Content**: Use book material to write blog posts, proposals, etc.

## Files Reference

| File | Purpose |
|------|---------|
| `batch_processor.py` | Main processor (this tool) |
| `analysis_batches/` | All batch outputs |
| `master_state.json` | Tracks progress, prevents duplication |
| `batch_NNN/manifest.json` | Conversations in batch N |
| `batch_NNN/results.json` | All extracted data for batch N |
| `batch_NNN/REPORT.md` | Human-readable summary |

## Support

See also:
- `ANALYSIS_README.md` - Overview of all analysis tools
- `PROCESS_DOCUMENTATION.md` - Complete pipeline documentation
- `COMPREHENSIVE_THEME_ANALYSIS.md` - Initial thematic analysis

---

**Created**: November 22, 2025
**Version**: 1.0
**System**: Incremental Theory of Mind Builder with Knowledge Graph Preparation
