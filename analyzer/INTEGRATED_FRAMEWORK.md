# Integrated Analysis Framework

> **Combining**: User-Centric Extraction + SAREC + Come Alive + Meaning Extraction

---

## Framework Integration

### 1. SAREC Protocol (Assessment Structure)

Every extraction includes SAREC structure:

```json
{
  "id": "bilal.meaning.creative_flow.v1",
  "score": 0.85,
  "reasoning": "Repeated expressions of 'aliveness' around creative work; consistent avoidance of structured tasks",
  "evidence": [
    {"type": "quote", "text": "I get lost on questions when they capture me", "source": "374f82b7", "date": "2023-03-27"},
    {"type": "pattern", "name": "research_enthusiasm", "frequency": 47},
    {"type": "tension", "description": "Innovation vs Getting Things Done"}
  ],
  "confidence": 0.85,
  "assessor": {"type": "claude-sonnet-4.5", "version": "2025-11"},
  "timestamp": "2025-11-22T19:30:00Z"
}
```

### 2. Come Alive Framework (CAPs, IAPs, Values)

#### Constitutive Actions (CAPs)
**What Bilal does for its own sake** - reveals sources of meaning:

```yaml
cap:
  description: "Getting lost in research questions"
  manifestations:
    - "Deep dives into ChatGPT usage"
    - "Framework comparisons (PERMAH, Universal Skills, etc.)"
    - "Exploring maker culture, hackerspaces"
  attention_policies:
    - "QUESTIONS that spark genuine curiosity"
    - "FRAMEWORKS that reveal patterns"
    - "CONNECTIONS between disparate ideas"
  evidence:
    - quote: "I'm nerdy, great at research, I get lost on questions when they capture me"
      source: "374f82b7"
      date: "2023-03-27"
```

#### Instrumental Actions (IAPs)
**What Bilal feels he "has to" do** - reveals tensions:

```yaml
iap:
  description: "Finishing structured work products"
  manifestations:
    - "Completing presentations"
    - "Calling potential clients"
    - "Turning research into action"
  attention_policies:
    - "OBLIGATIONS that create resistance"
    - "DEADLINES that interrupt flow"
    - "TASKS that feel draining"
  related_tensions:
    - "Innovation vs Completion"
    - "Research vs Action"
  evidence:
    - quote: "That's the problem I'm facing, how to stop innovating and get things to done"
    - quote: "I'm also scared to call people - that fear leads to procrastination"
```

#### Tensions (Growth Guides)

```yaml
tension:
  type: "CAP vs IAP"  # or "CAP vs CAP"
  title: "Creative Exploration vs Task Completion"
  from:
    current_state:
      iaps: ["Finish presentation", "Call clients", "Complete proposals"]
      emotions: ["Fear", "Procrastination", "Scattered"]
      quotes:
        - "I feel like I'm all over the place"
        - "I'm also scared to call people"
  to:
    potential_values:
      - "Research-Driven Innovation"
      - "Collaborative Discovery"
      - "Framework-Based Learning"
    attention_policies:
      - "QUESTIONS that reveal deeper patterns"
      - "COLLABORATIONS that turn ideas into reality"
      - "FRAMEWORKS that bridge theory and practice"
```

#### Values (Clusters of CAPs)

```yaml
value:
  title: "Curious Knowledge-Weaver"
  date_discovered: "2023-03-27"
  description: "Finding meaning through connecting frameworks, exploring questions deeply, and sharing insights with others"
  caps_cluster:
    - "Getting lost in research questions"
    - "Comparing educational frameworks"
    - "Building hackerspaces and maker communities"
    - "Teaching entrepreneurship through exploration"
  attention_policies:
    - "QUESTIONS that open new territories of understanding"
    - "FRAMEWORKS that reveal hidden patterns"
    - "COMMUNITIES where curious minds gather"
    - "MOMENTS when disparate ideas suddenly connect"
  ground_truth:
    quotes:
      - "I'm nerdy, great at research, I get lost on questions when they capture me"
      - "I would like to become more of an expert in something rather than a generalist"
    stories:
      - "Systematically explored 5+ educational frameworks in one conversation"
      - "Co-founded GEMSI to bring innovation culture to MENA"
```

### 3. Meaning Extraction (Attention Policies)

**Sources of Meaning** are identified through attention policies:

```yaml
source_of_meaning:
  title: "Education as Exploration, Not Instruction"
  attention_policies:
    - "QUESTIONS that reveal what learners truly care about"
    - "FRAMEWORKS that learners discover for themselves"
    - "MOMENTS when a student's eyes light up with connection"
    - "SPACES where curiosity drives the curriculum"
    - "INSIGHTS that emerge from grappling with real challenges"
  evidence:
    - "Designed Bloom curriculum around assessments + interventions for personal growth"
    - "Asked about online/remote performance assessments (COVID context)"
    - "Systematically compared multiple educational frameworks"
  confidence: 0.82
  first_observed: "2023-02-27"
  last_observed: "ongoing"
```

---

## Integrated Extraction Process

### For Each Conversation:

1. **Read user turns** (prioritize >100 words)
2. **Identify CAPs** (what does Bilal do for its own sake?)
3. **Identify IAPs** (what does he feel obligated to do?)
4. **Spot Tensions** (CAP vs CAP or IAP→CAP)
5. **Extract Attention Policies** (what does he pay attention to?)
6. **Cluster into Values** (when 3+ related CAPs appear)
7. **Structure with SAREC** (assessment, reasoning, evidence, confidence)

### Example Extraction Flow:

**Input** (from conversation):
> "I'm nerdy, great at research, I get lost on questions when they capture me like how should I use ChatGPT for work. And I ignore lots of important things that don't, which is a weakness."

**SAREC Extraction**:
```json
{
  "id": "bilal.cap.research_flow.001",
  "score": 0.92,
  "reasoning": "Self-identified pattern of deep engagement with questions; contrasted with 'important things' he ignores, suggesting CAP vs IAP tension",
  "evidence": [
    {"type": "quote", "text": "I get lost on questions when they capture me", "emotional_valence": "positive"},
    {"type": "quote", "text": "I ignore lots of important things that don't [capture me]", "emotional_valence": "negative"},
    {"type": "self_label", "text": "I'm nerdy"}
  ],
  "confidence": 0.92
}
```

**CAP Identified**:
```yaml
cap:
  description: "Getting absorbed in curiosity-driven research"
  attention_policies:
    - "QUESTIONS that spark genuine fascination"
    - "EXPLORATIONS where time disappears"
    - "TOPICS that pull me in despite 'should do' obligations"
```

**IAP Identified**:
```yaml
iap:
  description: "Important but unengaging tasks"
  related_tension: "What makes me come alive vs What I 'should' focus on"
```

**Tension**:
```yaml
tension:
  type: "CAP vs IAP"
  title: "Curiosity Flow vs Important But Boring"
  potential_transformation: "Find ways to make 'important things' capture his curiosity, or structure work to honor his research flow"
```

---

## Values Card Generation

When we identify a **cluster of CAPs** with coherent attention policies:

```markdown
## Values Card: "Curious Knowledge-Weaver"

**What you pay attention to:**
- QUESTIONS that open new territories of understanding
- FRAMEWORKS that reveal hidden connections
- COMMUNITIES where curious minds collaborate
- MOMENTS when disparate ideas suddenly click together

**Where this shows up:**
- Getting lost in research about educational frameworks
- Building hackerspaces across MENA region
- Comparing assessment methods systematically
- Teaching entrepreneurship through exploration

**Your words:**
> "I'm nerdy, great at research, I get lost on questions when they capture me"

**What might not be visible to you:**
This isn't just "being curious" - it's a specific way of finding meaning through *connecting* knowledge, not just consuming it. You don't just read; you compare, map, and weave frameworks together.

**Tension this reveals:**
Your curiosity-driven flow conflicts with "getting things done" - but what if the things you need to "get done" could be reframed as research questions? ("How do we make Bloom financially sustainable?" becomes "What financial models enable mission-driven organizations to thrive?")
```

---

## Batch Analysis Structure

### Every 50 Conversations:

1. **Extract** (using integrated framework)
2. **Identify new CAPs, IAPs, tensions**
3. **Update attention policies**
4. **Cluster CAPs into values** (when patterns emerge)
5. **Generate values cards** (when confidence >0.8)
6. **Save checkpoint** with SAREC metadata
7. **Review for blindspots & opportunities**

### Checkpoint Schema:

```json
{
  "batch_number": 1,
  "conversations": "1-50",
  "date_range": "2023-02-27 to 2023-03-XX",
  "caps_discovered": 12,
  "iaps_discovered": 8,
  "tensions_identified": 5,
  "values_cards_generated": 2,
  "attention_policies": [
    "QUESTIONS that reveal patterns",
    "FRAMEWORKS that connect ideas",
    "..."
  ],
  "blindspots": [
    "Difficulty turning research into action",
    "Fear of outreach/calling people"
  ],
  "opportunities": [
    "Reframe 'getting things done' as research questions",
    "Partner with 'execution-minded' collaborators"
  ],
  "next_focus": "Track evolution of 'research vs action' tension"
}
```

---

## Quality Checklist

After each batch:

- [ ] All CAPs have attention policies?
- [ ] All tensions have "from → to" structure?
- [ ] All values cards grounded in specific quotes?
- [ ] SAREC confidence scores calibrated?
- [ ] Evidence traceable to source conversations?
- [ ] Attention policies specific (not vague/abstract)?
- [ ] Values cards show "what you might not see"?

---

**Ready to start Batch 1 (conversations 1-50)!**
