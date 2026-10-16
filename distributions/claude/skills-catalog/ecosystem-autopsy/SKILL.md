---
name: ecosystem-autopsy
description: Orchestrate a full directory-graph autopsy across an ORGANVM workspace, then emit migration signals that unite repositories under canonical governance. Thin wrapper over organvm ecosystem + organvm irf + promotion-readiness-checklist. Triggers on auto-autopsy, map all directories, governance migration, ecosystem discovery, or "send the signal to unite" requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - autopsy
  - ecosystem
  - migration
  - governance
  - discovery
  - signal
tier: core
complements:
  - promotion-readiness-checklist
  - qa-audit
  - repo-onboarding-flow
  - organvm-governance-pack
  - github-repository-standards
triggers:
  - user-asks-for-auto-autopsy
  - user-asks-to-map-all-directories
  - context:ecosystem-discovery
  - context:governance-migration
  - context:directory-mapping
  - context:unite-under-new-governance
governance_phases: [frame, shape]
governance_norm_group: repo-hygiene
organ_affinity: [all]
---

# Ecosystem Autopsy

Open the ecosystem on the table, map every directory, classify every repository, and emit the signals that bring drifting work back under canonical governance.

## Authority boundary (read first)

This skill **orchestrates** the canonical surfaces already shipped in the ORGANVM substrate. It does not re-implement them.

- **Governance state machine** — defined in [`promotion-readiness-checklist`](../../project-management/promotion-readiness-checklist/SKILL.md). Do not restate. Invoke.
- **IRF queries** — exposed via `organvm irf {list,status,stats}`. Do not fabricate a parallel registry.
- **Ecosystem inventory + lifecycle scoring** — exposed via `organvm ecosystem {audit,list,actions,lifecycle,staleness,coverage}`. Do not duplicate.
- **Post-migration verification** — defer to [`qa-audit`](../qa-audit/SKILL.md). Do not execute remediation; stop at the signal.

If an autopsy step appears to require new state-machine definitions, IRF schema, or inventory logic, the substrate already has it. Search before authoring. See `references/integration-map.md` for the surface-by-surface mapping.

## When to use

- "Run an auto-autopsy on the workspace"
- "Map all directories under ~/Code and ~/Workspace"
- "Find every repo that's still LOCAL-only"
- "Send the signal to unite all of these under the new governance"
- "Triage what's drifting before we consolidate"
- After a long period (~30d+) without ecosystem-wide review
- Before a multi-repo consolidation, rename, or org migration

## Workflow

### Phase 1 — Discovery (registered + unregistered)

Run the canonical inventory:

```bash
organvm ecosystem --workspace ~/Workspace --workspace ~/Code audit
organvm ecosystem --workspace ~/Workspace --workspace ~/Code list
```

These cover repositories already known to the eight-organ registry.

For paths **outside** the registry (transient skill caches, `~/Documents`, scratch dirs, ad-hoc clones), supplement with:

```bash
bash scripts/discover_unregistered.sh ~/Workspace ~/Code ~/Documents
```

The helper lists git repos found on disk that are absent from `organvm ecosystem list` output. These are the autopsy's primary finds — directories the canonical inventory doesn't yet know about.

### Phase 2 — Triage (priority + IRF cross-reference)

Get the canonical prioritized next-action list:

```bash
organvm ecosystem --workspace ~/Workspace --workspace ~/Code actions --json
```

For each high-priority repo, cross-reference open IRF items by owner/domain:

```bash
organvm irf list --status open --owner <organ-or-substring> --json
organvm irf list --domain <domain-code> --status open --json
```

A repo is **truly drifting** when it appears in `ecosystem actions` AND has no open IRF row tracking the drift. That gap is the signal worth emitting.

### Phase 3 — State assessment (defer to canonical authority)

For each repo flagged in Phase 2, invoke `promotion-readiness-checklist` to assess current governance state and the evidence required to advance. Do NOT classify states from this skill. The state machine (LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED) and its evidence requirements (seed.yaml schema fields, LICENSE, README, CI, branch protection, etc.) live there.

```bash
organvm ecosystem --workspace ~/Workspace --workspace ~/Code lifecycle <repo>
```

`organvm ecosystem lifecycle` reports the current lifecycle stage as the ecosystem module sees it. Use it to confirm before invoking the checklist skill.

### Phase 4 — Migration signal (emit, do not execute)

For each repo with a confirmed state and a clear next-state target, emit a signal record (JSON, written to `autopsy/signals/<timestamp>.json` in the user-chosen working directory):

```json
{
  "signal_type": "migration",
  "repo": "<repo-name>",
  "current_state": "LOCAL",
  "target_state": "CANDIDATE",
  "evidence_gaps": ["seed.yaml missing", "no LICENSE", "no remote"],
  "invoke": "repo-onboarding-flow",
  "irf_gap": true,
  "emitted_at": "<ISO-8601>"
}
```

Signals route to the right downstream skill:
- LOCAL → CANDIDATE: invoke `repo-onboarding-flow`
- CANDIDATE → PUBLIC_PROCESS or PUBLIC_PROCESS → GRADUATED: invoke `promotion-readiness-checklist`
- IRF gap: emit an IRF-row proposal (do not auto-write — IRF mutations require user authorization per ORGANVM constitutional rules)

This skill **stops at signal emission**. Execution belongs to the downstream skill the signal names.

### Phase 5 — Verification (defer to qa-audit)

After downstream skills execute (in a separate session or under explicit user go), invoke `qa-audit` to verify that the claimed transitions match disk reality. The autopsy's signal file is the verification target.

## What this skill explicitly does NOT do

- Restate or redefine governance states
- Walk directory trees with bespoke Python (use `organvm ecosystem` + `discover_unregistered.sh`)
- Mutate IRF, seed.yaml, or any governance file (signals only)
- Execute git operations (push, branch, remote add) — those belong to `repo-onboarding-flow`
- Verify its own claims — that's `qa-audit`'s job

## Scripts

- `scripts/discover_unregistered.sh` — list git repos on disk that are absent from `organvm ecosystem list`

## References

- `references/integration-map.md` — phase-by-phase mapping to canonical surfaces

## Anti-patterns

- Authoring a `governance-states.md` reference in this skill (the source of truth is `promotion-readiness-checklist`)
- Writing Python that walks directories for inventory (the canonical CLI does this)
- Auto-writing IRF rows (mutations require explicit user authorization)
- Treating signals as commitments (signals are proposals; execution is a separate authorization)
