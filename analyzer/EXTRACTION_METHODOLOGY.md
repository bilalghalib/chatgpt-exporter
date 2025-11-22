# Conversation Analysis Methodology

> **Goal**: Extract Bilal's voice, theory of mind, projects, patterns, blindspots, and opportunities from 3,517 conversations

---

## Analysis Strategy

### Batched Processing
- **Batch size**: 50 conversations
- **Order**: Chronological (2023-02-27 → 2025-11-22)
- **Checkpoints**: After each batch, save progress
- **Total batches**: 71 batches (3,517 ÷ 50 = 70.34)

### What We're Looking For

#### 1. **USER VOICE** (High Priority)
- Substantive user inputs >100 words
- User questions (reveals learning path)
- User creative prompts & instructions
- User code examples
- User problem descriptions
- User self-reflections

#### 2. **THEORY OF MIND** (Meta-level)
- How does Bilal think?
- What are his assumptions?
- What does he value?
- How does he frame problems?
- What does he believe about the world?
- How does his thinking evolve over time?

#### 3. **PROJECTS & INITIATIVES**
- Named projects (e.g., "Bloom", "Flybrary", "GEMSI")
- Unnamed initiatives (e.g., "building a dashboard for...")
- Active vs abandoned projects
- Project evolution over time
- Cross-references between projects

#### 4. **DOMAINS OF EXPERTISE**
- What topics does he engage deeply with?
- What does he teach vs what does he learn?
- Where is he an expert vs a learner?
- Domain evolution over time

#### 5. **RECURRING PATTERNS**
- Repeated questions (unsolved problems)
- Repeated topics (core interests)
- Repeated challenges (blindspots)
- Repeated language/phrases (communication style)

#### 6. **BLINDSPOTS & OPPORTUNITIES**
- Questions asked but never resolved
- Topics approached but never completed
- Skills identified as weaknesses (in his own words)
- Gaps between what he wants to do vs what he does
- Missed connections between conversations

---

## Extraction Rules

### Priority System (What to Extract First)

**Priority 1: Always Extract**
- User turns >100 words (FULL TEXT)
- All user questions
- All user code/prompts
- User self-reflections ("I struggle with...", "I want to...")
- Project mentions (named projects)

**Priority 2: Extract if Novel**
- User insights/hypotheses (confidence >0.8)
- User domain expertise demonstrations
- User creative directions
- Unusual topics for the user

**Priority 3: Extract Rarely**
- LLM responses (ONLY if genuinely novel or contains user-requested info)
- Generic conversations
- Technical troubleshooting (unless reveals pattern)

### Tag Taxonomy

#### **Primary Tags** (What is this?)
- `substantive_user_input` - Large blocks of user text
- `user_question` - User asking questions
- `user_code` - User providing code
- `user_prompt` - User crafting prompts for LLM
- `user_self_reflection` - User reflecting on themselves
- `project_mention` - Reference to a named project
- `domain_expertise` - User demonstrating expertise
- `learning_progression` - User learning something over time
- `recurring_pattern` - Same topic/question appears multiple times
- `theory_of_mind` - Reveals how user thinks

#### **Domain Tags** (What topic?)
- `education` - Teaching, learning, curriculum design
- `entrepreneurship` - Business, startups, social enterprise
- `technology` - Coding, AI, tools, software
- `social_impact` - Nonprofits, social good, MENA region
- `research` - Academic research, analysis, data
- `creative` - Art, writing, design, creative work
- `personal` - Life, family, well-being, self-improvement
- `finance` - Money, budgets, fundraising, sustainability
- `management` - Leadership, team, organization
- `philosophy` - Meaning, values, ethics, big questions

#### **Project Tags** (Which project?)
- `bloom` - Bloom.pm organization
- `gemsi` - GEMSI.org nonprofit
- `flybrary` - Flybrary.co book lending
- `[dynamic]` - New projects discovered during analysis

#### **Meta Tags** (Context)
- `blindspot` - User identifies weakness or repeated challenge
- `opportunity` - Unseen connection or potential
- `evolution` - User's thinking/approach changes over time
- `core_value` - Deeply held belief/principle
- `fear` - User expresses fear/anxiety ("scared to call people")
- `aspiration` - User expresses goal/dream

### Source Tracking

Every extraction includes:
```json
{
  "conversation_id": "uuid",
  "conversation_title": "string",
  "conversation_date": "YYYY-MM-DD",
  "message_id": "uuid",
  "message_role": "user",
  "message_sequence": 0,
  "extraction_timestamp": "ISO-8601",
  "batch_number": 1
}
```

---

## Theory of Mind Builder

For each batch, we extract:

### **Beliefs & Assumptions**
- What does Bilal believe is true?
- What assumptions does he make about the world?
- Example: "I believe education can change the world" (inferred from actions)

### **Values & Principles**
- What does he care about?
- What principles guide his decisions?
- Example: "Access to knowledge", "Social impact", "Maker culture"

### **Mental Models**
- How does he frame problems?
- What frameworks does he use?
- Example: Uses educational frameworks (PERMAH, Universal Skills, etc.)

### **Communication Style**
- How does he ask questions?
- How does he explain things?
- What language patterns appear?
- Example: "I'm nerdy", "I get lost on questions", concise questions

### **Problem-Solving Patterns**
- How does he approach challenges?
- What's his default response?
- Example: Research-first, seeks frameworks, comparative analysis

### **Evolution Over Time**
- How do beliefs change?
- How do priorities shift?
- What triggers changes in thinking?

---

## Checkpoint System

After every 50 conversations:

1. **Save progress** to `knowledge_base_checkpoint_[batch].json`
2. **Generate summary**:
   - Conversations analyzed: X/3517
   - New projects discovered: N
   - New domains identified: N
   - Theory of mind updates: N
   - Patterns found: N
3. **Validate tags**:
   - Check for tag duplication
   - Cluster similar tags
   - Merge redundant categories
4. **Look for gaps**:
   - What questions are unanswered?
   - What projects are mentioned but not explained?
   - What topics appear but aren't explored?

---

## Outputs

### After Each Batch (50 conversations)
- `checkpoint_batch_[N].json` - Full data
- `summary_batch_[N].md` - Human-readable summary

### After Full Analysis (3,517 conversations)
- `bilal_knowledge_base.json` - Complete structured data
- `bilal_theory_of_mind.json` - Beliefs, values, mental models
- `bilal_projects.json` - All projects with timelines
- `bilal_domains.json` - Expertise map
- `bilal_patterns.json` - Recurring themes, blindspots, opportunities
- `bilal_timeline.json` - Chronological evolution

---

## Quality Checks

### Every 50 Conversations
- [ ] All user inputs >100 words extracted?
- [ ] All user questions captured?
- [ ] Tags consistent with taxonomy?
- [ ] Sources properly tracked?
- [ ] Theory of mind updated?

### Every 200 Conversations (4 batches)
- [ ] Review tag clusters - any duplicates?
- [ ] Review patterns - any emerging themes?
- [ ] Review projects - any missing context?
- [ ] Review blindspots - any new insights?

---

## Tag Clustering Strategy

### Automatic Clustering
- Group tags by co-occurrence
- Identify parent-child relationships
- Example: `education` + `bloom` → `bloom_education_work`

### Manual Review (Every 200 conversations)
- Are similar concepts using different tags?
- Should any tags be merged?
- Should any tags be split?

### Hierarchical Structure
```
Primary → Secondary → Tertiary
education → curriculum_design → bloom_curriculum
entrepreneurship → social_enterprise → gemsi_work
technology → ai_tools → chatgpt_exploration
```

---

## Next Steps

1. ✅ Create JSON schema for knowledge base
2. ✅ Define extraction methodology (this document)
3. 🔄 Analyze batch 1 (conversations 1-50)
4. ⏳ Create checkpoint 1
5. ⏳ Analyze batch 2 (conversations 51-100)
6. ⏳ Continue...

---

**Last Updated**: 2025-11-22
**Status**: Ready for batch analysis
**Total Batches Planned**: 71
