---
name: artifact-resurfacing
description: Four-phase protocol for clearing accumulated drift between memory claims, CLAUDE.md citations, and on-disk reality. Detects stale citations, missing files, and orphan plans; classifies findings; emits proposed diffs; codifies prevention. Companion to closeout (closeout discovers orphans; this skill polishes them). Discovery ≠ remediation — Phase 3 emits proposed diffs only; constitutional doc edits require explicit conductor authorization.
license: MIT
complexity: intermediate
time_to_learn: 30min
tier: core
tags:
  - drift-reconciliation
  - memory-hygiene
  - citation-audit
  - orphan-recovery
  - hall-monitor
  - propose-not-apply
inputs:
  - domain-scope-or-claude-md-path
  - cross-scope-memory-files
  - relevant-claude-plans
outputs:
  - drift-finding-table
  - proposed-edit-diffs
  - polish-log-md
  - irf-row-proposals
side_effects:
  - reads-filesystem
  - creates-files
triggers:
  - user-says-resurface-buried-artifacts
  - user-says-buried-bodies
  - user-says-stale-citations
  - user-says-memory-drift
  - user-says-future-fix
  - closeout-surfaced-three-or-more-orphans
  - claude-md-cited-path-test-f-fails
complements:
  - closeout
  - cross-agent-handoff
  - qa-audit
  - ecosystem-autopsy
governance_phases: [frame, shape]
governance_norm_group: repo-hygiene
organ_affinity: [all]
---

# Artifact Resurfacing

Open the drift on the table. Surface the buried artifacts — stale citations, missing referenced files, orphan plans, cross-scope memory entries pointing at paths that moved. Polish them in proposal form. Codify the lesson so the next session does not have to re-discover the same drift.

## Authority boundary (read first)

This skill is **propose-not-apply** for any constitutional surface. It produces drift tables, edit diffs, and IRF row proposals. It does not commit edits to `CLAUDE.md`, `MEMORY.md`, `governance-rules.json`, `registry-v2.json`, or any `seed.yaml` without explicit conductor authorization in the same session.

- **Closure for plans** — defer to [`closeout`](../closeout/SKILL.md). This skill does not assign DONE-NNN / IRF-XXX-NNN labels; it surfaces orphans for closeout's classifier.
- **Memory operations** — defer to your agent's memory-curation tool (for example, a built-in memory-consolidation skill, where the platform provides one) for memory file mutations. This skill emits proposed memory diffs.
- **Cross-session continuity** — defer to [`cross-agent-handoff`](../cross-agent-handoff/SKILL.md). This skill writes the polish-log entry; handoff carries it forward.
- **Verification of claimed transitions** — defer to [`qa-audit`](../qa-audit/SKILL.md).

Discovery ≠ remediation. The skill *finds* and *proposes*. The conductor *applies*.

## When to use

- "Resurface buried artifacts in <domain>"
- "Find stale citations in this CLAUDE.md"
- "Reconcile memory drift between scopes"
- "Audit this domain for orphans"
- "Polish referenced-but-missing files"
- "Future-fix this so it doesn't drift again"
- Closeout has surfaced ≥3 follow-ups whose root cause is drift between memory and disk
- A `MEMORY.md` walkback flags ≥1 stale path citation
- A `find` for a CLAUDE.md-cited path returns zero results

## Four-phase protocol

### Phase 1 — Detect

Enumerate the domain's surface. For a target `CLAUDE.md` or `MEMORY.md`, extract every:

- File path (absolute or `~/`-anchored)
- Function/script identifier (`foo.py`, `bar()`, `--flag`)
- Issue/ledger ID (`IRF-XXX-NNN`, `DONE-NNN`, `GH#123`)
- External reference (URL, package name, doc anchor)
- Plan filename (any `~/.claude/plans/*.md` referenced by path)

Run the citation audit:

```bash
bash scripts/audit-citations.sh <path-to-CLAUDE.md>
```

The script emits one JSONL record per citation: `{cited, kind, exists, found_at, status}`. A path is **present** if `test -f` (or `test -d`) succeeds. It is **stale** if a different path on disk holds the same canonical content (e.g., the institution moved from `~/Workspace/...` to `~/Code/...`). It is **missing** if no candidate path holds the artifact.

Run the orphan-plan scan:

```bash
bash scripts/find-orphan-plans.sh [glob]
```

Default glob is `~/.claude/plans/*.md`. Output: one JSONL record per plan, with `{path, mtime, has_done_ref, has_irf_ref, has_delivered_research_marker}`. Plans lacking all three markers are orphan candidates.

Surface a four-column finding table to the user before classifying:

| artifact | cited-at | status | candidate-action |
|---|---|---|---|
| ... | ... | present \| stale \| missing \| orphan | (proposed action, no execution yet) |

### Phase 2 — Classify

For each finding, assign one class:

- **Present** — no action.
- **Stale-citation** — the artifact exists on disk; the citation points at the wrong path. Polishable via citation rewrite.
- **Missing-but-probably-never-written** — citation appears to run ahead of an unwritten artifact (e.g., a paper title cited with no draft, no commit history, no cross-scope mention). Polishable via citation annotation (`(planned — not yet written, YYYY-MM-DD)`) rather than reconstruction.
- **Missing-but-lost** — citation points at an artifact whose creation history exists somewhere (a session transcript, an old commit, a cross-scope memory file) but the artifact itself is gone. Polishable via deep search; if search fails, propose reconstruction-from-context or citation removal.
- **Orphan-plan** — pass through to [`closeout`](../closeout/SKILL.md)'s classifier (EXECUTED / IN-PROGRESS / ABANDONED / DELIVERED-RESEARCH). This skill does not assign closure labels.

For ambiguous classifications, surface the finding to the conductor and stop. Universal Rule #21 ("Do what is asked — never preempt") applies.

See `references/buried-bodies-taxonomy.md` for the full taxonomy with worked examples.

### Phase 3 — Polish (propose, do not apply)

For each classified finding, generate a polish artifact. **Never write directly to constitutional files.** Emit diffs and proposals instead.

For **stale citations**, run the proposer:

```bash
python3 scripts/propose-citation-fix.py \
  --file <path-to-CLAUDE.md-or-memory-file> \
  --stale-path <wrong-path> \
  --canonical-path <correct-path>
```

Output: a unified diff to stdout. The conductor reviews and applies (or rejects) the diff via Edit. The script never writes the file itself.

For **missing-probably-never-written**, emit a one-line annotation diff:

```diff
- See ~/path/to/cited-but-missing.md for details.
+ See ~/path/to/cited-but-missing.md for details (planned — not yet written as of YYYY-MM-DD).
```

For **missing-but-lost**, emit the deep-search command set first:

```bash
find /Users/4jp -name "<artifact-name>*" 2>/dev/null | grep -v node_modules
grep -rl "<artifact-keyword>" ~/.claude/projects/*/memory/*.md 2>/dev/null
grep -rl "<artifact-keyword>" ~/Code/organvm/praxis-perpetua/prompt-corpus/ 2>/dev/null
```

If the search returns hits, the finding reclassifies as stale-citation and the citation-fix proposer runs. If the search returns zero hits across the deep corpus, the finding reclassifies as probably-never-written and the annotation diff applies.

For **orphan plans**, hand the plan path to `closeout` with a classification request. Do not move plans to `abandoned/` from this skill — closeout owns that decision.

See `references/constitutional-doc-policy.md` for the full rule set on what may/may not be auto-edited.

### Phase 4 — Codify (future-fix)

Polishing one drift instance is tactical. Codifying so the *next* drift self-corrects is strategic.

For each polished finding, append an entry to a `polish-log.md` in the affected repo's root (create if absent):

```markdown
## YYYY-MM-DD — <one-line summary>

- **Artifact**: <cited-path-or-id>
- **Class**: stale-citation | missing-never-written | missing-lost | orphan-plan
- **Finding**: <what was wrong>
- **Action**: <what was proposed; "applied" or "deferred-to-conductor">
- **Authorization**: <session-id-and-approver, or "pending">
- **Codification**: <what's been added to prevent recurrence, or "none yet">
```

Then check for compound patterns:

- **Same stale citation in ≥2 scopes** — propose updating the workspace `CLAUDE.md` autogen footer (under `<!-- ORGANVM:AUTO:START -->` sentinels) to assert the canonical path. The next `organvm refresh` will re-write it, making the truth periodic rather than ad-hoc.
- **Same orphan-plan class in ≥5 plans** — propose adding a detector clause to `closeout`'s SKILL.md so the class is auto-recognized in future sessions.
- **Cross-scope memory drift** — propose a `reference_<topic>_canonical_path.md` memory at the workspace scope so all sibling scopes can grep-find one truth.

Emit one IRF row proposal per unresolved finding (Universal Rule #1: N/A = vacuum). Format:

```yaml
- id: IRF-<DOMAIN>-<NNN>  # next available
  title: "<artifact>: <class> drift surfaced in session <id>"
  status: open
  domain: <domain-code>
  surfaced_by: artifact-resurfacing
  resurfacing_session: <session-id-or-date>
  action_required: <one line>
  authorization_required_from: conductor
```

The IRF row is a *proposal*. Writing it into `INST-INDEX-RERUM-FACIENDARUM.md` requires conductor authorization (Universal Rule #21).

## What this skill explicitly does NOT do

- Edit `CLAUDE.md`, `MEMORY.md`, `governance-rules.json`, `registry-v2.json`, or any `seed.yaml` without same-session conductor authorization
- Assign DONE-NNN or IRF-XXX-NNN closure labels (that's `closeout`'s job)
- Move plans to `~/.claude/plans/abandoned/` (also `closeout`'s job)
- Auto-reconstruct missing artifacts from context (proposes reconstruction; conductor authorizes)
- Run as a background daemon, cron, or LaunchAgent (Universal Rule #9 — HARD RULE)
- Walk a domain it was not asked to walk (scope visibility principle, memory rule #39)
- Batch-close orphan plans (memory rule #53)

## Scripts

- `scripts/audit-citations.sh` — citation audit; emits `{cited, kind, exists, found_at, status}` JSONL
- `scripts/find-orphan-plans.sh` — orphan-plan scan; emits `{path, mtime, has_done_ref, has_irf_ref, has_delivered_research_marker}` JSONL
- `scripts/propose-citation-fix.py` — propose-only unified diff for stale citation rewrites

## References

- `references/buried-bodies-taxonomy.md` — the four classes with worked examples from this skill's genesis session
- `references/composition-with-closeout.md` — how this skill chains with `/closeout` (closeout discovers; this polishes)
- `references/constitutional-doc-policy.md` — the propose-not-apply rule set

## Examples

- `examples/2026-05-17-praxis-perpetua-resurfacing.md` — the genesis case: praxis-perpetua moved from `~/Workspace/meta-organvm/` to `~/Code/organvm/`, leaving stale citations in pipeline `CLAUDE.md` + memory and three referenced-but-missing 2026-03-15 papers. The session that built this skill *is* the case study.

## Anti-patterns

- Treating Phase 1 detection as license to Phase 3 polish without conductor sign-off
- Editing the pipeline `CLAUDE.md` "Academic & Institutional Context" block in the same session that discovered it was stale (discovery ≠ remediation — surface, do not silently fix)
- Inventing the canonical path when ≥2 candidates exist on disk (ask the conductor which is truth)
- Treating cross-scope memory entries as fungible — each scope has its own `MEMORY.md`, each is independently mutable, all need their own proposed-diff
- Running on a domain the conductor did not name — buried-body hunting is *invited*, not autonomous
- Calling this skill's findings "fixed" when only the propose-diff has been emitted

## Universal rules this skill is built around

- **Universal Rule #1** — N/A is a vacuum. Every unresolved finding becomes an IRF row proposal.
- **Universal Rule #2** — Nothing local only. The skill source pushes to remote; polish-log entries commit.
- **Universal Rule #6** — Fix bases, not outputs. Phase 4's "codify" leg adds the prevention to the source (autogen sentinel, closeout SKILL.md, canonical-path memory), not to the symptom.
- **Universal Rule #8** — Plans are versioned, never overwritten. Orphan-plan reclassification emits `-v2` revisions when polish requires content change.
- **Universal Rule #9** — No LaunchAgents. Audit is on-demand only.
- **Universal Rule #12** — Memory is hypothesis. Every claim re-verified against current disk state before being acted on. This skill's Phase 1 is the operationalization of #12.

## Why this exists

Drift between memory claims, CLAUDE.md citations, and on-disk reality is the entropy of a multi-session, multi-scope, multi-repo workflow. Sessions name artifacts; artifacts move; sessions end; memory persists the old name; the next session re-discovers the same drift. Without a ritual, drift compounds until the system's self-description no longer matches the system.

The genesis session (2026-05-17) found four classes of drift in one domain (the institutional-authority / SGO / praxis-perpetua surface). Closeout caught the four as "follow-ups"; this skill exists to give those follow-ups a protocol instead of an ad-hoc fix-or-defer decision.

Pairs with `closeout` (which surfaces) and a memory-consolidation pass (which prunes). Three motions, one entropy regime.

## Related

- `~/.claude/plans/where-on-my-local-enchanted-meerkat.md` — genesis plan, Phase 2 section
- `~/.claude/plans/closeout-2026-05-17-plugin-surface-reconciliation.md` — genesis closeout
- `~/.claude/plans/2026-05-17-handoff-plugin-surface-reconciliation.md` — genesis handoff
- `references/buried-bodies-taxonomy.md`, `references/composition-with-closeout.md`, `references/constitutional-doc-policy.md`
