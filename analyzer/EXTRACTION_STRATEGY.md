# User-Centric Extraction Strategy

## Philosophy: Prioritize Human Input Over LLM Output

**Core Principle:** The most valuable insights come from what YOU said, not what the LLM responded. We want to create a knowledge base of YOUR thinking patterns, creative processes, problem-solving approaches, and domain expertise.

---

## Extraction Priorities (Ranked)

### 🥇 Priority 1: Large User Content Blocks
**Target:** Substantial user turns (>100 words)

These represent:
- Detailed explanations of your ideas
- Complex problem descriptions
- Creative briefs and prompts
- Domain expertise you shared
- Multi-paragraph thoughts

**Extraction Rule:** If `speaker === "user"` AND `word_count > 100`, extract the FULL text with minimal summarization.

**Example Event Type:**
```json
{
  "type": "substantive_user_input",
  "content": "Full user message here (preserved exactly)",
  "word_count": 347,
  "analysis": "Brief 1-sentence summary of what this represents",
  "tags": ["domain_expertise", "creative_brief", "problem_description"]
}
```

---

### 🥈 Priority 2: User Questions & Problem Framing
**Target:** How you frame problems and ask questions

These reveal:
- Your learning priorities
- What gaps you're trying to fill
- How you approach problem-solving
- What you consider important

**Event Types:**
- `strategic_question` - Questions about approach/strategy
- `knowledge_gap` - "How do I..." or "What's the best way to..."
- `problem_framing` - How you described a problem or challenge
- `clarification_request` - When you asked for specifics

**Extraction Rule:** Extract ALL user questions, even short ones. Questions reveal intent.

---

### 🥉 Priority 3: User Creative Direction
**Target:** Prompts, instructions, creative briefs you gave

These show:
- How you guide LLMs effectively
- Your prompt engineering skills
- Your creative vision
- Your communication patterns

**Event Types:**
- `detailed_prompt` - Multi-step instructions you provided
- `creative_direction` - "Make it X" or "Focus on Y"
- `constraint_specification` - Requirements/constraints you set
- `style_guidance` - Tone, style, format preferences

---

### Priority 4: User Insights & Hypotheses
**Target:** Moments when YOU figured something out or proposed ideas

**Event Types:**
- `user_aha_moment` - "Oh! I just realized..."
- `user_hypothesis` - "I think this might work because..."
- `user_insight` - Observations or realizations you shared
- `decision_rationale` - "I'm choosing X because Y"

---

### Priority 5: LLM Responses (ONLY When Exceptional)

**De-prioritize** generic LLM responses. **Only extract** if:
- The LLM introduced a genuinely novel concept you didn't mention
- The response directly led to a user aha moment (evidenced in next turn)
- The response contains a specific technique/framework you later reference

**Confidence Threshold for LLM Content:** >0.9 (vs >0.7 for user content)

---

## Content Extraction Guidelines

### For User Turns >200 Words:
```json
{
  "type": "extended_user_content",
  "full_text": "EXACT user message (unmodified)",
  "summary": "1-sentence high-level summary",
  "key_concepts": ["concept1", "concept2"],
  "intent": "What was the user trying to accomplish?",
  "word_count": 347,
  "contains_code": true,
  "contains_examples": false
}
```

### For User Questions:
```json
{
  "type": "user_question",
  "question": "Exact question text",
  "question_type": "strategic | tactical | clarification | exploratory",
  "context": "What conversation thread led to this question?",
  "implies_about_user": "What does this question reveal about user's goals?"
}
```

### For User Creative Direction:
```json
{
  "type": "creative_direction",
  "instruction": "Full instruction/prompt text",
  "constraints": ["constraint1", "constraint2"],
  "desired_outcome": "What the user wanted to achieve",
  "prompt_quality": "simple | detailed | multi-step | iterative"
}
```

---

## Filtering Rules

### ❌ **SKIP** (Don't Extract):
1. Short pleasantries ("thanks", "ok", "got it")
2. Generic LLM explanations you already know
3. Boilerplate LLM caveats ("I'm an AI...", "I can't...", "It's important to note...")
4. LLM summaries of things YOU just said
5. Turn confirmations ("Here's what I'll do...")

### ✅ **ALWAYS EXTRACT**:
1. User turns >100 words (100% of them)
2. User questions (all of them, even 1-liners)
3. User code snippets or examples YOU wrote
4. User-provided domain context ("In my field, we...")
5. User corrections ("Actually, I meant...")
6. User frustration or confusion (signals gaps)

---

## Evidence Requirements

### For User Content:
- **Quote:** FULL user message if <300 words, otherwise excerpt key paragraphs
- **Turn Number:** Exact turn number
- **Conversation Context:** 1-sentence summary of what conversation was about
- **Significance:** Why is this user input noteworthy?

### For LLM Content (if extracted):
- **Quote:** Specific novel information only (not generic explanation)
- **Turn Number:** Exact turn number
- **User's Reaction:** Did user acknowledge/use this in next turn?
- **Novelty Score:** 0.0-1.0 (how new is this information?)

---

## Conversation Metadata Enrichment

For each conversation, extract:

```json
{
  "conversation_id": "...",
  "conversation_title": "...",
  "user_content_stats": {
    "total_user_turns": 15,
    "total_user_words": 2847,
    "avg_words_per_turn": 189,
    "longest_user_turn": 456,
    "user_questions_count": 8,
    "user_code_blocks": 3
  },
  "conversation_type": "problem_solving | creative | learning | debugging | brainstorming",
  "user_expertise_level": "exploring | intermediate | expert",
  "primary_user_intent": "1-sentence summary of what user was trying to do",
  "key_user_contributions": ["concept1", "concept2", "insight1"]
}
```

---

## Output Structure Changes

### Current Structure:
```json
{
  "events": [
    {"speaker": "user", ...},
    {"speaker": "assistant", ...},
    {"speaker": "user", ...}
  ]
}
```

### Proposed User-Centric Structure:
```json
{
  "user_content": {
    "substantive_inputs": [...],
    "questions": [...],
    "creative_directions": [...],
    "insights": [...],
    "code_examples": [...]
  },
  "llm_contributions": {
    "novel_concepts": [...],
    "useful_frameworks": [...]
  },
  "conversation_pattern": {
    "user_primary_intent": "...",
    "user_outcome": "...",
    "user_expertise_demonstrated": [...]
  }
}
```

---

## Why This Matters

**Old Approach (Equal Weight):**
- 50% of extraction is generic LLM responses
- Your unique insights get buried
- Hard to see YOUR evolving expertise
- Difficult to understand YOUR problem-solving patterns

**New Approach (User-Centric):**
- 80% extraction focuses on YOUR content
- YOUR questions reveal your learning path
- YOUR prompts show your communication skills
- YOUR insights build a map of YOUR expertise

---

## Example Comparison

### ❌ Old Extraction (Equal Weight):
```
Event 1: User asked about React hooks
Event 2: Assistant explained useState and useEffect
Event 3: User said thanks
Event 4: Assistant provided code example
```

### ✅ New Extraction (User-Centric):
```
Event 1: User asked strategic question about React hooks
  → Question reveals user is working on state management
  → User's expertise level: intermediate (asked about hooks, not basics)

Event 2: User provided 234-word detailed context about their specific use case
  → FULL TEXT preserved (this is valuable domain context)
  → User is building a real-time dashboard with WebSocket updates
  → User already tried X, Y, Z approaches (shows problem-solving)

Event 3: User refined their question based on LLM response
  → Shows user actively learning and iterating
  → Question evolution: general → specific → architectural
```

The second approach tells a story about **YOUR** thinking process, not just "a conversation happened."
