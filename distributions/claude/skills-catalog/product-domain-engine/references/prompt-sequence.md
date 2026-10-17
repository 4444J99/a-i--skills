# The Prompt Sequence

Universal build commands, ordered by tier. The PDE selects which tier to run, in which order, based on the domain's *stage*. Within a tier, prompts are roughly parallel — they can be run in any order without breaking the formalization.

## Tier 1 — Foundation (what is this domain?)

Goal: state the domain in computable form. Establish what the agents are, what mode the build is in, what depth is required.

```
$MODE = "lean MVP (fast deployment)" | "full-stack system (multi-service, production-grade)"
$DEPTH = "operator-grade" | "dissertation-grade"
Formalize Natural Center as a computable object (not a concept)
Constraint-domain pillars (what can break or limit the system in reality)
```

**What "Natural Center" means:** the single sentence that, if true, makes everything else in the domain derivable. For chess-creator-brand: *"chess improvement at the amateur level is a hero's journey, not a technical curriculum."* For styx: *"loss aversion is a measurable force; the coefficient is 1.955."* For public-record-data-scrapper: *"every state's UCC filings are machine-readable if you build the right collection agent per jurisdiction."* For wellness-practitioner-brand: *"one practitioner's knowledge maps to multiple audience entry points through topology."*

**Output of Tier 1:** a one-sentence Natural Center, an agent census, a constraint-pillar list. This is the seed of everything downstream.

## Tier 2 — Research (scholarly study of the domain)

Goal: produce ethos-grade research depth. The audience will not read the papers, but the papers' *existence* is the credibility signal.

```
$RESEARCH_ATLAS_V3
or a full dissertation-grade atlas with milestones + outputs
exact peer-reviewed source list per pillar (30–80 sources)
Construct the exact reading ladder + source list (peer-reviewed, canonical)
exact canonical papers per pillar
Methodological rigor pillars (how you prove things are true)
$PILLAR_CAUSAL_INFERENCE
$PILLAR_UNIT_ECONOMICS
$PILLAR_ALGORITHMIC_INTERFACE
```

**Depth dial:** if `$DEPTH = operator-grade`, run a *light* pass — top 10 sources per pillar, no full dissertation atlas. If `$DEPTH = dissertation-grade`, run the full atlas with milestones, outputs, and 30–80 sources per pillar.

**Composition with `research-synthesis-workflow` skill:** that skill carries the workflow; the PDE adds the *pillar pattern* (causal inference, unit economics, algorithmic interface, etc.) and the *atlas* concept.

## Tier 3 — Architecture (how does it become a system?)

Goal: convert the formalization into a deployable repository structure.

```
Translate this into a full repository architecture + file tree + environment variables
$REPO_ARCHITECTURE_CME_FULL
build full repo architecture ($ENV variables, services, pipelines)
define brand embedding structure
formalise Natural Center extraction algorithm
Define exact algorithms for clip extraction and scoring
Build the attribution model mathematically
```

**The CME pattern:** Compute / Memory / Edge — every architecture has these three planes. *Compute* = where business logic runs. *Memory* = where state persists. *Edge* = where the audience touches the system (HTTP, WebSocket, CDN, physical retail).

**Composition with `product-requirements-designer`:** that skill produces the PRD; the PDE adds the *brand embedding structure* (how identity threads through architecture) and the *attribution model* (how outcomes link back to inputs).

**Output of Tier 3:** a deployable repo skeleton with file tree, env-var spec, service boundaries, and a typed Natural Center.

## Tier 4 — Product Expression (logos → ethos → pathos outputs)

Goal: produce the audience-facing artifacts. This is where the rhetorical modes become visible.

```
produce a sales one-pager vs technical spec split          [LOGOS + ETHOS]
create a landing page version (conversion-optimized)        [PATHOS + ETHOS]
tighten this into a pitch deck narrative (10–12 slides)     [PATHOS + ETHOS]
$NEXT = "EXPERIMENT DESIGN PACK (ready-to-run tests)"      [LOGOS]
a live research operating system (ROS) spec                 [LOGOS]
full experiment design templates                            [LOGOS]
```

**Composition with `brand-guidelines` and `pitch-deck-patterns` skills:** those carry the craft; the PDE adds the *mode tagging* (which output serves which rhetorical function) and the *blend ratios* (how much logos / ethos / pathos / kairos each output should contain — see `composition-matrix.md`).

**Output of Tier 4:** a one-pager, a landing page, a pitch deck, an experiment design pack, a live ROS spec. Each tagged with its mode signature.

## Tier 5 — Deployment & Scaling

Goal: ship to production, set up the autopoietic loop.

```
$NEXT = "SERVICE-BY-SERVICE CODE SCAFFOLD + FIRST DEPLOYMENT SCRIPTS"
$NEXT_ARTIFACT = "FULL_STACK_IMPLEMENTATION_BLUEPRINT"
expand into a multi-tenant SaaS system with orchestration layer
$PROC_NATURAL_CENTER_BOOTSTRAP
```

**The autopoietic loop:** Tier 5 outputs include the *observation instruments* (analytics modules, telemetry pipelines) that feed deployment metrics back into Tier 1. The system makes itself.

**Composition with `content-distribution`:** distribution is part of Tier 5, not separate. Shipping includes choosing which channels carry which outputs (POSSE pattern, syndication strategy).

## Tier Order By Stage

| Stage | Sequence | Why |
|-------|----------|-----|
| **New domain** (e.g. chess-creator-brand at session start) | 1 → 2 (light) → 3 → 4 → 5 | Standard pipeline; light research, then build |
| **Theory-heavy** (e.g. styx) | 1 → 2 (deep) → 3 → 4 → 5 | Research depth IS the product; invest before architecture |
| **Already-deployed** (e.g. public-record-data-scrapper) | 3 → 4 → 5 | Tiers 1–2 already done; iterate on architecture and expression |
| **Client-driven** (e.g. wellness-practitioner-brand) | 1 → 4 → 3 → 5 | Pathos first (client wants brand); architecture follows brand |
| **Re-launch / pivot** | 1 (refresh) → 4 → 5 | Re-state Natural Center; rebuild expression; re-ship |
| **Materia → graduation** | 1 → 3 → 4 → 5 | Skip research depth on first graduation pass; ship the seed |

**Within-tier parallelism:** the prompts within a single tier are largely parallel. In Tier 4, the one-pager / landing page / pitch deck can all run concurrently — each consumes the same logos input and projects through different modes.

## Selection Heuristics

When the user asks the PDE to start work, ask:

1. **Is there a repo already?** If yes, run `domain-audit.sh` first; the result determines tier-skip choices.
2. **What is `$DEPTH`?** Operator-grade or dissertation-grade? This sets Tier 2's depth.
3. **What is `$MODE`?** Lean MVP or full-stack system? This sets Tier 3's scope and Tier 5's complexity.
4. **What is the dominant audience-mode?** Logos / ethos / pathos / kairos? This determines which Tier 4 output to ship first.

These four questions are the PDE's intake.

## Composition With Existing Skills

| Tier | PDE adds | Composes with skill |
|------|---------|---------------------|
| 1 | $MODE / $DEPTH dials, Natural Center pattern, agent census | systemic-product-analyst (Lane A/B) |
| 2 | $RESEARCH_ATLAS, pillar pattern | research-synthesis-workflow, market-gap-analysis |
| 3 | $REPO_ARCHITECTURE_CME, brand embedding, attribution | product-requirements-designer |
| 4 | mode tagging, composition matrix, blend ratios | brand-guidelines, pitch-deck-patterns |
| 5 | autopoietic loop, observation instruments | content-distribution |

The PDE is the glue. The skills are the craft.

## Examples

### chess-creator-brand (new domain, lean MVP, dissertation-light; anonymized client engagement)

```
Tier 1: $MODE=lean MVP, $DEPTH=operator-grade
        Natural Center: "chess improvement at the amateur level is a hero's journey"
        Agents: improving player, opponent, coach, platform algorithm, community

Tier 2: $RESEARCH_ATLAS (light) — top 15 sources per pillar
        Pillars: skill-acquisition, content-economics, community-building, narrative-structure

Tier 3: $REPO_ARCHITECTURE_CME_FULL → Next.js + Tailwind, multi-section landing page
        Algorithms: title-scoring, narrative-framework, growth-model, analytics

Tier 4: Sales one-pager (client-facing), landing page (audience-facing),
        course catalog (offering), brand voice (rank-ladder identity),
        pitch deck (sponsor narrative)

Tier 5: Vercel deploy, Cloudflare domain, Kit (ConvertKit) integration,
        analytics wired, autopoietic loop on title-performance metrics
```

### styx-behavioral-economics-theory (theory-heavy)

```
Tier 1: $MODE=full-stack, $DEPTH=dissertation-grade
        Natural Center: "loss aversion coefficient = 1.955; peer audit converts that into stakes"

Tier 2: Full dissertation atlas — 80 sources per pillar
        Pillars: prospect theory, mechanism design, peer accountability, blockchain attestation

Tier 3: NestJS backend + Next.js frontend + React Native + Tauri desktop
        Theorem proofs (9), validation gates (8), 499+ tests

Tier 4: Academic paper (theorem-grade), pitch deck (capital-raise),
        landing page (operator-grade)

Tier 5: Multi-platform deployment, smart contract audit, peer-audit network
```

### public-record-data-scrapper (already-deployed)

```
Tier 3: 60+ collection agents, jurisdiction configs, normalization pipeline
Tier 4: Flagship README (4,455 words), live deployment URL, paying subscribers
Tier 5: Subscription billing, GRADUATED status, organic gravity confirmed

(Tiers 1 and 2 ran years ago; the engine continues forward from where it left.)
```

### wellness-practitioner-brand (client-driven; anonymized client engagement)

```
Tier 1: Natural Center: "one practitioner → multi-domain topology via a navigable visual model"
        Agents: practitioner, client, peer, protocol, cycle, measurement

Tier 4 (first): brand voice, naming, visual identity, visual-model renderer
                (because the client wants to *see* it before architecture is locked)

Tier 3: hub-and-spoke architecture, Astro, Tailwind, static hosting,
        visual model driven by a single config file as source of truth

Tier 5: deploy, domain wiring for hub and spokes, product funnel, affiliate flow
```

The order *adapts* to the domain. The engine does not prescribe a fixed pipeline.
