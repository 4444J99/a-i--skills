# DIWS — 8 Strata Specification

Each stratum has: canonical question, output artifact, fill protocol, validation gate, load-distribution note.

## Stratum 1 — Ontology

**Question:** What is the domain made of?

**Output:** `domain-ontology.md`

**Contents:**
- Entities (named things in the domain)
- Relations (how entities connect)
- Primitives (irreducible units of the domain's vocabulary)
- Canonical vocabulary (terminology with definitions; spelling/casing locked)
- Boundary cases (what's *not* this domain even if it looks adjacent)

**Fill protocol:** Use the [`domain-ontology-template.md`](../assets/domain-ontology-template.md). Start from existing canonical sources (textbooks, primary sources, peer-reviewed reviews). Build the entity-relation graph as text first; promote to YAML only if a downstream tool needs it.

**Validation gate:** A fresh agent reading `domain-ontology.md` alone can answer "what is X in this domain?" for any term used in strata 2–8 without external lookups.

**Load distribution:**
- Chess: medium (well-bounded vocabulary)
- Fitness: medium-high (overlapping schools, contested terms)
- Voodoo: high (entity boundaries are religious/ethical, not formal)
- Education: medium-high (pedagogical theory varies by tradition)
- Design: medium (well-defined principles, contested aesthetics)

## Stratum 2 — Lineage

**Question:** How did the domain become what it is?

**Output:** `domain-lineage.md`

**Contents:** 3 timeslices × 2 registers = 6 sections

| Timeslice | Academic register | Industry register |
|-----------|-------------------|-------------------|
| **History** | Foundational scholarship | Foundational practitioners / firms / movements |
| **Current** | Active research programs | Active product / service ecosystem |
| **Futures** | Emerging research directions | Emerging product / service trajectories |

**Fill protocol:** Use [`domain-lineage-template.md`](../assets/domain-lineage-template.md). For each cell: ≥3 named sources/entities, ≥1 unifying paragraph. Cite with stable identifiers (DOI / ISBN / org URL).

**Validation gate:** Each cell has at least 3 named entries; futures cells include explicit "wager language" (predictions with conditions, not platitudes).

**Load distribution:** Generally even across domains. Voodoo's academic register is exceptionally rich (anthropology, religious studies); chess has both heavy academic (theory) and heavy industry (chess.com / Chessable / Lichess).

## Stratum 3 — Constellation

**Question:** Who is doing it well, and where do we exist relative to them?

**Output:** `domain-constellation.yaml` (canonical 75-person file format)

**Contents:** YAML list of 75 named practitioners with:
- `name`, `tier` (top / mid / emerging), `domain_role`
- `surface_url` (primary platform), `audience_size`, `engagement_signal`
- `cross_domain_overlap` — list of other portfolio nodes this person bridges (Portfolio Operator output)
- `heist_target` (boolean) — is this a homage candidate (Layer 4 link)?
- `contribution_target` (boolean) — would they merit upstream contribution (Layer 8 link)?
- `notes` — relationship signal, contact channel, recent work

**Fill protocol:** Use [`domain-constellation-template.yaml`](../assets/domain-constellation-template.yaml). Start from 5–10 obvious anchors; expand by snowball sampling (each person's collaborators/citations). Target full 75. Empty entries placeholder as `# TBD <date>` rather than dropped.

**Validation gate:** ≥75 entries, ≥80% with surface URL, ≥30% with `cross_domain_overlap` populated.

**Load distribution:** This is the heaviest layer for community-driven domains (chess, fitness, education). Voodoo's constellation is smaller globally (≤30 named scholar-practitioners) but proportionally denser per-name.

**Reuse:** Format is canonical across domains (see `assets/domain-constellation-template.yaml`).

## Stratum 4 — Gap-map

**Question:** Where is the unexploited terrain?

**Output:** `domain-gap-map.md`

**Contents:**
- **Underserved segments** (audience × need-state cells with low coverage)
- **Stack gaps** (combinations of stack components no one ships)
- **Heist targets** (homages worth remixing — adjacent domains whose patterns transplant)
- **White-space wagers** (predictions about emerging gaps)

**Fill protocol:** Use [`domain-gap-map-template.md`](../assets/domain-gap-map-template.md). Cross-reference Stratum 3 constellation; gaps reveal themselves as cells nobody occupies. Include `market-gap-analysis` SOP output if available.

**Validation gate:** ≥3 underserved segments named with audience profile + competitor proximity. ≥3 heist targets named with explicit transplant rationale.

**Load distribution:**
- Chess: medium (mature, gaps require finesse — peer-level climbing, anime identity, build-in-public ELO)
- Fitness: high (massive market, many cells)
- Voodoo: low (entry barriers are ethical, not commercial)
- Education: high (institution-vs-creator-economy gap is generative)

**Loop with Stratum 8:** Heist targets here become contribution targets there — round-trip is mandatory.

## Stratum 5 — Agent fleet (the iceberg)

**Question:** Who serves the work when the user shows up to set?

**Output:** `domain-agent-fleet.yaml`

**Contents:** YAML list of practitioner-agents (real or model-augmented) covering:

| Role | Work-class | Default fleet pick |
|---|---|---|
| domain-ontologist | strategic | Claude (architecture) |
| domain-historian | research-volume | Perplexity / Gemini |
| domain-constellator | research-curation | Gemini / OpenCode |
| domain-gap-mapper | adversarial analysis | Claude (market-gap-analysis SOP) |
| domain-production-architect | tactical | Codex |
| domain-capture-engineer | mechanical | OpenCode |
| domain-attractor-builder | refinery | Claude (rules first, implementations derive) |
| domain-contribution-author | publishing | Claude + Gemini drafting |

Plus domain-specific roles (e.g. for chess: opening-book-curator, endgame-tablebase-consultant).

**Fill protocol:** Use [`domain-agent-fleet-template.yaml`](../assets/domain-agent-fleet-template.yaml). Start with the 8 default roles; add domain-specific. For each role: name the agent (or "TBD"), the SOP it consumes, the ASCII bandwidth (low/med/high).

**Validation gate:** All 8 default roles assigned. Domain-specific roles ≥3.

**Load distribution:** Even — every domain needs all 8 default roles.

**Trinity dispatch protocol:** Claude masterminds + merges; Codex / Gemini / OpenCode generate volume; user directs vision.

## Stratum 6 — Production stack

**Question:** What does the work require to ship?

**Output:** `domain-production-stack.md`

**Contents:**
- **Capture pipeline** (input acquisition: cameras, mics, sensors, scraping, ingest)
- **Processing pipeline** (transformation: editing, analysis, modeling, rendering)
- **Distribution pipeline** (output channels: platforms, formats, schedules)
- **Surface map** (where the audience encounters the work — 1st/2nd/3rd party)
- **Tool inventory** (specific software / hardware versioned)

**Fill protocol:** Use [`domain-production-stack-template.md`](../assets/domain-production-stack-template.md). Walk a single artifact end-to-end as the example.

**Validation gate:** A new contributor can ship a unit of work using only what's documented.

**Load distribution:**
- Chess: medium (digital-native, well-tooled)
- Fitness: high (physical capture is heavy)
- Voodoo: high (ethical capture protocols)
- Education: medium (cohort vs course-product distinction matters)

## Stratum 7 — Internal magnet

**Question:** What flows IN when the flag pierces?

**Output:** `domain-attractor.md`

**Contents:**
- **Refinery rules** — what corpus / web / archive / interview material to pull
- **Transmute-through-user-lens protocol** — how raw material becomes user-voice output
- **Alchemize-toward-ideal** — naming the ideal form per Tenet Protocol
- **Anti-extraction guard** — what NOT to magnetize (especially relevant for layered domains like voodoo)

**Fill protocol:** Use [`domain-attractor-template.md`](../assets/domain-attractor-template.md). Name 3+ corpora to pull from with cadence (real-time / batch / one-shot).

**Validation gate:** Refinery has named inputs, named transmutation steps, named outputs.

**Load distribution:** Even.

## Stratum 8 — External contribution

**Question:** What flows OUT to the community?

**Output:** `domain-contribution-charter.md`

**Contents:**
- **Open-source quotient** (% of work made public; rationale for closed pieces)
- **Publishing cadence** (academic / industry / social-research outlets, frequency)
- **Gift declarations** (what's given away unconditionally — methodology, datasets, lessons)
- **Heist-target contribution map** (Layer 4 link: for each heist target, what's pushed back upstream)
- **Dissertation-grade artifact** (mandatory per v2.2 — primary + secondary source synthesis)
- **Anti-extraction stance** (per voodoo case — explicit protections)

**Fill protocol:** Use [`domain-contribution-charter-template.md`](../assets/domain-contribution-charter-template.md). For each heist target named in Stratum 4: declare contribution channel + cadence.

**Validation gate:** ≥1 dissertation-grade artifact in flight or shipped. Heist + contribute round-trip closed for ≥3 targets.

**Load distribution:**
- Chess: medium
- Fitness: medium
- Voodoo: high (this is where ethical floor binds)
- Education: high (academic publication is the ground)

**Why mandatory:** Per rule 42 (knowledge creation imperative): academic output is substrate, not garnish. Per rule 51: the system IS the product.

## Cross-stratum invariants

- **Layer 4 ↔ Layer 8 closes** — heist + contribute round-trip
- **Stratum 3 cross-domain overlap column** is filled from Portfolio Operator push
- **Stratum 5 default roles ARE the trinity dispatch** — Claude / Codex / Gemini / OpenCode mapped to work-class
- **Stratum 7 refinery rules ARE the magnetic membrane operator's INTERNAL leg**
- **Stratum 8 charter rules ARE the magnetic membrane operator's EXTERNAL leg**

## Stratum-by-domain load reference (calibration)

| Layer | Chess | Fitness | Education | Design | Voodoo |
|---|---|---|---|---|---|
| 1 Ontology | M | M-H | M-H | M | H |
| 2 Lineage | M | M | H | M | H |
| 3 Constellation | H | H | H | M | M |
| 4 Gap-map | M | H | H | H | L |
| 5 Agent fleet | M | M | M | M | M |
| 6 Production | M | H | M | M | H |
| 7 Internal magnet | M | M | M | M | M |
| 8 External contribution | M | M | H | M | H |

Use this calibration when running Phase 0.5 (stretching rack) — domains with similar load profiles share more cross-pollination opportunities.
