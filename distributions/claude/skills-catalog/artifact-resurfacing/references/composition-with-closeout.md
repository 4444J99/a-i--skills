# Composition with `closeout`

This skill and [`closeout`](../../closeout/SKILL.md) are paired but distinct. Closeout discovers; this skill polishes. Together they handle the full session-end drift-reconciliation lifecycle.

Read alongside `../SKILL.md` Phase 4 (Codify) and `closeout`'s six-step protocol.

## The division of labor

| Concern | Owner | What it produces |
|---|---|---|
| Inventory session outputs | `closeout` Step 1 | Per-session file/plan/commit counts |
| Classify plans authored this session | `closeout` Step 2 | EXECUTED / IN-PROGRESS / ABANDONED / DELIVERED-RESEARCH labels |
| Walk back atoms touched | `closeout` Step 3 | Atom status updates (if applicable) |
| Verify git state | `closeout` Step 4 | Clean working tree assertion |
| CLAUDE.md autogen freshness | `closeout` Step 4.5 | Autogen-gate exit code |
| Active-handoff update | `closeout` Step 5 | `.conductor/active-handoff.md` update |
| Write CLOSEOUT_SUMMARY.md | `closeout` Step 6 | Session-end summary doc |
| Detect drift between memory + CLAUDE.md + disk | **artifact-resurfacing** Phase 1 | Drift-finding table |
| Classify drift findings | **artifact-resurfacing** Phase 2 | Four-class assignments |
| Emit polish diffs | **artifact-resurfacing** Phase 3 | Proposed Edit diffs |
| Codify lessons (autogen footer, SKILL updates, canonical-path memory) | **artifact-resurfacing** Phase 4 | Update proposals + IRF rows |

Closeout owns *what this session did*. Artifact-resurfacing owns *what this session and prior sessions left drifting*.

## When closeout invokes artifact-resurfacing

Closeout's Step 2 ("walk back through plans") emits a count of orphan candidates. When that count is **≥3**, closeout should suggest invoking `/artifact-resurfacing` to handle the broader drift surface (not just plans — also stale citations, missing artifacts, cross-scope memory).

The threshold of three is calibrated to the cost of invocation: one or two orphans is handled in-line by closeout's classifier; three or more is symptomatic of broader drift and warrants the four-phase protocol.

Proposed addition to `closeout` SKILL.md, at the end of Step 2:

```markdown
If three or more plans classify as orphan-candidates in this step, suggest
invoking `/artifact-resurfacing` after closeout completes. The orphan plans are
likely a surface symptom of broader drift (stale citations, missing referenced
artifacts, cross-scope memory pointing at moved paths) that artifact-resurfacing's
four-phase protocol handles.
```

This addition is a Phase 4 codification proposal of artifact-resurfacing's own genesis session. Adding it requires authorizing an edit to `closeout`'s SKILL.md — a peer-skill modification that should go through conductor review.

## When artifact-resurfacing invokes closeout

Artifact-resurfacing's Phase 2 (Classify) hands every **orphan-plan** finding to closeout's classifier rather than assigning closure labels itself. The handoff is informational:

```
For each plan path with no DONE/IRF marker, request a closeout classification:
  - EXECUTED, IN-PROGRESS, ABANDONED, or DELIVERED-RESEARCH
The conductor confirms; closeout applies the appropriate state transition
(label, move-to-abandoned, etc.).
```

Artifact-resurfacing does NOT:
- Move plans to `~/.claude/plans/abandoned/`
- Annotate plans with DONE-NNN or IRF-XXX-NNN
- Edit plan content to add closure markers

Those are closeout's authorities.

## When both run in the same session

The canonical order:

1. **closeout** Steps 1 through 6 run as written. The session's own outputs are inventoried and classified.
2. **artifact-resurfacing** runs after closeout completes, scoped to whatever drift surface the conductor names. The two skills don't share state — artifact-resurfacing reads the closeout summary doc to pick up any orphan-plan findings, but it doesn't depend on closeout's runtime state.
3. **closeout summary update** — after artifact-resurfacing emits its polish proposals, closeout's summary doc receives an addendum noting which proposed diffs were authorized and applied in-session vs deferred. This addendum is itself a closeout-step-6 edit; if closeout has already produced the summary, the edit is a one-line append.

## Conflict points

| Scenario | Resolution |
|---|---|
| Closeout marks a plan ABANDONED; artifact-resurfacing later finds a path-citation pointing at it | The path-citation is stale; emit a fix that removes the citation, not one that revives the plan |
| Artifact-resurfacing proposes editing CLAUDE.md mid-session; closeout's autogen-gate (Step 4.5) is failing because that exact CLAUDE.md is stale | Refresh the autogen sections first (closeout's gate authority), THEN run artifact-resurfacing on the refreshed file. The autogen footer is the canonical-path source; never propose path corrections that fight a known-stale autogen block |
| Both skills surface the same orphan-plan | Closeout's classification wins. Artifact-resurfacing records the finding in polish-log with closeout's classification, then closes the row |

## Memory parity

Both skills honor `[[feedback-memory-parity]]` (`(local):(remote) = 1:1`). Closeout's CLOSEOUT_SUMMARY.md commits and pushes; artifact-resurfacing's polish-log.md commits and pushes. Neither leaves working state in disk-only form.

A session that runs both skills and pushes neither has violated parity. The session-end check is:

```bash
git status --short  # should be empty after both skills' commits
git log @{u}..      # should be empty after pushes complete
```

## What this skill brings that closeout does not

Closeout is **session-scoped**. It walks back through what THIS session produced.

Artifact-resurfacing is **domain-scoped**. It walks the surface of a named domain (an institution, a repo, a workstream) and finds drift that may have accumulated across many prior sessions. The drift is not attributable to one session; it's the residue of session-boundary information loss.

The two complement: closeout prevents new orphans; artifact-resurfacing reduces accumulated orphans. Run closeout every session; run artifact-resurfacing when a domain is being touched after a long fallow period, after a repo move, or whenever closeout surfaces three or more drift symptoms.

## What closeout brings that this skill does not

Closeout's authority over plan-closure labels and atom-status transitions is canonical. Artifact-resurfacing does not duplicate the closure state machine — it defers.

Similarly, closeout's autogen-gate (Step 4.5) is the canonical check on CLAUDE.md staleness. Artifact-resurfacing's citation audits assume the autogen footer is fresh; if it isn't, closeout's gate fires first and artifact-resurfacing's findings against the same file are unreliable.

## Anti-pattern: absorbing one skill into the other

Both skills can grow toward the other. Resist:

- **Closeout adding domain-scoped drift detection**: closeout would then need to know about workspace `CLAUDE.md` autogen, sibling-scope memory, deep-corpus search. That's artifact-resurfacing's surface.
- **Artifact-resurfacing assigning closure labels**: this skill would then need to know about session windows, atom status, the DONE-NNN ledger. That's closeout's surface.

Composition over absorption. The cost of two skills is two SKILL.md files. The cost of absorbing is one over-broad skill with a leaky abstraction.
