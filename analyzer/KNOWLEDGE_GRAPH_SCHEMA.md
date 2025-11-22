# Knowledge Graph Schema

> **Purpose**: Extract entities, relationships, and attributes for graph visualization and computational analysis

---

## Graph Structure

### Node Types

#### 1. **Person**
```json
{
  "type": "Person",
  "id": "person.bilal_ghalib",
  "properties": {
    "name": "Bilal Ghalib",
    "full_name": "Bilal Ghalib",
    "roles": ["Co-founder", "Educator", "Roboticist", "Facilitator"],
    "locations": ["Detroit", "Lebanon", "MENA"],
    "faith": "Muslim",
    "status": "Expecting parent (wife pregnant as of 2023-03)",
    "self_descriptions": ["nerdy", "great at research", "all over the place"]
  }
}
```

#### 2. **Project**
```json
{
  "type": "Project",
  "id": "project.bloom",
  "properties": {
    "name": "Bloom",
    "full_name": "Bloom.pm",
    "type": "Social Enterprise / Nonprofit Accelerator",
    "status": "Active",
    "founded": "~2020",
    "description": "Training programs using assessments + interventions for personal/professional growth",
    "business_model": "Nonprofit accelerator, seeking corporate clients"
  }
}
```

#### 3. **Organization**
```json
{
  "type": "Organization",
  "id": "org.gemsi",
  "properties": {
    "name": "GEMSI",
    "full_name": "Global Entrepreneurship and Maker Space Initiative",
    "type": "Nonprofit",
    "status": "Active",
    "website": "gemsi.org",
    "mission": "Bring hackerspaces and innovation culture to MENA"
  }
}
```

#### 4. **Concept**
```json
{
  "type": "Concept",
  "id": "concept.permah",
  "properties": {
    "name": "PERMAH",
    "full_name": "Positive Emotion, Engagement, Relationships, Meaning, Accomplishment, Health",
    "domain": "Psychology / Well-being",
    "creator": "Martin Seligman",
    "category": "Educational Framework"
  }
}
```

#### 5. **Technology**
```json
{
  "type": "Technology",
  "id": "tech.chatgpt",
  "properties": {
    "name": "ChatGPT",
    "category": "AI / LLM",
    "used_for": ["Research", "Work exploration", "Curriculum design"]
  }
}
```

#### 6. **Location**
```json
{
  "type": "Location",
  "id": "location.mena",
  "properties": {
    "name": "MENA",
    "full_name": "Middle East and North Africa",
    "countries": ["Iraq", "Lebanon", "Egypt", "..."],
    "relevance": "Primary geographic focus for social impact work"
  }
}
```

#### 7. **Skill/Strength**
```json
{
  "type": "Skill",
  "id": "skill.creativity",
  "properties": {
    "name": "Creativity",
    "category": "Character Strength",
    "score": 5.0,
    "source": "Character Strengths Assessment",
    "date_assessed": "2023-03-27"
  }
}
```

#### 8. **Event**
```json
{
  "type": "Event",
  "id": "event.arab_spring",
  "properties": {
    "name": "Arab Spring",
    "year": "2011",
    "impact": "Inspired Bilal to work overseas and teach entrepreneurship",
    "significance": "Pivotal career change moment"
  }
}
```

#### 9. **Value** (from Come Alive framework)
```json
{
  "type": "Value",
  "id": "value.curious_knowledge_weaver",
  "properties": {
    "name": "Curious Knowledge-Weaver",
    "description": "Finding meaning through connecting frameworks, exploring questions, sharing insights",
    "confidence": 0.92,
    "first_observed": "2023-02-27",
    "attention_policies": ["QUESTIONS that spark fascination", "FRAMEWORKS revealing patterns", "..."]
  }
}
```

---

### Relationship Types

#### Person ↔ Project
- `FOUNDED` - Person founded Project
- `CO_FOUNDED` - Person co-founded Project with others
- `WORKS_ON` - Person actively works on Project
- `RESPONSIBLE_FOR` - Person has specific role/responsibility

#### Person ↔ Person
- `COLLABORATES_WITH` - Works together
- `MENTORED_BY` - Learning relationship
- `PROVIDES_FEEDBACK_TO` - 360 feedback relationships
- `PARTNERS_WITH` - Business/project partnership

#### Person ↔ Concept
- `EXPLORES` - Person researches/studies Concept
- `TEACHES` - Person educates others on Concept
- `APPLIES` - Person uses Concept in practice
- `COMPARES` - Person analyzes Concept vs other Concepts

#### Person ↔ Technology
- `USES` - Person uses Technology
- `EXPERIMENTS_WITH` - Person explores Technology
- `DEVELOPS` - Person builds Technology

#### Person ↔ Location
- `LOCATED_IN` - Current/past physical location
- `WORKS_IN` - Geographic focus of work
- `FROM` - Origin/background

#### Person ↔ Skill
- `HAS_STRENGTH` - Person exhibits Skill (high score)
- `HAS_WEAKNESS` - Person struggles with Skill (low score)
- `DEVELOPS` - Person actively working on Skill

#### Person ↔ Event
- `INFLUENCED_BY` - Event shaped Person's trajectory
- `PARTICIPATED_IN` - Person was involved in Event

#### Person ↔ Value
- `EMBODIES` - Person demonstrates Value
- `ASPIRES_TO` - Person seeks to develop Value

#### Project ↔ Location
- `OPERATES_IN` - Project serves Location
- `BASED_IN` - Project headquarters

#### Project ↔ Concept
- `BASED_ON` - Project uses Concept as foundation
- `IMPLEMENTS` - Project applies Concept

---

### Edge Properties

All relationships include:
```json
{
  "source_id": "person.bilal_ghalib",
  "target_id": "project.bloom",
  "relationship": "CO_FOUNDED",
  "properties": {
    "confidence": 0.95,
    "evidence": ["conversation_id", "quote", "..."],
    "first_observed": "2023-03-25",
    "last_observed": "2023-03-29",
    "strength": 0.9,
    "context": "Social enterprise education"
  }
}
```

---

## Extraction Rules for Knowledge Graph

### When reading conversations:

1. **Extract Named Entities:**
   - People (colleagues, partners, influencers)
   - Projects (with names: "Bloom", "Flybrary", "GEMSI")
   - Organizations (companies, nonprofits, institutions)
   - Concepts (frameworks, theories, methodologies)
   - Technologies (tools, platforms, software)
   - Locations (countries, regions, cities)
   - Events (pivotal moments, conferences, launches)

2. **Identify Relationships:**
   - Who works with whom?
   - What projects is Bilal involved in?
   - What concepts does he explore/compare?
   - What technologies does he use?
   - What events influenced his trajectory?

3. **Track Temporal Data:**
   - When was entity first mentioned?
   - When was relationship established?
   - How does relationship evolve over time?

4. **Compute Confidence:**
   - Single mention: 0.3-0.5
   - Multiple mentions: 0.6-0.8
   - Explicit detail: 0.8-1.0

---

## Knowledge Graph Export Formats

### Neo4j Cypher
```cypher
CREATE (bilal:Person {
  name: "Bilal Ghalib",
  roles: ["Co-founder", "Educator"]
})

CREATE (bloom:Project {
  name: "Bloom",
  type: "Social Enterprise"
})

CREATE (bilal)-[:CO_FOUNDED {
  year: 2020,
  confidence: 0.95
}]->(bloom)
```

### JSON Graph Format
```json
{
  "nodes": [
    {"id": "person.bilal_ghalib", "type": "Person", "properties": {...}},
    {"id": "project.bloom", "type": "Project", "properties": {...}}
  ],
  "edges": [
    {
      "source": "person.bilal_ghalib",
      "target": "project.bloom",
      "relation": "CO_FOUNDED",
      "properties": {...}
    }
  ]
}
```

### GraphML (for Gephi, Cytoscape)
```xml
<graph>
  <node id="person.bilal_ghalib" label="Bilal Ghalib">
    <data key="type">Person</data>
  </node>
  <edge source="person.bilal_ghalib" target="project.bloom">
    <data key="relation">CO_FOUNDED</data>
  </edge>
</graph>
```

---

## Example: Bilal's Knowledge Graph (Seed)

### Core Nodes (from first 4 conversations):

**People:**
- bilal_ghalib (self)
- andrew_archer (Robotics Redefined partner)
- mohammed (Bloom coder, Iraqi)
- avery (Bloom library/grants, friend)
- dara (Bloom programs lead, former mentee)
- habib (Bloom PM, facilitator)
- carol (Safir runner, HR professional)
- claude (Bloom library, quiet/systematic)
- ghina (M&E expert, mentioned by colleagues)
- fadel_zayad (Investment professional, Bloom module leader)
- habib_tawk (Bloom colleague)

**Projects:**
- bloom (Social enterprise accelerator)
- gemsi (Hackerspaces nonprofit)
- flybrary (Book lending platform)
- aiwayway (Tech project)
- robotics_redefined (Detroit automotive robots)
- instructables (Maker community - employment)
- gaza_sky_geeks (Mentorship)
- project_greencube (Vertical gardens)
- diy_sustainability (Initiative)

**Organizations:**
- bloom_pm
- gemsi_org
- instructables
- maker_faire_africa
- fab_lab_network

**Concepts:**
- permah (Well-being framework)
- universal_skills (21st century skills)
- habits_of_mind (16 cognitive habits)
- skills_builder (8 essential skills)
- perma_at_work (Workplace well-being)
- theory_of_change
- raci_matrix
- strategy_map

**Locations:**
- detroit (Robotics work)
- mena (Primary geographic focus)
- iraq (GEMSI work)
- lebanon (GEMSI work)
- egypt (GEMSI work)
- gaza (Sky Geeks mentorship)
- boston (2014 event with Nadeem - mentioned but unclear)
- uk (Visa application)

**Technologies:**
- chatgpt (AI exploration)
- arduino (DIY projects)
- 3d_printing (Workshops)
- mycelium (Biodegradable packaging experiments)
- solar_energy (Projects)

**Events:**
- arab_spring_2011 (Career pivot moment)
- wife_pregnancy_2023 (Personal/financial pressure)

**Skills (from assessments):**
- creativity (5/5)
- curiosity (4.8/5)
- love_of_learning (5/5)
- humor (5/5)
- judgement (5/5)
- persistence (3.2/5 - weakness)
- teamwork (2.67/8 - weakness)
- aiming_high (2.43/8 - weakness)

**Values (from Come Alive extraction):**
- curious_knowledge_weaver (0.92 confidence)

---

## Sample Relationships:

```
bilal_ghalib -[CO_FOUNDED]-> gemsi
bilal_ghalib -[CO_FOUNDED]-> bloom
bilal_ghalib -[CREATED]-> flybrary
bilal_ghalib -[PARTNERS_WITH]-> andrew_archer
bilal_ghalib -[WORKS_ON]-> bloom
bilal_ghalib -[RESPONSIBLE_FOR]-> bloom_curriculum
bilal_ghalib -[COLLABORATES_WITH]-> mohammed
bilal_ghalib -[COLLABORATES_WITH]-> dara
bilal_ghalib -[MENTORED]-> dara (past)
bilal_ghalib -[RECEIVES_FEEDBACK_FROM]-> avery
bilal_ghalib -[RECEIVES_FEEDBACK_FROM]-> habib
bilal_ghalib -[INFLUENCED_BY]-> arab_spring_2011
bilal_ghalib -[LOCATED_IN]-> lebanon
bilal_ghalib -[WORKS_IN]-> mena
bilal_ghalib -[EXPLORES]-> permah
bilal_ghalib -[EXPLORES]-> universal_skills
bilal_ghalib -[COMPARES {count: 5}]-> educational_frameworks
bilal_ghalib -[USES]-> chatgpt
bilal_ghalib -[EXPERIMENTS_WITH]-> mycelium
bilal_ghalib -[HAS_STRENGTH]-> creativity
bilal_ghalib -[HAS_WEAKNESS]-> persistence
bilal_ghalib -[HAS_WEAKNESS]-> teamwork
bilal_ghalib -[EMBODIES]-> curious_knowledge_weaver

bloom -[OPERATES_IN]-> mena
bloom -[BASED_ON]-> permah
bloom -[BASED_ON]-> universal_skills
bloom -[EMPLOYS]-> mohammed
bloom -[EMPLOYS]-> avery
bloom -[EMPLOYS]-> dara

gemsi -[OPERATES_IN]-> iraq
gemsi -[OPERATES_IN]-> lebanon
gemsi -[OPERATES_IN]-> egypt
gemsi -[MISSION]-> bring_hackerspaces_to_mena

andrew_archer -[PARTNERS_WITH]-> bilal_ghalib
andrew_archer -[CO_FOUNDED]-> robotics_redefined

dara -[MENTORED_BY {past: true}]-> bilal_ghalib
dara -[PROVIDES_FEEDBACK_TO]-> bilal_ghalib

permah -[CREATED_BY]-> martin_seligman
permah -[EXPANDS]-> perma
permah -[RELATED_TO]-> perma_at_work

arab_spring_2011 -[INFLUENCED]-> bilal_ghalib
arab_spring_2011 -[LOCATION]-> mena
```

---

## Incremental Graph Building

As I analyze each conversation:

1. **Extract new nodes** not yet in graph
2. **Create new edges** between nodes
3. **Update edge weights** (if relationship mentioned again, increase strength)
4. **Add temporal markers** (first_observed, last_observed)
5. **Compute centrality** (which nodes are most connected?)
6. **Identify clusters** (what communities emerge?)

---

**Next**: Continue Batch 1 analysis while building knowledge graph incrementally!
