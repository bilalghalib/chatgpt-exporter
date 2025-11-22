# ChatGPT Insights Analyzer - Desktop Tool

Standalone CLI for analyzing exported ChatGPT conversations with **checkpoint/resume** support.

## Why Use This Instead of Browser?

✅ **Safe for large batches** - Analyze 2,800 conversations without browser crashes
✅ **Resume from failures** - If interrupted, just add `--resume` flag
✅ **Checkpoint system** - Saves progress every 50 conversations
✅ **Better progress tracking** - Real-time cost and ETA
✅ **Run overnight** - Set it and forget it
✅ **No browser limits** - No tab crashes, no memory issues

## Setup (One-time)

```bash
cd /Users/bilalghalib/Projects/scripts/chatgpt-exporter
cd analyzer
npm install
```

## Usage

### 1. Export from Browser First

In ChatGPT:
1. Click "Export All"
2. Format: **JSON**
3. Click "Export" (NOT "Analyze"!)
4. Saves to `~/Downloads/conversations.json`

### 2. Analyze on Desktop

```bash
cd /Users/bilalghalib/Projects/scripts/chatgpt-exporter/analyzer

node cli.js analyze \
  --input ~/Downloads/conversations.json \
  --api-key sk-ant-YOUR_KEY \
  --output knowledge-base.json
```

**Get API key:** https://console.anthropic.com/settings/keys

### 3. If Interrupted, Resume

```bash
node cli.js analyze \
  --input ~/Downloads/conversations.json \
  --api-key sk-ant-YOUR_KEY \
  --resume
```

## Example Output

```
✓ Loaded 2800 conversations

Processing 2800 conversations...
Batch size: 50
Checkpoint: Enabled

Progress |██████████░░░░░░░░░░░░| 45% | 1260/2800 | Cost: $2.56 | ETA: 3850s

# If you hit Ctrl+C or it crashes, just resume:

Resuming from checkpoint: 1260 already processed
Processing 1540 conversations...

Progress |████████████████████████| 100% | 2800/2800 | Cost: $5.68 | ETA: 0s

✓ Analysis complete!

Summary:
  Conversations analyzed: 2800
  Total events extracted: 18,453
  Total cost: $5.68
  Output saved to: knowledge-base.json
```

## Commands

**Analyze:**
```bash
node cli.js analyze -i FILE -k API_KEY -o OUTPUT
```

**Resume:**
```bash
node cli.js analyze -i FILE -k API_KEY --resume
```

**Check stats:**
```bash
node cli.js stats
```

## Options

- `-i, --input <file>` - Input JSON (required)
- `-k, --api-key <key>` - Anthropic API key (required)
- `-o, --output <file>` - Output (default: knowledge-base.json)
- `-b, --batch-size <n>` - Checkpoint every N conversations (default: 50)
- `--resume` - Resume from last checkpoint
- `--no-checkpoint` - Disable checkpoints (not recommended)

## View Results

```bash
open ../knowledge-base-viewer.html
```

Drag the generated `knowledge-base.json` file!

## Tips

**Test first:**
```bash
# Analyze just 10 conversations to test
node cli.js analyze -i ~/Downloads/conversations.json -k sk-ant-... -b 10
# Ctrl+C after it processes 10
```

**Process in batches over multiple days:**
```bash
# Day 1: Process 500
node cli.js analyze -i conversations.json -k sk-ant-... -b 100
# Ctrl+C after ~500

# Day 2: Continue
node cli.js analyze -i conversations.json -k sk-ant-... --resume
```

##Cost Estimate

- ~$0.002 per conversation
- 100 conversations: ~$0.20
- 2,800 conversations: ~$5.60
