---
name: product-domain-engine
description: Conductor skill that formalizes any domain-tied product through a 5-phase protocol (identify-map-encode-express-deploy) expressed through four rhetorical modes (logos-ethos-pathos-kairos). Orchestrates seven existing skills.
license: MIT
organ_affinity: [all]
triggers: [user-asks-about-product-domain, context:new-product-launch]
complements: [systemic-product-analyst, market-gap-analysis]
---

# Product Domain Engine

The meta-system. Every product tied to a domain is an instance of the same operation: formalize informal knowledge into computable structure, then express that structure through four independent rhetorical channels.

This skill does not invent new patterns. It names a system that was already running across four products (`public-record-data-scrapper`, `styx`, and two client engagements anonymized here as `wellness-practitioner-brand` and `chess-creator-brand`) and was being re-derived every time. Naming it converts re-derivation into composition.

## What This Is

A **conductor**, not a monolith. The PDE sequences seven existing skills through a five-phase protocol, adds the rhetorical-mode framework that none of them carries, and provides the composition matrix that selects which output blends which mode.

You invoke this skill when the work to be done is *building a new product tied to a domain* — chess improvement, public records, behavioral economics, wellness, anything where lived knowledge needs to become computable structure.

## The Five-Phase Formalization Protocol

Every domain receives the same treatment. Phases are sequential within a single pass and recursive across product lifecycle.

### Phase 1 — IDENTIFY: the domain's agents

Who acts in this space? Their roles, incentives, constraints. The agent census is the first ontological move; it forces the domain to reveal itself as a graph of actors rather than a topic.

Drives the *systemic-product-analyst* skill (Lane A). Agents map onto users, opponents, intermediaries, gatekeepers, ledgers.

### Phase 2 — MAP: the domain's structures

Real relationships, hierarchies, flows, constraints. What binds the agents into a system? What can break or limit the system in reality (the constraint-domain pillars)?

Drives *market-gap-analysis* (competitive structure) and *research-synthesis-workflow* (causal structure).

### Phase 3 — ENCODE: structures as computable objects

Not concepts. Not documents. **Types, functions, schemas, tests.** The formalization becomes executable.

Drives *product-requirements-designer*. Output: typed interfaces, algorithm implementations, data schemas, deployable test suites.

This is the gate. A domain that cannot produce computable objects has not been formalized — it has only been described.

### Phase 4 — EXPRESS: through four rhetorical modes

The encoded structure speaks through four independent registers. They are not communication styles; they are independent output classes from the same underlying truth. See `references/rhetorical-modes.md`.

Drives *brand-guidelines* (pathos), *pitch-deck-patterns* (pathos+ethos), *content-distribution* (kairos+pathos).

### Phase 5 — DEPLOY: let density create gravity

The `public-record-data-scrapper` principle: a sufficiently dense, sufficiently real formalization attracts its own audience. The 4,455-word README, the 60+ collection agents, the 2,055 tests — that mass *was* the marketing.

Density is gravitational. Promotion only matters at low mass.

### The autopoietic loop

The protocol is not linear. Phase 5's output (deployment metrics, audience behavior, community questions) feeds back into Phase 1 (which agents matter most? which constraints are real?). The system makes itself.

```
IDENTIFY → MAP → ENCODE → EXPRESS → DEPLOY → OBSERVE
   ↑                                              │
   └──────────────────────────────────────────────┘
        observation refines the formalization
```

The OBSERVE step is implemented through analytics modules (e.g. a product's `analytics.ts`, `growth.ts`). They are the observation instruments, not afterthoughts.

## The Four Rhetorical Modes

Classical rhetoric has four modes. Earlier internal drafts of this engine carried only three — the omitted fourth, **kairos**, is the most strategic, and we restore it here. See `references/rhetorical-modes.md` for the full treatment.

| Mode | Greek | Internal/External | Question it answers | Generation method |
|------|-------|------------------|---------------------|-------------------|
| Logos | λόγος | Internal | What is structurally true? | Engineering — types, proofs, algorithms |
| Ethos | ἦθος | External | Why should this be trusted? | Academic density — research, tests, citations |
| Pathos | πάθος | External | Why does this matter to a human? | Social/media content — community, voice, narrative |
| Kairos | καιρός | Strategic | When is the right moment? | Market-timing analysis, zeitgeist alignment |

**Logos is never customer-facing on its own.** It always expresses through ethos (the audience sees that proofs *exist* and trusts the source) or pathos (the audience feels the formalization through narrative). The customer never consumes types directly; they consume credibility or feeling.

**Ethos is built through scholarly density.** Research papers, source lists, test counts, deployment URLs, PROVENANCE files. The depth of the research is the raw material that ethos is forged from.

**Pathos is built through social/media volume.** YouTube, Discord, email sequences, landing pages, brand voice, naming systems, physical objects. The authenticity and volume of the media is the raw material.

**Kairos is built through market-timing observation.** When is the wave arriving, peaking, fading? Each domain rides a zeitgeist; kairos is the choice of when to enter and when to hold.

## The Composition Matrix

Every product output is a specific blend of the four modes. The blend ratio determines what the output *is*. See `references/composition-matrix.md` for the full table; the abridged version:

| Output | Logos | Ethos | Pathos | Kairos |
|--------|:-----:|:-----:|:------:|:------:|
| Technical spec | ■■■ | — | — | — |
| Test suite | ■■■ | ■■ ext | — | — |
| Academic study | ■■■ | ■■■ ext | — | ■ |
| README (flagship) | ■■ | ■■■ ext | — | — |
| Source list | ■■■ | ■■■ ext | — | — |
| Financial model | ■■■ | ■■ ext | — | ■ |
| Pitch deck | ■ | ■■ ext | ■■ ext | ■ |
| Landing page | ■ | ■ | ■■■ ext | ■■ |
| YouTube content | ■ | — | ■■■ ext | ■■ |
| Community (Discord) | — | — | ■■■ ext | ■ |
| Physical product | — | — | ■■■ ext | ■ |
| Email sequence | — | — | ■■ ext | ■■ |
| Launch announcement | — | — | ■■ ext | ■■■ |
| Roadmap | ■ | ■ | — | ■■■ |

`ext` = the mode's *external function* (what the audience consumes), distinct from its internal mass.

## The Prompt Sequence

Universal build commands, ordered per domain stage. See `references/prompt-sequence.md` for the full sequence with example invocations. Five tiers:

1. **Foundation** — what is this domain? (`$MODE`, `$DEPTH`, Natural Center, constraint-domain pillars)
2. **Research** — scholarly study (`$RESEARCH_ATLAS_V3`, peer-reviewed sources, methodological pillars)
3. **Architecture** — how does it become a system? (`$REPO_ARCHITECTURE_CME_FULL`, brand embedding structure, algorithms)
4. **Product Expression** — logos→ethos→pathos outputs (one-pager, landing page, pitch deck, experiment design pack)
5. **Deployment & Scaling** — service scaffolds, multi-tenant SaaS, orchestration

**Order varies by stage:**

| Stage | Sequence |
|-------|----------|
| New domain (e.g. chess-creator-brand at session start) | 1 → 2 (light) → 3 → 4 → 5 |
| Theory-heavy (e.g. styx) | 1 → 2 (deep) → 3 → 4 → 5 |
| Already-deployed (e.g. public-record-data-scrapper) | 3 → 4 → 5 (1 and 2 already done) |
| Client-driven (e.g. wellness-practitioner-brand) | 1 → 4 → 3 → 5 (pathos first, architecture follows brand) |

## Organ Chain Traversal

Every domain selects which ORGANVM organs it must cross. Not every domain crosses all seven.

| Organ | Function | Logos role | Output kind |
|-------|----------|-----------|-------------|
| I — Theoria | Formalize the domain's truth | types, proofs, research | research papers, theory documents |
| II — Poiesis | Express it aesthetically | brand, visual identity | brand voice, visual system, narrative |
| III — Ergon | Derive revenue | products, pricing, funnel | landing page, course, SaaS |
| IV — Taxis | Orchestrate operations | CI/CD, automation | workflows, governance |
| V — Logos (organ) | Publish discourse | essays, case studies | flagship README, blog, dissertation |
| VI — Koinonia | Build community | Discord, cohorts | community space, events |
| VII — Kerygma | Distribute announcements | social, newsletter | POSSE syndication |

**Traversal patterns observed in proof instances:**

- `public-record-data-scrapper`: I → III → IV → V (no II, VI, VII — density alone sufficed)
- `styx-behavioral-economics-theory`: I → II → III (full theoretical→artistic→commercial chain)
- `wellness-practitioner-brand`: I (light) → II → III (the practitioner's brand and architecture)
- `chess-creator-brand`: I (light) → II → III → VI → VII (theory-light, heavy on art + community + distribution)

The PDE scores each domain's needed organs at Phase 1 and re-evaluates at Phase 5.

## The Cross-Domain Fertilization Registry

Patterns proven in one domain become available to all others. See `references/cross-fertilization.md` (registry living alongside this skill) for the full list. Examples:

- chess-creator-brand's **Ki-Shō-Ten-Ketsu narrative framework** → applicable to how styx presents its thesis (setup → development → twist → resolution)
- styx's **theorem-proving methodology** → applicable to how chess-creator-brand validates its title-scoring formula
- public-record-data-scrapper's **density principle** → applicable to all domains
- wellness-practitioner-brand's **hub-and-spoke topology** (several domains from one practitioner) → applicable to chess-creator-brand's future multi-domain architecture (separate community, course, and content sites)

When a pattern is proven in a new domain, register it. Subsequent domains inherit.

## How To Invoke

The PDE is not a single command. It is an *orchestration* — a sequence of skill invocations selected by the domain's stage and pattern. The high-level flow:

```
1. INTAKE
   - Run scripts/domain-audit.sh on the existing repo (if any).
     Output: scores per mode, dominant mode, composition gaps.
   - If no repo yet, run the agent census and structural map directly.

2. SELECT TIER ORDER
   - Based on stage (new / theory-heavy / deployed / client-driven), select sequence.

3. COMPOSE
   - For each tier in order, invoke the relevant orchestrated skill:
     - Tier 1 (foundation):    systemic-product-analyst (Lane A)
     - Tier 2 (research):      research-synthesis-workflow + market-gap-analysis
     - Tier 3 (architecture):  product-requirements-designer
     - Tier 4 (expression):    brand-guidelines + pitch-deck-patterns
     - Tier 5 (distribution):  content-distribution

4. SCORE & GAP-CLOSE
   - Re-run domain-audit.sh after each major output.
   - Identify mode imbalance: under-developed mode → next pass focuses there.

5. OBSERVE
   - Wire analytics for the deployed surface.
   - Feed metrics back into Phase 1 (refined agent map, refined constraint pillars).
```

## Existing Skills the PDE Composes With

The PDE references these by name and adds only what they do not cover. **Do not duplicate their content.**

| Skill | Composed at | Adds to PDE |
|-------|-------------|-------------|
| `systemic-product-analyst` | Tier 1 | Lane A/B audit — is the formalization real? does the world want it? |
| `market-gap-analysis` | Tier 2 | Competitive structure — what exists, what is missing, where to position |
| `research-synthesis-workflow` | Tier 2 | Scholarly depth — canonical papers, source evaluation, atlas |
| `product-requirements-designer` | Tier 3 | Spec — PRD, user stories, feature map |
| `brand-guidelines` | Tier 4 | Brand embedding — voice, naming, visual system, narrative |
| `pitch-deck-patterns` | Tier 4 | Pitch — 10–12 slide narrative |
| `content-distribution` | Tier 5 | Distribution — platform selection, POSSE, syndication |
| `project-alchemy-orchestrator` | All tiers | Lifecycle staging — Nigredo / Albedo / Rubedo |

What the PDE adds (and these skills do not carry):

1. **The four rhetorical modes** — logos, ethos, pathos, **kairos** — as a coordinate system over outputs
2. **The five-phase formalization protocol** — identify → map → encode → express → deploy
3. **The composition matrix** — which outputs blend which modes, with internal/external function distinction
4. **The ordered prompt sequence** keyed to domain stage
5. **The autopoietic observation loop** — deployment feeds back into formalization
6. **The organ-chain traversal** scoring — which organs each domain needs
7. **The cross-fertilization registry** — patterns proven once propagate to all

## Proof Instances

Four products that already ran the engine, before it was named. See `references/proof-instances.md` for full case data.

| Instance | Logos | Ethos | Pathos | Kairos | Dominant | What it proved |
|----------|:-----:|:-----:|:------:|:------:|:--------:|----------------|
| public-record-data-scrapper | ■■■ | ■■■ | ■ | ■ | logos+ethos | Density creates gravity |
| styx-behavioral-economics-theory | ■■■ | ■■ | ■ | ■■ | logos | Theory→Art→Commerce is real |
| wellness-practitioner-brand | ■■ | ■ | ■■ | ■ | balanced | One practitioner → multi-domain topology |
| chess-creator-brand | ■■ | ■ | ■■■ | ■■ | pathos | Full PDE in one session is feasible |

Each instance leads with a different rhetorical mode. The engine does not prescribe which mode dominates — the domain's nature determines it. B2B utility leads with logos. Entertainment brand leads with pathos. Academic product leads with ethos. Time-sensitive product leads with kairos.

The engine ensures **all four modes are addressed**, regardless of which leads.

## Materia-Collider Graduation

`chess-creator-brand` was dissolved into materia-collider during ORGAN-RESET, then graduated back to a formalized client repo in a single session. The PDE defines graduation criteria:

A domain graduates from materia-collider (incubation) to organ-residence (formalization) when:

1. At least one **computable object** exists (types, functions, tests).
2. At least one **rhetorical output** exists (a flagship README, a landing page, a pitch).
3. A **`seed.yaml`** declares organ membership and edges.
4. A **Natural Center** can be stated in one sentence.

Below this gate: still materia. At or above: organ-resident.

## Revenue Model Typology (Mode-Tagged)

Selecting a revenue model is a Phase 4 expression decision. Each model carries a default mode signature; pick the model that matches the domain's dominant mode.

| Revenue Type | Logos / Ethos / Pathos / Kairos | Domain fit |
|-------------|:---:|:---:|:---:|:---:|---|
| Freemium content (YouTube, blog) | ■ | ■ | ■■■ | ■■ | Entertainment, education |
| Subscription community ($9–99/mo) | — | ■ | ■■■ | ■ | Domains with recurring engagement |
| One-time digital product ($29–297) | ■■ | ■■ | ■ | ■ | Domains with teachable knowledge |
| Cohort program ($149+) | ■■ | ■■ | ■■ | ■■ | Measurable improvement domains |
| SaaS subscription | ■■■ | ■■ | — | — | B2B, data, tools |
| Physical product ($49–499) | — | — | ■■■ | ■ | Strong-brand domains |
| Service (coaching, consulting) | ■■ | ■■■ | ■ | — | Experiential-authority domains |
| Sponsorship / affiliate | — | ■ | ■■ | ■■ | Audience-scale domains |

## Voice / Tone Constraints

The PDE expresses in **system-building voice**. When generating PDE-derived artifacts:

- **Classify before describing.** Every entity is named within a taxonomy.
- **Define before acting.** No motion before the schema is specified.
- **Layer recursively.** Phases nest; modes coordinate; instances inherit.
- **Distinguish before merging.** Modes stay independent; outputs blend them by ratio, not by erasure.
- **Resist flattening.** Symbolic vocabulary is allowed when anchored to structure (logos, ethos, pathos, kairos are not ornament).

Avoid:

- Generic smoothness, marketing tone, enthusiasm-as-architecture.
- Mythic inflation without structural payload.
- Emotional reassurance replacing specification.

## Files

```
product-domain-engine/
├── SKILL.md                       # this file — the conductor
├── scripts/
│   └── domain-audit.sh            # repo → mode-score audit (bash, executable)
├── references/
│   ├── rhetorical-modes.md        # full treatment of logos / ethos / pathos / kairos
│   ├── composition-matrix.md      # output × mode blend table with internal/external function
│   ├── prompt-sequence.md         # universal build commands ordered by tier
│   └── proof-instances.md         # public-record / styx / two anonymized client cases
└── assets/
    └── domain-template/
        └── seed.yaml              # ORGANVM contract template for a new domain
```

## When To Skip This Skill

- The work is **not** tied to a domain (e.g. pure infrastructure, dotfiles, tooling).
- The domain is already deployed and stable; no new product expression is needed.
- The user is asking for a single output (a README, a landing page) without the full domain context — invoke the relevant single skill directly instead.

The PDE is for *systemic product creation*. Smaller jobs use smaller skills.
