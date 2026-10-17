---
name: closeout
description: Session-end ritual. Inventories plans, atoms, git state, and hanging work (unmerged PRs, unreaped branches, live-checkout lag, unfiled follow-ups) from live state, assigns plans a closure status (DONE-NNN, IRF-XXX-NNN, or plans/abandoned/), enforces the merged/live/observed status words, and writes a closeout summary. Triggers on "/closeout", "close out the session", "end of session", "wrap up", "session close", or before any planned `git push`.
license: MIT
complexity: beginner
time_to_learn: 5min
tags:
  - session-management
  - hygiene
  - hall-monitor
  - close-out
  - directive-traceability
inputs:
  - current-session-state
  - plans-authored-this-session
  - atoms-touched-this-session
  - session-branches-and-prs
outputs:
  - closure-marks
  - CLOSEOUT_SUMMARY-md
  - abandoned-plans-moved
  - hanging-work-inventory
side_effects:
  - creates-files
  - modifies-git
triggers:
  - user-says-closeout
  - user-says-end-session
  - user-says-wrap-up
  - before-git-push
---

# /closeout — Session Close-Out Ritual

The first closeout must be the real one. Two usage reports (2026-10-16) found closeouts that claimed "verified end-to-end" when fixes were merged but not deployed, and that left branches unreaped and follow-ups unfiled. Every claim in a closeout comes from live state read in this closeout, never from an earlier assistant statement, a checklist mark, or memory.

## When to invoke

- User explicitly says: `/closeout`, "close out", "wrap up", "end the session"
- Before any non-trivial `git push` (the close-out should precede the push)
- When the session has produced 3+ files, plans, or atoms and the user is signaling end

## Conventions used below

**Plan root.** Resolve in this order and use the first that exists:

1. `<project-root>/.<tool>/plans/` (for Claude Code: `.claude/plans/`) when working inside a project
2. `$CLAUDE_CONFIG_DIR/plans/` otherwise (the shared agent state root is `$LIMEN_AGENT_RUNTIME_ROOT/claude`)

Below, `$PLAN_ROOT` means whichever resolved. Create `$PLAN_ROOT/abandoned/` on first use. Do not use the retired legacy locations `~/.claude/plans/` or `~/.Codex/plans/`.

**Bare commands.** Run each command by itself, one per tool call. Do not chain (`&&`, `;`) or pipe a predicate into `head`/`tail`: the pipeline reports the last command's exit code, so a failing check reads as green. Read each predicate's own exit code and quote it.

**Status words.** Use exactly these, and no stronger:

| Word | Means | Evidence required |
|------|-------|-------------------|
| **merged** | The commit is on `origin/main` | `git merge-base --is-ancestor <sha> origin/main` exits `0` after `git fetch origin` |
| **live** | The running checkout or runtime contains the commit | The same predicate against the deployed checkout/artifact's HEAD exits `0` |
| **observed** | Runtime evidence shows the change working | A run, log line, health check, or output captured in this session, quoted |

"Verified end-to-end" requires **observed**. A merged fix is "merged, not live" until the deployed artifact contains the merge commit, and "live, not observed" until someone has run it. Never promote one word to the next because it is likely.

**Two-run idempotence.** Any predicate or gate this skill runs (`claude-md-autogen-gate`, `merge-base --is-ancestor`, a repo validation script) is run twice. Quote both bare exit codes. If the two runs disagree, the state is unsettled: report it as such and do not claim it either way.

## Seven-step protocol

### Step 1 — Inventory session outputs

Run, in parallel where possible, each as its own command:

```bash
# What files did this session create or modify?
git status --short

# What plans were authored in this session? (newest first; read the top 10)
ls -t "$PLAN_ROOT"

# What's the current branch and where does it stand vs origin?
git branch --show-current

# Commits not yet on the upstream (an error here means no upstream tracking)
git log @{u}..
```

Surface a brief inventory table to the user:
- N files modified, M created
- K plans authored this session
- L commits ahead of origin

### Step 2 — Walk back through plans

For each plan authored this session (filter `$PLAN_ROOT/*.md` by mtime within session window):

For each plan, classify it as one of:
- **EXECUTED**: contains `DONE-NNN` reference. No action.
- **IN-PROGRESS**: contains `IRF-XXX-NNN` reference but no DONE-NNN. Update its frontmatter to confirm continued status.
- **ABANDONED**: no closure reference, no follow-on commits. Move to `$PLAN_ROOT/abandoned/` with a brief abandonment-reason.

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

If the active repo has a `CLAUDE.md` carrying `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->` sentinels, run the gate (twice, per two-run idempotence):

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

### Step 5 — Hanging-work inventory (before the summary)

Work that is finished in the editor but not in the world is the commonest closeout failure. List the session's branches (the current one, plus every branch this session created; `git worktree list` shows checkouts), then check each of the four classes below from live state. Nothing here is "probably fine".

**5a. Unmerged PRs for session branches.** For each session branch:

```bash
gh pr list --repo OWNER/NAME --head <branch> --state all --json number,state,mergedAt,url
```

- `OPEN`: record the PR URL and its state. It is hanging work; do not call it landed.
- No PR and commits ahead of `origin/main`: the work has no home yet. Say so.
- `MERGED`: record the PR, then confirm the merge commit is on `origin/main` (the **merged** word) before saying so.

**5b. Landed-but-unreaped branches.** After `git fetch origin`:

```bash
git branch --merged origin/main
```

Branches listed there are landed and safe to reap with `git branch -d <branch>` (and `git worktree remove <path>` for a finished worktree of this session). **This command is blind to squash- and rebase-merges**, which rewrite the commits so the branch tip is never an ancestor of `origin/main`. For a branch not listed, check 5a: a `MERGED` PR whose head matches the branch tip means it has landed and the branch is reapable, though `git branch -d` will refuse and `-D` needs that PR evidence quoted. Only reap branches this session created; never touch another session's branch or worktree. Remote branch deletion is a push-class action: list it as an operator action (or note the repo's auto-delete-on-merge setting) rather than doing it.

**5c. Live-checkout lag.** In the checkout that actually runs the work (the live checkout, runtime, or deployed artifact — not just the session worktree):

```bash
git fetch origin
git rev-list --left-right --count origin/main...HEAD
```

The output is `<behind> <ahead>`: the left count is commits on `origin/main` that this checkout lacks, the right count is commits only here. Non-zero left means the checkout lags. Then test the specific merge commit(s) of this session's work against the deployed checkout or artifact:

```bash
git merge-base --is-ancestor <merge-sha> <deployed-HEAD>
```

Exit `0` means the deployed artifact contains it (**live**). Exit `1` means it does not: report **"merged, not live"** and name what must be rebuilt, restarted, or synced. Run it twice and quote both exit codes.

**5d. Unfiled follow-ups.** Collect every follow-up surfaced in the session: "later", "out of scope", "TODO", findings deferred, tests not run, steps skipped, activation or rebuild steps that remain. Each must be **filed with an owner** in its registry home (IRF item, GitHub issue, or the repo's tracker; use the registry that owns the answer rather than asking) before the closeout is complete. Record the ID or URL against each item.

**Operator action list.** Finish Step 5 by writing the list of actions left for the human operator. It must be **empty, or every entry explicitly homed** (item + owner + registry ID/URL). An entry with no home is not allowed to stand: file it, or state that it could not be filed and why. Recitation in chat without a durable home does not count as homed.

### Step 6 — Update active-handoff (if exists)

If `.conductor/active-handoff.md` exists in any active repo, update it with:
- What this session accomplished
- What's locked / not-yet-attempted
- What the next session should pick up

This is the cross-session continuity gate.

### Step 7 — Write CLOSEOUT_SUMMARY.md

Produce a session-close-out summary at `$PLAN_ROOT/closeout-{date}.md` (if it exists, write `-v2`, `-v3`; never overwrite) with:

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

## Status of delivered work
| Change | merged | live | observed | Evidence (commands + exit codes) |
|--------|--------|------|----------|----------------------------------|
| {commit/PR} | yes/no | yes/no | yes/no | {quoted} |

## Hanging work
- Unmerged PRs: {urls or none}
- Unreaped branches: {list or none, with reaped/not}
- Live-checkout lag: {behind/ahead counts, merged-not-live items}
- Follow-ups filed: {item -> owner -> ID/URL}
- Operator action list: {empty | each entry with its home}

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
- **Never say "verified end-to-end" without observed.** Use merged / live / observed exactly as defined above.
- **Never leave the operator list unhomed.** Empty, or every entry filed with an owner.
- **If the session produced no notable artifacts**, say so and exit cleanly. Closeout is fast on quiet sessions.

## Why this exists

Per `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md`, 90.4% of plans were ORPHANED: of 427 plans, 386 contained neither a DONE-NNN nor an IRF reference, and only 20 (4.7%) were EXECUTED and 21 (4.9%) IN-PROGRESS. The orphan rate is a direct artifact of the absence of a close-out ritual.

The 2026-10-16 usage reports found the second failure mode: plans were closed correctly, but delivered work was reported finished while it was merged-not-live, branches stayed unreaped, and follow-ups lived only in chat. Step 5 and the status-word rule exist for that.

The cost of skipping is invisible bookkeeping debt: plans accumulate, atoms stay open against doctrine that already encodes them, the system can't programmatically answer "what was done?". The cost of doing it is ~3-5 minutes per session.

## Related

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Pathology #4: plan-author cadence vastly exceeds plan-execution cadence (21:1)
- `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md` — full data behind the 90.4% orphan rate
- Universal Rule #2: "Nothing local only" — close-out is what makes "nothing local only" achievable per session
