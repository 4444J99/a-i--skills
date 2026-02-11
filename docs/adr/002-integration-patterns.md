# ADR-002: Cross-Organ Integration and Dependency Patterns

## Status

Accepted

## Date

2026-02-11

## Context

The organvm system enforces a strict dependency flow: ORGAN-I (Theory) feeds into ORGAN-II (Art), which feeds into ORGAN-III (Commerce). ORGAN-IV (Orchestration) governs all organs. No back-edges are permitted (e.g., ORGAN-III cannot depend on ORGAN-II). `a-i--skills` must define its integration points within this constraint.

## Decision

This repository participates in the cross-organ dependency graph as follows:
- **Upstream dependencies**: Defined in `registry-v2.json` under the `dependencies` field
- **Downstream consumers**: Other repos that list this repo in their dependencies
- **Integration pattern**: Direct Python package imports via pip installable modules
- **Communication**: Asynchronous — repos communicate through versioned releases and registry state, not runtime coupling

The promotion state machine (LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED -> ARCHIVED) governs when this repo's outputs become available to downstream consumers.

## Consequences

### Positive

- No circular dependencies — the dependency graph is a DAG validated by CI
- Loose coupling allows independent development and deployment
- Registry-driven discovery makes integration points explicit

### Negative

- Cross-organ changes require coordinated registry updates
- Promotion gates may slow down rapid iteration during prototyping

## References

- Dependency validation: `validate-dependencies.yml` in [orchestration-start-here](https://github.com/organvm-iv-taxis/orchestration-start-here)
- Organ: ORGAN-IV (Taxis)
- Orchestration system: `docs/implementation/orchestration-system-v2.md`
