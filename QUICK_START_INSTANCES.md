# Quick Start Guide: Parallel Instance Setup
## Copy-Paste Prompts for Each Claude Code Window

> **Use this guide to quickly spin up all 3 instances**

---

## 🚀 Setup Sequence (5 Minutes)

### Step 1: Open 3 Claude Code Windows

Open https://claude.ai/code in 3 separate browser windows/tabs, all pointing to this repository.

### Step 2: Copy-Paste Initial Prompts

Use the prompts below to initialize each instance.

---

## 📋 Instance 1 Prompt (Forward: 1→1758)

```
I'm Instance 1 of a 3-instance parallel analysis system analyzing 3,517 conversations.

MY TASK:
- Analyze conversations FORWARD chronologically (oldest → newest)
- Range: Conversations 1 to 1758
- Current status: Batch 1 in progress (7/50 conversations complete)

PLEASE DO THIS FIRST:
1. Read analyzer/COORDINATION.md (overall strategy)
2. Read analyzer/EXTRACTION_METHODOLOGY.md (how to extract)
3. Read analyzer/INTEGRATED_FRAMEWORK.md (SAREC framework)
4. Review analyzer/KNOWLEDGE_GRAPH_BATCH1_DATA.json (my work so far)

MY UNIQUE VALUE:
- See how values EMERGED over time
- Track project ORIGINS
- Understand relationship FORMATION
- Observe learning PROGRESSIONS (novice → expert)

CRITICAL INNOVATION TO ADOPT (from Instance 3):
For EACH conversation analyzed, create TWO files:
1. [conversation_file]_metadata.json - Structured extraction (entities, values, theory of mind, cross-instance questions)
2. [conversation_file]_metadata.md - Human-readable summary

Location: Same directory as original conversation (exported_conversations/)

MY FILE NAMING:
- Checkpoints: checkpoint_batch_[N]_forward.json
- Save to: analyzer/instance_1_forward/
- Update: analyzer/COORDINATION.md after each batch

COORDINATION:
- Post discoveries to analyzer/cross_instance_notes.md
- Ask Instance 2: "Is [X] still active in 2025?"
- Ask Instance 3: "Is [X] visible at middle (Dec 2024)?"

NEXT STEP: Continue Batch 1 from conversation 8/50

Ready to start?
```

---

## 📋 Instance 2 Prompt (Reverse: 3517→1759)

```
I'm Instance 2 of a 3-instance parallel analysis system analyzing 3,517 conversations.

MY TASK:
- Analyze conversations REVERSE chronologically (newest → oldest)
- Range: Conversations 3517 to 1759
- Current status: Batch 71 just started (minimal progress)

PLEASE DO THIS FIRST:
1. Read analyzer/COORDINATION.md (overall strategy - I'm Instance 2 section)
2. Read analyzer/EXTRACTION_METHODOLOGY.md (how to extract)
3. Read analyzer/INTEGRATED_FRAMEWORK.md (SAREC framework)
4. Check analyzer/instance_2_reverse/checkpoint_batch_71_reverse_PARTIAL.json (partial work)

MY UNIQUE VALUE:
- See CURRENT STATE of values, projects, relationships
- Understand what SUCCEEDED vs abandoned
- Track OUTCOMES of early experiments (that Instance 1 will see start)
- Identify what PERSISTED to present

CRITICAL INNOVATION TO ADOPT (from Instance 3):
For EACH conversation analyzed, create TWO files:
1. [conversation_file]_metadata.json - Structured extraction (entities, values, theory of mind, cross-instance questions)
2. [conversation_file]_metadata.md - Human-readable summary

Location: Same directory as original conversation (exported_conversations/)

MY FILE NAMING:
- Checkpoints: checkpoint_batch_[N]_reverse.json (N starts at 71, goes down to 37)
- Save to: analyzer/instance_2_reverse/
- Update: analyzer/COORDINATION.md after each batch

COORDINATION:
- Post discoveries to analyzer/cross_instance_notes.md
- Ask Instance 1: "When did [X] first appear?"
- Ask Instance 3: "Is [X] visible at middle (Dec 2024)?"

NEXT STEP: Start Batch 71 (conversations 3517→3468, working backward)

Ready to start from the MOST RECENT conversations?
```

---

## 📋 Instance 3 Prompt (Middle-Outward: ~1758)

```
I'm Instance 3 of a 3-instance parallel analysis system analyzing 3,517 conversations.

MY TASK:
- Analyze conversations BIDIRECTIONALLY from MIDDLE outward
- Range: Start at ~1758-1759 (middle), expand outward in both directions
- Current status: Batch M0 in progress (3/50 conversations complete)

PLEASE DO THIS FIRST:
1. Read analyzer/COORDINATION_INSTANCE3_MIDDLE_OUTWARD.md (MY unique strategy)
2. Read analyzer/COORDINATION.md (overall coordination)
3. Review analyzer/instance_3_middle_outward/middle_baseline_M0.md (my work so far - excellent quality!)

MY UNIQUE VALUE:
- Identify INFLECTION POINTS and transitions
- Detect CONVERGENCE patterns (what persisted from past to present)
- See what CHANGED before/after middle (~Dec 2024)
- Cross-validate findings from Instance 1 (origins) and Instance 2 (outcomes)
- I'm the VALIDATION HUB where the other two instances meet

I INNOVATED THE METADATA PATTERN - keep using it:
For EACH conversation analyzed, create TWO files:
1. [conversation_file]_metadata.json - Structured extraction
2. [conversation_file]_metadata.md - Human-readable summary

Location: Same directory as original conversation (exported_conversations/)

MY FILE NAMING:
- Checkpoints: checkpoint_batch_M[N]-[B|F]_[direction].json
  - M0 = middle origin batch
  - M1-B = first backward expansion
  - M1-F = first forward expansion
- Save to: analyzer/instance_3_middle_outward/
- Update: analyzer/COORDINATION.md after each batch

BATCH PATTERN (Alternating Outward):
- M0 (Middle): 1734-1783 [IN PROGRESS]
- M1-B (Backward): 1684-1733 [NEXT]
- M1-F (Forward): 1784-1833 [AFTER M1-B]
- Continue alternating...

COORDINATION:
- Post discoveries to analyzer/cross_instance_notes.md
- Ask Instance 1: "When did [X] originate?" (they see beginnings)
- Ask Instance 2: "Is [X] still active in 2025?" (they see endings)
- Your cross-instance questions are VERY valuable - you've already posted 12 great ones!

NEXT STEP: Continue Batch M0 from conversation 4/50

Your middle-baseline analysis is excellent quality - keep it up!

Ready to continue?
```

---

## ✅ Verification Checklist

After initializing all 3 instances, verify:

### Instance 1:
- [ ] Reading forward from conversation 1
- [ ] Saving files to `analyzer/instance_1_forward/`
- [ ] Naming files: `checkpoint_batch_[N]_forward.json`
- [ ] Creating metadata files for each conversation
- [ ] Posting to `cross_instance_notes.md`

### Instance 2:
- [ ] Reading backward from conversation 3517
- [ ] Saving files to `analyzer/instance_2_reverse/`
- [ ] Naming files: `checkpoint_batch_[N]_reverse.json`
- [ ] Creating metadata files for each conversation
- [ ] Posting to `cross_instance_notes.md`

### Instance 3:
- [ ] Reading from middle (~1758) outward
- [ ] Saving files to `analyzer/instance_3_middle_outward/`
- [ ] Naming files: `checkpoint_batch_M[N]-[B|F]_[direction].json`
- [ ] Creating metadata files for each conversation
- [ ] Posting cross-instance questions (you're the validation hub!)

---

## 🔄 Daily Sync Ritual (5 Minutes)

Each instance should do this once per session:

1. **Read** `analyzer/cross_instance_notes.md` - What did others discover?
2. **Update** `analyzer/COORDINATION.md` Progress Log - Your progress
3. **Post** New discoveries to `cross_instance_notes.md`
4. **Ask** Cross-instance questions for validation

---

## 📊 Progress Tracking Template

Each instance adds to `analyzer/COORDINATION.md` after each batch:

```markdown
### Instance [N] Updates:
- [Date Time]: Batch [N] - [X]/50 conversations complete
  - Major discoveries: [list]
  - Entities extracted: [count]
  - Cross-instance questions: [count]
  - Next batch: [batch_id]
```

---

## 🎯 Quality Standards (All Instances)

### Every Conversation Must Have:
1. Metadata JSON file (`_metadata.json`)
2. Metadata markdown file (`_metadata.md`)
3. Entities with consistent IDs (use `entity_registry.json`)
4. Evidence-based claims (minimum 3 conversation citations)
5. SAREC framework (Score, Assessment, Reasoning, Evidence, Confidence)

### Confidence Calibration:
- **0.9-1.0**: Explicit, repeated, central (20+ mentions)
- **0.7-0.9**: Strong implicit evidence (10+ conversations)
- **0.5-0.7**: Moderate evidence (5-10 conversations)
- **0.3-0.5**: Weak evidence (3-5 mentions)
- **Below 0.3**: Too speculative (need more evidence)

### Entity ID Format:
- People: `person.[firstname_lastname]`
- Projects: `project.[project_name]`
- Organizations: `org.[org_name]`
- Concepts: `concept.[concept_name]`
- Values: `value.[value_name]`
- Knowledge: `knowledge.[domain_name]`

---

## 🚨 Common Pitfalls to Avoid

### ❌ DON'T:
- Cross instance boundaries (each has exclusive range)
- Create entities without checking entity_registry.json first
- Make claims without evidence (minimum 3 conversations)
- Skip metadata file creation
- Forget to update COORDINATION.md
- Work in isolation (post to cross_instance_notes.md!)

### ✅ DO:
- Stay in your assigned range
- Use consistent entity IDs
- Provide evidence for every claim
- Create metadata for every conversation
- Update progress daily
- Communicate with other instances
- Ask cross-instance questions
- Validate findings from multiple perspectives

---

## 💡 Pro Tips

### For Instance 1 (Forward):
- You'll see ORIGINS of everything - document first mentions carefully
- Track evolution: novice → expert, idea → project, person → relationship
- Your cross-instance questions should be about OUTCOMES ("Did this persist?")

### For Instance 2 (Reverse):
- You'll see CURRENT STATE - this is the "ground truth" for what succeeded
- Track backwards: outcome → process → origin
- Your cross-instance questions should be about ORIGINS ("When did this start?")

### For Instance 3 (Middle):
- You're the VALIDATION HUB - you can see if Instance 1 and 2 findings meet
- Look for INFLECTION POINTS around Dec 2024
- Your cross-instance questions are bidirectional (ask both about origins AND outcomes)
- Your work quality is already excellent - maintain that standard!

---

## 🎬 Ready to Launch?

**Now**: Copy the 3 prompts above into 3 separate Claude Code windows

**Start analyzing**: Each instance begins their batch

**Sync daily**: Update COORDINATION.md and cross_instance_notes.md

**Quality check**: Use SAREC framework, create metadata files, validate claims

**Coordinate**: Ask cross-instance questions, validate findings, merge insights

---

**LET'S GO! 🚀**
