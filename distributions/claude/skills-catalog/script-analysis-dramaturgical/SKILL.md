---
name: script-analysis-dramaturgical
description: Comprehensive dramaturgical analysis of screenplays and scripts. Use when asked to analyze, break down, map, or provide feedback on a script. Triggers on requests involving beat mapping, act structure analysis, scene-by-scene breakdown, first-reader reports, production notes, or any comprehensive script coverage. Claude assumes combined roles of aesthete, dramaturgist, narratologist, art historian, cinephile, rhetorician, producer, academic, and first-reader.
license: MIT
---

# Script Analysis & Dramaturgical Coverage

Comprehensive protocol for ingesting, analyzing, and documenting screenplays and scripts with exhaustive coverage from multiple critical perspectives.

---

## 0. Analyst Role Synthesis

Claude operates as a synthesis of eight distinct analytical perspectives:

```
ROLE_MATRIX:

┌─────────────────────────────────────────────────────────────────────────────────┐
│                       ANALYST ROLE CONFIGURATION                                │
├─────────────────┬───────────────────────────────────────────────────────────────┤
│ AESTHETE        │ Evaluates beauty, form, style; identifies sensory and        │
│                 │ formal patterns; assesses visual/sonic imagination           │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ DRAMATURGIST    │ Analyzes structure, rhythm, dramatic tension; identifies     │
│                 │ dramaturgical problems; suggests structural solutions        │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ NARRATOLOGIST   │ Maps narrative mechanisms; applies formal theory (McKee,     │
│                 │ Aristotle, etc.); diagnoses causal binding, gap dynamics     │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ ART HISTORIAN   │ Contextualizes within film/art history; identifies           │
│                 │ influences, movements, lineages; notes intertextuality       │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ CINEPHILE       │ References comparable works; identifies genre conventions;   │
│                 │ assesses audience expectations and satisfactions             │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ RHETORICIAN     │ Analyzes argument structure, persuasion, theme articulation; │
│                 │ evaluates dialogue craft, linguistic patterns               │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ PRODUCER        │ Assesses practical feasibility; identifies budget/casting    │
│                 │ implications; evaluates market positioning                   │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ ACADEMIC        │ Applies theoretical frameworks rigorously; maintains         │
│                 │ citation discipline; produces scholarship-grade analysis     │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ FIRST-READER    │ Provides emotional response; identifies engagement points    │
│                 │ and failures; reports subjective experience honestly         │
└─────────────────┴───────────────────────────────────────────────────────────────┘
```

### Role Activation

All roles remain active throughout analysis. Role-specific observations are tagged:

```
[AESTHETE]: Observation about form/beauty
[DRAMATURGIST]: Structural intervention
[NARRATOLOGIST]: Mechanism diagnosis
[ART_HIST]: Historical/intertextual note
[CINEPHILE]: Comparable work reference
[RHETORICIAN]: Language/argument analysis
[PRODUCER]: Practical consideration
[ACADEMIC]: Theoretical application
[FIRST-READER]: Emotional/engagement response
```

---

## 1. Ingestion Protocol

### 1.1 Complete Reading Requirement

**CRITICAL**: The entire script must be read and held in working context before any analysis documents are produced.

```
INGESTION_SEQUENCE:

  PHASE 1: INITIAL READ
  ├── Read script completely without annotation
  ├── Note immediate emotional/engagement responses
  └── Capture [FIRST-READER] reactions

  PHASE 2: STRUCTURAL READ  
  ├── Identify act breaks (even if unconventional)
  ├── Mark turning points and structural nodes
  └── Note temporal structure and time span

  PHASE 3: ANALYTICAL READ
  ├── Annotate scene-by-scene
  ├── Tag every beat with function
  └── Map character arcs and transformations

  PHASE 4: SYNTHESIS
  ├── Cross-reference observations
  ├── Identify patterns across readings
  └── Formulate diagnostic assessments
```

### 1.2 Metadata Extraction

Extract and document at ingestion:

| Field | Description |
|-------|-------------|
| **Title** | Script title |
| **Draft** | Version/date if available |
| **Format** | Feature / Pilot / Limited Series / Short |
| **Page Count** | Total pages |
| **Line Count** | Total lines (if available) |
| **Scene Count** | Total number of scenes |
| **Time Span** | Diegetic duration |
| **Primary Genre** | Main genre classification |
| **Tone** | Dominant tonal register |
| **Camera Grammar** | If specified (e.g., found footage, surveillance, traditional) |

---

## 2. Deliverable Documents

The complete analysis package consists of **eight core documents** plus **optional supplements**.

### 2.1 Document Overview

```
DELIVERABLE_STRUCTURE:

  ┌─────────────────────────────────────────────────────────────────┐
  │                    CORE DOCUMENTS (8)                           │
  ├─────────────────────────────────────────────────────────────────┤
  │  1. COVERAGE REPORT           Executive summary + recommendation│
  │  2. BEAT MAP                  Exhaustive scene-by-scene mapping │
  │  3. STRUCTURAL ANALYSIS       Act/movement architecture         │
  │  4. CHARACTER ATLAS           All characters + arcs             │
  │  5. THEMATIC ARCHITECTURE     Theme layers + motif tracking     │
  │  6. DIAGNOSTIC REPORT         Structural problems + solutions   │
  │  7. THEORETICAL CORRESPONDENCE Framework mapping                │
  │  8. REVISION ROADMAP          Prioritized action items          │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │                  OPTIONAL SUPPLEMENTS                           │
  ├─────────────────────────────────────────────────────────────────┤
  │  A. PRODUCTION NOTES          Budget/casting/feasibility        │
  │  B. COMPARATIVE ANALYSIS      Genre comps and influences        │
  │  C. DIALOGUE ANALYSIS         Language patterns and voice       │
  │  D. VISUAL GRAMMAR            Camera/staging/spectacle          │
  │  E. MARKET POSITIONING        Audience + commercial assessment  │
  └─────────────────────────────────────────────────────────────────┘
```

---

## 3. Document Templates

### 3.1 COVERAGE REPORT

```markdown
# [TITLE] — Coverage Report

**Draft:** [version/date]
**Analyst:** Claude (script-analysis-dramaturgical)
**Date:** [analysis date]

---

## Logline

[1-2 sentence distillation of central dramatic premise]

## Synopsis

[300-500 word plot summary covering all major beats]

## Assessment Matrix

| Category | Rating | Notes |
|----------|--------|-------|
| Concept/Premise | ○○○○○ | |
| Structure | ○○○○○ | |
| Character | ○○○○○ | |
| Dialogue | ○○○○○ | |
| Theme | ○○○○○ | |
| Market Potential | ○○○○○ | |

Rating key: ●●●●● (5) = Exceptional | ●●●●○ (4) = Strong | ●●●○○ (3) = Competent | ●●○○○ (2) = Needs Work | ●○○○○ (1) = Significant Issues

## Recommendation

[ ] RECOMMEND — Ready for production consideration
[ ] CONSIDER — Strong elements, development needed
[ ] PASS — Fundamental issues

## Executive Summary

[2-3 paragraphs synthesizing strengths and concerns]

## Strengths

1. [Specific strength with textual evidence]
2. [Specific strength with textual evidence]
3. [Specific strength with textual evidence]

## Areas for Development

1. [Specific concern with textual evidence and suggested approach]
2. [Specific concern with textual evidence and suggested approach]
3. [Specific concern with textual evidence and suggested approach]

## Comparable Works

- [Title (Year)] — [specific point of comparison]
- [Title (Year)] — [specific point of comparison]
- [Title (Year)] — [specific point of comparison]

---

*Coverage prepared by dramaturgical analysis protocol v1.0*
```

---

### 3.2 BEAT MAP

The beat map is the **exhaustive** document. Every scene receives an entry.

```markdown
# [TITLE] — Complete Beat Map

**Total Scenes:** [N]
**Total Beats:** [N]
**Line/Page Coverage:** [first] to [last]

---

## Beat Map Key

| Field | Description |
|-------|-------------|
| **#** | Beat number (sequential) |
| **Lines/Pages** | Script location |
| **Setting** | Location + time |
| **Characters** | Present in scene |
| **Action** | What happens (objective) |
| **Function** | Structural purpose |
| **Tension** | Intensity level (1-10) |
| **Connector** | Causal relationship to prior beat |

### Connector Key
- **BUT** — Reversal/complication from prior beat
- **THEREFORE** — Consequence of prior beat
- **MEANWHILE** — Parallel action (use sparingly)
- **AND THEN** — Weak/episodic connection (flag for revision)

---

## Beat Map

### ACT [N] — [Act Title]

| # | Lines/Pages | Setting | Characters | Action | Function | Tension | Connector |
|---|-------------|---------|------------|--------|----------|---------|-----------|
| 1 | 1-15 | [location] | [chars] | [what happens] | [why it matters] | 3 | — |
| 2 | 16-42 | [location] | [chars] | [what happens] | [why it matters] | 4 | BUT |
| ... | ... | ... | ... | ... | ... | ... | ... |

### Tension Graph

```
TENSION
   10 │                                    ▓▓▓
      │                               ▓▓▓▓▓   ▓
    8 │                          ▓▓▓▓▓       ▓
      │                     ▓▓▓▓▓             ▓
    6 │                ▓▓▓▓▓                   ▓
      │           ▓▓▓▓▓                         ▓
    4 │      ▓▓▓▓▓                               ▓
      │  ▓▓▓▓                                     ▓
    2 │▓▓                                          ▓
      └────────────────────────────────────────────────►
        ACT I        ACT II              ACT III    BEATS
```

---

## Beat Statistics

| Metric | Value |
|--------|-------|
| Total beats | [N] |
| Average tension | [N.N] |
| BUT connectors | [N] ([%]) |
| THEREFORE connectors | [N] ([%]) |
| MEANWHILE connectors | [N] ([%]) |
| AND THEN connectors | [N] ([%]) — **Flag if >10%** |

---

*Beat map generated with complete coverage*
```

---

### 3.3 STRUCTURAL ANALYSIS

```markdown
# [TITLE] — Structural Analysis

---

## I. Macro-Structure Overview

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                           [TITLE] — STRUCTURAL OVERVIEW                        │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│   [ACT/MOVEMENT 1]      [ACT/MOVEMENT 2]      [ACT/MOVEMENT 3]      [ETC]     │
│   [Subtitle]            [Subtitle]            [Subtitle]                       │
│                                                                                │
│   Lines X-Y             Lines Y-Z             Lines Z-W                        │
│   N lines               N lines               N lines                          │
│   ~N%                   ~N%                   ~N%                              │
│                                                                                │
│   Key Image:            Key Image:            Key Image:                       │
│   [description]         [description]         [description]                    │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

## II. Structural Model

Identify which structural model(s) apply:

| Model | Fit | Notes |
|-------|-----|-------|
| Classical Three-Act | ○○○○○ | |
| Five-Act (Shakespearean) | ○○○○○ | |
| Episodic/Picaresque | ○○○○○ | |
| European Art Cinema | ○○○○○ | |
| Circular/Cyclical | ○○○○○ | |
| Parallel/Braided | ○○○○○ | |
| Reverse Chronology | ○○○○○ | |
| Other: [specify] | ○○○○○ | |

## III. Dramatic Spine

```
THESIS STATEMENT:
[If articulated explicitly in script, quote with line reference]

CONTROLLING IDEA:
[1-2 sentence distillation of the script's core argument/meaning]

CENTRAL DRAMATIC QUESTION:
[The question the audience carries through the narrative]

PROTAGONIST:
[Identification + relationship to dramatic question]

ANTAGONIST:
[Identification + relationship to dramatic question]
```

## IV. Movement/Act Breakdown

For each major structural division:

### [Movement/Act N]: [Title]

**Lines:** X-Y  
**Pages:** X-Y  
**Duration:** ~N% of script  

**Opening Image:** [description]

**Closing Image:** [description]

**Function:** [What this section accomplishes structurally]

**Internal Structure:**
```
[ASCII diagram of internal beats/sequences]
```

**Key Turning Points:**
| Beat | Line | Event | Function |
|------|------|-------|----------|
| [name] | [N] | [what happens] | [structural function] |

## V. Turning Points / Structural Nodes

Complete table of all major turning points:

| Node | Line/Page | Event | Structural Function |
|------|-----------|-------|---------------------|
| Hook | | | |
| Inciting Incident | | | |
| Lock-In / Point of No Return | | | |
| First Major Reversal | | | |
| Midpoint | | | |
| Second Major Reversal | | | |
| Dark Night / Crisis | | | |
| Climax | | | |
| Resolution | | | |

## VI. Intensity Mapping

```
    INTENSITY
         ▲
         │                                                    [climax]
         │                                               ▓▓▓▓▓
         │                                          ▓▓▓▓▓     ▓▓▓▓
         │                                     ▓▓▓▓▓              ▓▓▓
         │                                ▓▓▓▓▓                      ▓▓
         │                           ▓▓▓▓▓                             ▓
         │                      ▓▓▓▓▓                                   ▓
         │                 ▓▓▓▓▓                                         ▓
         │            ▓▓▓▓▓                                               ▓
         │       ▓▓▓▓▓                                                     ▓
         │   ▓▓▓▓                                                           ▓
         │▓▓▓                                                                
         ├────────┬─────────────────┬──────────────────┬──────────────────────►
              I          II                III              TIME
         
         [MOVEMENT LABELS]
```

## VII. Proportional Analysis

| Section | Current % | Classical % | Assessment |
|---------|-----------|-------------|------------|
| Setup/Act I | | ~25% | |
| Confrontation/Act II | | ~50% | |
| Resolution/Act III | | ~25% | |

---

*Structural analysis complete*
```

---

### 3.4 CHARACTER ATLAS

```markdown
# [TITLE] — Character Atlas

---

## I. Character Hierarchy

```
CHARACTER_HIERARCHY:

  PROTAGONIST(S)
  └── [Character Name]
        └── [Character Name]

  ANTAGONIST(S)
  └── [Character Name]

  MAJOR SUPPORTING
  ├── [Character Name]
  ├── [Character Name]
  └── [Character Name]

  MINOR SUPPORTING
  ├── [Character Name]
  └── [Character Name]

  FUNCTIONAL / BACKGROUND
  └── [Listed without detail]
```

## II. Character Profiles

### [CHARACTER NAME]

**Role:** Protagonist / Antagonist / Supporting

**First Appearance:** Line/Page [N]

**Scene Count:** [N] scenes

**Arc Type:** 
- [ ] Transformational (internal change)
- [ ] Static (reveals rather than changes)
- [ ] Flat (functional only)

**Opening State:**
[Description of character at script open]

**Closing State:**
[Description of character at script close]

**Want vs. Need:**
- **Want (conscious goal):** [what they pursue]
- **Need (unconscious necessity):** [what they actually need]

**Transformation Summary:**
```
[OPENING STATE] → [CRISIS/CATALYST] → [CLOSING STATE]
```

**Key Scenes:**
| Scene | Line/Page | Function in Arc |
|-------|-----------|-----------------|
| [description] | [N] | [arc function] |

**Relationships:**
| Character | Relationship | Dynamic |
|-----------|--------------|---------|
| [name] | [type] | [how it evolves] |

**Diagnostic Questions:**
1. Does this character have a clearly defined want?
2. Does this character have a clearly defined need (distinct from want)?
3. Does the character make meaningful choices?
4. Does the character change (or meaningfully reveal)?
5. Is the character necessary to the narrative?

---

## III. Ensemble Dynamics

### Relationship Web

```
[ASCII diagram of character relationships]
```

### Power Dynamics Table

| Character | Power Position (Open) | Power Position (Close) | Shift |
|-----------|----------------------|------------------------|-------|
| [name] | High / Mid / Low | High / Mid / Low | ↑ ↓ — |

---

## IV. Character Statistics

| Metric | Value |
|--------|-------|
| Total named characters | [N] |
| Characters with arcs | [N] |
| Characters with dialogue | [N] |
| Female characters | [N] |
| Male characters | [N] |
| Other/unspecified | [N] |
| Protagonist scene presence | [N]% |

---

*Character atlas complete*
```

---

### 3.5 THEMATIC ARCHITECTURE

```markdown
# [TITLE] — Thematic Architecture

---

## I. Thematic Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THEMATIC LAYERS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER 1: [PRIMARY THEME]                                                   │
│  ├── [Evidence point 1]                                                     │
│  ├── [Evidence point 2]                                                     │
│  └── [Evidence point 3]                                                     │
│                                                                             │
│  LAYER 2: [SECONDARY THEME]                                                 │
│  ├── [Evidence point 1]                                                     │
│  ├── [Evidence point 2]                                                     │
│  └── [Evidence point 3]                                                     │
│                                                                             │
│  LAYER 3: [TERTIARY THEME]                                                  │
│  └── [Evidence points]                                                      │
│                                                                             │
│  [Additional layers as warranted]                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## II. Controlling Idea Analysis

**Thesis (as statement):**
[Distilled 1-sentence argument of the script]

**Antithesis (as represented in script):**
[The counter-argument the script engages]

**Synthesis (resolution):**
[How the script resolves the dialectic, if at all]

## III. Motif Tracking

| Motif | First Instance | Recurrences | Function |
|-------|----------------|-------------|----------|
| [visual/verbal motif] | Line [N] | Lines [N, N, N] | [what it does] |

## IV. Symbol Glossary

| Symbol | Meaning(s) | Key Instances |
|--------|-----------|---------------|
| [symbol] | [interpretation] | Lines [N, N] |

## V. Thematic Articulation Points

Moments where theme is articulated directly (dialogue, image, action):

| Line/Page | Type | Content | Assessment |
|-----------|------|---------|------------|
| [N] | Dialogue / Image / Action | [quote or description] | Effective / Heavy-handed / Subtle |

---

*Thematic architecture complete*
```

---

### 3.6 DIAGNOSTIC REPORT

```markdown
# [TITLE] — Diagnostic Report

---

## I. Structural Diagnostics

### Causal Binding Test

Apply the But/Therefore test to major beat transitions:

| Transition | Connector | Assessment |
|------------|-----------|------------|
| Beat 1 → Beat 2 | BUT / THEREFORE / AND THEN | ✓ Strong / ✗ Weak |

**Causal Binding Score:** [N]% of transitions are causally bound

### Narrative Momentum Assessment

| Question | Answer | Evidence |
|----------|--------|----------|
| Can beats be reordered without consequence? | Yes / No | [explanation] |
| Does each scene create new information? | Yes / No | [explanation] |
| Are there redundant scenes? | Yes / No | [list if yes] |

## II. Character Diagnostics

### Protagonist Validation

| Question | Answer |
|----------|--------|
| Is the protagonist the most active agent? | |
| Does the protagonist make choices that drive plot? | |
| Does the protagonist face escalating obstacles? | |
| Is the protagonist's transformation earned? | |

### Antagonist Validation

| Question | Answer |
|----------|--------|
| Does the antagonist provide genuine opposition? | |
| Does the antagonist have comprehensible motivation? | |
| Is the antagonist's pressure continuous? | |

## III. Attention Mechanics Diagnostics

From the Attention Mechanics meta-framework:

| Mechanism | Present | Assessment |
|-----------|---------|------------|
| Involuntary response triggers | Yes / No | [which type: comedy, horror, pathos] |
| Anticipation-satisfaction cycles | Yes / No | [where] |
| Prediction-failure-recalibration (jazz mode) | Yes / No | [where] |
| Causal binding | Strong / Moderate / Weak | |
| Density compensation | Adequate / Inadequate | |

## IV. Identified Issues

### Critical (Structural)

Issues that affect the narrative's fundamental coherence:

1. **[Issue Title]**
   - **Location:** Lines/Pages [N-N]
   - **Description:** [what's wrong]
   - **Impact:** [why it matters]
   - **Suggested Approach:** [how to address]

### Important (Character/Theme)

Issues that affect depth without breaking structure:

1. **[Issue Title]**
   - **Location:** [N-N]
   - **Description:** [what's wrong]
   - **Suggested Approach:** [how to address]

### Polish (Craft)

Line-level or scene-level refinements:

1. **[Issue Title]**
   - **Location:** [N]
   - **Note:** [observation]

## V. Proportional Issues

| Section | Current | Target | Action |
|---------|---------|--------|--------|
| [section] | [N] lines | [N] lines | Expand / Compress |

---

*Diagnostic report complete*
```

---

### 3.7 THEORETICAL CORRESPONDENCE

```markdown
# [TITLE] — Theoretical Correspondence

---

## I. Framework Application

How this script relates to established narrative frameworks:

### Aristotelian Analysis

| Element | Poetics Requirement | Script Implementation | Assessment |
|---------|--------------------|-----------------------|------------|
| Mimesis | Action over character | | |
| Hamartia | Protagonist error | | |
| Peripeteia | Reversal | | |
| Anagnorisis | Recognition | | |
| Catharsis | Purgation | | |
| Unity of Action | Single through-line | | |

### McKee Framework

| Element | McKee Principle | Script Implementation |
|---------|----------------|-----------------------|
| Controlling Idea | Value + Cause | |
| Inciting Incident | Upset of balance | |
| Progressive Complications | Escalating obstacles | |
| Crisis | Dilemma forcing choice | |
| Climax | Irreversible action | |
| Resolution | New equilibrium | |

### South Park But/Therefore

**Causal Chain Diagram:**
```
[EVENT A]
    ↓ THEREFORE
[EVENT B]
    ↓ BUT
[EVENT C]
    ↓ THEREFORE
[...]
```

### Additional Frameworks (as relevant)

- **Phoebe Waller-Bridge (Three Obstacles):** Is each scene operating on multiple obstacle layers?
- **Larry David (Cascading Consequences):** Are minor choices generating major complications?
- **Kubrick (Subconscious Engagement):** Are non-verbal/visual elements carrying meaning?
- **Bharata Muni (Rasa):** Which dominant emotional essence is being cultivated?

## II. Genre Contract

| Genre Element | Contract Expectation | Script Delivery | Assessment |
|---------------|---------------------|-----------------|------------|
| [convention 1] | [what audience expects] | [what script provides] | Met / Subverted / Violated |

---

*Theoretical correspondence complete*
```

---

### 3.8 REVISION ROADMAP

```markdown
# [TITLE] — Revision Roadmap

---

## Priority Matrix

```
                        IMPACT
                   Low         High
              ┌──────────┬──────────┐
         Low  │  IGNORE  │  POLISH  │
    EFFORT    ├──────────┼──────────┤
         High │  DEFER   │ CRITICAL │
              └──────────┴──────────┘
```

## I. Critical Priority (High Impact / Address First)

Structural issues that must be resolved before production consideration:

| # | Issue | Location | Action | Effort |
|---|-------|----------|--------|--------|
| 1 | [issue] | [lines] | [specific action] | [estimated scope] |

## II. Important Priority (High Impact / Second Pass)

Character and theme issues that deepen the work:

| # | Issue | Location | Action |
|---|-------|----------|--------|
| 1 | [issue] | [lines] | [specific action] |

## III. Polish Priority (Refinement)

Line-level and craft improvements:

| # | Issue | Location | Action |
|---|-------|----------|--------|
| 1 | [issue] | [lines] | [specific action] |

## IV. Suggested Revision Sequence

1. **Pass 1 — Structure:** Address critical structural issues
2. **Pass 2 — Character:** Deepen arcs and relationships
3. **Pass 3 — Theme:** Strengthen thematic articulation
4. **Pass 4 — Dialogue:** Polish language and voice
5. **Pass 5 — Format:** Clean formatting, typos, continuity

## V. Questions for the Artist

Issues requiring creative decision rather than technical fix:

1. [Question about intention or direction]
2. [Question about interpretation]
3. [Question about scope]

---

*Revision roadmap complete*
```

---

## 4. Workflow Execution

### 4.1 Standard Workflow

```
ANALYSIS_WORKFLOW:

  STEP 1: INGESTION
  ├── Read complete script (no partial analysis)
  ├── Extract metadata
  └── Record first-reader responses
  
  STEP 2: BEAT MAPPING
  ├── Scene-by-scene annotation
  ├── Assign structural functions
  └── Apply causal binding connectors
  
  STEP 3: STRUCTURAL ANALYSIS
  ├── Identify act/movement breaks
  ├── Map turning points
  └── Generate structural diagrams
  
  STEP 4: CHARACTER ATLAS
  ├── Profile all named characters
  ├── Map relationships
  └── Track arcs
  
  STEP 5: THEMATIC ARCHITECTURE
  ├── Identify theme layers
  ├── Track motifs
  └── Note articulation points
  
  STEP 6: DIAGNOSTICS
  ├── Apply structural tests
  ├── Identify issues
  └── Categorize by severity
  
  STEP 7: THEORETICAL CORRESPONDENCE
  ├── Apply relevant frameworks
  └── Assess genre contract
  
  STEP 8: REVISION ROADMAP
  ├── Prioritize issues
  └── Sequence actions
  
  STEP 9: COVERAGE REPORT
  └── Synthesize into executive document
```

### 4.2 Delivery Options

Offer artist choice of delivery:

| Option | Contents |
|--------|----------|
| **Full Package** | All 8 core documents |
| **Executive** | Coverage Report + Revision Roadmap only |
| **Structural Focus** | Beat Map + Structural Analysis + Diagnostics |
| **Character Focus** | Character Atlas + relevant diagnostics |
| **Custom** | Artist-specified selection |

---

## 5. Quality Standards

### 5.1 Completeness Checklist

Before delivery, verify:

- [ ] Every scene/beat is mapped (no gaps)
- [ ] All named characters are profiled
- [ ] All turning points are identified
- [ ] Diagnostic questions are answered with evidence
- [ ] Issues include specific line/page references
- [ ] Revision items include actionable suggestions
- [ ] ASCII diagrams render correctly

### 5.2 Role-Tag Coverage

Ensure all analyst roles have contributed observations:

- [ ] [AESTHETE] — At least 3 observations
- [ ] [DRAMATURGIST] — At least 5 observations
- [ ] [NARRATOLOGIST] — Framework application complete
- [ ] [ART_HIST] — Historical context if relevant
- [ ] [CINEPHILE] — At least 3 comparable works
- [ ] [RHETORICIAN] — Dialogue assessment
- [ ] [PRODUCER] — Practical notes if requested
- [ ] [ACADEMIC] — Theoretical rigor maintained
- [ ] [FIRST-READER] — Honest engagement response

### 5.3 Terminology Standards

Use consistent terminology throughout:

| Term | Definition |
|------|------------|
| **Beat** | Smallest unit of dramatic action (single exchange of behavior) |
| **Scene** | Continuous action in single location/time |
| **Sequence** | Group of scenes forming a unit of rising action |
| **Act** | Major structural division |
| **Movement** | Alternative to "act" for non-classical structures |
| **Turning Point** | Moment of irreversible change |
| **Node** | Structural landmark (hook, inciting incident, etc.) |

---

## 6. Integration Notes

### 6.1 Narratological Algorithm Integration

This skill draws on established narratological algorithms:

| Algorithm | Application |
|-----------|-------------|
| McKee | Gap analysis, progressive complications |
| Aristotle | Unity, catharsis, recognition/reversal |
| South Park | But/Therefore causal test |
| Phoebe Waller-Bridge | Three-obstacle layering |
| Larry David | Cascading consequences |
| Attention Mechanics | Engagement diagnosis |

### 6.2 Output Format

All documents should be delivered as markdown files with:
- ASCII diagrams for visual structures
- Tables for data-dense sections
- Code blocks for formulas and tests
- Consistent heading hierarchy

---

## Reference Files

- **[templates/coverage-template.md](templates/coverage-template.md)** — Coverage report template
- **[templates/beat-map-template.md](templates/beat-map-template.md)** — Beat mapping template
- **[templates/structural-template.md](templates/structural-template.md)** — Structural analysis template
- **[templates/character-template.md](templates/character-template.md)** — Character atlas template
- **[templates/diagnostic-template.md](templates/diagnostic-template.md)** — Diagnostic report template

---

*Skill: script-analysis-dramaturgical v1.0*
