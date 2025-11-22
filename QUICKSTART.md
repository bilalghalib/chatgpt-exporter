# 🚀 ChatGPT Insights - Complete Guide

Two ways to analyze your conversations: **Browser** (small batches) or **Desktop** (large batches).

---

## 📋 Step 1: Install Userscript

```bash
# Copy built userscript to clipboard (Mac)
cat dist/chatgpt.user.js | pbcopy
```

Then:
1. Open Tampermonkey dashboard
2. Click "+" (new script)
3. Paste (Cmd+V)
4. Save (Cmd+S)

---

## 🌐 Option A: Analyze in Browser (Quick, Small Batches)

**Best for:** Testing, analyzing 10-50 conversations

1. Go to https://chatgpt.com
2. Click "Export All"
3. Add your Anthropic API key in Settings
4. Use Smart Filters to select interesting conversations
5. Select 10-20 conversations
6. Expand "🧠 AI Analysis" panel
7. Click "Analyze Selected"
8. Wait ~30-60 seconds
9. Click "Export Knowledge Base" to download JSON
10. Open `knowledge-base-viewer.html` and drag JSON file

**Pros:** Immediate, no setup
**Cons:** Browser can crash with many conversations, no resume

---

## 💻 Option B: Analyze on Desktop (Safe, Large Batches)

**Best for:** Analyzing 100-2,800 conversations safely

### 1. Export from Browser

1. Go to https://chatgpt.com
2. Click "Export All" → JSON → Export
3. Downloads to `~/Downloads/conversations.json`

### 2. Setup Analyzer (One-time)

```bash
cd /Users/bilalghalib/Projects/scripts/chatgpt-exporter/analyzer
npm install
```

### 3. Run Analysis

```bash
node cli.js analyze \
  --input ~/Downloads/conversations.json \
  --api-key sk-ant-YOUR_KEY_HERE \
  --output knowledge-base.json
```

**Get API key:** https://console.anthropic.com/settings/keys

### 4. If Interrupted, Resume

```bash
node cli.js analyze \
  --input ~/Downloads/conversations.json \
  --api-key sk-ant-YOUR_KEY \
  --resume
```

### 5. View Results

```bash
open ../knowledge-base-viewer.html
```

Drag `knowledge-base.json` onto the page!

**Pros:** Safe, resumable, no browser limits, can run overnight
**Cons:** Requires Node.js setup

---

## 📊 Cost & Time Estimates

| Conversations | Browser Time | Desktop Time | Cost |
|--------------|--------------|--------------|------|
| 10           | 30 sec       | 1 min        | $0.02 |
| 50           | 3 min        | 5 min        | $0.10 |
| 100          | ❌ Risky      | 15 min       | $0.20 |
| 500          | ❌ Will crash | 1 hour       | $1.00 |
| 2,800        | ❌ Impossible | 6-8 hours    | $5.60 |

---

## 💡 Recommendations

**Just testing?**
→ Use browser, analyze 5-10 conversations

**Want insights from ~50-100 conversations?**
→ Use browser in batches of 20 at a time

**Have 500+ conversations to analyze?**
→ Use desktop tool with checkpoints

**Have 2,800 conversations?**
→ Definitely use desktop tool, let it run overnight

---

## 🎯 Quick Commands Cheat Sheet

```bash
# Copy userscript to clipboard (Mac)
cat dist/chatgpt.user.js | pbcopy

# Build latest version
npm run build

# Setup analyzer
cd analyzer && npm install

# Analyze conversations
node cli.js analyze -i ~/Downloads/conversations.json -k sk-ant-... -o kb.json

# Resume if interrupted
node cli.js analyze -i ~/Downloads/conversations.json -k sk-ant-... --resume

# Check progress
node cli.js stats

# View results
open ../knowledge-base-viewer.html
```

---

## ❓ FAQ

**Q: Should I use browser or desktop for 2,800 conversations?**
A: Desktop. Browser will crash or freeze.

**Q: What if analysis gets interrupted?**
A: Desktop tool has checkpoints. Just add `--resume` flag.

**Q: Can I analyze in batches over multiple days?**
A: Yes! Desktop tool saves progress every 50 conversations.

**Q: How much does it cost?**
A: ~$0.002 per conversation. 2,800 = ~$5.60.

**Q: What if I just want to test first?**
A: Use browser, analyze 5 conversations. Costs ~$0.01.
