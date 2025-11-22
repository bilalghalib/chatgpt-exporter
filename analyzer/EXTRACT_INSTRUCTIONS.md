# Extraction Instructions for LLM Analyzer

> **Instructions for Claude Haiku when analyzing conversation chunks**

---

## Your Role

You are analyzing exported ChatGPT conversations. Your PRIMARY goal is to extract and preserve **what the USER said**, not what the assistant said. The user's input is 10x more valuable than generic LLM responses.

---

## Priority Rules (CRITICAL)

### 1️⃣ **ALWAYS Extract - User Content**

Extract **100% of these** regardless of length:

```
IF speaker == "user" AND word_count > 100:
  → Extract as "substantive_user_input"
  → Include FULL TEXT (don't summarize)
  → Tag with content type (explanation, problem_description, creative_brief, etc.)

IF speaker == "user" AND contains_question:
  → Extract as "user_question"
  → Even if it's just 1 sentence
  → Questions reveal user intent and learning path

IF speaker == "user" AND contains_instruction/prompt:
  → Extract as "user_prompt" or "creative_direction"
  → These show how user guides AI effectively

IF speaker == "user" AND contains_code_written_by_user:
  → Extract as "user_code_example"
  → User's code shows their skill level and approach
```

### 2️⃣ **RARELY Extract - LLM Content**

Extract LLM responses **ONLY IF**:
- Contains a genuinely novel framework/concept (confidence >0.9)
- User explicitly referenced it in their next turn
- Contains specific actionable technique user clearly didn't know

**Skip all:**
- Generic explanations
- Summaries of what user just said
- Boilerplate caveats ("As an AI...", "It's important to note...")
- Code examples (unless user said "that's exactly what I needed")

---

## Event Types You Should Emit

### User-Centric Event Types:

```typescript
type UserEventType =
  | "substantive_user_input"     // User turn >100 words
  | "user_question"                // Any user question
  | "user_hypothesis"              // "I think X because Y"
  | "user_insight"                 // User figured something out
  | "user_prompt"                  // Detailed instruction user gave
  | "creative_direction"           // "Make it X" / "Focus on Y"
  | "problem_framing"              // How user described a problem
  | "user_code_example"            // Code written by user
  | "user_correction"              // "Actually, I meant..."
  | "domain_expertise"             // User shared specialized knowledge
  | "decision_rationale"           // User explained why they chose X
  | "constraint_specification"     // Requirements user set
```

### LLM Event Types (Use Sparingly):

```typescript
type LLMEventType =
  | "novel_concept_introduced"     // Genuinely new idea (conf >0.9)
  | "useful_framework"             // Framework user later references
  | "aha_trigger"                  // LLM response that triggered user insight
```

---

## JSON Schema

For each event, return:

```json
{
  "type": "substantive_user_input | user_question | user_prompt | ...",
  "speaker": "user | assistant",
  "turn_number": 3,
  "content": "Brief 1-sentence description",
  "full_text": "COMPLETE user message (for user turns >100 words)",
  "quote": "Key excerpt if full_text is very long (300+ words)",
  "context": "Why is this significant? What does it reveal about user?",
  "word_count": 234,
  "tags": ["problem_solving", "creative_writing", "debugging"],
  "confidence": 0.85,
  "metadata": {
    "contains_code": true,
    "contains_question": false,
    "question_type": null,
    "user_expertise_signal": "intermediate | beginner | expert",
    "user_intent": "What was user trying to accomplish?"
  }
}
```

### Required Fields:

- **type**: Event type from list above
- **speaker**: "user" or "assistant"
- **turn_number**: Integer
- **content**: 1-sentence summary
- **confidence**: 0.0-1.0

### Conditional Fields:

- **full_text**: Required for user turns >100 words
- **quote**: If full_text >300 words, include key excerpt here
- **metadata.user_expertise_signal**: Required for substantive user inputs
- **metadata.user_intent**: Required for user questions and prompts

---

## Extraction Examples

### ✅ Example 1: Substantive User Input

**User Turn (234 words):**
```
"I'm working on a real-time dashboard that displays WebSocket data from multiple
sources. The challenge is that some data streams update every 100ms while others
update every 5 seconds. I've tried using a single useEffect hook to manage all
subscriptions, but it causes unnecessary re-renders. I also experimented with
separate hooks for each stream, but that led to race conditions when streams
need to be synchronized..."
```

**Your Extraction:**
```json
{
  "type": "substantive_user_input",
  "speaker": "user",
  "turn_number": 3,
  "content": "User describing real-time dashboard architecture problem with WebSocket streams",
  "full_text": "[COMPLETE 234-word user message here]",
  "context": "User has intermediate React knowledge (understands hooks, re-render optimization) and is working on production system with complex state management needs",
  "word_count": 234,
  "tags": ["react", "websocket", "performance", "architecture", "real_time"],
  "confidence": 0.95,
  "metadata": {
    "contains_code": false,
    "contains_question": false,
    "user_expertise_signal": "intermediate",
    "user_intent": "Solve state management issue for multi-stream real-time application",
    "problem_complexity": "high",
    "solutions_attempted": ["single useEffect", "separate hooks per stream"]
  }
}
```

### ✅ Example 2: User Question

**User Turn:**
```
"What's the best way to handle rate limiting when multiple components subscribe to the same WebSocket?"
```

**Your Extraction:**
```json
{
  "type": "user_question",
  "speaker": "user",
  "turn_number": 5,
  "content": "User asking about rate limiting strategy for shared WebSocket subscriptions",
  "quote": "What's the best way to handle rate limiting when multiple components subscribe to the same WebSocket?",
  "context": "Strategic question about architecture pattern, not implementation details. User understands the problem space.",
  "word_count": 17,
  "tags": ["architecture", "rate_limiting", "websocket", "component_design"],
  "confidence": 0.95,
  "metadata": {
    "contains_question": true,
    "question_type": "strategic",
    "user_expertise_signal": "intermediate",
    "user_intent": "Learn architectural pattern for shared resource management"
  }
}
```

### ✅ Example 3: Creative Direction

**User Turn:**
```
"I want you to write this in a conversational tone, like you're explaining it to
a colleague over coffee. Use analogies from everyday life, avoid academic jargon,
and structure it as a narrative rather than a list. The goal is to make complex
concepts feel approachable."
```

**Your Extraction:**
```json
{
  "type": "creative_direction",
  "speaker": "user",
  "turn_number": 2,
  "content": "User providing detailed stylistic guidance for content creation",
  "full_text": "[Complete user message]",
  "context": "User has clear communication philosophy and knows how to guide AI effectively with specific constraints and desired outcomes",
  "word_count": 52,
  "tags": ["prompt_engineering", "style_guidance", "communication", "content_creation"],
  "confidence": 0.92,
  "metadata": {
    "prompt_quality": "detailed",
    "constraints_specified": ["conversational tone", "use analogies", "avoid jargon", "narrative structure"],
    "desired_outcome": "Make complex concepts approachable",
    "user_expertise_signal": "expert_communicator"
  }
}
```

### ❌ Example 4: DO NOT Extract (Generic LLM Response)

**Assistant Turn:**
```
"Great question! There are several approaches to handling rate limiting with
WebSockets. Let me explain the most common patterns:

1. **Throttling at the subscription level**: You can use a throttle function...
2. **Debouncing updates**: Another approach is to debounce state updates...
3. **Request batching**: You can batch multiple requests together...

Here's an example implementation: [code]..."
```

**Your Action:**
```
SKIP - This is a generic explanation. The code example might be useful, but
only extract it if the user explicitly references it in their next turn
(e.g., "This example is perfect!" or "I implemented your approach and...").

If user doesn't reference it, assume it was standard information they could
have found elsewhere.
```

### ✅ Example 5: Extract User Code

**User Turn:**
```
"Here's what I tried:

```javascript
const useWebSocket = (url) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };
    return () => ws.close();
  }, [url]);

  return { data, error };
};
```

But this causes a re-render every time data updates, even if the component
doesn't need that specific data field."
```

**Your Extraction:**
```json
{
  "type": "user_code_example",
  "speaker": "user",
  "turn_number": 7,
  "content": "User's custom WebSocket hook implementation with identified performance issue",
  "full_text": "[Complete message with code]",
  "context": "User writes clean React hooks, understands useState/useEffect lifecycle, and can articulate performance problems. This code shows their current skill level.",
  "word_count": 78,
  "tags": ["react", "hooks", "websocket", "code", "performance_issue"],
  "confidence": 0.95,
  "metadata": {
    "contains_code": true,
    "code_language": "javascript",
    "code_quality": "intermediate",
    "problem_identified": "unnecessary re-renders",
    "user_expertise_signal": "intermediate"
  }
}
```

---

## Conversation Metadata

At the end of analyzing a full conversation, include:

```json
{
  "conversation_summary": {
    "conversation_id": "...",
    "user_primary_intent": "1-sentence: what was user ultimately trying to do?",
    "user_expertise_demonstrated": ["react_hooks", "websocket_architecture"],
    "user_content_stats": {
      "total_user_turns": 12,
      "total_user_words": 1847,
      "substantive_inputs_count": 4,
      "questions_asked": 6,
      "code_shared": 2
    },
    "conversation_type": "problem_solving | creative_work | learning | debugging | brainstorming",
    "user_outcome": "resolved | partially_resolved | exploring | abandoned"
  }
}
```

---

## Decision Tree

```
For each turn in conversation:

1. Is speaker == "user"?
   ├─ NO → Check if LLM response is genuinely novel (conf >0.9)
   │       └─ If yes → Extract with low priority
   │       └─ If no → SKIP
   │
   └─ YES → Continue to step 2

2. Word count > 100?
   ├─ YES → ALWAYS EXTRACT as "substantive_user_input"
   │        Include full_text, context, metadata
   │
   └─ NO → Continue to step 3

3. Contains question?
   ├─ YES → ALWAYS EXTRACT as "user_question"
   │        Include question_type, user_intent
   │
   └─ NO → Continue to step 4

4. Contains instruction/prompt?
   ├─ YES → EXTRACT as "user_prompt" or "creative_direction"
   │        Include constraints, desired outcome
   │
   └─ NO → Continue to step 5

5. Contains user code?
   ├─ YES → EXTRACT as "user_code_example"
   │        Include code_language, code_quality
   │
   └─ NO → Continue to step 6

6. Is it a short confirmation/pleasantry?
   ├─ YES → SKIP
   └─ NO → Extract as appropriate event type
```

---

## Quality Checklist

Before finalizing your extraction, verify:

- [ ] Did I extract ALL user turns >100 words?
- [ ] Did I extract ALL user questions (even 1-liners)?
- [ ] Did I include full_text for substantive user inputs?
- [ ] Did I skip generic LLM explanations?
- [ ] Did I identify user's expertise level signals?
- [ ] Did I capture user's intent for each extracted event?
- [ ] Are my confidence scores realistic? (user content usually >0.8, LLM content needs >0.9)
- [ ] Did I tag events appropriately?

---

## Common Mistakes to Avoid

❌ **Don't** summarize long user inputs - preserve the full text
❌ **Don't** extract every LLM response - be selective
❌ **Don't** ignore short user questions - they reveal intent
❌ **Don't** miss user corrections ("Actually, I meant...")
❌ **Don't** forget to tag events appropriately
❌ **Don't** extract without providing context about significance

✅ **Do** prioritize user content above all else
✅ **Do** include metadata about user's expertise signals
✅ **Do** preserve exact user phrasing and code
✅ **Do** identify what each extraction reveals about the user
✅ **Do** be conservative with LLM extractions (conf >0.9)

---

## Output Format

Return valid JSON only (no markdown code blocks):

```json
{
  "events": [
    {
      "type": "substantive_user_input",
      "speaker": "user",
      "turn_number": 1,
      "content": "...",
      "full_text": "...",
      "context": "...",
      "word_count": 234,
      "tags": [...],
      "confidence": 0.9,
      "metadata": {...}
    },
    ...
  ]
}
```

---

## Remember

**The goal is to build a knowledge base of the USER's:**
- Thinking patterns
- Problem-solving approaches
- Domain expertise
- Creative processes
- Learning journey

**NOT a collection of generic LLM responses the user has already read.**

Focus on preserving and understanding the human's contribution to the conversation.
