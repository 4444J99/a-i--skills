# DIWS ↔ MSP Mapping

Modular Synthesis Philosophy (MSP) names *how patches compose*. DIWS names *what the modules contain*. This document is the isomorphism that lets a system designer think in either vocabulary and translate.

## Synthesis primitive → DIWS construct

| MSP primitive | DIWS construct | Function in DIWS context |
|---|---|---|
| **Oscillator** (signal generator) | DIWS instance (1 per domain) | Generates the substrate signal — 8 strata + 4 operator outputs |
| **Filter** (signal processor) | Stratum filter (e.g. constellation → top-tier only) OR mode blender (DIWS substrate → PDE composition matrix) | Selects / shapes the signal |
| **Modulator** (control voltage) | The 4 operators (selfish-altruistic / magnetic / portfolio / reflexive) | Modulates the substrate signal across time + scope |
| **Mixer** (combiner) | Phase 0.5 stretching rack ([`scripts/portfolio-gap-audit.sh`](../scripts/portfolio-gap-audit.sh)) | Combines N DIWS instances into a portfolio-scale signal |
| **VCA** (amplitude control) | Capital-flow channel selection (monetary / meta-skill / audience / tool / work-improvement) | Gates which channel carries the signal |
| **Feedback loop** | Phase 10 cross-pollination diagnosis (autopoietic) + Reflexive Operator | Output refines next-cycle input |
| **Envelope** (ADSR shaping over time) | Lifecycle phase (FRAME / SHAPE / BUILD / PROVE / DONE) | Shapes signal intensity over engagement lifecycle |
| **Sequencer** (rhythmic gating) | Domain-specific cadence (publishing / capture / refinery rhythm in Stratum 7-8) | Gates output by time-domain pattern |

## Patching patterns → DIWS phase patterns

| MSP patching pattern | DIWS phase pattern |
|---|---|
| **Series (linear)** | DIWS Phase 0 → 0.5 → 1-8 → 9 → 10 (single instantiation walk) |
| **Parallel (split & merge)** | Multiple DIWS instances run independently, results blended at Phase 0.5 stretching rack |
| **Feedback loop** | Reflexive Operator (build + meta-study co-arise); autopoietic Phase 10 → next-cycle Phase 0 |
| **Cross-modulation** | Cross-pollination between domain pairs (Portfolio Operator push leg cross-flow #2) |
| **Patch-bay** | The full portfolio matrix — every DIWS instance can route to every operator on every other instance |

## Module-type taxonomy mapped

MSP names 4 module types. DIWS uses each:

| MSP module type | DIWS use | Example |
|---|---|---|
| **Oscillators** (signal generators) | Stratum 1-2 outputs (ontology + lineage carry the domain's "signal") | chess ontology generates the chess-signal |
| **Filters** (signal processors) | Stratum 3-4 outputs (constellation + gap-map filter the signal to actionable subset) | gap-map filters chess-signal to "peer-level climbing" niche |
| **Modulators** (control systems) | Operators 1-4 (selfish-altruistic / magnetic / portfolio / reflexive) | Portfolio Operator modulates chess-signal with wellness-signal cross-flow |
| **Utilities** (infrastructure) | Stratum 5-6 + Phase 0/0.5 scripts (agent-fleet + production-stack + portfolio-audit) | trinity-dispatch is utility infrastructure |

## Signal-flow vocabulary at portfolio scale

When designing portfolio-level architecture, prefer the synthesis vocabulary because it makes routing visible:

> "Patch the chess oscillator's gap-map filter through the Portfolio Operator modulator with the wellness oscillator as cross-modulation source. Send to the Phase 0.5 mixer. Feedback the Reflexive Operator output back to the chess oscillator's Stratum 1 input."

This is the same statement as:

> "Run cross-pollination diagnosis between chess and wellness gap-maps; output goes to the stretching rack; Reflexive Operator's meta-study refines the chess ontology for next cycle."

The synthesis vocabulary scales better for higher-order combinations because patch-bay diagrams have well-known visual grammar.

## Why DIWS is *not* MSP

DIWS contains MSP as a routing-vocabulary tool but is not equivalent. MSP is general-purpose; DIWS is domain-specific (about flag-pierces and creative-portfolio life). DIWS's invariants (Tenet Protocol, capital-flow N-channel, layer 4↔8 round-trip) are not in MSP's spec.

The mapping here lets a system designer:
1. Think in DIWS vocabulary when working *inside* a domain
2. Think in MSP vocabulary when working *across* domains
3. Translate between them at any boundary

## Reverse mapping (DIWS → MSP for system-design crossover)

When the user wants to bring a DIWS pattern into a MSP context (e.g. designing a generative music system with creative-portfolio architecture borrowed):

| DIWS pattern | MSP equivalent |
|---|---|
| 8 strata as parallel artifacts | 8-channel polyphonic oscillator stack |
| 4 operators firing simultaneously | 4-modulator parallel matrix |
| Phase 0 portfolio-audit | Patch-state-recall (load saved patch before designing new one) |
| Phase 0.5 stretching rack | Multi-channel mixer with auto-routing |
| Layer 4↔8 round-trip | Feedback loop with delay |
| Tenet Protocol (both directions simultaneously) | Bidirectional patch (input ↔ output simultaneously) |

## Worked example: chess × wellness as a synthesis patch

```
[chess-oscillator: 8-strata signal]
    │
    ├── [filter: gap-map → "peer-level climbing"]
    │     │
    │     └── [modulator: Portfolio Operator, source: wellness-oscillator]
    │           │
    │           └── [mixer: Phase 0.5 stretching rack]
    │                 │
    │                 └── [output: cross-pollination diagnosis]
    │
    └── [feedback: Reflexive Operator → chess Stratum 1 update]
```

In DIWS vocabulary: "Run cross-pollination diagnosis between chess and wellness, with chess's gap-map gated to peer-level climbing only. Reflexive feedback updates chess ontology for next cycle."

Both statements describe the same operation. The synthesis vocabulary makes routing/topology visible; the DIWS vocabulary makes content/semantics visible.

## When to use which vocabulary

| Context | Prefer |
|---|---|
| Single-domain instantiation | DIWS |
| Cross-portfolio architecture diagrams | MSP |
| Operator-level diagnostics | DIWS |
| Visual flow / topology | MSP |
| Capital-flow analysis | DIWS |
| Feedback / autopoietic systems design | MSP |
| Heist + contribute round-trips | DIWS |
| Patch state save/load | MSP |

The two compose; they are not interchangeable.
