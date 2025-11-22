# Extraction Guide for ALL LLMs

> **Purpose**: Create a queryable "commonplace book" - tagged, sorted, timed database that Bilal can query to remember what he's worked on, who to follow up with, what he's actually up to, and discover unseen patterns.

**Last Updated**: 2025-11-22 (Instance 2, after Bilal feedback)

---

## 🎯 **WHAT WE'RE BUILDING**

### **Commonplace Book Features:**
- **Queryable**: "Show me all conversations about VX design"
- **Tagged**: Each entry has multiple tags (domain, emotion, people, projects)
- **Sorted**: By date, domain, person, project, emotion, etc.
- **Timed**: Precise dates, monthly snapshots, evolution tracking
- **Followup-ready**: "Who should I follow up with? When did I last talk to X?"
- **Pattern-revealing**: What's hidden? What am I avoiding? What's unseen?

---

## ⚡ **PRIORITY EXTRACTION AREAS** (Bilal's Feedback)

### **MUST EXTRACT:**
1. **Emotions** (positive, negative, ambivalent, intensity)
2. **Avoidance/Shadow** (what's being postponed, feared, hidden)
3. **Gaps** (what's missing, what's unclear, what's forgotten)
4. **Who to follow up with** (people mentioned but not contacted recently)
5. **What he's actually up to** (current projects, not just past)
6. **Unseen/unseens** (patterns he might not see)

### **ALSO EXTRACT:**
7. Financial reality (little consulting, not making money)
8. Decision-making (prayer and values)
9. Family/personal (Joséphine, health, rest)
10. Temporal tracking (when did X happen? how long since Y?)

---

## 📋 **EXTRACTION SCHEMA (Commonplace Book Format)**

### **Entry Structure:**
Every conversation → multiple entries (one per topic/person/project)

```json
{
  "entry_id": "entry_20251121_happiness_tracker_muhasaba",
  "conversation_id": "1f620fa8",
  "conversation_title": "Happiness tracker notification channels",
  "date": "2025-11-21",
  "source": "claude",

  "tags": {
    "domains": ["wellbeing", "Islamic_practice", "technology", "product_design"],
    "people": [],
    "projects": ["happiness_tracker"],
    "organizations": [],
    "concepts": ["muhasaba", "muraja3a", "ESM", "SMS", "WhatsApp"],
    "emotions": ["curious", "practical", "frustrated_with_tech_constraints"],
    "decision_type": ["technical_design", "vendor_selection"],
    "location": [],
    "custom": ["notification_design", "islamic_tech_integration"]
  },

  "content": {
    "summary": "Bilal wants to build happiness tracker integrated with Islamic practices (muhasaba/muraja'a), exploring notification channels (SMS vs WhatsApp vs PWA)",
    "bilal_quotes": [
      "I want to make something like a happiness tracker that sends messages every so often randomly to accurately measure happiness - also maybe to connect it to muhasaba muraja3a"
    ],
    "key_insights": [
      "Integration of tech + Islamic spiritual practices is a recurring theme",
      "Practical constraints (WhatsApp hard/expensive, SMS costly) shape design decisions",
      "Random sampling (ESM) for accurate measurement without anticipation bias"
    ],
    "user_questions": [
      "How can I do it best to get notifications for people who don't want to get an app and we don't have WhatsApp or email notifications are flooded what can we do?",
      "Is it easy or hard to automatically do WhatsApp?"
    ]
  },

  "emotion_tracking": {
    "positive": ["Excited about Islamic practices integration", "Curious about ESM methodology"],
    "negative": ["Frustrated with WhatsApp API complexity", "Concerned about SMS costs"],
    "ambivalent": [],
    "intensity": "medium",
    "context": "Ideation phase - exploring options, hitting practical constraints"
  },

  "avoidance_shadow": {
    "avoided": [],
    "procrastinated": [],
    "feared": [],
    "shadows": [],
    "note": "None detected - active exploration mode"
  },

  "financial_mentions": {
    "costs": ["SMS: $3-5/person/month (too expensive for scale)"],
    "revenue": [],
    "grants": [],
    "time": "Ideation phase, <5 hours invested so far",
    "constraints": "Cost sensitivity - looking for free/low-cost options"
  },

  "people_followup": {
    "mentioned": [],
    "should_contact": [],
    "last_contact": {}
  },

  "projects_status": {
    "happiness_tracker": {
      "status": "ideation",
      "stage": "exploring notification channels",
      "blockers": ["WhatsApp automation difficulty", "SMS cost"],
      "next_steps": ["Decide on notification channel", "Build MVP"],
      "time_since_started": "new (2025-11-21)",
      "time_since_last_mention": "0 days (current)"
    }
  },

  "decision_making": {
    "decision": "Which notification channel for happiness tracker?",
    "options": ["SMS (Twilio)", "WhatsApp Business API", "PWA browser notifications", "Telegram bot"],
    "criteria": ["User accessibility", "Cost", "Technical feasibility", "Ease of automation"],
    "recommendation_from_llm": "SMS via Twilio (most reliable despite cost)",
    "bilal_decision": "unknown - still exploring",
    "process": "Practical exploration, asking LLM for technical advice",
    "values_alignment": "Islamic practice integration (muhasaba/muraja'a)"
  },

  "temporal": {
    "date": "2025-11-21",
    "month": "2025-11",
    "quarter": "2025-Q4",
    "year": "2025",
    "time_since_event": {},
    "related_past_events": [],
    "related_future_events": []
  },

  "queryable_fields": {
    "can_query_by": [
      "date", "month", "year", "domain", "person", "project", "organization",
      "concept", "emotion", "location", "decision_type", "financial_mention",
      "avoidance_type", "followup_needed", "project_status"
    ]
  },

  "confidence": 0.85,
  "extraction_notes": "User voice only, high confidence on Islamic integration theme"
}
```

---

## 🔍 **WHAT TO EXTRACT (Detailed)**

### **1. EMOTIONS (Priority!)**

**Positive emotions to track:**
- Excited, curious, grateful, joyful, energized, inspired, confident, proud, hopeful
- **Extract from**: "I'm excited about...", "I love...", "This is amazing..."
- **Tag intensity**: low (mentioned once) → medium (repeated) → high (emphatic, multiple mentions)

**Negative emotions to track:**
- Frustrated, anxious, guilty, ashamed, fearful, angry, sad, overwhelmed, stuck, drained
- **Extract from**: "I'm frustrated with...", "I feel guilty about...", "I'm scared to..."
- **Tag intensity**: low → medium → high

**Ambivalent emotions to track:**
- Conflicted, uncertain, torn, ambivalent, hesitant
- **Extract from**: "On one hand... on the other...", "I'm not sure if...", "Part of me wants... but..."

**Context**: What triggered the emotion? Project? Person? Decision? External event?

---

### **2. AVOIDANCE/SHADOW (Priority!)**

**What to look for:**

**"I should..." statements** (unfulfilled intentions):
- "I should update my website" → AVOIDED
- "I need to call X" → PROCRASTINATED
- "I really should reach out to Y" → DELAYED

**Repeated postponement:**
- Project mentioned in March, no progress by June → STUCK
- "Still haven't done X" → PROCRASTINATION
- Website mentioned 5 times, never updated → AVOIDANCE

**Fears blocking action:**
- "I'm scared to call people" → FEAR
- "I feel ashamed to share during war" → SHAME/GUILT
- "I don't want to be seen as promoting myself" → FEAR_OF_JUDGMENT

**Projects that disappear:**
- Mentioned enthusiastically, then never again → ABANDONED
- Track: When last mentioned? What happened?

**Shadows (things in the dark):**
- What's NOT being talked about? (e.g., if finances never mentioned → shadow)
- What's glossed over? (e.g., "Bloom ended" with no details → shadow)
- What's rationalized? (e.g., "I'm too busy for X" but spending time on Y → shadow)

---

### **3. GAPS (Priority!)**

**Information gaps:**
- "When did Bilal leave Bloom?" → GAP (Instance 2 doesn't know)
- "How much does Nur Coop make annually?" → GAP (never mentioned)
- "Does Bilal have children?" → GAP (pregnancy mentioned March 2023, current status unknown)

**Temporal gaps:**
- "When did VX methodology emerge?" → GAP (need Instance 1 to find)
- "When did Bilal meet Aaron Hurst?" → GAP

**Relationship gaps:**
- "How did Bilal meet Saleh?" → GAP
- "What's Joséphine's background?" → GAP (co-owner of Nur Coop, but how did they meet?)

**Project gaps:**
- "Why did Flybrary pause?" → GAP
- "What happened to GEMSI?" → GAP

**Tag all gaps** for Bilal to fill in or for other instances to investigate.

---

### **4. WHO TO FOLLOW UP WITH (Priority!)**

**Track for each person mentioned:**

```json
{
  "person": "Aaron Hurst",
  "relationship": "VX collaborator, Wellbeing Project founder",
  "last_mentioned": "2025-11-20",
  "last_contact_inferred": "2025-11 (active collaboration on Wellbeing Registry)",
  "follow_up_needed": "low (currently collaborating)",
  "follow_up_reason": null,
  "emotional_quality": "intellectually stimulating, professionally generative",
  "network_position": "professional mentor, methodological co-developer"
}
```

```json
{
  "person": "Joe Edelman",
  "relationship": "Friend/mentor since 2014 (per Instance 1)",
  "last_mentioned": "unknown in Nov 2024 conversations",
  "last_contact_inferred": "unknown",
  "follow_up_needed": "HIGH (long-term friend, not mentioned recently)",
  "follow_up_reason": "Check in - it's been a while?",
  "emotional_quality": "unknown (need to extract)",
  "network_position": "long-term mentor (per Instance 1)"
}
```

**Flag HIGH priority for people who:**
- Were important in the past (Instance 1 found them) but not mentioned recently (Instance 2)
- Bilal expressed intention to contact but didn't ("I should call X")
- Mentioned positively but not followed up ("It was great talking to Y")

---

### **5. WHAT HE'S ACTUALLY UP TO (Priority!)**

**Current projects (Nov 2024):**

For each project, track:
```json
{
  "project": "Beit-al-Atlas Artist Residency",
  "status": "grant_writing_phase",
  "last_activity": "2025-11-17 (grant application prepared)",
  "next_milestone": "Wait for AFAC decision (submitted Nov 21)",
  "time_invested": "Significant (full grant application prepared)",
  "emotional_investment": "High (philosophy: 'unlikely friendships heal divided planet')",
  "financial_investment": "EUR 35K grant sought",
  "collaborators": ["Saleh Ramadan", "Joséphine", "community partners"],
  "what_next": "WAITING (grant decision expected March 2026)",
  "blockers": [],
  "opportunities": []
}
```

Track monthly: What's active NOW vs what was active last month vs 3 months ago?

---

### **6. UNSEEN/UNSEENS (Priority!)**

**Patterns Bilal might not see:**

**Pattern type: Recurring tension**
- Innovation vs Completion (Instance 1 found this March 2023)
- Still visible Nov 2024? (VX methodology developed, but website still not updated)
- UNSEEN: Does Bilal know this tension is chronic?

**Pattern type: Project lifecycle**
- Bloom: Started ~2020, ended Nov 2024 (~4 years)
- Flybrary: Mentioned March 2023, paused by then
- GEMSI: Founded ~2011 (per Instance 1), status unknown
- Beit-al-Atlas: Active Nov 2024
- Nur Coop: Active 10 years (2015-2024+)
- UNSEEN: What makes projects persist (Nur Coop, Beit-al-Atlas) vs end (Bloom, Flybrary)?

**Pattern type: Relationship persistence**
- Joe Edelman: Friend/mentor since 2014 (11+ years)
- Joséphine: Marriage date unknown, but 10+ years (Nur Coop founded ~2015)
- Saleh: Unknown start, active Nov 2024
- UNSEEN: Who persists over time? What makes these relationships last?

**Pattern type: Geographic movement**
- Unknown origins → Lille, France (when?)
- Considering Madison, WI (Nov 2024)
- UK Global Talent Visa applied March 2023 (outcome unknown)
- UNSEEN: Why the moves? What's the pattern?

**Pattern type: Values evolution**
- "Curious Knowledge-Weaver" (March 2023) → "VX Design" (Nov 2024)
- Tech/education work → Wellbeing/contemplative work
- UNSEEN: Was this intentional evolution or gradual drift?

**Pattern type: Decision-making**
- Bilal says: "Prayer and values"
- Evidence: Islamic practice integration (muhasaba/muraja'a), VX methodology (values-first design)
- UNSEEN: Does Bilal recognize this consistency? Is this conscious?

**Pattern type: Avoidance**
- Website update: Mentioned repeatedly, not done
- Social media: Conflicted about sharing during war, hasn't resolved
- Calling people: "Scared to call people" (mentioned somewhere?)
- UNSEEN: What's the common thread in avoidance? Fear of visibility? Self-promotion discomfort?

---

## 📊 **EXTRACTION PROCESS (Step-by-Step)**

### **For Each Conversation:**

**STEP 1: Scan for substantive user input** (>100 words)
- If trivial (recipe, quick tech fix) → SKIP
- If substantive → CONTINUE

**STEP 2: Extract basic metadata**
- Conversation ID, title, date, source, message count
- User word count (estimate)
- Domains covered (wellbeing, tech, Islamic practice, etc.)

**STEP 3: Extract EMOTIONS (Priority!)**
- Read user messages for emotion words: "I feel...", "I'm excited/frustrated/anxious..."
- Infer from context: Procrastination = avoidance/fear, Repeated mention = care/importance
- Tag: positive, negative, ambivalent
- Rate intensity: low, medium, high
- Note context: What triggered this emotion?

**STEP 4: Extract AVOIDANCE/SHADOW (Priority!)**
- Look for: "I should...", "Still haven't...", "I need to..."
- Look for: Fears stated ("scared to...", "ashamed to...")
- Look for: Projects mentioned then disappearing
- Look for: Rationalizations ("too busy for X" while doing Y)
- Tag as: avoided, procrastinated, feared, shadow

**STEP 5: Extract WHO TO FOLLOW UP WITH**
- List all people mentioned by name
- For each: Relationship, last mentioned, last contact (inferred), follow-up needed?
- Flag HIGH priority: Long-term connections not mentioned recently

**STEP 6: Extract WHAT HE'S ACTUALLY UP TO**
- Current project status (ideation, active, paused, waiting)
- Last activity, next milestone, blockers, opportunities
- Time/emotional/financial investment

**STEP 7: Extract GAPS**
- What's unclear? (when, why, how, who)
- What's missing? (family, finances, health)
- What needs Instance 1 to find? (origins, emergence)

**STEP 8: Extract UNSEEN PATTERNS**
- What patterns might Bilal not see?
- What's recurring? (tensions, project lifecycles, relationship persistence)
- What's chronic? (avoidance patterns, decision-making style)

**STEP 9: Tag for queryability**
- Domains, people, projects, organizations, concepts
- Emotions, decisions, locations, financial mentions
- Avoidance types, follow-up needs, project status

**STEP 10: Save as commonplace entry**
- Multiple entries per conversation (one per major topic)
- Queryable by: date, domain, person, project, emotion, etc.
- Include summary, quotes, insights, questions

---

## 🔍 **QUERY EXAMPLES (What Bilal Can Ask)**

### **Project queries:**
- "Show me all mentions of Beit-al-Atlas"
- "What's the status of happiness tracker?"
- "When did I last work on VX methodology?"
- "What happened to Flybrary?"

### **People queries:**
- "Who should I follow up with?"
- "When did I last mention Joe Edelman?"
- "Show me all conversations with Aaron Hurst mentioned"
- "Who are my long-term collaborators?"

### **Emotion queries:**
- "When was I most excited in Nov 2024?"
- "What am I frustrated about?"
- "Show me all conversations where I felt conflicted"
- "What brings me joy?"

### **Avoidance queries:**
- "What am I avoiding?"
- "What have I procrastinated on?"
- "What did I say I 'should' do but didn't?"
- "What are my shadows?"

### **Temporal queries:**
- "What was I working on in Oct 2024?"
- "How has my focus changed from Sept to Nov 2024?"
- "When did I start working on X?"
- "What projects have lasted >2 years?"

### **Gap queries:**
- "What don't I know about my own work?"
- "What information is missing?"
- "What questions are unanswered?"

### **Pattern queries:**
- "What patterns am I not seeing?"
- "What keeps recurring?"
- "What makes projects succeed vs fail?"
- "What makes relationships last?"

---

## ⚙️ **FOR ALL LLMs: EXTRACTION RULES**

### **✅ DO:**
1. **Extract from user messages ONLY** (not LLM responses)
2. **Track emotions explicitly** (positive, negative, ambivalent, intensity, context)
3. **Flag avoidance aggressively** ("I should", procrastination, fears, shadows)
4. **Note all gaps** (missing info, unclear timeline, unknown relationships)
5. **Track who to follow up with** (people mentioned, last contact, follow-up needed)
6. **Describe what he's actually up to** (current project status, next steps)
7. **Identify unseen patterns** (recurring tensions, project lifecycles, relationship persistence)
8. **Tag for queryability** (domain, person, project, emotion, etc.)
9. **Include confidence scores** (0.9-1.0 = explicit, 0.7-0.9 = inferred, 0.5-0.7 = speculative)
10. **Save in commonplace format** (multiple entries per conversation, queryable fields)

### **❌ DON'T:**
1. **Don't extract from LLM responses as if they're Bilal's thoughts**
2. **Don't skip emotions** (this is a priority!)
3. **Don't ignore avoidance** (shadows are important!)
4. **Don't skip trivial-seeming details** (they might reveal patterns)
5. **Don't assume** (mark as GAP if unclear)
6. **Don't batch** (create separate entries for separate topics)
7. **Don't editorialize** (extract what's there, not what should be there)
8. **Don't forget temporal context** (when, how long, time since)
9. **Don't miss financial mentions** (money, time, costs, constraints)
10. **Don't skip family/personal** (Joséphine, health, hobbies, rest)

---

## 🎯 **BILAL'S FEEDBACK (Context for All LLMs)**

**Purpose:** Create a queryable commonplace book to:
- Remember what I've worked on
- Know who to follow up with
- Understand what I'm actually up to
- Discover unseen/unseens
- Track avoidance/shadow work

**Answers to key questions:**
- **AFAC grant**: ✅ Submitted Nov 21, waiting for decision (expected March 2026)
- **Bloom departure**: Didn't align with cofounder anymore, glad to not be in shadows of org
- **Money**: Not making money, little consulting
- **Decision-making**: Prayer and values

**Priorities (Bilal's explicit likes):**
1. Avoidance/shadow work
2. Gaps (what's missing, unclear)
3. Emotions (feelings, not just facts)

**Use this context to prioritize extraction!**

---

## 📝 **OUTPUT FORMAT**

Save as: `commonplace_entries_batch_[number]_[instance].json`

```json
{
  "batch": 71,
  "instance": 2,
  "direction": "reverse (newest→oldest)",
  "date_range": "2025-11-21 to 2025-11-08",
  "conversations_analyzed": 50,
  "entries_created": 150,

  "entries": [
    {
      "entry_id": "entry_20251121_happiness_tracker_muhasaba",
      "conversation_id": "1f620fa8",
      ...
    },
    ...
  ],

  "summary": {
    "emotions_tracked": 47,
    "avoidance_flagged": 12,
    "gaps_identified": 23,
    "follow_ups_needed": 8,
    "unseen_patterns": 5
  }
}
```

---

**This guide ensures ALL LLMs (Instance 1, Instance 2, future instances) extract consistently and create a unified, queryable commonplace book for Bilal.**

Yallah! 🚀
