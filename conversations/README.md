# Organized Conversations

**Total conversations**: 10
**Organized**: 10
**Errors**: 0

## Structure

Each conversation is in its own folder with:

```
<conversation_id>/
├── conversation.json      # Original export
├── metadata.json          # Stats and info
├── theory_of_mind.json    # Beliefs extracted (to be populated by LLM)
├── highlights.json        # Key insights (to be populated)
├── transitions.json       # Thinking shifts (to be populated)
├── themes.json           # Core themes (to be populated)
└── README.md             # Human-readable summary
```

## Files

- `INDEX.json` - List of all organized conversations
- `README.md` - This file

## Next Steps

1. Run LLM analysis to populate theory_of_mind.json for each conversation
2. Extract highlights from user messages
3. Identify transitions and theme evolution
4. Generate aggregate analysis across all conversations

## Usage

```bash
# List all conversations
cat INDEX.json | jq '.conversations[] | .folder'

# Read a specific conversation
cat 2023-03-21_claude_Bilal_s_strengths_8f6f6926/README.md

# Check metadata
cat 2023-03-21_claude_Bilal_s_strengths_8f6f6926/metadata.json
```
