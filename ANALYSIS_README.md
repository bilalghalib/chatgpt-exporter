# Conversation Analysis Tools

**Analyze your exported ChatGPT/Claude conversations** to build a comprehensive Theory of Mind, extract insights, and create deliverables.

---

## Quick Start

### 1. Organize Your Conversations
```bash
# Create structured folders for all conversations
python3 organize_conversations.py

# Or start with a sample
python3 organize_conversations.py 100
```

### 2. Extract Your Voice
```bash
# Extract your substantive messages (not AI responses)
python3 extract_your_voice.py

# Then read your highlights
cat your_voice/HIGHLIGHTS.md
```

### 3. Build Theory of Mind (LLM-Based)
```bash
# Requires Anthropic API key
python3 build_llm_theory_of_mind.py YOUR_API_KEY 50

# Process all conversations (costs ~$1,750)
python3 build_llm_theory_of_mind.py YOUR_API_KEY
```

---

## What Gets Generated

### Organized Conversations (`conversations/`)
Each conversation in its own folder:
```
2023-03-21_claude_Bilal_s_strengths_8f6f6926/
├── conversation.json      # Original
├── metadata.json          # Stats
├── theory_of_mind.json    # Beliefs extracted
├── highlights.json        # Key quotes
├── transitions.json       # Thinking shifts
├── themes.json           # Topics covered
└── README.md             # Summary
```

### Your Voice (`your_voice/`)
Your own words organized by theme:
- `HIGHLIGHTS.md` - Top 100 most reflective messages
- `AI_and_Automation.md` - 1,568 messages
- `Technology_and_Development.md` - 1,217 messages
- `Personal_Growth_and_Values.md` - 972 messages
- Plus 8 more themed files

### Theory of Mind (`llm_theory_of_mind/`)
SAREC-based beliefs with evidence:
- `knowledge/` - What you know (skills, expertise)
- `values/` - What you care about (priorities)
- `goals/` - What you're trying to do (projects)
- `needs/` - What you need (gaps, challenges)
- `provenance.json` - Which conversations contributed what

---

## Analysis Outputs

### Completed ✅
- **`theme_analysis.json`** - 16 themes, temporal patterns, top keywords
- **`deep_theme_analysis.json`** - Multi-dimensional clustering
- **`COMPREHENSIVE_THEME_ANALYSIS.md`** - 40-page narrative synthesis
- **`your_voice/`** - 2,080 substantive messages from 500 conversations
- **`conversations/`** - Structured organization (started)

### Ready to Build
- **LLM Theory of Mind** - Evidence-based belief extraction
- **Knowledge Graph** - Aggregate knowledge across all conversations
- **Thematic Compilations** - Methodology documents by theme
- **Deliverable Generators** - Portfolio-ready artifacts

---

## Use Cases

### For Portfolio/CV
- **Evidence-based claims**: "Bilal has expertise in X" + 12 conversations with quotes
- **Case studies**: Project descriptions with exact quotes and provenance
- **Skills timeline**: Track expertise evolution 2023→2025

### For Self-Understanding
- **See what you actually care about** (not what you think you care about)
- **Track skill development** over time
- **Identify patterns** you didn't know existed
- **Find hidden connections** between domains

### For Content Creation
- **Blog posts** from your own insights
- **Frameworks** you've developed
- **Methodologies** in your own words
- **Quotable insights** for talks/presentations

### For Knowledge Management
- **Personal wiki** auto-generated from conversations
- **Training materials** from your explanations
- **Reference docs** by theme (solar, Bloom, spiritual, etc.)

---

## Questions & Suggestions

See `PROCESS_DOCUMENTATION.md` Section "5 Critical Questions" and "5 Suggestions for Maximum Long-Term Value"

**Key questions**:
1. What deliverables do you want? (Portfolio, grants, wiki, blog?)
2. How will you query this? (By theme, time, project, belief?)
3. Should we version beliefs over time?
4. Who else might use this?
5. What's your LLM processing budget?

**Key suggestions**:
1. Create conversation priority scores
2. Build incremental processing system (50/week)
3. Generate "knowledge cards" for each skill
4. Set up weekly review process
5. Create themed compilations

---

## Cost Estimates

### Free Tools
- Thematic analysis ✅
- Voice extraction ✅
- Conversation organization ✅

### LLM-Based (Paid)
- **Theory of Mind**: ~$0.50/conversation
  - 50 conversations: ~$25
  - 500 conversations: ~$250
  - All 3,517: ~$1,750

**Recommendation**: Start with 50-100 priority conversations to test quality before scaling.

---

## Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `analyze_themes.py` | Basic categorization | ✅ Ready |
| `deep_theme_analyzer.py` | Multi-dimensional analysis | ✅ Ready |
| `extract_your_voice.py` | Extract user messages | ✅ Ready |
| `organize_conversations.py` | Create folder structure | ✅ Ready |
| `build_llm_theory_of_mind.py` | SAREC belief extraction | ✅ Ready |
| `PROCESS_DOCUMENTATION.md` | Complete pipeline docs | ✅ Complete |
| `COMPREHENSIVE_THEME_ANALYSIS.md` | 40-page synthesis | ✅ Complete |
| `ANALYSIS_COMPLETE.md` | Summary & next steps | ✅ Complete |

---

## Next Steps

1. **Read the analysis** → Start with `COMPREHENSIVE_THEME_ANALYSIS.md`
2. **Read your voice** → `your_voice/HIGHLIGHTS.md`
3. **Organize all conversations** → `python3 organize_conversations.py`
4. **Decide on LLM strategy** → Budget, priority, scope
5. **Run Theory of Mind** → `python3 build_llm_theory_of_mind.py API_KEY 50`

---

**Documentation**: `PROCESS_DOCUMENTATION.md`
**Questions**: See "5 Critical Questions" in process docs
**Support**: Review analysis outputs and iterate

**Created**: November 22, 2025
**Dataset**: 3,517 conversations (Feb 2023 - Nov 2025)
