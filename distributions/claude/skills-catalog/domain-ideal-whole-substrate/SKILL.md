---
name: domain-ideal-whole-substrate
description: Foundational layer beneath PDE. Governs eight-strata substrate (ontology, lineage, constellation, gap-map, agent-fleet, production-stack, internal-magnet, external-contribution) plus four operators (selfish-altruistic loop, magnetic membrane, portfolio operator, reflexive operator) for any domain a flag pierces — chess, fitness, voodoo, education, design, taxidermy. Pre-instantiates engine reuse via Phase 0 portfolio audit and stretching-rack gap diagnosis.
license: MIT
governance_phases: [frame, shape]
governance_auto_activate: false
organ_affinity: [all]
inputs: [domain-anchor, candidate-flag-pierce]
outputs: [domain-ontology, domain-lineage, domain-constellation, domain-gap-map, domain-agent-fleet, domain-production-stack, domain-attractor, domain-contribution-charter, domain-meta-study, portfolio-reuse-map, holes-fat-report]
side_effects: [creates-files, reads-filesystem]
triggers: [user-asks-about-new-domain, context:flag-pierce, context:portfolio-audit, context:stretching-rack, context:reflexive-study]
complements: [product-domain-engine, modular-synthesis-philosophy, market-gap-analysis, systemic-product-analyst, recursive-systems-architect, project-alchemy-orchestrator]
tier: core
complexity: advanced
time_to_learn: multi-hour
tags:
  - substrate
  - ontology
  - domain-modeling
  - portfolio-audit
  - eight-strata
version: "2.2"
---

# Domain Ideal-Whole Substrate (DIWS)

The substrate beneath every flag-pierce. Where **Product Domain Engine (PDE)** handles the *product* layer (logos / ethos / pathos / kairos), this skill handles the *domain* layer beneath. Every domain — chess, fitness, voodoo, education, design — composes from the same eight strata under the same four operators, with load distribution shifting by domain.

User's foundational question: *"What elements, systems, structures, environments, agents so forth make the ideal whole (be it fitness, chess, or voodoo)?"*

DIWS answers it as substrate, not as workflow.

## What This Is

A **substrate**, not a workflow. PDE is a 5-phase formalization protocol that consumes a domain and produces a product. DIWS is what the domain itself *is* before any product gets built on top of it. PDE pulls from DIWS substrate; DIWS does not pull from PDE.

DIWS does two things PDE cannot:
1. **Cross-portfolio reuse** — Phase 0 audits `~/Workspace/` for existing engines (3-tier taxonomy: domain / meta / consultant) before any new domain instantiates. Engine + skin pattern, not from-scratch every time.
2. **Stretching rack** — Phase 0.5 runs the gap-map operator across N concurrent DIWS instances simultaneously. Surfaces holes (under-developed dimensions) and fat (redundant scaffolding) at portfolio scale, not just per-domain.

You invoke this skill when a flag has been pierced or is about to be — a friend's domain, a research interest, a consulting engagement, a side practice. The goal is to load the substrate ahead of any product-building work so that PDE / synthesis / cross-pollination diagnoses operate over filled scaffolding rather than empty types.

## Invariants

These hold across every flag-pierce, regardless of domain:

1. **Phase 0 portfolio-audit runs BEFORE layer-1 ontology** — never scratch-build what an existing engine can re-skin (rule 41: audit before building)
2. **Phase 0.5 engine-overlap board comes between Phase 0 and layer-1** — visualize candidate engines + gaps before scaffolding (rule 36: seed not specification)
3. **All 8 strata instantiate** — even if a stratum is sparse for the domain (load shifts, layers don't disappear)
4. **All 4 operators fire on every instantiation** — selfish-altruistic + magnetic + portfolio + reflexive (Tenet Protocol — both directions simultaneously)
5. **Layer 4 (gap-map) and Layer 8 (contribution) close as a loop** — heist + contribute round-trip; never steal without giving back
6. **Layer 8 produces dissertation-grade research output** — academic capital is substrate, not garnish
7. **Reflexive Operator produces `domain-meta-study.md` alongside the 8 stratum artifacts** — every build co-arises with a study-of-build
8. **Capital flow is N-channel, not 1-channel** — monetary is one of many; meta-skill capital, audience cross-flow, tool extraction, work-improvement all count

## The 8 Strata

Every domain composes from these. See [`references/8-strata-spec.md`](references/8-strata-spec.md) for full per-stratum spec.

| # | Layer | Question | Output artifact |
|---|---|---|---|
| 1 | **Ontology** | What is the domain made of? | `domain-ontology.md` |
| 2 | **Lineage** | How did it become what it is? | `domain-lineage.md` (3 timeslices × 2 registers) |
| 3 | **Constellation** | Who is doing it well, where do we exist relative? | `domain-constellation.yaml` (75-person file) |
| 4 | **Gap-map** | Where is unexploited terrain? | `domain-gap-map.md` (gaps + heist targets) |
| 5 | **Agent fleet** | Who serves the work when you arrive? | `domain-agent-fleet.yaml` |
| 6 | **Production stack** | What does shipping require? | `domain-production-stack.md` |
| 7 | **Internal magnet** | What flows IN when the flag pierces? | `domain-attractor.md` |
| 8 | **External contribution** | What flows OUT to the community? | `domain-contribution-charter.md` |

Voodoo loads layer 8 heavily (ethical floor, anti-extraction guard). Chess and fitness share a similar load profile. Both shapes validate the schema — generative across radically dissimilar domains rather than overfit to one.

## The 4 Operators

See [`references/4-operators-spec.md`](references/4-operators-spec.md) for full spec. All four fire simultaneously on every flag-pierce.

### 1. Selfish-altruistic loop (single-engagement)

```
Learn-for-self → Quality-of-product → Service-to-friends →
Friends-elevated → Network-effect → Self-elevated → More-learning
```

The selfishness is a feature. It locks the user into being a real practitioner rather than a curator. Without the lock, the system curates dead.

### 2. Magnetic membrane (single-domain, two-way)

```
Flag pierces →
  INTERNAL: magnetize all applicable, transmute through user's lens, alchemize toward ideal
  EXTERNAL: contribute to community
```

Pull-in = refinery. Push-out = gift. Per Tenet Protocol — both directions simultaneously, never one without the other.

### 3. Portfolio Operator (cross-portfolio, two-way) — v2 + v2.1

**Push** (v2): every flag-pierce produces three cross-flows simultaneously:
- meta-skill extraction (writing / voice / community-building)
- domain-pair overlaps (each new domain creates N-1 publishable conversation surfaces)
- tool/audience cross-flow (engines amortize across portfolio nodes)

**Pull** (v2.1): every flag-pierce begins with portfolio-audit — scan `~/Workspace/` for engines / skills / primitives that match candidate-domain shape; only enter layers 1-8 after `portfolio-reuse-map.md` is filled.

### 4. Reflexive Operator (build + study, parallel) — v2.2

Every domain instantiation produces `domain-meta-study.md` alongside the 8 stratum artifacts. Where the other three operators govern *flow*, this one governs *recursion* — the thing and the thing-studied co-arise. Per Tenet Protocol, every build-action triggers its opposing reflection-action simultaneously.

## The Use Protocol

Sequential within a single instantiation; recursive across portfolio lifecycle.

### Phase 0 — Portfolio audit (PULL)

Run [`scripts/audit-portfolio.sh`](scripts/audit-portfolio.sh). Globs `~/Workspace/` for existing engines and classifies them into the 3-tier engine taxonomy (see [`references/engine-taxonomy.md`](references/engine-taxonomy.md)):

- **Domain engines** — re-skinnable within similar domain (a membership 4-level funnel, a visual-flow renderer, a landing-page engine)
- **Meta-engines** — cross-domain pattern (cross-pollination diagnosis, 75-person Constellation, PDE skill, Bridge Content templates, Discord rituals)
- **Consultant engines** — every engagement regardless of domain (knowledge base, application pipeline, plan-mode discipline, IRF/MEMORY/chezmoi protocols, conversation-corpus pipeline)

Output: `portfolio-reuse-map.md` showing which engines re-skin, which need invention, which are skin-only domain-specific work.

### Phase 0.5 — Engine overlap board (THE STRETCHING RACK)

Run [`scripts/portfolio-gap-audit.sh`](scripts/portfolio-gap-audit.sh). Operates across N concurrent DIWS instances simultaneously to surface holes and fat at portfolio scale.

For each axis (the 8 strata + 4 operators), the script reports:
- **Holes** — under-developed in 1+ instances; transplantable from a sibling instance
- **Fat** — over-engineered in 1+ instances; consolidatable into a shared engine
- **N-way overlap** — concept present in ≥2 instances; promotion candidate to meta-engine

Output: `holes-fat-report.md`. Refines portfolio reuse from listing engines to *seeing* them in spatial relation, identifying white-space across the whole portfolio.

### Phase 1-8 — Stratum instantiation

Walk each stratum in order, filling its template from [`assets/`](assets/) into the domain's instantiation directory. Use [`references/8-strata-spec.md`](references/8-strata-spec.md) for canonical questions.

Order is canonical but not strictly serial — strata 1-3 can be parallelized; 4 depends on 3; 5-8 are largely independent once 1-4 are in place.

### Phase 9 — Operators fire (REFLEXIVE)

After stratum artifacts ship:
- Selfish-altruistic loop: confirm the user is in practitioner-mode, not curator-mode (gate)
- Magnetic membrane: confirm both INTERNAL and EXTERNAL outputs exist (no one-way pierces)
- Portfolio Operator: write `portfolio-resonance.md` — 3 cross-flows fired
- Reflexive Operator: write `domain-meta-study.md` alongside the 8 strata

### Phase 10 — Cross-pollination diagnosis (synthesis)

Run [`scripts/portfolio-gap-audit.sh`](scripts/portfolio-gap-audit.sh) with this new instance + sibling instances. Surfaces N-1 cross-pollination opportunities by default. Each becomes a candidate essay, video, or joint-product opportunity.

## Engine + Skin Pattern

```
Engine = portfolio-pull primitive (re-skinnable)
Skin   = domain-specific 8-stratum instantiation
New code = only what neither engine nor skin can express
```

Target ratio: next 5 friend-engagements consume **60–80% engine + 20–40% skin**, not 100% from-scratch. Phase 0 enforces this.

## Layer 4 ↔ Layer 8 Heist + Contribute Loop

Layer 4 names heist targets — homages worth remixing. Layer 8 closes the loop by pushing improvements back upstream to the same competitors. **Heist becomes relationship; relationship becomes co-development.** Never steal without giving back.

Intelligence-gathering is ongoing protocol, not one-shot. Continuous monitoring of gap-map targets means the contribution charter has continuous output.

## Composition with PDE

DIWS sits *beneath* PDE. PDE invocations consume a filled DIWS instance:

```
DIWS Phase 0  →  audit portfolio
DIWS Phase 0.5 →  stretching-rack diagnosis
DIWS Phase 1-8 →  fill 8 strata for domain
DIWS Phase 9  →  fire 4 operators
─────────────────────────────────────────
PDE Phase 1   →  IDENTIFY (consumes DIWS Stratum 5 agent-fleet)
PDE Phase 2   →  MAP (consumes DIWS Strata 1-4)
PDE Phase 3   →  ENCODE (types, schemas, tests)
PDE Phase 4   →  EXPRESS (4 rhetorical modes)
PDE Phase 5   →  DEPLOY
─────────────────────────────────────────
DIWS Phase 10 →  cross-pollination diagnosis (post-PDE)
```

PDE Phase 1 (IDENTIFY) was previously rebuilding the agent census from scratch every time. With DIWS, Stratum 5 (`domain-agent-fleet.yaml`) is the canonical source — PDE consumes it.

## Composition with MSP (Modular Synthesis Philosophy)

See [`references/diws-msp-mapping.md`](references/diws-msp-mapping.md) for the full isomorphism. Briefly:

| MSP primitive | DIWS construct |
|---|---|
| Oscillator | DIWS instance (one per domain) |
| Filter | Mode blender (DIWS substrate → PDE composition matrix) |
| Modulator | The 4 operators (selfish / magnetic / portfolio / reflexive) |
| Mixer | Phase 0.5 stretching rack (combines N DIWS instances) |
| VCA | Capital-flow channel selection |
| Feedback | Phase 10 cross-pollination diagnosis (autopoietic) |

MSP names *how* the patches compose. DIWS names *what* the modules contain.

## Modes

Distinct invocation modes the skill supports:

- **`mode portfolio-pull`** — Phase 0 driver; produces `portfolio-reuse-map.md`
- **`mode portfolio-resonance`** — Phase 0.5 driver; runs stretching rack across N instances
- **`mode reflexive-study`** — produces `domain-meta-study.md` alongside any stratum artifact
- **`mode engine-extract`** — when an instance reveals a generalizable pattern, flag for promotion to meta-engine or consultant-engine (user-authorized)
- **`mode full-instantiation`** — all phases 0 → 10 for a single domain
- **`mode cross-pollination-diagnosis`** — focused Phase 10 run between 2+ existing instances

## Proof Instances

Stress-tested fills under [`proof-instances/`](proof-instances/):

- [`voodoo/`](proof-instances/voodoo/) — outlier validator (loads layer 8 heavily; design-only)

The voodoo outlier proves the schema generates across radically dissimilar domains. Earlier client-derived proof instances were removed from the public repository for privacy; when you run DIWS on your own engagements, keep client-specific instances in a private workspace and fill them from the `assets/*-template.*` files. A typical portfolio pairs a commercial domain (e.g. chess or fitness coaching), a pre-active stub (most fields UNKNOWN, to show how a flag is loaded before first engagement), and an ethically-floored outlier like voodoo.

## Out-of-Scope

- DIWS does NOT build products — that's PDE's job
- DIWS does NOT execute outreach to constellation members — that's the user's call
- DIWS does NOT modify source-repo state when building proof instances — substrate fills live in this skill's directory only
- DIWS does NOT auto-promote engines to higher tiers — the user authorizes promotion via `mode engine-extract`

## Verification (after running on a new flag-pierce)

- [ ] `portfolio-reuse-map.md` exists; ≥3 reuse decisions documented
- [ ] `holes-fat-report.md` exists; ≥1 entry per axis per instance
- [ ] All 8 stratum artifacts exist in the instantiation directory
- [ ] `domain-meta-study.md` exists (Reflexive Operator output)
- [ ] `portfolio-resonance.md` exists; ≥3 cross-flows named
- [ ] Engine taxonomy declared (which tier each consumed engine sits in)
- [ ] Heist + contribute round-trip declared in Layer 4 ↔ 8

## Rules of Engagement

- **Dissertation-grade default:** Layer 8 output is substrate, not garnish
- **Heist + Contribute:** stealing an idea requires an equal or greater upstream gift
- **Engine Taxonomy:** categorize reusables as Domain, Meta, or Consultant tier
- **All 4 operators or none:** Tenet Protocol — partial firing is system failure
- **Read-only on source repos:** when building proof instances from existing client work, never write into source repos

## Cross-references

- Plan: `~/.claude/plans/2026-04-25-domain-ideal-whole-substrate-design.md` (v2.2 spec source)
- Sibling skill: `~/Workspace/a-i--skills/skills/project-management/product-domain-engine/SKILL.md`
- MSP: `~/Workspace/a-i--skills/skills/creative/modular-synthesis-philosophy/SKILL.md`
- Stretching-rack genesis: `~/.claude/plans/okay-so-now-harmonic-kettle.md` (Stream Σ definition)
- Engine taxonomy: [`references/engine-taxonomy.md`](references/engine-taxonomy.md)
- 8 strata: [`references/8-strata-spec.md`](references/8-strata-spec.md)
- 4 operators: [`references/4-operators-spec.md`](references/4-operators-spec.md)
- Portfolio composition: [`references/portfolio-composition-map.md`](references/portfolio-composition-map.md)
- DIWS↔MSP isomorphism: [`references/diws-msp-mapping.md`](references/diws-msp-mapping.md)
