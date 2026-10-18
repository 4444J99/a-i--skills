---
name: closeout
description: Repo-agnostic session-end ritual. Proves every obligation this session created is homed in a durable, remotely visible owner (merged work, open PR, filed issue or plan, explicit blocker), discovers and defers to the repo's own closeout protocol when it has one, and reports merged / live / observed as separate claims. Triggers on "/closeout", "close out the session", "end of session", "wrap up", "session close", or before a planned `git push`.
license: MIT
complexity: beginner
time_to_learn: 5min
tags:
  - session-management
  - hygiene
  - close-out
  - handoff
inputs:
  - current-session-state
  - repo-closeout-protocol-if-any
outputs:
  - closure-evidence
  - handoff-note-if-unfinished
side_effects:
  - modifies-git
triggers:
  - user-says-closeout
  - user-says-end-session
  - user-says-wrap-up
  - before-git-push
---

# /closeout — Session Close-Out

A closeout answers one question: **is every obligation this session created now owned by
something durable?** Not "is the code good" (verification) and not "is the estate healthy"
(diagnostics). Four claims stay distinct and are never blurred: *session released*, *task
completed*, *estate healthy*, *deletion eligible*.

This skill works in any git repository. It carries only the universal floor. Anything a
repo knows about itself (its plan ledger, its scripts, its merge rail) comes from the repo.

## When to invoke

- The user says `/closeout`, "close out", "wrap up", "end the session".
- Before a non-trivial `git push`; closeout prepares the push, it does not perform it.
- The session produced files, commits, branches, plans, or tasks and the user signals the end.
- A quiet session with no artifacts: say so and exit. Closeout is fast when there is nothing to home.

## Steps

### 1. Resolve scope

Establish what "this session" owns before inspecting anything:

```bash
git rev-parse --show-toplevel          # the real worktree, not an installed copy of a protocol
git worktree list
git branch --show-current
```

Use the native session id if the harness exposes one. A session may span several
repositories; name each root. Inspect only the accepted scope. Never adopt a sibling
checkout or another session's worktree to obtain a green result, and never reset, stash,
or reap work you did not start.

### 2. Discover the repo's own protocol (overlay)

Look for how this repo already closes a session, in this order, and stop at the first hit:

1. `<root>/.agents/skills/closeout/SKILL.md` (when it is not this skill)
2. `<root>/.claude/skills/closeout/SKILL.md`
3. A "Closeout" (or "Session end") section in `<root>/AGENTS.md` or `<root>/CLAUDE.md`
4. A committed predicate: `scripts/closeout*`, `done.sh`, or a `closeout` Makefile / package script

If one exists, **it governs the repo-specific steps and the final predicate**; the steps
below are the floor it must not drop. If none exists, the floor stands alone. If a repo
points at an overlay you cannot read or run, report that precisely rather than guessing.

Repos that keep an ORGANVM-style plan ledger (a `CLAUDE.md` with the `ORGANVM:AUTO`
sentinel, or DONE-NNN / IRF-XXX-NNN plan references) opt into the preserved ritual in
`references/organvm-plan-ledger-overlay.md`. It is an example overlay, not a default.

### 3. Inventory (read-only)

```bash
git status --short                      # modified, staged, untracked
git log @{u}.. --oneline 2>/dev/null    # unpushed commits (empty output with an upstream = none)
git stash list                          # work parked outside any branch
gh pr list --head "$(git branch --show-current)" 2>/dev/null   # only if gh and a remote exist
```

Add whatever the session touched in the repo's *own* plan, task, or issue locations,
found by looking, not by assuming a path. Also flag substantive content delivered only
in the conversation and never written to a file; mark those rows
`Inline only; not file-persisted`. They are un-homed items (Step 4), and the natural
next step is the `transcript-promotion` skill if installed. Present a short table:
files changed, commits ahead of upstream, open PRs, plans or tasks touched, stashes,
inline-only deliverables.

### 4. Home every item

Each item ends in exactly one durable form:

- merged to the default branch, with the SHA;
- an open PR with a named owner and a merge condition;
- a filed issue, plan, or task in the repo's existing tracker (committed and pushed);
- one explicit blocker, `BLOCKED: <atom>`, stated once with its owner and next command.

"On disk" is not a form. A timed-out lane, an empty diff, a stale-looking branch, or a
remote-pushed branch is not closed; it is an item that still needs one of the four forms.
Never batch-close plans or tasks without the user's confirmation. Never delete a plan;
move it to the repo's abandoned/archive convention if it has one.

### 5. Verify once, on the final tree

Run the repo's verification for what changed, once per changed tree: the overlay's
predicate if there is one, otherwise the narrowest build/test/lint the repo declares
(CI config, Makefile, package scripts). Do not replay a green run on an unchanged tree.

Read the **predicate's own exit code**. `predicate | tail` reports `tail`'s status, so a
printed FAIL can read as green. Run it bare, or capture to a file and filter the copy.

### 6. Report status words separately

- **merged**: `git fetch` then `git merge-base --is-ancestor <sha> origin/<default>` exits 0.
- **live**: the running checkout or installed runtime contains the commit
  (`git -C <live-root> merge-base --is-ancestor <sha> HEAD`) plus runtime evidence.
- **observed**: evidence of the behavior itself (a log line, a probe output, a rendered page).

Never write "verified end-to-end" without *observed*. Never claim a status above its evidence.

### 7. Hand off only what is unfinished

If work remains, write the handoff into the repo's existing continuation owner (a
handoff file, plan, or issue that already exists): what was done, what is locked, what
the next session picks up first. Do not create a new file or capsule unless the
overlay asks for one. A finished session needs no successor.

### 8. Idempotent fixed point

Run the session predicate (the overlay's, or the Step 3 inventory plus Step 5 check)
twice and quote both bare exit codes. Both must be 0, and the second run must create
no files, branches, issues, PRs, or processes.

Only then emit, as the last line:

`CLOSEOUT COMPLETE — idempotent fixed point, zero dangling items`

Nothing follows it. If any step failed, report the real outcome and the precise owner
of what remains; do not emit the statement.

## Rules

- **Authority is bounded by the session.** Do not push, merge, force-push, or delete
  beyond what the user or the repo's own charter granted for this session.
- **Fail closed on unknown ownership.** If you cannot tell whether a branch, worktree, or
  file is this session's, leave it alone and name it.
- **No invented paths.** If the repo has no plan ledger, there is nothing to classify;
  do not create `~/.<tool>/plans` or a summary file to have something to close.
- **A filed task is homed, not done.** Filing creates an owner; it does not satisfy the
  task's own acceptance predicate.
- **A genuine external gate** is stated once as `BLOCKED: <atom>` and homed with its
  owner, predicate, and next command. Then keep closing every other item.

## Related

- `references/organvm-plan-ledger-overlay.md`: the preserved six-step plan/atom ledger
  ritual for repos that opt into it.
- `artifact-resurfacing` and `transcript-promotion` compose with closeout; each carries a
  "composition with closeout" note in its own references.
