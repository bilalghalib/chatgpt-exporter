# PARALLEL ANALYSIS COORDINATION

> **Strategy**: Multiple LLM instances can analyze conversations collaboratively, with coordination to prevent duplication

---

## Instance Assignment

### **Instance 1 (This Session)**
**Status**: 🟢 ACTIVE
**Direction**: Scattershot Random (Week 1 exploration)
**Range**: Random 50 from all 3,517 conversations
**Current Progress**: Batch 1 starting
**Last Checkpoint**: 2025-11-22
**Next Checkpoint**: After 50 conversations

**Strategy**: 100% random sampling to discover themes across entire dataset before systematic processing

---

## Coordination Protocol

### **1. Progress Tracking**

Each instance updates this file after completing a batch:

```markdown
## Progress Log

### Instance 1 Updates:
- 2025-11-22: Batch 1 started (scattershot mode, 50 random conversations)
- [NEXT UPDATE GOES HERE]

### Instance 2 Updates:
- [FUTURE INSTANCE STARTS HERE]
```

### **2. File Naming Convention**

**Instance 1** (scattershot):
- Checkpoint files: `checkpoint_batch_[N]_scattershot.json`
- Knowledge graph: `knowledge_graph_batch_[N]_scattershot.json`
- Extraction log: `extraction_batch_[N]_scattershot.md`

**Future Instances**:
- Use directional naming (forward/reverse) or other strategies

### **3. Tag Clustering**

**CRITICAL**: To prevent tag explosion, use tag clustering:

- Merge synonyms: "solar_energy" + "solar_power" + "solar" → "solar_energy"
- Track variations: `tag_aliases.json` maps all variants to canonical form
- Auto-cluster: Similar tags (edit distance < 3) should be reviewed for merging
- Hierarchy: "solar_energy" is subcategory of "energy_systems"

### **4. Conflict Resolution**

If multiple instances analyze the same conversation:
1. **Keep both extractions** initially
2. **Compare confidence scores** (higher confidence wins)
3. **Merge complementary insights** (if both found different things)
4. **Log conflict** in `conflicts.json` for manual review

---

## Scattershot Mode (Week 1)

**Goal**: Discover themes across entire dataset (2023-2025)

**Benefits**:
- ✅ Find recurring themes early (solar, Bloom, spiritual integration, etc.)
- ✅ Identify major projects and people across all years
- ✅ Establish tag taxonomy before systematic processing
- ✅ Preview what's in the dataset without processing everything

**Tag Clustering Rules**:
1. Before creating new tag, check if similar exists
2. Use canonical forms: lowercase, underscores, no plurals
3. Maintain `tag_aliases.json` for all variations
4. Group related tags hierarchically

---

## Communication Protocol

### **Extraction Requirements**

**CRITICAL**: All instances must extract the following from each conversation:

#### 1. **SAREC Beliefs** (Theory of Mind)
Extract beliefs in 4 categories with full SAREC structure:

```json
{
  "belief_id": "bilal.category.specific_topic",
  "category": "knowledge|values|goals|needs",
  "subcategory": "domain",
  "claim": "Clear statement of what Bilal knows/values/wants/needs",
  "score": 0.0-1.0,
  "reasoning": "Why you believe this (2-3 sentences)",
  "evidence": [
    {"quote": "exact quote from conversation", "speaker": "user|assistant"}
  ],
  "confidence": 0.0-1.0,
  "book_worthy": true|false,
  "tags": ["tag1", "tag2"]
}
```

**Categories**:
- **Knowledge**: What Bilal knows (skills, expertise, experience)
- **Values**: What Bilal cares about (priorities, passions, principles)
- **Goals**: What Bilal is trying to do (projects, aspirations)
- **Needs**: What Bilal needs (gaps, challenges, support)

#### 2. **Come Alive Values Cards**
Extract sources of meaning using Come Alive framework:

```json
{
  "id": "vc_unique_id",
  "title": "Name of source of meaning",
  "cap_indicators": ["quotes showing intrinsic motivation"],
  "attention_policies": ["what Bilal consistently notices"],
  "ground_truth": {
    "quotes": ["exact quotes"],
    "stories": ["narrative examples"],
    "recurring_themes": ["patterns"]
  },
  "tensions": ["contradictions that reveal values"],
  "energy_level": 0.0-1.0,
  "status": "emerging|active|confirmed",
  "conversation_id": "conv_id"
}
```

**Look for**:
- **CAPs** (Constitutive Actions): Activities that feel intrinsically meaningful
- **IAPs** (Instrumental Actions): Activities done as means to an end
- **Tensions**: Contradictions reveal what matters most

#### 3. **Book Material Flagging**
Mark beliefs as `book_worthy: true` if they are:
- Compelling insights or frameworks
- Unique perspectives or methodologies
- Vulnerable admissions or struggles
- Core identity or life work
- Cross-cultural or interdisciplinary integration

Track separately for book planning:
```json
{
  "claim": "belief claim",
  "category": "knowledge|values|goals|needs",
  "confidence": 0.0-1.0,
  "why_book_worthy": "Explanation of why this belongs in a book"
}
```

**Target books**:
- **Book D**: Islamic Values in Secular/Tech Work
- **Book F**: Cross-Cultural Education Design
- **Book G**: Portfolio Approach (blog posts, case studies)
- **Book E**: AI for Social Good
- **Book A**: The Integrated Approach

#### 4. **Tags & Themes**
Extract and cluster thematic tags:
- Use canonical forms (lowercase, underscores, no plurals)
- Check `tag_aliases.json` before creating new tags
- Track: themes, projects, people, locations, skills

### **Cross-Instance Notes**

File: `cross_instance_notes.md`

Use this to share discoveries between instances:
- Key entities found
- Tag clustering decisions
- Questions for other instances
- Validation requests

---

## Progress Log

### Instance 1 Updates:
- **2025-11-22**: Batch 1 starting (scattershot mode, 50 random conversations)
  - Strategy: 100% random to discover themes
  - Tag clustering: ENABLED
  - Expected: Broad overview of all major themes 2023-2025

### Instance 2 Updates:
- **[WAITING]**

---

## File Structure

```
/home/user/chatgpt-exporter/
├── COORDINATION.md (this file)
├── analysis_batches/
│   ├── batch_001/
│   │   ├── manifest.json
│   │   ├── results.json
│   │   ├── REPORT.md
│   │   └── tag_clusters.json
│   ├── master_state.json
│   └── tag_aliases.json (canonical tag mapping)
└── analyzer/ (legacy, keep for reference)
```

---

**STATUS**: Instance 1 starting scattershot mode
**NEXT STEP**: Process 50 random conversations with tag clustering
