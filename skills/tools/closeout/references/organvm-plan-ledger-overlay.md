# ORGANVM plan-ledger overlay (preserved ritual)

> **This is an overlay, not the skill.** `closeout` is repo-agnostic; see `../SKILL.md`.
> This file preserves the six-step ritual structure; its historical verbatim form is
> retained in Git at `62214d3`. Amendments below apply the generic ownership contract
> and so the cross-skill references that cite its Step numbers (`artifact-resurfacing`,
> `transcript-promotion` → `references/composition-with-closeout.md`) stay true.
>
> **Apply it only when the repo opts in**: its `CLAUDE.md` carries the
> `<!-- ORGANVM:AUTO:START -->` sentinel, or it keeps a DONE-NNN / IRF-XXX-NNN plan ledger.
> Everywhere else it does not apply. Paths below (`~/.Codex/plans`, `data/prompt-registry/`,
> `.conductor/`) are ORGANVM conventions, not universal ones.

## When to invoke

- User explicitly says: `/closeout`, "close out", "wrap up", "end the session"
- Before a non-trivial `git push`, inventory and prepare only. Final closure follows
  authorized publication and remote readback.
- When the session has produced 3+ files, plans, or atoms and the user is signaling end

## Six-step protocol

Resolve the active tool's plan root from the repository's instructions: normally
`<root>/.<tool>/plans/` in a project, otherwise its native configured plan root.
Set `CLOSEOUT_PLAN_ROOT` to that resolved path. The historical `~/.Codex/plans` path
is not a current default. A local summary is a convenience copy; every work product
still needs the generic skill's remotely visible durable owner.

### Step 1 — Inventory session outputs

Run, in parallel where possible:

```bash
# What files did this session create or modify?
git status --short

# What plans were authored in this session?
rg --files "$CLOSEOUT_PLAN_ROOT"

# What's the current branch and where does it stand vs origin?
git branch --show-current
git log @{u}.. 2>/dev/null || echo "(no upstream tracking)"
```

Surface a brief inventory table to the user:
- N files modified, M created
- K plans authored this session
- L commits ahead of origin

### Step 2 — Walk back through plans

For each plan attributable to this native session in `CLOSEOUT_PLAN_ROOT` (use source
lineage and session evidence; mtime alone does not prove ownership):

For each plan, classify it as one of:
- **EXECUTED**: contains `DONE-NNN` reference. No action.
- **IN-PROGRESS**: contains `IRF-XXX-NNN` reference but no DONE-NNN. Update its frontmatter to confirm continued status.
- **ABANDONED**: no closure reference, no follow-on commits. Move only under the resolved plan root archive convention with a brief abandonment-reason.

Ask the user for ambiguous cases. Do NOT bulk-classify without confirmation — the home-scope AGENTS.md rule "Atoms are permanent — never batch-close" applies to plans-as-artifacts too.

### Step 3 — Walk back through atoms (if applicable)

If `data/prompt-registry/prompt-atoms.json` was touched this session, identify atoms that were closed in this session and confirm their `status` field is updated.

If not (most sessions), skip.

### Step 4 — Verify git state

Cross-check:
- Working tree is clean (no uncommitted changes meant for this session)
- Local main is in sync with origin (or branch tracks correctly)
- No stray exports/temp files in workspace root (`ls /Users/4jp/Workspace/*.txt` should be empty)

If stray exports exist (the auto-named `2026-MM-DD-NNNNNN-this-session-being-continued-from-a-previous-c.txt` pattern), move them to `~/Documents/session-exports/` or delete if duplicative.

### Step 4.5 — Verify CLAUDE.md autogen freshness (hall-monitor gate)

If the active repo has a `CLAUDE.md` carrying `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->` sentinels, run the gate:

```bash
~/.local/bin/claude-md-autogen-gate
```

If it exits non-zero, the autogen tail is older than 7 days. **Refuse to mark the session as DONE.** Refresh first:

```bash
organvm context sync --write     # autogen sections only
# or
organvm refresh                  # full 10-step pipeline
```

Then re-stage `CLAUDE.md` and commit (the `claude-md-autogen-freshness` pre-commit hook will re-verify), and re-run the gate.

Bypass only with explicit user authorization:

```bash
AUTOGEN_FRESHNESS_THRESHOLD_DAYS=999 ~/.local/bin/claude-md-autogen-gate
```

Pairs with the pre-commit hook (`claude-md-autogen-freshness`); together they catch staleness at both the commit boundary and the session boundary. Root-cause precedent: 32-day autogen-tail staleness traced on 2026-05-16 to `organvm refresh` step 6 soft-failing on `system-system--system: invalid tier 'sovereign'` (closed via schema + validator lockstep edit; see GH `4444J99/domus-semper-palingenesis#30`, IRF-DOM-048).

### Step 4.6 — Reconcile retained work and runtime evidence

Use the generic helper to inventory all local branches, related PRs, stashes,
ignored/index-hidden outputs and retained worktrees. A pushed branch alone is not
closed. Prove squash landings through the repository-qualified PR and its landed
commit. Home every deferred follow-up and operator action in an existing remote
owner. Record each change's merged, live and observed evidence separately; verify
live-checkout lag only against the explicitly identified running checkout/runtime.
Do not infer installation from the development worktree or remove retained data.

### Step 5 — Update active-handoff (if exists)

If `.conductor/active-handoff.md` exists in any active repo, update it with:
- What this session accomplished
- What's locked / not-yet-attempted
- What the next session should pick up

Finish this and the summary before final-tree verification. Publish and read back
every updated owner before the final read-only ownership check.

### Step 6 — Write CLOSEOUT_SUMMARY.md

Produce a session-close-out summary in the resolved existing owner with:

```markdown
# Session Close-Out — {date}

## Outputs
- {N} files created, {M} modified
- {K} plans authored: {filenames}
- {L} commits made (SHAs): {sha-list}

## Closure marks
- EXECUTED plans (DONE-NNN refs): {list}
- IN-PROGRESS plans (IRF refs): {list}
- ABANDONED plans (moved): {list}

## Pending
- Uncommitted changes: {if any}
- Unpushed commits: {if any}
- Active handoff: {path if exists}

## Hand-off note for next session
{one-paragraph context for resumability}
```

## Rules to honor

- **Never batch-close atoms or plans without explicit user confirmation.** Per Universal Rule (memory rule #53): atoms are permanent, never batch-close.
- **Never delete plan files.** Move to `abandoned/` instead, preserving the history (per the plan-discipline section of the home AGENTS.md).
- **Never push as part of closeout** unless user has explicitly authorized push for this session. Closeout's job is to *prepare* for push, not perform it.
- **Quiet sessions still require measured ownership.** No notable files does not
  exclude inline obligations, hidden files or unknown ownership. Require the read-only
  ownership pass and any repository session predicate before claiming completion.

## Why this exists

Per `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md`:

> 90.4% of plans are ORPHANED. Of 427 plans in `~/.Codex/plans/`, 386 contain neither a DONE-NNN nor IRF reference. Only 20 (4.7%) are EXECUTED, 21 (4.9%) are IN-PROGRESS.

The orphan rate is a direct artifact of the absence of a close-out ritual. This skill is the ritual.

The cost of skipping is invisible bookkeeping debt: plans accumulate, atoms stay open against doctrine that already encodes them, the system can't programmatically answer "what was done?". The cost of doing it is ~3-5 minutes per session.

## Related

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Pathology #4: plan-author cadence vastly exceeds plan-execution cadence (21:1)
- `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md` — full data behind the 90.4% orphan rate
- Universal Rule #2: "Nothing local only" — close-out is what makes "nothing local only" achievable per session
