---
name: session-governance-audit
description: Parse a session transcript into a structured Session Governance Index — an annotated bibliography of every file modified and commit made, internal-energy accounting (tool uses, estimated tokens), shipped-vs-tasked atom tally, and classification of missing items as Gaps or Vacuums. Triggers on "visibility-schema-substrate-sweep", "session cascade audit", "session governance audit", or any request to summarize what a session actually produced versus what it was asked to produce.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - session-management
  - governance
  - audit
  - hall-monitor
  - traceability
  - vacuum-detection
governance_phases: [prove]
organ_affinity: [all]
inputs:
  - session transcript (JSONL, exported markdown, or live-session recall)
  - the session's originating task list (prompts, IRF rows, or plan document)
outputs:
  - Session Governance Index (structured markdown report)
  - Gap and Vacuum rows ready for IRF filing
side_effects:
  - reads-filesystem
  - creates-files
triggers: [user-asks-for-session-audit, context:visibility-schema-substrate-sweep, context:session-cascade-audit, context:shipped-vs-tasked]
complements: [closeout, qa-audit, cross-agent-handoff, artifact-resurfacing]
---

# Session Governance Audit

Turn a raw session transcript into an accountable record: what was touched, what it cost, what shipped against what was asked, and — most importantly — what is *missing* and which kind of missing it is.

## Why this exists

Sessions produce two failure modes that look identical from the outside: work that was **attempted and incomplete** (a Gap) and work that was **never represented anywhere at all** (a Vacuum). Closeout rituals catch the first; only a deliberate sweep catches the second. This skill is the deliberate sweep — the "hall monitor" pass that compiles evidence rather than trusting the session's own self-report.

## Core doctrine

- **N/A is a vacuum, never a resting state.** Any metric, deliverable, or task that resolves to "N/A / unknown / not done" must become a named item in the output — never silently dropped.
- **Evidence over self-report.** Claims in the transcript ("pushed", "fixed", "done") are hypotheses; verify each against disk/remote before recording it as shipped.
- **The audit is itself an artifact.** The index must be durable (committed or filed), or the audit becomes its own vacuum.

## Workflow

### 1. Establish the tasked set
Collect everything the session was *supposed* to do:
- explicit user prompts (each imperative sentence = one tasked atom)
- plan documents authored or referenced in-session
- IRF rows / registry items the session claimed
- handoff documents the session inherited

Number them `T-01 … T-NN`.

### 2. Compile the annotated bibliography (the shipped set)
Walk the transcript chronologically and record every artifact event:

| ID | Artifact | Event | Evidence | Verified? |
|----|----------|-------|----------|-----------|
| A-01 | `path/to/file` | created / modified / deleted / committed / pushed | commit SHA, tool-use ref, or diff excerpt | disk/remote check result |

Rules:
- One row per artifact per event class (a file edited then committed = two events, one row each is acceptable but collapse when noise outweighs signal).
- **Verify each row**: `git log`/`git show` for commits, `test -f`/content grep for files, remote ref comparison for pushes. Mark unverifiable claims `UNVERIFIED`, not shipped.
- Include non-file artifacts: PRs opened, issues filed, branches created, external messages sent.

### 3. Account for internal energy
Estimate what the session consumed:
- **Tool uses**: count by class (read/search vs write/execute vs network).
- **Tokens**: estimate from transcript size (chars ÷ 4) split into input/output where derivable.
- **Wall-clock**: first-to-last timestamp.
- **Subagents/parallel work**: count and attribute their energy separately.

Energy data contextualizes the tally: a session that burned 400K tokens to ship 1 of 7 tasked atoms reads very differently from one that shipped 6 of 7.

### 4. Tally shipped vs tasked
Cross-join the tasked set against the shipped set:
- `SHIPPED` — tasked atom with verified artifact evidence
- `PARTIAL` — evidence of attempt, incomplete result
- `UNSHIPPED` — no artifact evidence at all
- `UNTASKED-SHIPPED` — artifacts with no originating task (scope additions; flag, don't condemn)

### 5. Classify the missing
For every `PARTIAL` and `UNSHIPPED` atom, classify:
- **Gap** — the item is *represented* somewhere durable (IRF row, plan, TODO, open PR) but unfinished. Remediation: finish or re-route the existing representation.
- **Vacuum** — the item exists *nowhere* durable; if this audit didn't name it, it would vanish. Remediation: file it (IRF row, plan, or registry entry) **as part of this audit**, then record the filed ID.

A vacuum that this audit names but does not file remains a vacuum. The audit is not complete until every vacuum has a durable home.

### 6. Emit the Session Governance Index
Assemble the report:

```markdown
# Session Governance Index — {session-id} ({date})
## 1. Identity        — session id(s), agent, scope, duration
## 2. Bibliography    — the verified artifact table (step 2)
## 3. Energy          — tool-use counts, token estimate, subagent attribution
## 4. Tally           — shipped / partial / unshipped / untasked-shipped counts + per-atom table
## 5. Gaps            — each with its existing durable representation
## 6. Vacuums         — each with the durable home filed during this audit
## 7. Verdict         — one paragraph: did the session do what it said it did?
```

Route the index to the session's governance home (e.g. `docs/evaluation/` or the session archive), commit it, and reference it from the closeout record.

## Anti-patterns

- **Trusting the transcript's own summary.** Sessions over-report completion; always re-verify.
- **Counting prompts instead of imperatives.** One dense prompt can pack ten tasked atoms; decompose before tallying.
- **Filing the index locally only.** An uncommitted audit is unfinished work, not a finished audit.
- **Treating untasked-shipped work as free.** Scope additions consumed energy that tasked atoms didn't get; surface the trade.

## Worked micro-example

> Tasked: "fix the CI matrix and push" (T-01, T-02). Transcript shows an edit to `.github/workflows/ci.yml` (A-01, verified via `git show abc1234`) and a push claim with no remote evidence (A-02, `git branch -r --contains` empty → UNVERIFIED).
> Tally: T-01 SHIPPED, T-02 UNSHIPPED.
> Classification: T-02 is a **Gap** if the push failure is recorded in a handoff doc; a **Vacuum** if nothing durable mentions it — in which case file `IRF-OPS-NNN: push abc1234 to origin` now and record the ID in §6.
