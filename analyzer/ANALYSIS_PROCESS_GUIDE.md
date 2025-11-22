# Per-Conversation Analysis Process Guide

> **Goal**: Extract rich qualitative data from individual conversations and maintain aggregate datasets

---

## 📋 Files to Update Per Conversation

### **For EACH Conversation Analyzed:**

```
exported_conversations/
├── [conversation].json                          (original - DO NOT MODIFY)
├── [conversation]_metadata.json                 (✨ CREATE - structured extraction)
└── [conversation]_metadata.md                   (✨ CREATE - human-readable summary)
```

### **After EACH Conversation (Update Aggregates):**

```
analyzer/
├── conversation_registry.json                   (UPDATE - mark conversation as analyzed)
├── instance_3_middle_outward/
│   ├── entities_aggregate.json                  (UPDATE - add new entities)
│   ├── projects_timeline.json                   (UPDATE - add/update project mentions)
│   └── values_aggregate.json                    (UPDATE - add/update values)
```

### **After EACH Batch (50 conversations):**

```
analyzer/instance_3_middle_outward/
├── checkpoint_batch_M0_middle.json              (CREATE - batch summary)
├── knowledge_graph_batch_M0_middle.json         (CREATE - batch graph)
└── extraction_batch_M0_middle.md                (CREATE - batch report)
```

### **Periodically (Significant Findings):**

```
analyzer/
├── cross_instance_notes.md                      (UPDATE - add questions/discoveries)
└── COORDINATION_INSTANCE3_MIDDLE_OUTWARD.md     (UPDATE - progress log)
```

---

## 🔄 Analysis Process (Step-by-Step)

### **STEP 1: Select Conversations to Analyze**

**Criteria for "Medium-Long" Conversations:**
- Message count: 15-100 messages (substantial but not overwhelming)
- Avoid very short (<5 messages) or extremely long (>200 messages)
- Prefer conversations with substantive user inputs (not just technical troubleshooting)

**Selection Command:**
```bash
# Get all conversations with message counts
for file in ./exported_conversations/*.json; do
  count=$(jq '.message_count' "$file" 2>/dev/null)
  if [ "$count" -ge 15 ] && [ "$count" -le 100 ]; then
    echo "$count|$(basename "$file")"
  fi
done | sort -rn | shuf | head -20
```

**Random Sampling:**
- Use batch M0 file list: `/tmp/batch_m0_files.txt` (already created for middle batch)
- Or random sample across entire corpus
- Aim for diversity: different dates, sources (ChatGPT/Claude), topics

---

### **STEP 2: Read & Analyze Conversation**

**Read the conversation:**
```bash
Read [conversation_file_path]
```

**Look for:**
1. **User Questions**: What is Bilal asking? What's he trying to understand/solve?
2. **User Statements**: Direct quotes revealing values, beliefs, decisions
3. **Documents Provided**: Book proposals, code, specifications, data
4. **Entities Mentioned**: People, projects, organizations, concepts
5. **Values Revealed**: What matters to Bilal in this conversation?
6. **Tensions**: Choices, dilemmas, conflicts
7. **Theory of Mind**: Beliefs, mental models, decision-making patterns
8. **Temporal Context**: Date, time of day, what else was happening concurrently

---

### **STEP 3: Create `[conversation]_metadata.json`**

**Template Structure:**
```json
{
  "conversation_id": "string",
  "source_file": "string",
  "analyzed_by": "instance_3_middle_outward",
  "batch": "M0|M1-B|M1-F|etc",
  "analysis_date": "YYYY-MM-DD",

  "conversation_metadata": {
    "title": "string",
    "created_at": "ISO-8601 timestamp",
    "source": "chatgpt|claude",
    "message_count": number
  },

  "temporal_data": {
    "created_at": "ISO-8601 full timestamp",
    "date_only": "YYYY-MM-DD",
    "time_of_day": {
      "hour": number,
      "period": "morning|afternoon|evening|night"
    },
    "day_of_week": "Monday|Tuesday|...",
    "position_in_corpus": "number/3517",
    "days_since_previous": number,
    "days_until_next": number
  },

  "substantive_content": {
    "user_questions": [
      {
        "text": "string",
        "sequence": number,
        "type": "exploration|technical|decision|reflection",
        "topic": "string"
      }
    ],
    "user_statements": [
      {
        "text": "string (exact quote)",
        "sequence": number,
        "significance": "CORE_VALUE|BELIEF|DECISION|REFLECTION",
        "values_revealed": ["array of value IDs"],
        "confidence": 0.0-1.0
      }
    ],
    "documents_provided": [...]
  },

  "entities_extracted": {
    "people": [
      {
        "id": "person.identifier",
        "name": "string",
        "relationship": "string",
        "roles": ["array"],
        "first_mentioned_here": boolean,
        "confidence": 0.0-1.0
      }
    ],
    "projects": [
      {
        "id": "project.identifier",
        "name": "string",
        "status": "ideation|active_development|launched|paused|abandoned",
        "first_mentioned_here": boolean,
        "status_change": "string (if status changed in this convo)",
        "confidence": 0.0-1.0
      }
    ],
    "organizations": [...],
    "concepts": [...],
    "values": [
      {
        "id": "value.identifier",
        "name": "string",
        "score": 0.0-1.0,
        "evidence": ["array"],
        "quotes": ["array"],
        "persistence": "stable|emerging|declining"
      }
    ],
    "tensions": [
      {
        "id": "tension.identifier",
        "type": "career_choice|technical|philosophical",
        "description": "string",
        "status": "unresolved|resolved|ongoing",
        "values_in_conflict": ["array"]
      }
    ]
  },

  "theory_of_mind": {
    "beliefs": ["array"],
    "mental_models": ["array"],
    "decision_making_patterns": {},
    "communication_style": {}
  },

  "rhythm_analysis": {
    "conversation_clustering": {
      "is_cluster_member": boolean,
      "gap_before": number,
      "gap_after": number
    },
    "project_activity": {
      "new_projects_mentioned": ["array"],
      "abandoned_projects": ["array"],
      "active_projects": ["array"]
    },
    "work_intensity_signals": {
      "urgency_detected": boolean,
      "stress_signals": ["array"],
      "flow_signals": ["array"]
    }
  },

  "cross_instance_questions": {
    "for_instance_1_origins": ["array"],
    "for_instance_2_outcomes": ["array"]
  },

  "tags": ["array"],
  "extraction_confidence": 0.0-1.0,
  "notes": "string"
}
```

**Save as:**
```
exported_conversations/[conversation_file_name]_metadata.json
```

---

### **STEP 4: Create `[conversation]_metadata.md`**

**Template Structure:**
```markdown
# [Conversation Title] - Analysis

**Conversation ID**: [id]
**Date**: YYYY-MM-DD
**Time**: HH:MM (if available)
**Source**: ChatGPT|Claude
**Analyzed By**: Instance 3
**Batch**: M0
**Position**: [N]/3517
**Confidence**: 0.0-1.0

---

## 🎯 Summary

[1-2 sentence summary of conversation purpose/outcome]

---

## 💬 Key User Inputs

### **Questions Asked:**
- [Question 1]
- [Question 2]

### **🔥 CORE STATEMENTS:**
> "[Direct quote showing value/belief/decision]"

**Significance**: [Why this matters]

---

## 💎 Values Extracted

### **[Value Name]** (Score: 0.XX)
**Evidence**: [What reveals this value]
**Quote**: "[Supporting quote]"
**Context**: [Situational context]

---

## 📦 Entities Discovered

### **Projects:**
- **[Project Name]**: Status, significance

### **People:**
- **[Person Name]**: Relationship, role

### **Organizations:**
- **[Org Name]**: Role, status

### **Concepts:**
- **[Concept Name]**: Definition, source

---

## ⚖️ Tensions Identified

### **[Tension Name]** (Status: unresolved|resolved)
**Type**: career_choice|technical|philosophical
**Description**: [What's the dilemma]
**Values in Conflict**: [Value A] vs [Value B]

---

## 🧠 Theory of Mind Insights

**Beliefs**: [What Bilal believes based on this conversation]
**Mental Models**: [Frameworks he uses]
**Decision-Making**: [How he approaches choices]
**Communication Style**: [Tone, formality, patterns]

---

## 🎵 Rhythm Signals

**Clustering**: [Part of burst or gap?]
**Project Activity**: [New projects? Abandoned?]
**Work Intensity**: [Urgency? Stress? Flow?]
**Time of Day**: [Morning/afternoon/evening/night]
**Gap Before**: [X days since previous conversation]

---

## 🔗 Connections

### **To Other Work:**
[How this connects to other projects/conversations]

### **Temporal Context:**
[What else was happening at this time?]

---

## 🔍 Cross-Instance Questions

### **For Instance 1 (Origins):**
- [Question about when something started]

### **For Instance 2 (Outcomes):**
- [Question about what happened after]

---

## 🏷️ Tags

`tag1` `tag2` `tag3`

---

## 📝 Analyst Notes

[Free-form observations, patterns noticed, significance]

---

**Last Updated**: YYYY-MM-DD
**Extraction Confidence**: 0.XX
```

**Save as:**
```
exported_conversations/[conversation_file_name]_metadata.md
```

---

### **STEP 5: Update Aggregate Files**

#### **A. Update `conversation_registry.json`**

**Add entry:**
```json
{
  "conversations": {
    "[conversation_id]": {
      "analyzed_by": "instance_3_middle_outward",
      "batch": "M0",
      "status": "completed",
      "date": "YYYY-MM-DD",
      "position": "number/3517",
      "metadata_file": "[filename]_metadata.json"
    }
  }
}
```

#### **B. Update `entities_aggregate.json`**

**Create/update aggregate tracking all entities:**
```json
{
  "people": {
    "person.bilal_ghalib": {
      "name": "Bilal Ghalib",
      "first_mentioned": "conversation_id (earliest)",
      "last_mentioned": "conversation_id (latest)",
      "mention_count": number,
      "conversations": ["array of conversation IDs"],
      "roles": ["array aggregated across all mentions"],
      "confidence": 0.0-1.0
    }
  },
  "projects": {
    "project.barakanomics": {
      "name": "Barakanomics",
      "first_mentioned": "conversation_id",
      "last_mentioned": "conversation_id",
      "status_timeline": [
        {"date": "YYYY-MM-DD", "status": "ideation", "conversation_id": "..."},
        {"date": "YYYY-MM-DD", "status": "active_development", "conversation_id": "..."}
      ],
      "lifespan_days": number,
      "conversations": ["array"],
      "confidence": 0.0-1.0
    }
  }
}
```

**Save as:**
```
analyzer/instance_3_middle_outward/entities_aggregate.json
```

#### **C. Update `projects_timeline.json`**

**Track all project lifecycle events:**
```json
{
  "timeline": [
    {
      "date": "YYYY-MM-DD",
      "project_id": "project.barakanomics",
      "event": "first_mentioned",
      "status": "ideation",
      "conversation_id": "...",
      "evidence": "Quote or description"
    },
    {
      "date": "YYYY-MM-DD",
      "project_id": "project.friend_reflection_tool",
      "event": "status_change",
      "from_status": "ideation",
      "to_status": "active_development",
      "conversation_id": "...",
      "evidence": "..."
    }
  ],
  "projects_summary": {
    "total_projects": number,
    "active": number,
    "abandoned": number,
    "completed": number,
    "average_lifespan_days": number
  }
}
```

**Save as:**
```
analyzer/instance_3_middle_outward/projects_timeline.json
```

#### **D. Update `values_aggregate.json`**

**Track values across conversations:**
```json
{
  "values": {
    "value.autonomy_meaning_driven_work": {
      "name": "Autonomy + Meaning-Driven Work",
      "first_observed": "YYYY-MM-DD",
      "last_observed": "YYYY-MM-DD",
      "observations": [
        {
          "date": "YYYY-MM-DD",
          "conversation_id": "...",
          "score": 0.95,
          "evidence": "Quote",
          "context": "Consulting vs business choice"
        }
      ],
      "average_score": 0.93,
      "persistence": "stable",
      "conversations_count": number
    }
  }
}
```

**Save as:**
```
analyzer/instance_3_middle_outward/values_aggregate.json
```

---

### **STEP 6: Update Cross-Instance Notes (If Significant)**

**When to update:**
- New major project discovered
- New core value identified
- Significant life event mentioned
- Question for other instances arises

**Add to `cross_instance_notes.md`:**
```markdown
## From Instance 3 (Middle→Outward):

**NEW FINDING** ([Date]):
- [Description of finding]
- **Question for Instance 1**: [When did this originate?]
- **Question for Instance 2**: [What's the outcome?]
```

---

### **STEP 7: Commit and Push**

**After analyzing 5-10 conversations:**
```bash
git add exported_conversations/*_metadata.json \
        exported_conversations/*_metadata.md \
        analyzer/conversation_registry.json \
        analyzer/instance_3_middle_outward/entities_aggregate.json \
        analyzer/instance_3_middle_outward/projects_timeline.json \
        analyzer/instance_3_middle_outward/values_aggregate.json \
        analyzer/cross_instance_notes.md

git commit -m "feat: analyze conversations [N-M] - [brief findings summary]

- Conversations analyzed: [list]
- New entities: [count]
- New projects: [names]
- Core values: [identified]
- Significant findings: [1-2 key discoveries]"

git push -u origin claude/review-middle-instance-01X834jcH2HCRVAFef1T87dD
```

---

## 🎯 Quick Reference Checklist

**For Each Conversation:**
- [ ] Read conversation fully
- [ ] Extract entities, values, tensions, quotes
- [ ] Create `[conversation]_metadata.json`
- [ ] Create `[conversation]_metadata.md`
- [ ] Update `conversation_registry.json`
- [ ] Update `entities_aggregate.json`
- [ ] Update `projects_timeline.json`
- [ ] Update `values_aggregate.json`
- [ ] Update `cross_instance_notes.md` (if significant)
- [ ] Commit and push (every 5-10 conversations)

**Quality Checks:**
- [ ] All quotes are verbatim (exact from conversation)
- [ ] Confidence scores justified with evidence
- [ ] Entity IDs consistent (person.name_lastname format)
- [ ] Temporal data complete (dates, times, gaps)
- [ ] Cross-instance questions clear and specific
- [ ] Tags descriptive and searchable

---

## 📊 Progress Tracking

**Use conversation_registry.json to track:**
- Total conversations analyzed
- Coverage percentage (analyzed/3517)
- Batch progress (M0, M1-B, M1-F, etc.)
- Entities discovered per batch
- Values identified

**Generate status report:**
```bash
# Count analyzed conversations
jq '.conversations | length' analyzer/conversation_registry.json

# List analyzed conversation IDs
jq -r '.conversations | keys[]' analyzer/conversation_registry.json

# Check batch progress
jq '.batches.instance_3_middle_outward' analyzer/conversation_registry.json
```

---

**Last Updated**: 2025-11-22
**Status**: Process guide complete, ready for systematic analysis
