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
