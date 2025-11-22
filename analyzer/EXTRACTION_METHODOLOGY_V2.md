# IMPROVED Extraction Methodology v2.0

> Incorporating meta-analysis feedback: emotions, family, finances, avoidance, user-voice-only

**Last Updated**: 2025-11-22 (Instance 2, post-meta-analysis)

---

## 🎯 **What to Extract (Priority Order)**

### **TIER 1: Always Extract (User Voice ONLY)**

**1. SUBSTANTIVE USER INPUT** (>100 words)
- Full text of user messages >100 words
- ONLY user messages, NOT LLM responses
- Mark source: user turn #, date, conversation ID

**2. EMOTIONS & AFFECT** ⭐ NEW
```json
{
  "emotion_tracking": {
    "positive": ["excited about VX methodology", "grateful for Saleh"],
    "negative": ["guilt about social media", "fear of calling people", "shame about promoting during war"],
    "ambivalent": ["conflicted about job offer", "uncertain about website"],
    "intensity": "low|medium|high",
    "context": "what triggered this emotion"
  }
}
```

**3. AVOIDANCE & PROCRASTINATION** ⭐ NEW
- "I should..." statements (unfulfilled intentions)
- Repeated procrastination patterns
- Projects mentioned then abandoned
- Fears/anxieties blocking action
- Mark as IAPs (Instrumental Actions - things felt as obligations)

**4. FINANCIAL & MATERIAL REALITY** ⭐ NEW
```json
{
  "financial_mentions": {
    "income_sources": ["Nur Coop", "Bloom salary", "consulting", "grants"],
    "amounts": ["EUR 35K grant", "$3-5/person/month SMS cost"],
    "constraints": ["cost prohibitive", "need new contracts"],
    "time_allocation": ["10 hours/week on X", "full-time role"],
    "geographic_constraints": ["visa status", "family ties", "housing"]
  }
}
```

**5. FAMILY & PERSONAL LIFE** ⭐ NEW
- Family mentions (Joséphine, children, parents, siblings, in-laws)
- Health/body/sleep patterns
- Non-work activities (cooking, exercise, hobbies)
- Friendships separate from work
- Rest/recreation/joy

**6. DECISION-MAKING PROCESS** ⭐ NEW
For each major decision, extract:
```json
{
  "decision": "Leave Bloom / Accept job offer / Submit grant",
  "options_considered": ["Stay", "Leave", "Negotiate"],
  "criteria": ["Values alignment", "Financial need", "Family impact", "Location", "Growth opportunity"],
  "who_consulted": ["Joséphine", "Saleh", "Aaron", "Prayer/meditation"],
  "what_tipped_balance": "specific moment or realization",
  "confidence_level": "0.0-1.0",
  "regrets_or_doubts": "any second-guessing"
}
```

**7. TEMPORAL GRANULARITY** ⭐ NEW
Track changes over time, not just static facts:
```json
{
  "2024-01": {
    "top_projects": ["Bloom (employed)", "Beit-al-Atlas (planning)"],
    "emotional_state": "Stressed about Bloom, excited about Beit",
    "financial_state": "Stable salary, considering freelance",
    "key_relationships": ["Bloom team", "Saleh"],
    "top_values": ["Curious Knowledge-Weaver"],
    "top_tensions": ["Innovation vs Completion"]
  },
  "2024-11": {
    "top_projects": ["Beit-al-Atlas (grant writing)", "Job offer (deciding)"],
    "emotional_state": "Crossroads anxiety, self-criticism",
    "financial_state": "Freelance/seeking contracts",
    "key_relationships": ["Joséphine", "Saleh", "Aaron", "Richard"],
    "top_values": ["VX Design", "Islamic Integration", "Unlikely Friendships"],
    "top_tensions": ["Authenticity vs Promotion", "Work during war"]
  }
}
```

---

### **TIER 2: Extract if Novel (High Confidence)**

**8. USER QUESTIONS**
- All user questions (reveals learning path, uncertainties, priorities)
- Tag: seeking_info, seeking_validation, seeking_decision_support

**9. PROJECTS & INITIATIVES**
- Named projects (Beit-al-Atlas, Nur Coop, Wellbeing Registry)
- Status: ideation, active, paused, completed, abandoned
- Evidence of success/failure
- Financial info (grants, revenue, costs)
- Time investment (hours/week, total duration)

**10. RELATIONSHIPS**
- People mentioned by name
- Nature of relationship (friend, colleague, collaborator, mentor, client)
- **Emotional quality** ⭐ NEW: energizing vs draining, inspiring vs depleting
- Frequency of mention (proxy for importance)
- **Network position** ⭐ NEW: connector, supporter, mentee, peer

**11. VALUES & PATTERNS (CAPs)**
- Constitutive Actions (done for their own sake)
- Attention policies (what you notice, care about, orient toward)
- Evidence: quotes, patterns, behaviors
- **Evolution over time** ⭐ NEW: how values shifted

**12. TENSIONS & CONFLICTS (IAPs)**
- Instrumental Actions (felt as obligations)
- What creates resistance/procrastination
- **What's being avoided** ⭐ NEW: fear, shame, guilt drivers
- CAP vs IAP tensions
- Unresolved dilemmas

---

### **TIER 3: Extract Rarely (Context Only)**

**13. LLM RESPONSES**
- ONLY if they reveal USER's thinking (user asked LLM to help articulate something)
- Mark clearly as "LLM-generated" with lower confidence score
- Never attribute LLM framing to user

**14. TECHNICAL/TRIVIAL CONVERSATIONS**
- Skip recipes, quick tech fixes, one-off questions
- UNLESS they reveal pattern (e.g., cooking as CAP, tech skills as professional identity)

---

## 🔍 **EXTRACTION SCHEMA (Updated)**

### **Conversation-Level Metadata**
```json
{
  "conversation_id": "1f620fa8-aa9c-4a48-82f4-a3f5f25ff25b",
  "title": "Happiness tracker notification channels",
  "date": "2025-11-21",
  "source": "claude",
  "message_count": 4,
  "user_word_count": 150,
  "substantive": true,
  "domains": ["wellbeing", "Islamic practice", "technology"],
  "emotional_tone": "curious, practical, some frustration with tech constraints",
  "extraction_confidence": 0.85
}
```

### **Entity Extraction**
```json
{
  "people": [
    {
      "id": "person.josephine_lesaffre",
      "name": "Joséphine Lesaffre",
      "relationship": "Wife, Nur Coop co-owner, Beit-al-Atlas advisor",
      "emotional_quality": "supportive, collaborative, grounding",
      "first_mention": "2023-XX-XX",
      "mention_frequency": 47,
      "context": ["Nur Coop", "Beit-al-Atlas", "Personal decisions", "Job relocation"],
      "network_role": "Core support, co-creator",
      "confidence": 0.95
    }
  ],

  "projects": [
    {
      "id": "project.happiness_tracker",
      "name": "Happiness Tracker",
      "status": "ideation",
      "dates": {
        "first_mention": "2025-11-21",
        "launched": null,
        "paused": null,
        "ended": null
      },
      "description": "ESM-based happiness tracking integrated with Islamic practices (muhasaba/muraja'a)",
      "financial": {
        "revenue": null,
        "costs": ["SMS: $3-5/person/month estimate"],
        "grants_sought": [],
        "time_investment": "ideation phase, <5 hours so far"
      },
      "emotional_investment": "medium excitement, practical problem-solving mode",
      "success_indicators": [],
      "failure_indicators": [],
      "confidence": 0.7
    }
  ],

  "financial_snapshot": {
    "income_sources": [
      {"source": "Nur Coop", "type": "business revenue", "stability": "stable, 10 years", "amount": "unknown"},
      {"source": "Consulting", "type": "freelance", "stability": "seeking new contracts", "amount": "unknown"},
      {"source": "Bloom salary", "type": "employment", "stability": "ended Nov 2024", "amount": "unknown"}
    ],
    "expenses_mentioned": [
      {"item": "SMS notifications", "amount": "$3-5/person/month", "context": "happiness tracker"},
      {"item": "Beit-al-Atlas operations", "amount": "EUR 35K grant sought", "context": "artist residency"}
    ],
    "constraints": ["Seeking new work", "Grant-dependent for Beit-al-Atlas"],
    "geographic_factors": ["France-based", "Considering US relocation", "Visa status unknown"]
  },

  "family_personal": {
    "immediate_family": [
      {"name": "Joséphine Lesaffre", "relationship": "Wife", "involvement_in_work": "High (Nur Coop, Beit-al-Atlas)"},
      {"name": "Child", "relationship": "Unknown", "context": "Pregnancy mentioned March 2023, current status unclear"}
    ],
    "extended_family": [],
    "health_mentions": [],
    "non_work_activities": ["Cooking (mentions of recipes)", "Nature/mountain walks (Saleh-led)", "Prayer/Islamic practices"],
    "rest_patterns": "unknown",
    "hobbies_separate_from_work": "unclear - work and life seem integrated"
  }
}
```

### **Values Extraction (SAREC + Emotional + Temporal)**
```json
{
  "value": {
    "id": "value.vx_design_methodology",
    "name": "Values Experience (VX) Design",
    "description": "Enable ways of being, not just features - design for values first",
    "emotional_quality": "Intellectually excited, professionally confident, socially uncertain (how to share?)",
    "cap_manifestations": [
      "Deep practitioner interviews (Rukudzo, Justin, Barry, Yazmany, Deepa)",
      "Values cards → Affordances → UX framework development",
      "Collaboration with Aaron Hurst on Wellbeing Registry"
    ],
    "iap_manifestations": [
      "Selling/promoting VX methodology feels uncomfortable",
      "Website update procrastination related to sharing this publicly"
    ],
    "evolution": {
      "2023-03": {"form": "Curious Knowledge-Weaver", "confidence": 0.92, "manifestation": "Getting lost in research questions"},
      "2024-11": {"form": "VX Design Methodology", "confidence": 0.85, "manifestation": "Systematic framework with professional application"}
    },
    "financial_implications": "Could be professional identity/consulting niche, but unclear monetization",
    "relationship_implications": "Collaboration with Aaron Hurst, connection to Richard Davidson/Center for Healthy Minds",
    "decision_implications": "Job offer at Center for Healthy Minds aligns with this value",
    "sarec": {
      "score": 0.85,
      "reasoning": "Repeated application across projects, systematic framework developed, external validation (Aaron collaboration)",
      "evidence": [
        {"type": "quote", "text": "values cards->affordances that would help them be they way they want to be -> ux", "source": "c42b78d4", "date": "2025-11-20"},
        {"type": "pattern", "name": "practitioner_interviews", "frequency": 5, "context": "Rukudzo, Justin, Barry, Yazmany, Deepa"},
        {"type": "collaboration", "with": "Aaron Hurst", "project": "Wellbeing Registry", "duration": "ongoing as of Nov 2024"}
      ],
      "confidence": 0.85
    }
  }
}
```

### **Decision Extraction** ⭐ NEW
```json
{
  "decision": {
    "id": "decision.leave_bloom_nov_2024",
    "decision": "Leave Bloom (Nov 2024)",
    "status": "completed",
    "options_considered": ["Stay at Bloom", "Leave Bloom", "Negotiate part-time/consultant role"],
    "criteria": {
      "values_alignment": "unknown (need to extract)",
      "financial": "unknown (had salary, now seeking contracts)",
      "family_impact": "unknown (Joséphine's thoughts?)",
      "location": "unknown (France-based, was Bloom remote?)",
      "growth_opportunity": "unknown (what wasn't growing?)"
    },
    "who_consulted": ["unknown - need to extract"],
    "process": {
      "timeline": "unknown - when was decision made vs executed?",
      "turning_point": "unknown - was there a specific moment?",
      "emotional_journey": "unknown - anxiety? Relief? Both?"
    },
    "outcome": {
      "immediate": "Left Nov 2024, still interviewing Bloom teams (ongoing connection)",
      "feelings": "unknown - regrets? Relief? Both?",
      "what_learned": "unknown",
      "what_glad_to_leave": "unknown"
    },
    "confidence": 0.5,
    "extraction_note": "User mentioned 'left Bloom Nov 2024, still interviewing teams' but details sparse - need more conversations"
  }
}
```

---

## 🎯 **Extraction Rules (Updated)**

### **1. USER VOICE ONLY**
- ❌ DO NOT extract from LLM responses as if they're user thoughts
- ✅ ONLY extract from user messages
- ✅ IF LLM summary is useful, mark it as "LLM-generated summary, confidence 0.6"

### **2. EMOTION TRACKING**
- ✅ Look for: "I feel...", "I'm excited/anxious/frustrated...", "I'm scared to..."
- ✅ Infer from context: procrastination = avoidance/fear, repeated mention = care/importance
- ✅ Track intensity: low (mentioned once) → high (repeated, emphatic language)

### **3. AVOIDANCE DETECTION**
- ✅ "I should..." (unfulfilled intentions)
- ✅ Repeated postponement ("still haven't done X")
- ✅ Projects mentioned then disappear
- ✅ Fears stated ("I'm scared to call people", "I feel ashamed to share during war")

### **4. FINANCIAL GROUNDING**
- ✅ Extract ALL mentions of money: salaries, grants, costs, revenue, pricing
- ✅ Extract time: "10 hours/week", "full-time role", "side project"
- ✅ Extract constraints: "can't afford", "need new contracts", "seeking funding"
- ✅ Geographic/material: visa status, housing, family obligations

### **5. FAMILY/PERSONAL INCLUSION**
- ✅ Family: spouse, children, parents, siblings, in-laws
- ✅ Health: sleep, exercise, illness, energy levels
- ✅ Non-work: cooking, hobbies, friendships, rest
- ✅ Integration: Is work/life integrated or separated?

### **6. TEMPORAL TRACKING**
- ✅ Create monthly snapshots (what changed month-to-month?)
- ✅ Track evolution: How did X value/project/relationship change over time?
- ✅ Identify inflection points: When did major shifts happen?

### **7. CONFIDENCE SCORING**
- **0.9-1.0**: User explicitly stated, multiple evidence sources, cross-validated
- **0.7-0.9**: User implied, single strong evidence, logically inferred
- **0.5-0.7**: Inferred from context, some ambiguity, needs validation
- **0.3-0.5**: Speculative, thin evidence, LLM-generated summary
- **<0.3**: Guess, no real evidence, exclude from extraction

---

## 📊 **Network Analysis Capability**

**YES - from knowledge graph we CAN do network analysis!**

### **Network Nodes:**
- People (Bilal, Joséphine, Saleh, Aaron, Richard, Dalal, etc.)
- Projects (Bloom, Beit-al-Atlas, Nur Coop, Wellbeing Registry, etc.)
- Organizations (WHEN, Wellbeing Project, Center for Healthy Minds, etc.)

### **Network Edges (Relationships):**
```json
{
  "relationships": [
    {
      "from": "person.bilal_ghalib",
      "to": "person.josephine_lesaffre",
      "type": "MARRIED_TO",
      "strength": 1.0,
      "emotional_quality": "supportive, collaborative, grounding",
      "duration": "unknown (marriage date unclear)",
      "frequency": "daily, integrated in work and life",
      "network_function": "core support, co-creator, decision partner"
    },
    {
      "from": "person.bilal_ghalib",
      "to": "person.aaron_hurst",
      "type": "COLLABORATES_WITH",
      "strength": 0.8,
      "emotional_quality": "intellectually stimulating, professionally generative",
      "duration": "unknown start, active as of Nov 2024",
      "frequency": "project-based (Wellbeing Registry)",
      "network_function": "professional mentor, methodological co-developer"
    },
    {
      "from": "person.bilal_ghalib",
      "to": "project.bloom",
      "type": "EMPLOYED_BY",
      "strength": 0.0,
      "status": "ended Nov 2024",
      "duration": "~4 years (approx 2020-2024)",
      "emotional_quality": "unknown - need to extract (why leave? what glad to leave behind?)",
      "network_function": "past employer, still connected (interviewing teams)"
    }
  ]
}
```

### **Network Metrics We Can Calculate:**
1. **Centrality**: Who/what is most connected? (Bilal to how many people/projects?)
2. **Betweenness**: Who/what bridges different clusters? (Does Bilal connect tech world + wellbeing world?)
3. **Closeness**: Who is close to whom? (Joséphine + Saleh = core; others = peripheral?)
4. **Clustering**: What groups exist? (Bloom team, Beit-al-Atlas team, VX collaborators, family)
5. **Strength**: Which relationships are strongest? (Marriage, co-founders vs acquaintances)
6. **Evolution**: How did network change over time? (Bloom connections faded, wellbeing connections grew)

### **Network Analysis Questions We Can Answer:**
- Who are the CONNECTORS in Bilal's network? (People who bridge worlds)
- Who are the SUPPORTERS? (People who energize vs drain)
- What are the CLUSTERS? (Professional, personal, geographic)
- What's the TRAJECTORY? (Network growing or contracting? Shifting domains?)
- Who PERSISTS over time? (Joe Edelman since 2014 vs recent connections)

**YES - this is totally doable from the knowledge graph!**

---

## 🚀 **Next Steps with Improved Methodology**

### **Immediate:**
1. ✅ Extract from remaining Batch 71 conversations with NEW focus areas:
   - Emotions (positive, negative, ambivalent)
   - Avoidance (what's being postponed/feared)
   - Financial reality (money, time, constraints)
   - Family/personal (Joséphine, children, health, hobbies)
   - Decision-making (how choices are made)

2. ✅ Create monthly snapshots (how did Nov 2024 differ from Oct 2024? Sept 2024?)

3. ✅ Flag gaps for Bilal's top 10 questions

### **This Week:**
4. Complete Batch 71 with improved extraction
5. Instance 1 completes Batch 1 with same improvements
6. Cross-validate: What do both instances see?
7. Bilal answers top 10 questions → adjust priorities

### **This Month:**
8. Monthly snapshot analysis (2023-03 → 2024-11)
9. Network analysis: Who persists? Who's central? What clusters?
10. Decision-tree mapping: Job offer, grant, Bloom departure - how to decide?

---

**Ready to continue Batch 71 with THIS improved methodology?**

Yallah! 🚀
