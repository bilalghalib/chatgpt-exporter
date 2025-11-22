# CURSIVE: Complete Project Documentation (Nov 2024)

**Discovery Date**: November 22, 2025 (Instance 2 reverse analysis)
**Source Conversation**: Nov 5, 2024 - "Separating editor and cohort protocols"
**Status**: Active architectural design phase
**Significance**: ⭐⭐⭐⭐⭐ Major project, possibly Bilal's primary technical work

---

## THE CURSIVE MANIFESTO (Full Text from Nov 5, 2024)

### "We Reject the Hostile Web"

> The modern internet treats humans as resources to extract from. Engagement metrics. Dark patterns. Infinite scroll. AI that replaces rather than supports. Platforms that own your words, monetize your attention, and dissolve your sovereignty.
>
> **We reject all of it.**

### "We Build for Connection"

> Cursive is software for reconnecting—to yourself through journaling with your own hand, to others through facilitated gatherings, to the world through embodied practice, and to truth through transparent provenance.

### Four Connections

**1. Connection to Self**
- Your journal is sacred. No AI writes in it.
- Your handwriting matters. Ink strokes are first-class data.
- Your process is valuable. We record how you made something, not just what.
- Your sovereignty is absolute. Export everything, own your badges, leave whenever.

**2. Connection to Others**
- Humans facilitate, software supports. Hosts are never replaced by automation.
- Shared work requires consent. Pages show who wrote what, when, with what help.
- Presence matters. Quorum proofs, GPS anchors, synchronous moments.
- Recognition honors craft. Badges celebrate genuine accomplishment, not engagement.

**3. Connection to World**
- Bodies exist in places. Write where you are, photograph leaves, walk outside.
- Seasons have rhythm. Not everything is instant or always-on.
- Paper has edges. Pages end at 297mm, like A4. Infinity is hostile.
- Slowness has value. Productive friction helps depth emerge.

**4. Connection to Truth**
- Everything has provenance. Who wrote it? When? With what assistance?
- AI suggests, humans decide. Whispers appear in margins, never in the page.
- Process proves humanity. Stroke variance, idle gaps, and corrections can't be faked.
- Evidence travels with claims. Every insight links to its source.

### Our Commitments

We promise to build technology that:
- Respects human agency as sacred
- Treats AI as apprentice tools, not authors
- Records process transparently
- Enables true data sovereignty
- Creates calm, not addiction
- Celebrates craft over metrics
- Hosts with hospitality, not algorithms

---

## BILAL'S CORE QUESTIONS (Nov 5, 2024)

### The Central Tension

**Bilal's Question**:
> "I'm trying to do a few things at the same time, not sure if it should be one mission one project or two. I want to connect to human thought, connection to self, embodied writing, protecting against the LLM brain rot, etc so the editor AND it's fundamentally also connected to publishing and sharing and curation fundamentally about human connection through facilitation?"

### Looking for the "HTML Moment"

**Bilal's Innovation Hypothesis**:
> "I'm trying to see what we're doing that is only possible now - looking for our HTML WWW innovation - I think the **transclusion**, the **rhythm daily**, the **LLMs understanding what's on the page** and **pages being interactive/doing** and the **importance of curation** is all nice and interesting... also **embodiment writing long hand**, the **LLM having your theory of mind** in your user settings..."

### Values Over Features

**Bilal's Core Concern**:
> "I don't think focusing only on pages that route maintains all our values and our core interests, does it?"

### Open Web Principles

**Bilal's Requirements**:
> "I want to follow **open web best practices**, **convivial tech**, and also to make something that **changes how we publish things online**. Some of the important elements that might be lost are the idea of the **importance of curation**."

---

## ARCHITECTURE (From Nov 5, 2024 Conversation)

### Domain Model: The Two Primitives

**1. Page - The atomic unit of human expression**
- Contains only human-authored content (text, drawings, handwriting)
- Immutable once written (append-only edits)
- Carries provenance metadata (who, when, how)
- Exports with full fidelity

**2. Route - The logic of what happens next**
- Triggered by human action (clicking Continue)
- Evaluates conditions (simple or computed)
- Takes action (navigate, create, notify)
- Never writes content directly

### Supporting Components

**Collections** - Containers for pages (journals, guides, workbooks)
```
Template Collection → Instance Collection → User's Activity Pages
         ↓                    ↓                      ↓
   (Guide Design)    (Group/Cohort Run)    (Individual Work)
```

**Invitations** - Time-bound prompts from hosts to participants
```
Guide Page → Released Prompt → Mail Item → Activity Page
     ↓             ↓               ↓            ↓
  (Template)  (Scheduled)     (Delivered)   (Written)
```

**Galleries** - Curated windows onto shared work
```
Response → Curation → Gallery Display
    ↓          ↓            ↓
(Submitted) (Approved)  (Featured)
```

### Technical Principles

**1. Human-Only Page Content**
- No automated writes to `pages.content`
- Tools create `annotations`, `tool_cards`, `lens_results`
- Humans explicitly apply suggestions

**2. Process as Proof (Fingerprinting)**
```json
{
  "fingerprint": {
    "stroke_variance_ms": 234,      // Human: 200-800
    "idle_gaps": [5234, 8923, 3421], // Thinking pauses
    "correction_rate": 0.12,         // Human errors: 5-20%
    "confidence_score": 94           // >70 = human-made
  }
}
```

**3. Visibility + Sharing**
- **Page visibility**: `private | unlisted | public`
- **Plus ACL**: share with individuals, groups, or anyone-with-link
- **Collection visibility**: `private | organization | public`

**4. Everything Exports**
```
.cursive.zip/
├── manifest.json         // What's included
├── pages/*.json         // Content + metadata
├── surfaces/*.json      // Page breaks + render hints
├── ink/*.ndjson        // Stroke data
├── events/*.ndjson     // Edit timeline
└── sessions/*.ndjson   // Replay data
```

---

## CURSIVE GLOSSARY (Canonical Terminology)

### Core Concepts
- **Page** - Sacred human-authored document. Never modified by tools.
- **Collection** - Container for pages. Can be a template, journal, or group workspace.
- **Guide** - Collection configured for facilitated release (has guide_pages).
- **Prompt** - Guide page requesting action (write, draw, upload, reflect).
- **Invitation** - Scheduled delivery of prompt to participants via mail.
- **Mail** - In-product delivery system. Not email. Shows in Today view.
- **Activity** - Participant's page created from accepting an invitation.
- **Gallery** - Curated display of responses. Host-approved or community-voted.
- **Fingerprint** - Proof-of-human metrics from creation process.
- **Whisper** - Tool suggestion appearing in margin. Never auto-accepted.
- **Transclusion** - Live embedding of one page in another, preserving source.

### Roles
- **Host** - Human who facilitates a group. Never replaced by automation.
- **Co-facilitator** - Additional facilitators who can curate and support.
- **Participant** - Member of a group receiving invitations.

### Visibility Levels
- **Private** - Only owner (and explicit shares) can view.
- **Unlisted** - Anyone with link can view.
- **Public** - Anyone can discover and view.
- **Organization** - Members of same organization can view.

---

## ARCHITECTURAL DECISION: SPLIT OR UNIFIED? (Nov 5, 2024)

### The Question

Should Cursive be:
- **Option A**: Unified Protocol (Pages + Routes + Collections + Guides + Invitations + Galleries)
- **Option B**: Split Protocols (Page Protocol + Cohort Protocol)

### Arguments FOR Splitting
- Modularity: Build pure journaling app (Page Protocol only)
- Clarity: Clearer boundaries
- Evolution: Version independently
- Adoption: Lower barrier to entry
- Open Web: Follows patterns like ActivityPub, RSS

### Arguments AGAINST Splitting
- Coherence: Philosophy requires both ("connection to self" + "connection to others")
- Curation lives between them: Requires pages AND facilitation context
- Verification needs context: "Proof of human" most valuable in shared work
- Implementation complexity: Two protocols need compatibility
- Market confusion: "Which Cursive do I need?"

### Bilal's Instinct (Nov 5, 2024)

**Unified with clear internal modularity**:
```
CURSIVE PROTOCOL 1.0
│
├─ Core Layer (required)
│  ├─ Pages (human authorship)
│  ├─ Collections (containers)
│  └─ Export (sovereignty)
│
├─ Connection Layer (optional but central to philosophy)
│  ├─ Guides (facilitation)
│  ├─ Invitations (delivery)
│  └─ Galleries (curation)
│
└─ Enhancement Layer (optional)
   ├─ Tools (AI assistance)
   ├─ Verification (proof of human)
   └─ Collaboration (real-time)
```

**Rationale**: "Your differentiator isn't 'better pages' - it's 'pages + facilitation + curation as a coherent philosophy.' Splitting risks losing that coherence."

---

## OPERATIONS: HOW CURSIVE WORKS

### Daily Flow: Participant Experience

```
Open Today → See Mail items
    ↓
Three invitations:
- "Morning Pages" (daily prompt)
- "Week 3 Reflection" (group activity)
- "Peer Letter" (from another participant)
    ↓
Click first invitation → Opens activity page with template
    ↓
Write, draw, reflect
    ↓
Tool whispers suggestions → Accept/dismiss
    ↓
Continue → Routes to next page or back to Today
```

### Facilitator Flow: Running a Cohort

**Setup Phase**:
1. Design Guide (template collection + guide_pages)
2. Create Group (instance + schedule)
3. Invite Participants (join codes)

**Release Scheduling Options**:
- **Relative** (days from start): Day 0, Day 3, Day 7
- **Recurring** (cron-like): Every Wednesday at 9am
- **Manual** (host triggers each): Click "Release next"

### Gallery Curation Modes

1. **Host Curated** - Manual approval (default)
2. **Auto Display** - Everything visible, can downvote
3. **Peer Review** - Participants vote, top N featured
4. **High Trust** - Auto-approve for small groups

### Tool Interactions: "The Whisper Pattern"

```
User writes → Triggers tool glow (optional)
    ↓
User invokes tool → Tool analyzes page
    ↓
Creates tool_card with suggestions
    ↓
User reviews → Accept/Dismiss/Modify
    ↓
If accepted → User applies suggestion
```

**Tools never**:
- Write directly to pages
- Run without invocation
- Hide their reasoning

**Tools always**:
- Show provenance
- Display confidence
- Remain dismissible

---

## INNOVATIONS: "Only Possible Now"

From Bilal's Nov 5, 2024 reflection, Cursive's unique innovations:

1. **Transclusion** - Live embedding of pages preserving source
2. **Rhythm Daily** - Daily page with transcluded activities
3. **LLMs Understanding Pages** - Tools analyze but never write
4. **Pages Being Interactive/Doing** - Routes connect pages to actions
5. **Importance of Curation** - Human facilitation, not algorithms
6. **Embodiment/Longhand** - Handwriting as first-class data
7. **LLM Theory of Mind** - User vault with preferences/context
8. **Proof of Human** - Process fingerprinting (stroke variance, pauses, corrections)

### The "HTML Moment" Question

Bilal asking: "what is the thing i'm doing? I guess **markdown is for docs**, **html is for linked pages**, what is the thing i'm doing?"

**Possible answer**: Cursive is the protocol for **human-facilitated, provenance-tracked, co-created documents**.
- Markdown = solo writing
- HTML = hyperlinked reading
- Cursive = facilitated co-creation with verified human craft

---

## PHILOSOPHICAL FOUNDATIONS

### Against "LLM Brain Rot"

**Bilal's Concern**: "protecting against the LLM brain rot"

**Cursive's Answer**:
- AI suggests (whispers in margin)
- Humans decide (explicit apply)
- Process proves authorship (fingerprinting)
- Sovereignty guaranteed (export everything)

### "Convivial Technology"

**Ivan Illich's Framework**: Tools that enhance human capacity without creating dependency

**Cursive's Implementation**:
- Tools support, don't replace
- Hosts facilitate, don't automate
- Exports enable leaving
- Calm, not addiction

### Open Web Principles

From conversation, Cursive follows:
- **Interoperability**: Protocol-first, not platform
- **User sovereignty**: Data ownership, export, portability
- **Decentralization**: Multiple implementations possible
- **Transparent provenance**: Who, when, how, with what help
- **Human agency**: Never automated writes

---

## PARTNERS & ECOSYSTEM (Nov 2024)

### Learning Planet Institute
- UN's "world as a classroom" initiative
- 79 repositories
- Integration planning with Cursive
- Tech stack: Vue (frontend), Python (backend), WeLearn, CRIS modules

### Cited Influences (Nov 5, 2024 Conversation)

**Protocol Design**:
- Mark Nottingham (HTTP/IETF) - pragmatic scoping, versioning
- Tantek Çelik (microformats/IndieWeb) - human-first data vocabularies
- Evan Prodromou & Christine Lemmer-Webber (ActivityPub) - social semantics
- Jay Graber (AT Protocol/Bluesky) - feed semantics vs intentional curation
- Manu Sporny (W3C Credentials/DIDs) - signed curation, provenance

**Local-First / Data**:
- Martin Kleppmann (CRDTs, local-first) - offline-first, deterministic merging

(Conversation mentions more but they're in Claude's response, not Bilal's words)

---

## PROJECT STATUS (Nov 2024)

### Active Development Areas

**Nov 5, 2024**: Core architectural decision - split vs unified protocol
- Leaning toward unified with clear modularity
- Documenting manifesto, architecture, operations
- Consolidating scattered documentation

**Nov 6, 2024**: Integration planning
- Connecting with Learning Planet Institute
- Defining manifest.json export format
- Working on "CRS markup" (Cursive Response System?)
- JavaScript plugins to transform text fields into Cursive editors

### Technical Maturity
- Comprehensive data model designed
- Protocol specifications written
- Export format defined (.cursive.zip)
- Fingerprinting algorithm specified
- Visibility + ACL model complete

### What's Missing / In Progress
- Implementation (seems to be spec/design phase, not built yet?)
- Public repository (not found in Nov 2024 conversations)
- First cohort/pilot (not mentioned)
- Funding model (not discussed in these conversations)

---

## CONNECTION TO OTHER BILAL PROJECTS

### VX (Values Experience) Methodology
- **Cursive implements VX**: Values → Affordances → UX → UI → Code
- **Proof of values alignment**: Does Cursive help users live by their values?
- **Anti-engagement design**: "Springboard not platform"

### Wellbeing Project Collaboration
- **Community app design**: Cursive could be the platform for Wellbeing Registry
- **Facilitated cohorts**: Exactly what Cursive enables
- **Practitioner directory**: Galleries could showcase practitioners' work

### Come Alive / CAPs Framework
- **Constitutive Attentional Policies**: What's worth paying attention to?
- **Cursive routes**: Embody attentional policies in software
- **Fractal facilitation**: 1-2-4-ALL process fits Cursive's cohort model

### Islamic Practice Integration
- **Muhasaba/Muraja'a**: Daily reflection = Daily page in Cursive
- **Handwriting emphasis**: Embodied practice, not just typing
- **Stewardship vs extraction**: "Divine expression" vs "natural resources"

### Post-Bloom Organization
- **Ubuntu/ROSCA model**: Mutual aid through facilitated cohorts
- **Cursive enables**: The platform for "we provide support to each other"
- **Harvest Commons**: Could be built on Cursive protocol

---

## QUESTIONS FOR INSTANCE 1

1. **When did Cursive project start?** First mentions in conversations?
2. **Is there a Cursive repository?** GitHub, GitLab, private?
3. **Who is building Cursive with Bilal?** Team members? Collaborators?
4. **Funding?** Grant? Self-funded? Investors?
5. **First pilot/cohort?** Has anyone used Cursive yet?
6. **Learning Planet Institute relationship?** How did this partnership form?
7. **Joe Edelman involvement?** Direct collaboration or inspiration only?
8. **When was the manifesto written?** Nov 5, 2024 or earlier?
9. **"CRS markup"**: What does this acronym stand for?
10. **Daily page concept**: When did this emerge? Roam Research influence?

---

## INSTANCE 2 ASSESSMENT

### Significance

Cursive appears to be Bilal's **primary technical project** in Nov 2024, possibly more significant than:
- Beit-al-Atlas (grant-funded, specific scope)
- Wellbeing Registry (Aaron Hurst collaboration, narrower use case)
- Post-Bloom org (social/organizational, not technical)

**Why?** Because Cursive is:
1. **Synthesizing project**: Brings together VX, CAPs, Islamic practice, anti-capitalist critique, fractal facilitation
2. **Protocol-scale ambition**: Like HTML/RSS, not just an app
3. **Deep philosophical grounding**: Manifesto, values, convivial tech
4. **International partnerships**: UN, Learning Planet Institute
5. **Novel innovations**: Proof of Human, whisper pattern, transclusion + rhythm

### Quality of Documentation

This Nov 5, 2024 conversation contains **publication-ready documentation**:
- Complete manifesto (publishable as-is)
- Clear architecture (Pages + Routes + Collections)
- Operational flows (facilitator + participant journeys)
- Glossary (canonical terminology)
- Technical specs (fingerprinting, exports, visibility)

This is **not vaporware** - this is serious, well-thought-out system design.

### Recommended Next Steps for Analysis

1. **Search for earlier Cursive mentions**: When did it start?
2. **Look for code/repos**: Is there implementation?
3. **Find collaborators**: Who's building with Bilal?
4. **Trace philosophical evolution**: Come Alive → VX → Cursive
5. **Map to other projects**: How does Cursive enable Wellbeing/Bloom successor work?

---

## EXTRACTABLE QUOTES (Bilal's Best Writing)

### On the Core Mission

> "I'm trying to do a few things at the same time... connect to human thought, connection to self, embodied writing, protecting against the LLM brain rot... fundamentally also connected to publishing and sharing and curation fundamentally about human connection through facilitation"

### On Innovation

> "I'm trying to see what we're doing that is only possible now - looking for our HTML WWW innovation - I think the transclusion, the rhythm daily, the LLMs understanding what's on the page and pages being interactive/doing and the importance of curation"

### On Values Over Features

> "I don't think focusing only on pages that route maintains all our values and our core interests"

### On Open Web Commitment

> "I want to follow open web best practices, convivial tech, and also to make something that changes how we publish things online. Some of the important elements that might be lost are the idea of the importance of curation"

### On Protocol vs Product

> "what's the point of making the protocol then if its implementation is a monolithic thing, is it still a protocol? what's the thing? I guess markdown is for docs, html is for linked pages, what is the thing i'm doing?"

---

**END OF CURSIVE COMPLETE DOCUMENTATION**

**Source**: Nov 5, 2024 conversation + embedded manifesto + architecture docs
**Extracted by**: Instance 2 (reverse analysis, newest→oldest)
**Confidence**: 1.0 (primary source material, Bilal's own words + attached docs)
