# Comprehensive Extraction Plan
## Random Sampling Strategy for Theory of Mind Building

**Created**: 2025-11-22
**Purpose**: Extract insights from 3,517 conversations using random sampling approach
**Status**: Ready to Execute

---

## 📋 Executive Summary

**Goal**: Build comprehensive Theory of Mind from conversations by randomly sampling and deeply analyzing conversations to extract:
- Knowledge domains (what you know)
- Values & priorities (what you care about)
- Goals & projects (what you're trying to do)
- Needs & challenges (what you need)
- Evolution patterns (how you've changed over time)

**Approach**: Random sampling with stratification by time period and conversation depth

---

## 🎲 Sampling Strategy

### Total Dataset
- **3,517 conversations** (Feb 2023 - Nov 2025)
- **71,711 total messages**
- **Sources**: 2,264 ChatGPT, 1,252 Claude, 1 Gemini

### Stratification Dimensions
1. **Time Period** (3 periods)
   - 2023: 667 conversations (19%)
   - 2024: 1,150 conversations (33%)
   - 2025: 1,699 conversations (48%)

2. **Conversation Depth** (3 tiers)
   - Short (1-14 messages): 1,992 conversations (57%)
   - Medium (15-100 messages): 1,074 conversations (31%)
   - Long (100+ messages): 451 conversations (12%)

3. **Source** (3 sources)
   - ChatGPT: 2,264 (64%)
   - Claude: 1,252 (36%)
   - Gemini: 1 (<1%)

### Sample Size Recommendations

**Option A: Quick Validation (50 conversations)**
- Cost: ~$25
- Coverage: ~1.4% of dataset
- Purpose: Test extraction quality before scaling

**Option B: Representative Sample (200 conversations)**
- Cost: ~$100
- Coverage: ~5.7% of dataset
- Purpose: Build solid Theory of Mind with good coverage

**Option C: Deep Coverage (500 conversations)**
- Cost: ~$250
- Coverage: ~14.2% of dataset
- Purpose: Comprehensive Theory of Mind with high confidence

**Option D: Near-Complete (1000 conversations)**
- Cost: ~$500
- Coverage: ~28.4% of dataset
- Purpose: Very comprehensive, diminishing returns after this

---

## 🎯 Proposed Execution: Option B (200 conversations)

### Stratified Random Sample Breakdown

| Period | Depth  | Count | ChatGPT | Claude |
|--------|--------|-------|---------|--------|
| 2023   | Short  | 10    | 6       | 4      |
| 2023   | Medium | 15    | 10      | 5      |
| 2023   | Long   | 15    | 10      | 5      |
| 2024   | Short  | 15    | 10      | 5      |
| 2024   | Medium | 25    | 16      | 9      |
| 2024   | Long   | 25    | 16      | 9      |
| 2025   | Short  | 20    | 13      | 7      |
| 2025   | Medium | 35    | 22      | 13     |
| 2025   | Long   | 40    | 26      | 14     |
| **Total** | | **200** | **129** | **71** |

**Rationale**:
- More weight on recent years (reflects current state)
- More weight on deeper conversations (more insight per conversation)
- Proportional representation by source

---

## 🔄 Execution Workflow

### Phase 1: Random Sampling (Day 1)
**Tools**: Python script
**Output**: `selected_conversations_random_200.json`

```python
# Pseudo-code for sampling
import random
import json

# Load all conversations
conversations = load_all_conversations()

# Stratify by year, depth, source
strata = stratify_conversations(conversations)

# Sample according to table above
sample = []
for stratum_key, target_count in sampling_plan.items():
    stratum_conversations = strata[stratum_key]
    sampled = random.sample(stratum_conversations, target_count)
    sample.extend(sampled)

# Save sample
save_sample(sample, 'selected_conversations_random_200.json')
```

### Phase 2: Organize Sampled Conversations (Day 1)
**Tool**: `organize_conversations.py` (modified)
**Output**: Folder structure for 200 conversations

```bash
python3 organize_conversations.py --sample selected_conversations_random_200.json
```

### Phase 3: Extract Voice (Day 1-2)
**Tool**: `extract_your_voice.py` (modified)
**Output**: User messages from sampled conversations

```bash
python3 extract_your_voice.py --sample selected_conversations_random_200.json
```

### Phase 4: LLM Theory of Mind Extraction (Day 2-3)
**Tool**: `build_llm_theory_of_mind.py` or `batch_processor.py`
**Output**: SAREC-structured beliefs

```bash
# Option A: Batch processor (recommended - has resume capability)
python3 batch_processor.py YOUR_API_KEY --sample selected_conversations_random_200.json

# Option B: One-shot (no resume)
python3 build_llm_theory_of_mind.py YOUR_API_KEY --sample selected_conversations_random_200.json
```

### Phase 5: Analysis & Synthesis (Day 3-4)
**Manual review + synthesis**
**Output**:
- Knowledge cards
- Values identification
- Goals mapping
- Needs assessment
- Evolution timeline

---

## 📂 Output Structure

```
theory_of_mind/
├── knowledge/
│   ├── technical/
│   │   ├── solar_energy.json              # SAREC beliefs
│   │   ├── web_development.json
│   │   ├── data_engineering.json
│   │   └── README.md                       # Summary
│   ├── domains/
│   │   ├── education.json
│   │   ├── social_entrepreneurship.json
│   │   └── curriculum_design.json
│   └── cultural/
│       ├── mena_context.json
│       └── islamic_knowledge.json
├── values/
│   ├── core_values/
│   │   ├── integration.json                # Faith-tech integration
│   │   ├── depth.json                      # Marathon focus sessions
│   │   ├── meaning_making.json             # Values-driven work
│   │   └── education_empowerment.json
│   └── attention_policies/
│       ├── what_bilal_notices.md           # CAPs analysis
│       └── sources_of_meaning.md
├── goals/
│   ├── projects/
│   │   ├── solar_iraq.json
│   │   ├── barakanomics_book.json
│   │   ├── bloom_social_enterprise.json
│   │   └── prayer_tools.json
│   └── aspirations/
│       ├── expertise_development.json
│       └── impact_goals.json
├── needs/
│   ├── knowledge_gaps.json
│   ├── resources_needed.json
│   └── challenges.json
├── evolution/
│   ├── 2023_patterns.json
│   ├── 2024_patterns.json
│   ├── 2025_patterns.json
│   └── transitions.json
├── provenance/
│   ├── conversation_contributions.json     # Which conv contributed what
│   └── belief_evidence_map.json            # Belief → Evidence mapping
└── README.md                                # Overview & navigation
```

---

## 🎨 Extraction Framework

### SAREC Structure (for each belief)
```json
{
  "belief_id": "bilal.knowledge.solar_energy.iraq_training",
  "category": "knowledge",
  "subcategory": "solar_energy",
  "claim": "Bilal has expertise in solar PV training for Iraq context",
  "score": 0.85,
  "reasoning": "Developed comprehensive training curriculum, demonstrates deep technical knowledge, contextualizes for Iraqi climate and infrastructure",
  "evidence": [
    {
      "type": "conversation",
      "id": "2025-07-09_solar_iraq",
      "messages": [12, 15, 18],
      "weight": 0.9,
      "quote": "We need to account for dust accumulation in Iraqi climate..."
    },
    {
      "type": "pattern",
      "name": "recurring_solar_work",
      "conversation_count": 86,
      "weight": 0.8
    }
  ],
  "confidence": 0.85,
  "first_observed": "2023-03",
  "last_updated": "2025-07",
  "related_beliefs": [
    "bilal.cares.mena_development",
    "bilal.trying_to_do.capacity_building"
  ]
}
```

### Come Alive Framework
**Identifies**:
- CAPs (Constitutive Actions): What Bilal does for its own sake
- IAPs (Instrumental Actions): What feels like obligation
- Tensions: Conflicts between CAPs and IAPs
- Values: Clusters of related CAPs

**Example**:
```yaml
cap:
  description: "Deep research dives into frameworks"
  attention_policies:
    - "QUESTIONS that spark genuine fascination"
    - "FRAMEWORKS that reveal hidden patterns"
    - "CONNECTIONS between disparate domains"
  evidence:
    - "I get lost on questions when they capture me"
    - "Systematically explored 5+ educational frameworks in one sitting"
```

---

## 🔍 Analysis Types

### For Each Sampled Conversation:

1. **Knowledge Extraction**
   - Technical skills demonstrated
   - Domain expertise shown
   - Problem-solving patterns
   - Learning/growth moments

2. **Values Identification**
   - What gets attention (CAPs)
   - What feels like obligation (IAPs)
   - Emotional markers (enthusiasm, resistance)
   - Priorities revealed through choices

3. **Goals Mapping**
   - Projects mentioned
   - Aspirations expressed
   - Problems being solved
   - Future plans discussed

4. **Needs Assessment**
   - Knowledge gaps identified
   - Resources requested
   - Challenges faced
   - Support sought

5. **Contribution Tracking**
   - What this conversation accomplished
   - Insights gained
   - Decisions made
   - Progress on projects

---

## 📊 Quality Assurance

### Validation Steps

1. **Sample Representativeness**
   - Check distribution matches population
   - Verify no systematic bias in random selection
   - Ensure coverage of major themes

2. **Extraction Quality**
   - Manually review 10 random extractions
   - Check evidence attribution accuracy
   - Verify SAREC confidence calibration
   - Validate quote context

3. **Consistency Checks**
   - Cross-reference beliefs across conversations
   - Flag contradictions for investigation
   - Track belief evolution coherence

4. **Completeness**
   - Ensure all major domains covered
   - Check for missing time periods
   - Verify depth of analysis

---

## 💰 Cost Analysis

### Option B: 200 Conversations

**LLM Processing**:
- 200 conversations × $0.50/conv = $100.00
- Estimated time: 8-12 hours (with API rate limits)

**Total Project Cost**:
- LLM processing: $100
- Manual review time: ~8 hours
- Synthesis time: ~6 hours

**Expected Output**:
- 200-400 knowledge beliefs
- 30-50 value statements
- 50-80 goal entries
- 40-60 need identifications
- Rich provenance mapping

---

## 📅 Timeline

### Week 1: Sampling & Setup
- **Day 1**: Create sampling script, generate random sample
- **Day 2**: Organize sampled conversations into folders
- **Day 3**: Extract voice from sampled conversations

### Week 2: LLM Processing
- **Day 4-5**: Run batch processor on sampled conversations
- **Day 6**: Quality check first 50 results
- **Day 7**: Complete remaining 150

### Week 3: Analysis & Synthesis
- **Day 8-9**: Manual review and validation
- **Day 10**: Generate knowledge cards
- **Day 11**: Create values framework
- **Day 12**: Map goals and needs

### Week 4: Documentation & Deliverables
- **Day 13**: Write comprehensive README
- **Day 14**: Create interactive visualization/query tool
- **Day 15**: Generate sample deliverables (portfolio content)

---

## 🚀 Next Steps

### Immediate Actions (Ready to Execute)

1. **Create Sampling Script**
   ```bash
   # Create random_sampler.py
   python3 random_sampler.py --size 200 --output selected_conversations_random_200.json
   ```

2. **Verify Sample Quality**
   ```bash
   # Check distribution
   python3 analyze_sample.py selected_conversations_random_200.json
   ```

3. **Organize Sampled Conversations**
   ```bash
   python3 organize_conversations.py --sample selected_conversations_random_200.json
   ```

4. **Get API Key Ready**
   - Go to https://console.anthropic.com/settings/keys
   - Create new API key for this project
   - Set budget limit if desired

5. **Run Batch Processing**
   ```bash
   python3 batch_processor.py YOUR_API_KEY --sample selected_conversations_random_200.json
   ```

---

## 🎯 Success Metrics

### Quantitative
- [ ] 200 conversations randomly sampled
- [ ] 200 conversations organized into folders
- [ ] 200 conversations analyzed with LLM
- [ ] 200+ knowledge beliefs extracted
- [ ] 30+ value statements identified
- [ ] 50+ goals mapped

### Qualitative
- [ ] Can answer "What does Bilal know about X?"
- [ ] Can identify "What makes Bilal come alive?"
- [ ] Can map "How has Bilal evolved 2023-2025?"
- [ ] Can generate portfolio content with evidence
- [ ] Can identify knowledge gaps and growth areas

---

## 📝 Open Questions

1. **Sample Size**: Start with 200 or go directly to 500?
2. **Time Focus**: Weight recent conversations more heavily?
3. **Theme Focus**: Bias sample toward certain themes (solar, spiritual, etc.)?
4. **Incremental Processing**: Process in batches of 50 or all 200 at once?
5. **Validation**: What % of extractions should be manually reviewed?

---

## 🛠️ Tools Reference

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `random_sampler.py` | Generate stratified sample | All conversations | Sample JSON |
| `organize_conversations.py` | Create folder structure | Sample conversations | Organized folders |
| `extract_your_voice.py` | Extract user messages | Sample conversations | Voice markdown files |
| `batch_processor.py` | LLM analysis (resumable) | Sample + API key | Theory of Mind JSON |
| `build_llm_theory_of_mind.py` | LLM analysis (one-shot) | Sample + API key | Theory of Mind JSON |
| `analyze_themes.py` | Thematic categorization | Conversations | Theme analysis JSON |

---

## 📖 Related Documentation

- **PROCESS_DOCUMENTATION.md** - Complete pipeline overview
- **BATCH_PROCESSOR_GUIDE.md** - Incremental processing guide
- **INTEGRATED_FRAMEWORK.md** - SAREC + Come Alive framework
- **theory_of_mind_framework.md** - Theory of Mind structure
- **ANALYSIS_README.md** - Quick start guide
- **OPEN_QUESTIONS_FOR_BILAL.md** - 75 questions to validate findings

---

**Ready to start? Let me know which option (A/B/C/D) you prefer, and I'll create the sampling script!**

---

**Maintained by**: Claude Code
**Last Updated**: 2025-11-22
**Status**: Ready for Execution
