# ChatGPT Exporter - Technical Documentation

## Project Overview

**ChatGPT Exporter** is a Tampermonkey/Greasyfork userscript that enables users to export their ChatGPT conversations in multiple formats (Markdown, HTML, JSON, PNG). It integrates seamlessly with the ChatGPT web interface and runs entirely in the browser.

- **Version**: 2.29.1
- **Type**: Browser Userscript (Tampermonkey/Greasyfork)
- **License**: MIT
- **Author**: pionxzh
- **Tech Stack**: Preact, TypeScript, Vite, Tailwind CSS

---

## Architecture Overview

### Directory Structure

```
src/
├── main.tsx                    # Entry point - userscript initialization
├── page.ts                     # Page interaction utilities (URL parsing, token extraction)
├── api.ts                      # ChatGPT API wrapper (735 lines - core data layer)
├── constants.ts                # Configuration constants
├── i18n.ts                     # Internationalization setup
├── type.ts                     # TypeScript type definitions
│
├── exporter/                   # Export format implementations
│   ├── text.ts                 # Plain text export
│   ├── html.ts                 # HTML export with styling
│   ├── markdown.ts             # Markdown export with GFM
│   ├── json.ts                 # JSON/JSONL export (Official, Tavern, Ooba)
│   └── image.ts                # PNG screenshot export (html2canvas)
│
├── ui/                         # Preact/React UI components
│   ├── Menu.tsx                # Main menu component
│   ├── ExportDialog.tsx        # Export All dialog (batch export) - 400 lines
│   ├── SettingDialog.tsx       # Settings configuration
│   ├── SettingContext.tsx      # React context for settings
│   └── [other components]
│
├── hooks/                      # React hooks
│   ├── useGMStorage.ts         # Tampermonkey storage hook
│   └── [other hooks]
│
├── utils/                      # Utility functions
│   ├── queue.ts                # RequestQueue for batch processing (116 lines)
│   ├── download.ts             # File download utilities
│   ├── markdown.ts             # Markdown parsing/generation
│   └── [other utilities]
│
└── locales/                    # i18n translations (8+ languages)
```

---

## How Export Works

### Single Conversation Export

**Flow:**
1. User clicks export button in menu
2. Fetches conversation via API: `fetchConversation(chatId, shouldReplaceAssets)`
3. Processes raw API response: `processConversation()`
4. Transforms to selected format (markdown/html/json/png)
5. Downloads file directly

**Key Files:**
- `src/api.ts:441` - `fetchConversation()` - Fetches single conversation
- `src/api.ts:635` - `processConversation()` - Transforms raw API data
- `src/exporter/*.ts` - Format-specific transformation

### Export All (Batch Export)

**Current Flow (THE BOTTLENECK):**

```
User clicks "Export All"
    ↓
fetchAllConversations() - Fetches metadata for all conversations (up to 1000)
    ↓
User selects conversations (or "Select All")
    ↓
RequestQueue processes ALL selected conversations sequentially:
    - Fetches each conversation one-by-one
    - Stores ALL results in memory
    ↓
When queue completes, exportAll function receives ALL conversations at once
    ↓
Process ALL conversations into format (markdown/html/json)
    - Line 34 (markdown.ts): apiConversations.map(x => processConversation(x))
    - ALL conversations processed and held in memory
    ↓
Add ALL files to JSZip
    - Lines 35-52 (markdown.ts): forEach conversation, add to zip
    ↓
Generate ZIP blob (HUGE memory spike)
    ↓
Download single ZIP file
```

**Key Files:**
- `src/ui/ExportDialog.tsx:220-233` - `exportAllFromApi()` - Adds all to RequestQueue
- `src/utils/queue.ts:69-100` - `RequestQueue.process()` - Sequential processing
- `src/exporter/markdown.ts:31-64` - `exportAllToMarkdown()` - Processes ALL at once
- `src/exporter/html.ts:34-69` - `exportAllToHtml()` - Processes ALL at once
- `src/exporter/json.ts:63-106` - `exportAllToJson()` - Processes ALL at once

---

## The Performance Bottleneck

### Problem Analysis

When exporting thousands of conversations, the browser freezes due to:

#### 1. **Memory Overload**
   - All conversations fetched and stored in `RequestQueue.results[]` array
   - All conversations processed into `ConversationResult[]` objects
   - All conversations converted to strings (markdown/html/json)
   - All files added to JSZip in memory
   - Final ZIP compression happens on entire dataset at once

#### 2. **DOM Bloat** (Secondary Issue)
   - Conversation list renders ALL items (could be 1000+)
   - No virtual scrolling implemented

#### 3. **Sequential API Calls**
   - RequestQueue processes conversations one-by-one with backoff delays
   - Can take 10+ minutes for thousands of conversations
   - No ability to pause/resume

### Specific Code Locations

**ExportDialog.tsx:**
```typescript
// Line 225-230: Adds ALL selected conversations to queue
selected.forEach(({ id, title }) => {
    requestQueue.add({
        name: title,
        request: () => fetchConversation(id, exportType !== 'JSON'),
    })
})
```

**queue.ts:**
```typescript
// Line 86: ALL results stored in single array
this.results.push(result)

// Line 192 (ExportDialog.tsx): Receives ALL results at once
const off = requestQueue.on('done', (results) => {
    const callback = exportAllOptions.find(o => o.label === exportType)?.callback
    if (callback) callback(format, results, metaList)
})
```

**markdown.ts (and html.ts, json.ts):**
```typescript
// Line 34: Processes ALL conversations at once
const conversations = apiConversations.map(x => processConversation(x))

// Lines 35-52: Adds ALL to ZIP at once
conversations.forEach((conversation) => {
    const content = conversationToMarkdown(conversation, metaList)
    zip.file(fileName, content)
})

// Lines 54-60: Generates entire ZIP blob
const blob = await zip.generateAsync({
    type: 'blob',
    compression: 'DEFLATE',
    compressionOptions: { level: 9 }
})
```

---

## Proposed Solution: Chunked Export Processing

### Solution Design

Instead of processing ALL conversations at once, implement **chunked/batched export**:

#### Option A: Multiple ZIP Files (Recommended)
- Process conversations in chunks (e.g., 50-100 at a time)
- Generate separate ZIP files per chunk
- Downloads: `chatgpt-export-part1.zip`, `chatgpt-export-part2.zip`, etc.
- **Pros**: Simple, reliable, prevents memory overflow
- **Cons**: Multiple files to manage

#### Option B: Single ZIP with Progressive Processing
- Process in chunks, clear memory between chunks
- Add files to ZIP progressively
- Generate single ZIP at the end
- **Pros**: Single output file
- **Cons**: More complex, still risks memory issues on final compression

#### Option C: Streaming ZIP Generation
- Use streaming ZIP library (e.g., `zip-stream`)
- Stream files directly to download without holding in memory
- **Pros**: Best memory efficiency
- **Cons**: Requires library change, more complex

### Recommended Implementation (Option A)

**Changes Required:**

#### 1. Add Chunk Size Setting
**File: `src/ui/SettingContext.tsx`**
- Add `exportChunkSize` setting (default: 100)
- Allow users to configure chunk size

#### 2. Modify RequestQueue to Support Chunking
**File: `src/utils/queue.ts`**
- Add `onChunkComplete` event that fires every N items
- Emit intermediate results instead of waiting for full completion
- Clear processed results from memory after each chunk

#### 3. Update ExportDialog to Handle Chunks
**File: `src/ui/ExportDialog.tsx`**
- Listen for `onChunkComplete` events
- Process and download each chunk immediately
- Update UI to show "Processing chunk X of Y"
- Prevent UI freeze by using `requestIdleCallback` or Web Workers

#### 4. Update Export Functions for Chunked Processing
**Files: `src/exporter/markdown.ts`, `html.ts`, `json.ts`**
- Add `exportChunkToMarkdown()`, `exportChunkToHtml()`, `exportChunkToJson()`
- Generate ZIP per chunk with part number in filename
- OR accumulate chunks and generate single ZIP (Option B)

### Pseudo-code Implementation

```typescript
// RequestQueue modification
class RequestQueue<T> {
    private chunkSize: number = 100

    on(event: 'chunkComplete', fn: (chunk: T[], chunkIndex: number) => void): void

    private async process() {
        // ... existing code ...

        // After each item completes:
        if (this.completed % this.chunkSize === 0) {
            const chunk = this.results.splice(0, this.chunkSize)
            this.eventEmitter.emit('chunkComplete', chunk, chunkIndex++)
        }
    }
}

// ExportDialog.tsx modification
useEffect(() => {
    let chunkIndex = 0
    const off = requestQueue.on('chunkComplete', (chunk, index) => {
        // Process chunk immediately
        const callback = exportChunkOptions.find(o => o.label === exportType)?.callback
        if (callback) callback(format, chunk, metaList, index)
        chunkIndex++
    })
    return () => off()
}, [requestQueue])

// markdown.ts modification
export async function exportChunkToMarkdown(
    fileNameFormat: string,
    apiConversations: ApiConversationWithId[],
    metaList: ExportMeta[],
    chunkIndex: number,
    totalChunks: number
) {
    const zip = new JSZip()
    // ... existing processing logic ...

    const blob = await zip.generateAsync({ ... })
    const filename = totalChunks > 1
        ? `chatgpt-export-markdown-part${chunkIndex}.zip`
        : 'chatgpt-export-markdown.zip'
    downloadFile(filename, 'application/zip', blob)
}
```

---

## Implementation Status ✅

All core chunked export functionality has been implemented!

### ✅ Completed Changes

#### Phase 1: Add Chunk Size Setting
- ✅ Added `KEY_EXPORT_CHUNK_SIZE` constant to `src/constants.ts`
- ✅ Added `exportChunkSize` to SettingContext (default: 100)
- ✅ Added UI slider control in SettingDialog (range: 10-500)
- ✅ Added translations for chunk size settings

#### Phase 2: Modified RequestQueue
- ✅ Added `chunkSize` optional parameter to constructor
- ✅ Implemented `onChunkComplete` event with TypeScript types
- ✅ Emit chunks as they complete (every N items)
- ✅ Clear processed items from memory after chunk emission
- ✅ Emit final chunk when queue completes (for remaining items)

#### Phase 3: Updated ExportDialog
- ✅ Pass `exportChunkSize` to RequestQueue constructor
- ✅ Listen for `chunkComplete` events
- ✅ Track chunk progress separately in state
- ✅ Update progress UI to show "Processing chunk X of Y"
- ✅ Process and download each chunk immediately
- ✅ Reset chunk progress when export completes

#### Phase 4: Updated All Exporters
- ✅ Updated `exportAllToMarkdown()` with chunk parameters
- ✅ Updated `exportAllToHtml()` with chunk parameters
- ✅ Updated `exportAllToJson()` with chunk parameters
- ✅ Updated `exportAllToOfficialJson()` with chunk parameters
- ✅ Multi-part ZIP naming: `chatgpt-export-{format}-part{N}of{total}.zip`
- ✅ Backward compatible: single file when chunk size >= total conversations

### How It Works Now

When you export conversations:

1. **Configure chunk size**: Settings → Export Chunk Size (10-500, default 100)
2. **Select conversations**: Export All dialog → Select conversations
3. **Click Export**: RequestQueue fetches conversations one-by-one
4. **Automatic chunking**: Every 100 conversations (or your chunk size):
   - Creates ZIP file with those conversations
   - Downloads: `chatgpt-export-markdown-part1of10.zip`
   - Clears from memory
   - Continues with next chunk
5. **Progress display**: Shows both overall progress and current chunk
6. **Memory efficient**: Only holds chunk size conversations in memory at once

### Future Improvements (Optional)
1. Add virtual scrolling to conversation list (use `react-window`)
2. Add pause/resume functionality
3. Add cancel button during export
4. Show estimated time remaining
5. Add option to combine ZIPs at the end (optional)

---

## Key API Endpoints

```typescript
// Fetch all conversation metadata
GET /backend-api/conversations?offset=0&limit=100

// Fetch single conversation
GET /backend-api/conversation/{id}

// Fetch projects/GPTs
GET /backend-api/gizmos/snorlax/sidebar

// Fetch project conversations
GET /backend-api/gizmos/{gizmo}/conversations?cursor=0&limit=50

// Archive conversation
PATCH /backend-api/conversation/{id}
Body: { is_archived: true }

// Delete conversation
PATCH /backend-api/conversation/{id}
Body: { is_visible: false }

// Download file assets
GET /backend-api/files/{id}/download
```

---

## Data Flow Diagrams

### Current Export All Flow
```
User Action → Fetch Metadata (ALL) → User Selects →
RequestQueue Fetches (1-by-1, stores ALL) →
Process ALL → Add ALL to ZIP → Generate ZIP → Download
                ↑
         BOTTLENECK: All in memory
```

### Proposed Chunked Flow
```
User Action → Fetch Metadata (ALL) → User Selects →
RequestQueue Fetches (1-by-1) →
Every N items: Process CHUNK → Add CHUNK to ZIP → Generate ZIP → Download →
Clear Memory → Continue...
                ↑
         IMPROVED: Only chunk in memory
```

---

## Configuration Settings

### Current Settings
- `exportAllLimit`: Max conversations to fetch (default: 1000)
- `fileNameFormat`: Template for filenames (default: `ChatGPT-{title}`)
- `enableMeta`: Include metadata in exports
- `exportMetaList`: Custom metadata fields
- `enableTimestamp`: Show timestamps in exports

### Proposed New Settings
- `exportChunkSize`: Conversations per chunk/ZIP (default: 100)
- `enableVirtualScroll`: Use virtual scrolling for conversation list
- `autoMergeChunks`: Combine chunk ZIPs at the end (optional)

---

## Testing Recommendations

### Performance Testing
1. Test with 100 conversations
2. Test with 500 conversations
3. Test with 1000 conversations
4. Monitor memory usage during export
5. Test on different browsers (Chrome, Firefox, Edge)

### Edge Cases
1. Export with image asset replacement enabled
2. Export with very long conversation titles
3. Export with special characters in titles
4. Export interrupted mid-process
5. Network failures during fetch

---

## Known Issues & Limitations

### Current Issues
1. **Memory overflow** when exporting 1000+ conversations
2. **Browser freeze** during large exports
3. **No pause/resume** functionality
4. **No progress estimation** (only shows count)
5. DOM bloat with large conversation lists

### API Limitations
- Rate limiting on `/backend-api/conversations` (hence the backoff in RequestQueue)
- Max 100 conversations per request (regular) or 50 (projects)
- Image assets require separate API calls

---

## Dependencies

### Runtime
- **Preact**: 10.17 (React alternative)
- **JSZip**: 3.9 (ZIP file generation)
- **html2canvas**: 1.4 (PNG screenshot)
- **i18next**: Multi-language support

### Build
- **Vite**: 5.3 (Bundler)
- **vite-plugin-monkey**: 3.5 (Userscript generation)
- **TypeScript**: 5.5

---

## File Size Estimates

### Single Conversation
- Markdown: ~5-50 KB
- HTML: ~10-100 KB (with styling)
- JSON: ~10-200 KB (raw API response)
- PNG: ~100 KB - 5 MB (depends on length)

### Batch Export (1000 conversations)
- Markdown ZIP: ~5-50 MB
- HTML ZIP: ~10-100 MB
- JSON ZIP: ~10-200 MB
- **Memory usage during processing: 200-500 MB** (PROBLEM!)

---

## Contributing Guidelines

### Code Style
- Use TypeScript strict mode
- Follow existing naming conventions
- Add JSDoc comments for public APIs
- Use functional components (Preact hooks)

### Adding New Export Format
1. Create `src/exporter/newformat.ts`
2. Implement `exportToNewFormat()` and `exportAllToNewFormat()`
3. Add format to `exportAllOptions` in `ExportDialog.tsx`
4. Add translations to `src/locales/*.json`
5. Update README with examples

### Debugging
- Use browser DevTools console
- Check Tampermonkey logs
- Enable verbose logging in `api.ts`

---

## Resources

- **GitHub**: https://github.com/pionxzh/chatgpt-exporter
- **GreasyFork**: https://greasyfork.org/scripts/456055-chatgpt-exporter
- **Issues**: https://github.com/pionxzh/chatgpt-exporter/issues
- **ChatGPT API**: Unofficial reverse-engineered API

---

## Desktop Analyzer: AI-Powered Insights Extraction

### Overview

The **Desktop Analyzer** (`analyzer/cli.js`) is a standalone Node.js CLI tool that analyzes exported conversations using Claude Haiku 4.5 to extract structured insights and build a personal knowledge base.

### Why Desktop Instead of Browser?

**Problem:** Analyzing 2,800 conversations in browser = 6-8 hours of runtime, risk of crashes, no resume capability.

**Solution:** Separate export (fast, browser) from analysis (slow, desktop with checkpoints).

### Key Features

1. **Checkpoint/Resume System**
   - Saves progress every N conversations (configurable)
   - Resume from `.analyzer-checkpoint.json` if interrupted
   - Never lose progress on large batches

2. **User-Centric Extraction Strategy** 🆕
   - **Prioritizes YOUR content** over LLM responses
   - Extracts large user inputs (>100 words) with full text
   - Captures all user questions (reveals learning path)
   - Preserves creative prompts and instructions you wrote
   - De-prioritizes generic LLM explanations

3. **Real-Time Progress**
   - Progress bar with ETA and cost tracking
   - Skip failed conversations without stopping
   - Cost: ~$0.002/conversation (~$5.60 for 2,800 conversations)

### Usage

```bash
# Install dependencies
cd analyzer && npm install

# Analyze conversations
node cli.js analyze \
  --input ~/Downloads/conversations.json \
  --api-key sk-ant-YOUR_KEY \
  --output knowledge-base.json

# Resume from checkpoint
node cli.js analyze \
  --input ~/Downloads/conversations.json \
  --api-key sk-ant-YOUR_KEY \
  --resume

# Check progress
node cli.js stats
```

### Extraction Philosophy

**Old Approach (Equal Weight):**
- 50% extraction is generic LLM responses
- User insights buried in noise
- Hard to see YOUR evolving expertise

**New Approach (User-Centric):**
- 80% focus on YOUR content
- YOUR questions reveal learning journey
- YOUR prompts show communication skills
- YOUR insights map YOUR expertise

See `analyzer/EXTRACTION_STRATEGY.md` for complete methodology.

### Architecture

**File:** `analyzer/cli.js` (491 lines)

**Key Components:**
- `loadCheckpoint()` / `saveCheckpoint()` - Checkpoint management
- `parseConversationTurns()` - Extract turns from ChatGPT format
- `chunkConversation()` - Split into 10-turn chunks with 2-turn overlap
- `analyzeChunk()` - Send to Claude API with extraction prompt
- `analyzeConversation()` - Process all chunks for one conversation

**Extraction Priorities:**
1. 🥇 **Substantive user inputs** (>100 words) - Extract full text
2. 🥈 **User questions** - All questions, even 1-liners
3. 🥉 **User creative direction** - Prompts and instructions
4. **User insights** - Aha moments, hypotheses, decisions
5. **LLM responses** - ONLY if genuinely novel (confidence >0.9)

**Event Types (User-Focused):**
```typescript
type UserEventType =
  | "substantive_user_input"     // Full text preserved
  | "user_question"                // Reveals intent
  | "user_hypothesis"              // Your theories
  | "user_prompt"                  // Your prompts
  | "creative_direction"           // Your guidance
  | "problem_framing"              // How you describe problems
  | "user_code_example"            // Code YOU wrote
  | "domain_expertise"             // Your specialized knowledge
```

### Output Structure

```json
{
  "meta": {
    "conversations_analyzed": 2800,
    "total_entities": 8420,
    "total_cost": 5.64
  },
  "entities": {
    "evt_123_0_0": {
      "type": "substantive_user_input",
      "speaker": "user",
      "full_text": "Complete user message preserved here...",
      "word_count": 234,
      "context": "User describing complex architecture problem",
      "tags": ["react", "websocket", "architecture"],
      "metadata": {
        "user_expertise_signal": "intermediate",
        "user_intent": "Solve state management for real-time data"
      }
    }
  }
}
```

### Documentation Files

- `analyzer/README.md` - Quick start guide
- `analyzer/EXTRACTION_STRATEGY.md` - Complete extraction philosophy
- `analyzer/EXTRACT_INSTRUCTIONS.md` - LLM analyzer instructions
- `QUICKSTART.md` - User guide for browser + desktop workflow

### Performance

| Conversations | Time    | Cost    | Memory  |
|--------------|---------|---------|---------|
| 100          | 30 min  | $0.20   | ~50 MB  |
| 500          | 2.5 hrs | $1.00   | ~50 MB  |
| 2,800        | 6-8 hrs | $5.60   | ~50 MB  |

**Benefits:**
- Constant memory usage (only holds chunk in memory)
- Can run overnight safely
- Resume from any point
- Skip failed conversations without losing progress

---

## Conclusion

The main performance bottleneck is the **all-at-once processing** in the export functions. By implementing **chunked export processing**, we can:

1. ✅ Prevent memory overflow
2. ✅ Avoid browser freezing
3. ✅ Provide better progress feedback
4. ✅ Enable larger exports (5000+ conversations)
5. ✅ Improve user experience

The recommended approach is **Option A: Multiple ZIP Files** as it's the simplest and most reliable solution.

For **analysis**, the desktop CLI analyzer provides:
- Safe, resumable processing for thousands of conversations
- User-centric extraction that prioritizes YOUR content
- Structured knowledge base of YOUR expertise and thinking patterns
