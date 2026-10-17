# Integration Map — phase → canonical surface

This skill is a thin orchestrator. Every workflow phase maps to a surface that already ships in the ORGANVM substrate. If you find yourself authoring net-new logic, stop — the substrate likely already has it.

## Surface inventory

| Surface | Invocation | Authority |
|---|---|---|
| Ecosystem inventory | `organvm ecosystem --workspace <path>... audit` | Authoritative repo inventory scoped to the eight-organ registry |
| Ecosystem listing | `organvm ecosystem --workspace <path>... list` | Plain list of products with/without ecosystem profiles |
| Prioritized actions | `organvm ecosystem --workspace <path>... actions [--json]` | Canonical next-action prioritization |
| Lifecycle stage | `organvm ecosystem --workspace <path>... lifecycle <repo> [--json]` | Current lifecycle stage for one repo |
| Staleness report | `organvm ecosystem --workspace <path>... staleness` | Pillar DNA staleness |
| Coverage matrix | `organvm ecosystem --workspace <path>... coverage` | Product × pillar coverage |
| IRF query | `organvm irf list [--priority --domain --status --owner --json]` | Index Rerum Faciendarum — universal work registry |
| IRF item detail | `organvm irf status <id>` | All fields for one IRF row |
| IRF summary | `organvm irf stats` | Counts by status/priority/domain |
| Governance state machine | `promotion-readiness-checklist` skill | Authoritative state definitions + evidence requirements |
| Onboarding (LOCAL → CANDIDATE) | `repo-onboarding-flow` skill | Scaffold seed.yaml, README, CI, remote, etc. |
| Repo standards (READMEs, layout) | `github-repository-standards` skill | "Minimal Root" + "World-Class README" |
| Post-migration verification | `qa-audit` skill | Claim-vs-disk verification; stops at verification |

## Phase → surface mapping

### Phase 1 — Discovery
- **Registered**: `organvm ecosystem audit` + `organvm ecosystem list`
- **Unregistered**: `scripts/discover_unregistered.sh` (the only net-new helper)

### Phase 2 — Triage
- Prioritization: `organvm ecosystem actions --json`
- IRF cross-reference: `organvm irf list --status open`
- Drift signal: `(in actions) AND (no open IRF row)`

### Phase 3 — State assessment
- Lifecycle peek: `organvm ecosystem lifecycle <repo> --json`
- Evidence rubric: invoke `promotion-readiness-checklist` (do not restate)

### Phase 4 — Migration signal
- Emit: JSON to `autopsy/signals/<timestamp>.json`
- Route LOCAL → CANDIDATE: invoke `repo-onboarding-flow`
- Route higher gates: invoke `promotion-readiness-checklist`
- IRF gap: emit proposal only (mutations require user authorization)

### Phase 5 — Verification
- Invoke `qa-audit` with the signal file as input

## Why this skill exists (and what it is NOT)

The canonical CLIs are the substrate. This skill is the **discovery workflow** that connects them in a single named procedure: autopsy → triage → state → signal → verify. Without this skill, an agent asked for an "auto-autopsy" might invent parallel scripts (as the Gemini-authored first draft of this skill did). With this skill, the right answer routes to the right canonical surface.

If a future contributor proposes adding:
- A Python directory walker → reject, use `organvm ecosystem` + `discover_unregistered.sh`
- A governance-state YAML schema → reject, defer to `promotion-readiness-checklist`
- An IRF query implementation → reject, use `organvm irf`
- A post-migration verification routine → reject, defer to `qa-audit`

The skill's value is **the workflow**, not the implementation. The implementations are already canonical.
