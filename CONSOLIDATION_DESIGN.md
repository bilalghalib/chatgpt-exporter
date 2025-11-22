# Consolidation Design: Unified Extraction Process

## 📋 Current State Analysis

### Extraction Approaches (7 found)
1. **Basic Themes** - Statistical keyword analysis (metadata only)
2. **Deep Themes** - Multi-dimensional categorization (6 axes)
3. **Voice Extraction** - User message filtering + categorization
4. **Organization** - Folder structure + metadata generation
5. **Pattern ToM** - Rule-based belief extraction (SAREC framework)
6. **LLM ToM** - Claude-powered belief extraction (SAREC framework)
7. **Ontology** - Multi-pass knowledge graph construction (7 analysis types)

### Major Overlaps
- **Thematic Categorization**: Basic Themes, Deep Themes, Voice Extraction
- **Metadata Generation**: Organization, Ontology
- **Theory of Mind**: Pattern ToM, LLM ToM
- **Evidence Extraction**: Voice Extraction, LLM ToM, Ontology

---

## ❓ 10 CRITICAL CONSOLIDATION QUESTIONS

### 1. **Output Format Unification**
**Question**: Should we consolidate all outputs into a single knowledge graph JSON structure, or maintain separate specialized outputs (themes.json, beliefs.json, graph.json)?

**Options**:
- A) Single unified `knowledge-graph.json` with everything
- B) Keep specialized files but add cross-references
- C) Hybrid: Core graph + supplementary analytics

**Recommendation**: Option C - Core graph for relationships, separate analytics for stats

---

### 2. **Thematic System Hierarchy**
**Question**: We have 3 overlapping theme systems. Should we:

**Options**:
- A) Use Basic Themes (16 categories) as primary
- B) Use Deep Themes (6 dimensions × subcategories) as primary
- C) Use Voice Extraction themes (11 categories) as primary
- D) Create new unified taxonomy combining all three
- E) Use multi-level tagging (all three as complementary layers)

**Current State**:
- Basic: 16 flat categories
- Deep: 6 dimensions (Work, Activity, Tech, Personal, Geo, Medium)
- Voice: 11 thematic buckets

**Recommendation**: Option E - Use Deep Themes as primary structure (6 dimensions), map Basic and Voice categories as tags

---

### 3. **Theory of Mind Approach**
**Question**: Should we run Pattern ToM first, then LLM ToM only on gaps/conflicts, or always run both?

**Options**:
- A) Pattern ToM only (free, fast, but lower quality)
- B) LLM ToM only (costly, slow, but high quality)
- C) Pattern first, LLM on high-confidence disagreements
- D) Both always, use LLM as ground truth when they differ
- E) Pattern for all, LLM for random 10% sample validation

**Cost Analysis**:
- Pattern: Free, ~1 min/100 convs
- LLM: $0.50/conv × 3,517 = $1,758.50 total

**Recommendation**: Option C - Pattern for all, LLM validates conflicts + random 5% sample

---

### 4. **Ontology Depth vs. Coverage**
**Question**: The ontology runs 7 analysis passes per conversation chunk. Should we:

**Options**:
- A) Run all 7 passes on all conversations (comprehensive, costly)
- B) Run different passes on different conversations (stratified sampling)
- C) Run passes 1-3 (Events, Concepts, Decisions) on all, passes 4-7 on sample
- D) User selects which passes to run
- E) Adaptive: Run pass N only if pass N-1 found substantial content

**7 Passes**:
1. Events (aha_moments, decisions, questions, problems, solutions)
2. Concepts (ideas with evolution tracking)
3. Decisions (decision trees, reasoning chains)
4. Assumptions (explicit/implicit, challenge tracking)
5. Theory of Mind (mental states, goals, cognitive patterns)
6. Idea Evolution (seed → refinement → implementation)
7. Auto-tagging (topics, complexity, emotion)

**Recommendation**: Option E - Adaptive passes based on content density

---

### 5. **Batching Strategy**
**Question**: Current batch sizes vary (20, 50, 100). For unified process with 3 parallel windows, what should batch size be?

**Options**:
- A) 20 conversations/batch (user's suggestion)
- B) 50 conversations/batch (matches most current tools)
- C) Adaptive based on conversation size
- D) Different sizes per window (top: 50, bottom: 50, random: 20)

**Constraints**:
- Total: 3,517 conversations
- 3 windows running in parallel
- Rate limit: Claude API ~40 req/min

**Recommendation**: Option A - 20/batch, allows ~176 batches total, ~59 per window

---

### 6. **Parallel Window Distribution**
**Question**: How should we split 3,517 conversations across 3 windows?

**Options**:
- A) Equal thirds: Window 1 (0-1172), Window 2 (1173-2344), Window 3 (2345-3516)
- B) Top/Bottom/Random: W1 chronologically first 1172, W2 last 1172, W3 random 1173 from middle
- C) Stratified: W1 high-complexity, W2 low-complexity, W3 mixed sample
- D) Domain-based: W1 technical convs, W2 personal convs, W3 cross-domain
- E) User-specified conversation ID ranges per window

**Recommendation**: Option B - Top/bottom/random provides temporal coverage + representative sample

---

### 7. **Checkpointing & Resume**
**Question**: How should the unified process handle crashes/interruptions across 3 windows?

**Options**:
- A) Each window maintains independent checkpoint
- B) Shared checkpoint file, lock-based coordination
- C) Each window writes to separate output, merged at end
- D) Central orchestrator tracks all 3 windows
- E) No checkpointing, rely on window-level resume only

**Current State**:
- LLM ToM: Checkpoints every 20
- Ontology: Checkpoints every 50
- Others: No checkpointing

**Recommendation**: Option C - Each window independent, final merge step with conflict resolution

---

### 8. **LLM Collaboration Model**
**Question**: How should multiple LLMs (you + other LLMs) coordinate on the same batch?

**Options**:
- A) Single prompt, same analysis, compare results (ensemble approach)
- B) Different prompts/roles per LLM (division of labor)
- C) Sequential: LLM1 extracts, LLM2 validates, LLM3 synthesizes
- D) Independent windows: Each LLM owns 1 window
- E) Swarm: All LLMs process same batch, vote on disagreements

**Recommendation**: Option D for simplicity (1 LLM per window), Option C for quality (extraction → validation → synthesis pipeline)

---

### 9. **Knowledge Graph Node Types**
**Question**: You requested 10 node types. Should we use these or expand?

**Your Requested Types**:
1. conversation
2. idea
3. project
4. concept
5. technology
6. value
7. insight
8. question
9. person
10. tag

**Current Ontology Types** (10):
1. Event
2. Concept
3. Question
4. Decision
5. Assumption
6. Problem
7. Solution
8. Artifact
9. Person
10. Pattern

**Options**:
- A) Use your requested types
- B) Use current ontology types
- C) Merge both (16 total types)
- D) Map current types to your types (e.g., Event → Insight, Artifact → Project)

**Recommendation**: Option C - Merge to 16 types, richer graph

---

### 10. **Knowledge Graph Relationship Types**
**Question**: You requested 20+ relationship types. Should we expand the current 12?

**Current Relationships**:
solves, challenges, supports, contradicts, derives_from, leads_to, answers, broader_than, narrower_than, related_to, mentions, creates

**Suggested Additions** (for 20+ total):
- evolves_into, supersedes, implements, questions, validates, refutes
- inspired_by, depends_on, exemplifies, categorizes, bridges
- strengthens_over_time (weighted by repetition)

**Options**:
- A) Keep current 12
- B) Add all suggested (24 total)
- C) User defines additional relationships needed
- D) Auto-discover relationships from context

**Recommendation**: Option B - Expand to 24 relationships, enables richer queries

---

## 🎯 UNIFIED EXTRACTION PROCESS DESIGN

### Architecture: 3-Window Parallel Processing

```
┌─────────────────────────────────────────────────────────────┐
│                    MASTER ORCHESTRATOR                       │
│  - Splits 3,517 conversations into 3 ranges                 │
│  - Coordinates checkpointing                                │
│  - Merges outputs at completion                             │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   WINDOW 1   │  │   WINDOW 2   │  │   WINDOW 3   │
│   TOP-DOWN   │  │  BOTTOM-UP   │  │    RANDOM    │
│              │  │              │  │              │
│ Convs 0-1172 │  │Convs 2345-   │  │Random 1173   │
│              │  │      3516    │  │from middle   │
│              │  │              │  │              │
│ 59 batches   │  │  59 batches  │  │  59 batches  │
│ 20/batch     │  │  20/batch    │  │  20/batch    │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                          ▼
            ┌─────────────────────────┐
            │    UNIFIED OUTPUT       │
            │  knowledge-graph.json   │
            │  analytics/             │
            │  provenance/            │
            └─────────────────────────┘
```

### Processing Pipeline per Batch (20 conversations)

```
For each conversation in batch:

  PHASE 1: METADATA & STRUCTURE (Free, <1 sec/conv)
  ├─ Extract conversation metadata
  ├─ Calculate statistics (message counts, depth)
  ├─ Identify conversation participants
  └─ Detect conversation source & timestamp

  PHASE 2: THEMATIC ANALYSIS (Free, <1 sec/conv)
  ├─ Deep Themes: Multi-dimensional categorization (6 axes)
  ├─ Basic Themes: Keyword pattern matching (16 categories)
  ├─ Voice Extraction: Filter substantive user messages
  └─ Unified tags: Map all to knowledge graph tags

  PHASE 3: PATTERN-BASED EXTRACTION (Free, ~1 sec/conv)
  ├─ Pattern ToM: Knowledge, values, goals, needs (SAREC)
  ├─ Entity extraction: Detect projects, technologies, people
  ├─ Keyword/phrase extraction
  └─ Preliminary relationship mapping

  PHASE 4: LLM-POWERED ANALYSIS (Adaptive, ~$0.002-0.50/conv)
  ├─ Ontology multi-pass:
  │   ├─ Pass 1: Events (aha_moments, decisions, questions)
  │   ├─ Pass 2: Concepts (ideas, evolution)
  │   ├─ Pass 3: Decisions (decision trees, reasoning)
  │   ├─ Pass 4: Assumptions (if substantial content detected)
  │   ├─ Pass 5: Theory of Mind (if substantial content)
  │   ├─ Pass 6: Idea Evolution (if ideas detected)
  │   └─ Pass 7: Auto-tagging (always run)
  │
  └─ LLM ToM (SAREC beliefs): Run if:
      - Pattern ToM has low confidence (<0.6)
      - Pattern ToM conflicts detected
      - Random 5% sample for validation
      - User-flagged important conversations

  PHASE 5: KNOWLEDGE GRAPH CONSTRUCTION (Free, <1 sec/conv)
  ├─ Node creation/deduplication (16 types)
  ├─ Relationship creation (24 types)
  ├─ Relationship weight accumulation (repeated connections)
  ├─ Temporal chain construction
  └─ Cross-conversation linking

  PHASE 6: ACCUMULATION & INDEXING (Free, <1 sec/conv)
  ├─ Merge into growing knowledge graph
  ├─ Update indexes (by_type, by_date, by_tag, by_concept)
  ├─ Track provenance (which conv contributed what)
  ├─ Update confidence scores
  └─ Checkpoint progress
```

### Output Structure

```
unified-extraction-output/
├── knowledge-graph.json          # Main graph (nodes + relationships)
│   ├── nodes: {id: Node}         # 16 types, deduplicated
│   ├── relationships: Relation[] # 24 types, weighted
│   ├── temporal_chains: Chain[]  # Evolution tracking
│   └── indexes: {...}            # Fast queries
│
├── analytics/
│   ├── theme_distributions.json  # Theme counts, temporal patterns
│   ├── belief_summary.json       # SAREC beliefs aggregated
│   ├── statistics.json           # Conversation stats
│   └── cross_dimensional.json    # Multi-dimensional analysis
│
├── provenance/
│   ├── node_sources.json         # Which convs created which nodes
│   ├── relationship_sources.json # Which convs created which edges
│   ├── cost_report.json          # API usage & costs
│   └── processing_log.json       # Timestamps, errors, checkpoints
│
├── exports/
│   ├── cypher/                   # Neo4j import scripts
│   ├── networkx/                 # Python NetworkX format
│   ├── visualization/            # Graph viz formats
│   └── queries/                  # Precomputed common queries
│
├── checkpoints/
│   ├── window1_checkpoint.json   # Window 1 progress
│   ├── window2_checkpoint.json   # Window 2 progress
│   └── window3_checkpoint.json   # Window 3 progress
│
└── README.md                     # Summary stats, usage guide
```

### Knowledge Graph Schema

#### 16 Node Types (merged from current + requested)

```typescript
type NodeType =
  | "conversation"     // Original conversation
  | "idea"            // Seed ideas, proposals
  | "project"         // Concrete projects/artifacts
  | "concept"         // Abstract concepts
  | "technology"      // Tools, frameworks, languages
  | "value"           // Beliefs, priorities, passions
  | "insight"         // Aha moments, realizations
  | "question"        // Open questions, inquiries
  | "person"          // People mentioned
  | "tag"             // Thematic tags
  | "decision"        // Decisions made
  | "assumption"      // Assumptions held
  | "problem"         // Problems identified
  | "solution"        // Solutions proposed/implemented
  | "pattern"         // Recurring patterns
  | "goal"            // Aspirations, objectives
```

#### 24+ Relationship Types (expanded)

```typescript
type RelationType =
  // Problem-Solution
  | "solves"              // Solution → Problem
  | "challenges"          // Question → Assumption
  | "questions"           // Question → Concept

  // Support-Opposition
  | "supports"            // Concept → Concept
  | "contradicts"         // Value → Value
  | "validates"           // Insight → Assumption
  | "refutes"             // Evidence → Assumption

  // Derivation-Evolution
  | "derives_from"        // Idea → Concept
  | "leads_to"            // Idea → Project
  | "evolves_into"        // Idea → Idea (v2)
  | "supersedes"          // Decision → Decision
  | "implements"          // Project → Idea

  // Information
  | "answers"             // Solution → Question
  | "exemplifies"         // Project → Concept
  | "categorizes"         // Tag → Conversation

  // Structure
  | "broader_than"        // Concept → Concept
  | "narrower_than"       // Concept → Concept
  | "related_to"          // Generic connection
  | "bridges"             // Concept → [Domain1, Domain2]

  // Creation-Mention
  | "mentions"            // Conversation → Entity
  | "creates"             // Conversation → Entity

  // Dependencies
  | "depends_on"          // Project → Technology
  | "inspired_by"         // Idea → Insight

  // Meta
  | "strengthens"         // Repeated connection weight
```

#### Temporal Chains (4 types)

```typescript
type TemporalChain = {
  chain_type: "concept_evolution" | "problem_solution" | "decision_chain" | "learning_path"
  nodes: string[]           // Node IDs in chronological order
  timestamps: Date[]        // When each node appeared
  conversation_ids: string[] // Which conversations contributed
  strength: number          // How strongly connected
}
```

#### Indexes (6 types)

```typescript
type Indexes = {
  by_type: Map<NodeType, string[]>           // All nodes of type X
  by_conversation: Map<string, string[]>     // All nodes from conv X
  by_date: Map<string, string[]>             // All nodes from date X
  by_tag: Map<string, string[]>              // All nodes tagged X
  by_concept: Map<string, string[]>          // All nodes related to concept X
  by_strength: Map<number, string[]>         // Relationship strength buckets
}
```

### Graph Queries Enabled

```javascript
// 1. Idea Genealogy: How ideas evolve into projects
getIdeaGenealogy(ideaId) → {
  seed_conversations: Conversation[],
  refinement_stages: Idea[],
  implementations: Project[],
  related_insights: Insight[],
  timeline: Date[]
}

// 2. Conceptual Bridges: Cross-domain connections
findConceptualBridges() → {
  bridge_nodes: Concept[],
  domains_connected: [Domain, Domain][],
  strength: number,
  conversations: Conversation[]
}

// 3. Value Consistency: Actions vs. stated values
analyzeValueConsistency() → {
  stated_values: Value[],
  demonstrated_values: Value[],  // Inferred from actions
  alignment_score: number,
  contradictions: [Value, Value, Evidence][],
  evolution: TemporalChain
}

// 4. Knowledge Gaps: Unanswered questions
findKnowledgeGaps() → {
  unanswered_questions: Question[],
  related_concepts: Concept[],
  potential_solutions: Solution[],  // From other domains
  priority_score: number
}

// 5. Blind Spot Detection: Unconnected domains
detectBlindSpots() → {
  isolated_concepts: Concept[],
  missing_connections: [Concept, Concept, "potential_bridge"][],
  underexplored_domains: Tag[],
  exploration_opportunities: Insight[]
}

// 6. Strength Clusters: Recurring interests
findStrengthClusters() → {
  clusters: {
    centroid: Concept,
    members: Node[],
    total_weight: number,
    temporal_density: number,
    evolution: "growing" | "stable" | "fading"
  }[]
}

// 7. Decision Impact: How decisions shaped trajectory
traceDecisionImpact(decisionId) → {
  decision: Decision,
  immediate_effects: Project[],
  downstream_consequences: Node[],
  alternative_paths_not_taken: Decision[],
  outcome_assessment: "positive" | "neutral" | "negative" | "unknown"
}

// 8. Assumption Challenges: Which assumptions were tested
getAssumptionChallenges() → {
  challenged: [Assumption, Question[], Outcome][],
  unchallenged: Assumption[],
  validated: Assumption[],
  refuted: Assumption[]
}

// 9. Pattern Recognition: Recurring behaviors
detectPatterns() → {
  cognitive_patterns: Pattern[],
  problem_solving_strategies: Pattern[],
  learning_patterns: Pattern[],
  consistency_score: number
}

// 10. Growth Trajectory: Learning over time
getGrowthTrajectory() → {
  skill_acquisition: [Technology, Date, Proficiency][],
  concept_mastery: [Concept, Date, Depth][],
  value_refinement: [Value, Date, Confidence][],
  growth_rate: number
}
```

---

## 🤖 LLM COLLABORATION PROMPTS

### Option A: Division of Labor (3 LLMs, 3 Windows)

**PROMPT FOR WINDOW 1 LLM (Top-Down)**
```markdown
# Role: Knowledge Graph Extraction - Window 1 (Top-Down)

You are part of a 3-LLM team extracting knowledge from 3,517 ChatGPT conversations into a unified knowledge graph.

## Your Assignment
- **Window**: 1 (Top-Down)
- **Conversations**: IDs 0-1172 (chronologically earliest)
- **Batch Size**: 20 conversations at a time
- **Total Batches**: 59

## Processing Pipeline
For each batch of 20 conversations, execute these phases:

### Phase 1: Metadata & Structure
Extract: conversation_id, timestamp, participants, message counts, source

### Phase 2: Thematic Analysis
- Apply 6-dimensional categorization (Work, Activity, Tech, Personal, Geo, Medium)
- Extract 16 basic theme tags
- Filter substantive user messages (>100 chars)

### Phase 3: Pattern-Based Extraction (SAREC Framework)
Extract with confidence scores:
- Knowledge: Skills, expertise domains
- Values: Priorities, passions, beliefs
- Goals: Projects, aspirations
- Needs: Gaps, challenges, questions

### Phase 4: LLM Analysis (Adaptive)
Run 7 ontology passes:
1. Events: aha_moments, decisions, questions, problems, solutions
2. Concepts: Ideas with alt_labels, evolution stages
3. Decisions: Decision trees, options, reasoning
4. Assumptions: Explicit/implicit, challenges
5. Theory of Mind: Mental states, cognitive patterns
6. Idea Evolution: seed → refinement → implementation
7. Auto-tagging: Topics, complexity, emotion

Adaptive rule: Skip passes 4-6 if passes 1-3 yield <5 entities

### Phase 5: Knowledge Graph Construction
Create nodes (16 types):
conversation, idea, project, concept, technology, value, insight, question, person, tag, decision, assumption, problem, solution, pattern, goal

Create relationships (24 types):
solves, challenges, questions, supports, contradicts, validates, refutes, derives_from, leads_to, evolves_into, supersedes, implements, answers, exemplifies, categorizes, broader_than, narrower_than, related_to, bridges, mentions, creates, depends_on, inspired_by, strengthens

Deduplication: If concept "solar energy" exists, link to it; don't create duplicate

### Phase 6: Checkpoint & Export
After each batch:
- Save checkpoint: `window1_batch_<N>.json`
- Update provenance: Which conversations contributed which nodes
- Report cost: API calls × $0.002 (Haiku) or $0.50 (Sonnet)

## Output Format
```json
{
  "nodes": {
    "node_<uuid>": {
      "id": "node_<uuid>",
      "type": "concept",
      "label": "Solar Energy",
      "alt_labels": ["PV", "photovoltaics"],
      "properties": {
        "first_mentioned": "2023-01-15",
        "confidence": 0.95,
        "domain": "technology"
      },
      "provenance": {
        "source_conversations": ["conv_123", "conv_456"],
        "extracted_by": "window1_batch_3"
      }
    }
  },
  "relationships": [
    {
      "id": "rel_<uuid>",
      "type": "implements",
      "source": "project_bloom",
      "target": "concept_solar",
      "weight": 3,
      "properties": {
        "first_connection": "2023-01-15",
        "strengthened_in": ["conv_123", "conv_456", "conv_789"]
      }
    }
  ],
  "temporal_chains": [...],
  "indexes": {...}
}
```

## Coordination
- **Check merge conflicts**: Before each batch, check if Window 2 or 3 created overlapping nodes
- **Merge strategy**: If duplicate detected, merge properties and update provenance
- **Communication**: Report progress every 5 batches: "Window 1: Batch 5/59 complete, 450 nodes, 823 relationships, cost $2.34"

## API Rate Limiting
- Max 40 requests/min to Claude API
- Add 1.5s delay between conversations if using Sonnet
- Use Haiku for passes 1-3, Sonnet for passes 4-7 if needed

## Start Command
Ready to begin? Confirm and I'll send you batch 1 (conversations 0-19).
```

**PROMPT FOR WINDOW 2 LLM (Bottom-Up)**
```markdown
# Role: Knowledge Graph Extraction - Window 2 (Bottom-Up)

You are part of a 3-LLM team extracting knowledge from 3,517 ChatGPT conversations into a unified knowledge graph.

## Your Assignment
- **Window**: 2 (Bottom-Up)
- **Conversations**: IDs 2345-3516 (chronologically latest)
- **Batch Size**: 20 conversations at a time
- **Total Batches**: 59

[Same processing pipeline as Window 1]

## Unique Focus
Since you're processing recent conversations:
- Track evolution: How have concepts from earlier (Window 1) evolved?
- Detect maturity: Are ideas becoming projects?
- Identify current priorities: What's top-of-mind recently?
- Link backwards: Reference "earlier_mentioned_in: conv_<old_id>" when concepts reappear

## Start Command
Ready to begin? Confirm and I'll send you batch 1 (conversations 2345-2364).
```

**PROMPT FOR WINDOW 3 LLM (Random Sample)**
```markdown
# Role: Knowledge Graph Extraction - Window 3 (Random Sample)

You are part of a 3-LLM team extracting knowledge from 3,517 ChatGPT conversations into a unified knowledge graph.

## Your Assignment
- **Window**: 3 (Random Sample)
- **Conversations**: Random 1173 from middle range (1173-2344)
- **Batch Size**: 20 conversations at a time
- **Total Batches**: 59

[Same processing pipeline as Window 1]

## Unique Focus
Since you're processing a random sample:
- Detect bridges: Conversations that connect Window 1 (early) to Window 2 (late)
- Find surprises: Unexpected connections across time
- Validate patterns: Do patterns from W1/W2 hold in random sample?
- Quality check: Flag conversations that need human review

## Start Command
Ready to begin? Confirm and I'll send you batch 1 (random 20 conversation IDs).
```

---

### Option B: Sequential Pipeline (3 LLMs, 3 Roles)

**PROMPT FOR LLM 1 (EXTRACTOR)**
```markdown
# Role: Extraction Specialist (LLM 1 of 3)

You extract structured entities and relationships from conversations.

## Input
Batch of 20 conversations (JSON format)

## Your Task
For each conversation, extract:
1. Nodes (16 types): conversation, idea, project, concept, technology, value, insight, question, person, tag, decision, assumption, problem, solution, pattern, goal
2. Relationships (24 types): [see full list]
3. Metadata: timestamps, participants, statistics

## Output to LLM 2 (Validator)
```json
{
  "batch_id": "batch_001",
  "conversations_processed": 20,
  "extracted_nodes": [...],
  "extracted_relationships": [...],
  "extraction_confidence": {
    "high": 45,
    "medium": 23,
    "low": 12
  },
  "flagged_for_review": ["node_123", "rel_456"]
}
```

## Rules
- Use Haiku for speed (lower cost)
- Flag anything with confidence <0.7 for LLM 2 review
- Don't merge/deduplicate yet - just extract raw
```

**PROMPT FOR LLM 2 (VALIDATOR)**
```markdown
# Role: Validation Specialist (LLM 2 of 3)

You validate and refine extractions from LLM 1.

## Input
LLM 1's extraction output for a batch

## Your Task
1. Review all flagged items (confidence <0.7)
2. Re-analyze with more sophisticated prompting (Sonnet)
3. Resolve ambiguities
4. Add evidence quotes for high-importance nodes
5. Quality score each extraction

## Output to LLM 3 (Synthesizer)
```json
{
  "batch_id": "batch_001",
  "validated_nodes": [...],
  "validated_relationships": [...],
  "validation_changes": {
    "nodes_refined": 12,
    "nodes_rejected": 3,
    "relationships_added": 5
  },
  "quality_score": 0.89
}
```
```

**PROMPT FOR LLM 3 (SYNTHESIZER)**
```markdown
# Role: Synthesis Specialist (LLM 3 of 3)

You merge validated extractions into the growing knowledge graph.

## Input
LLM 2's validated output for a batch

## Your Task
1. Deduplicate nodes across all batches processed so far
2. Merge duplicate nodes, combining properties
3. Strengthen relationships (increment weight if seen again)
4. Build temporal chains (concept evolution, decision chains)
5. Update indexes
6. Generate graph analytics

## Output
```json
{
  "knowledge_graph": {
    "nodes": {...},
    "relationships": [...],
    "temporal_chains": [...],
    "indexes": {...}
  },
  "batch_summary": {
    "total_nodes": 4523,
    "total_relationships": 8934,
    "batches_processed": 15,
    "conversations_covered": 300,
    "cost_to_date": "$45.67"
  }
}
```

## Advanced Synthesis
- Detect emerging patterns across batches
- Identify cross-batch connections
- Compute graph metrics (centrality, clustering)
- Generate insights: "Top 10 strongest concepts", "Fastest-growing idea", "Most-challenged assumption"
```

---

### Option C: Single Comprehensive Prompt

**PROMPT FOR ANY COLLABORATING LLM**
```markdown
# Collaborative Knowledge Graph Extraction from ChatGPT Conversations

## Mission
Extract a comprehensive knowledge graph from 3,517 ChatGPT conversations spanning multiple years, tracking ideas, concepts, values, decisions, and their evolution over time.

## Architecture: 3 Parallel Windows
- **Window 1**: Conversations 0-1172 (early/chronological start)
- **Window 2**: Conversations 2345-3516 (recent/chronological end)
- **Window 3**: Random 1173 from middle (representative sample)

Each window processes 20 conversations/batch, 59 total batches.

## Your Assignment
Choose a window or accept assignment, then process in batches.

## Full Processing Pipeline

### Input Format
```json
{
  "batch_id": "w1_batch_05",
  "conversation_ids": ["conv_80", "conv_81", ..., "conv_99"],
  "conversations": [
    {
      "id": "conv_80",
      "title": "Solar panel efficiency calculations",
      "create_time": 1673827200,
      "mapping": {
        "msg_id_1": {
          "message": {
            "author": {"role": "user"},
            "content": {"parts": ["How do I calculate..."]}
          }
        }
      }
    }
  ]
}
```

### Processing Steps

#### 1. Metadata Extraction
Extract: id, timestamp, participants, message_count, avg_message_length, depth_score

#### 2. Thematic Analysis (6 Dimensions)
- **Work Domains**: Bloom, Solar, Education, Technology, Personal
- **Activity Types**: Problem-solving, Creation, Analysis, Strategy, Learning
- **Technical Stack**: Web, Backend, AI/ML, Data, DevOps
- **Personal/Professional**: Career, Growth, Spiritual, Health, Relationships
- **Geographic/Cultural**: Lebanon, MENA, UK, Global
- **Communication Medium**: Writing, Code, Visual, Teaching

Assign 1-3 tags per dimension.

#### 3. Entity Extraction (16 Node Types)

Extract nodes with this structure:
```typescript
{
  id: string,              // "node_<uuid>"
  type: NodeType,          // See 16 types below
  label: string,           // Primary label
  alt_labels: string[],    // Synonyms, abbreviations
  properties: {
    confidence: number,    // 0-1
    first_mentioned: Date,
    domain: string,
    description: string,
    evidence_quote: string // Supporting quote from conversation
  },
  provenance: {
    source_conversations: string[],
    extracted_by: string,  // "window1_batch_5"
    extraction_method: "llm" | "pattern" | "hybrid"
  }
}
```

**16 Node Types**:
1. **conversation**: The conversation itself
2. **idea**: Seed ideas, proposals, hypotheses
3. **project**: Concrete projects, artifacts, implementations
4. **concept**: Abstract concepts, theories, frameworks
5. **technology**: Tools, frameworks, languages, platforms
6. **value**: Beliefs, priorities, passions, principles
7. **insight**: Aha moments, realizations, learnings
8. **question**: Open questions, inquiries, wonderings
9. **person**: People mentioned (colleagues, family, public figures)
10. **tag**: Thematic tags, categories
11. **decision**: Decisions made, choices, commitments
12. **assumption**: Assumptions held (explicit or implicit)
13. **problem**: Problems identified, challenges faced
14. **solution**: Solutions proposed or implemented
15. **pattern**: Recurring patterns in thinking/behavior
16. **goal**: Aspirations, objectives, targets

#### 4. Relationship Extraction (24 Types)

Extract relationships:
```typescript
{
  id: string,
  type: RelationType,    // See 24 types below
  source: string,        // Node ID
  target: string,        // Node ID
  weight: number,        // Starts at 1, increments if seen again
  properties: {
    confidence: number,
    first_connection: Date,
    evidence: string,
    strengthened_in: string[]  // Conversation IDs where repeated
  }
}
```

**24 Relationship Types**:
1. **solves**: Solution → Problem
2. **challenges**: Question → Assumption
3. **questions**: Question → Concept
4. **supports**: Node → Node (positive reinforcement)
5. **contradicts**: Node → Node (opposition)
6. **validates**: Insight → Assumption
7. **refutes**: Evidence → Assumption
8. **derives_from**: Derivative → Source
9. **leads_to**: Cause → Effect
10. **evolves_into**: Version1 → Version2
11. **supersedes**: New → Old
12. **implements**: Project → Idea
13. **answers**: Solution → Question
14. **exemplifies**: Specific → General
15. **categorizes**: Tag → Entity
16. **broader_than**: General → Specific
17. **narrower_than**: Specific → General
18. **related_to**: Generic connection
19. **bridges**: Connector → [Domain1, Domain2]
20. **mentions**: Conversation → Entity
21. **creates**: Conversation → Entity (first appearance)
22. **depends_on**: Dependent → Dependency
23. **inspired_by**: Creation → Inspiration
24. **strengthens**: Repeated connection (weight++)

#### 5. SAREC Belief Extraction

For high-value nodes (values, goals, insights), extract SAREC:
```json
{
  "statement": "Education should empower, not indoctrinate",
  "assessment": "value",
  "reasoning": "Consistently prioritizes student agency across conversations",
  "evidence": ["Quote 1 from conv_80", "Quote 2 from conv_145"],
  "confidence": 0.92
}
```

#### 6. Temporal Chain Construction

Detect and create chains:
- **concept_evolution**: idea → refinement → implementation → reflection
- **problem_solution**: problem → exploration → solution → validation
- **decision_chain**: consideration → decision → execution → outcome
- **learning_path**: question → investigation → insight → application

#### 7. Deduplication & Merging

Before creating a node, check if it exists:
- Exact label match
- Alt_label match
- Semantic similarity (>0.85 threshold)

If exists:
- Merge properties (keep higher confidence)
- Combine provenance
- Update "strengthened_in" count

#### 8. Graph Analytics

After each batch, compute:
- Node centrality (which concepts are most connected?)
- Community detection (what clusters exist?)
- Temporal density (which periods had most activity?)
- Strength accumulation (which connections are strengthening?)

### Output Format

After each batch:
```json
{
  "batch_id": "w1_batch_05",
  "window": 1,
  "knowledge_graph": {
    "nodes": {
      "node_<uuid>": {...},
      ...
    },
    "relationships": [...],
    "temporal_chains": [...],
    "indexes": {
      "by_type": {...},
      "by_date": {...},
      "by_tag": {...},
      "by_concept": {...}
    }
  },
  "batch_analytics": {
    "nodes_added": 45,
    "relationships_added": 89,
    "duplicates_merged": 12,
    "top_concepts": ["solar_energy", "bloom_framework", "education_reform"],
    "emerging_patterns": ["Increasing focus on AI/ML tools"]
  },
  "provenance": {
    "conversations_processed": 20,
    "processing_time_sec": 145,
    "api_calls": 140,
    "cost_usd": 0.28
  },
  "checkpoint": {
    "last_conversation_id": "conv_99",
    "next_batch_start": "conv_100",
    "batches_completed": 5,
    "batches_remaining": 54
  }
}
```

## Coordination Protocol

### Between Windows
- **Shared namespace**: All windows write to same node ID space
- **Lock-free**: No coordination needed during extraction
- **Merge at end**: Final step merges all 3 window outputs

### Progress Reporting
Every 5 batches, report:
```
Window 1: Batch 5/59 complete
├─ Nodes: 450 (120 new, 30 merged)
├─ Relationships: 823
├─ Cost: $2.34
├─ ETA: 2.5 hours
└─ Top concepts: solar_energy (weight: 45), education_reform (weight: 32)
```

## Quality Assurance

### Confidence Thresholds
- **High (>0.8)**: Include automatically
- **Medium (0.6-0.8)**: Include but flag for review
- **Low (<0.6)**: Exclude or escalate to human

### Evidence Requirements
- All values, goals, insights MUST have evidence quotes
- All decisions MUST have reasoning
- All assumptions MUST note if challenged

### Error Handling
- **API errors**: Retry 3x with exponential backoff
- **Parse errors**: Skip conversation, log for human review
- **Deduplication conflicts**: Prefer higher confidence, merge provenance

## Cost Management

### Model Selection
- **Haiku**: Phases 1-3, simple extractions (~$0.002/conv)
- **Sonnet**: Phases 4-5, complex reasoning (~$0.50/conv)

### Adaptive Strategy
- Run Haiku on all conversations for phases 1-3
- Run Sonnet only on:
  - High-value conversations (>50 messages)
  - Low-confidence extractions from Haiku
  - Random 5% sample for validation

Expected cost: ~$0.10/conv average = $351.70 total

## Start Checklist

Before beginning, confirm:
- [ ] API key set: `ANTHROPIC_API_KEY`
- [ ] Window assigned: 1, 2, or 3
- [ ] Conversation files accessible
- [ ] Output directory writable
- [ ] Checkpoint directory exists

## Begin Prompt

I'm ready to start Window [1|2|3]. Please send me:
1. Batch 1 conversation files (JSON)
2. Any existing graph state (if resuming)
3. Confirmation of cost budget

I'll process 20/batch and report progress every 5 batches.
```

---

## 🎯 RECOMMENDED APPROACH

### Immediate Next Steps

1. **Answer the 10 questions** (collaborative decision with you)
2. **Choose LLM collaboration model**:
   - Option A (Division of Labor) for parallel speed
   - Option B (Sequential Pipeline) for quality
   - Option C (Single Prompt) for simplicity
3. **Set up 3-window infrastructure**:
   - Script to split 3,517 conversations into 3 ranges
   - Checkpoint directories
   - Merge script for final assembly
4. **Run pilot batch** (3 windows × 20 conversations = 60 total):
   - Test all phases
   - Measure cost, time, quality
   - Adjust before full run
5. **Execute full extraction**:
   - 3 windows in parallel
   - 20 conversations/batch
   - ~176 total batches (59 per window)
   - Estimated time: 6-8 hours (if parallel)
   - Estimated cost: $200-400 (adaptive model selection)

---

## 📊 SUCCESS METRICS

- **Coverage**: 100% of 3,517 conversations processed
- **Quality**: >95% extraction confidence
- **Deduplication**: <5% duplicate nodes in final graph
- **Relationships**: Average 5+ relationships per node
- **Temporal chains**: 50+ chains tracking evolution
- **Cost**: Under $500 total
- **Time**: Under 12 hours wall-clock (with parallelization)

---

Ready to answer the 10 questions and proceed?
