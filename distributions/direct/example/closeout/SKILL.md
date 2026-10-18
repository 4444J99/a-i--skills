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
  - reads-filesystem
  - runs-commands
  - network-access
  - creates-files
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
- Before a non-trivial `git push`: closeout is then **preparation only**. It runs Steps 1-5,
  stops at "ready to publish", and names the exact push command. It does not push without
  authority and it does not emit the terminal line. Final closure (Steps 6-8) follows the
  authorized publication and a readback of what was published, handoff included.
- The session produced files, commits, branches, plans, or tasks and the user signals the end.
- A quiet session with no artifacts: complete Step 2 first, because the repo's protocol may
  still require something; if it does not, say so and exit. Closeout is fast when there is
  nothing to home.

## Steps

### 1. Resolve scope

Establish what "this session" owns before inspecting anything:

```bash
git rev-parse --show-toplevel          # the real worktree, not an installed copy of a protocol
git worktree list
git branch --show-current
```

Confirm the current branch is the one intended for this session's work. Use the native session id if the harness exposes one. A session may span several
repositories; name each root. Inspect only the accepted scope. Never adopt a sibling
checkout or another session's worktree to obtain a green result, and never reset, stash,
or reap work you did not start.

### 2. Discover the repo's own protocol (overlay)

Look for how this repo already closes a session, in this order, and stop at the first hit:

1. `<root>/.agents/skills/closeout/SKILL.md` (when it is not this skill)
2. `<root>/.codex/skills/closeout/SKILL.md` (when it is not this skill)
3. `<root>/.claude/skills/closeout/SKILL.md` (when it is not this skill)
4. A closeout section in an `AGENTS.md` or `CLAUDE.md`, headed "Closeout", "Session end",
   or "Session Review". Check the nearest such file to the directory you are working in
   first, then each parent up to `<root>`; a nested file governs its own subtree.
5. A committed predicate: `scripts/closeout*`, `done.sh`, or a `closeout` Makefile / package script

Skip a candidate in items 1, 2 and 3 only if it is the file you were invoked from or is
byte-for-byte identical to it (`cmp -s`). Identity is decided by content, never by the
description text: a repo that copied this skill and customized it has an overlay, and
that overlay wins even though its description still matches. A stale or generic installed
copy that differs in content is also treated as an overlay; report that it looks generic
rather than silently skipping it. Finding an identical copy must not end discovery before
items 4 and 5 are checked.

If one exists, **it governs the repo-specific steps and the final predicate**; the steps
below are the floor it must not drop. If none exists, the floor stands alone. If a repo
points at an overlay you cannot read or run, report that precisely rather than guessing.

A repo opts into the preserved ORGANVM ritual in `references/organvm-plan-ledger-overlay.md`
only when it owns the convention itself: its own `CLAUDE.md` or `AGENTS.md` carries the
`ORGANVM:AUTO` sentinel, or its own plan and tracker files cite concrete ledger ids
(`DONE-` plus three digits, `IRF-` plus a domain and three digits). The literal
placeholders `DONE-NNN` and `IRF-XXX-NNN` do not count, and neither does any text under
`skills/`, `distributions/`, an installed `closeout` skill directory, or documentation
examples: a repo that merely vendors this skill has not opted in. The overlay is an
example, not a default.

### 3. Inventory (read-only)

```bash
git status --short                      # modified, staged, untracked
# Unpushed commits: empty with an upstream means none; missing upstream is an inventory state, not failure
if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git log @{u}.. --oneline
else
  echo "(no upstream configured; remote commit ownership unverified — inspect session base if known)"
fi
git stash list                          # work parked outside any branch
# Open PRs for this branch. Do not hide failures: an empty list from a failed call is not "no PRs".
gh pr list --head "$(git branch --show-current)" || echo "(PR inventory unmeasured: gh missing, unauthenticated, or unreachable)"
```

With no upstream, an empty `git log` proves nothing. Inspect from a known session base
(for example `git log <remote>/<default>..`) or report remote commit ownership as unverified.

Resolve the remote and default branch instead of assuming `origin/main`: use the remote
the branch tracks (`git config branch.<name>.remote`), else the only remote, else name
the remote you chose; take its default from `git symbolic-ref --short refs/remotes/<remote>/HEAD`.
Use that `<remote>/<default>` wherever Step 6 or the session base needs one. With no
remote at all, report remote ownership as unverified rather than passing it. A PR
inventory that is unmeasured is a dangling row, not an empty one.

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
- one explicit blocker, `BLOCKED: <atom>`, stated once, with its owner and next command
  recorded in a persisted, remotely visible record (an issue, a PR, or a pushed handoff).
  Without that record, report the item as unfinished, not blocked.

"On disk" is not a form. A timed-out lane, an empty diff, a stale-looking branch, or a
remote-pushed branch is not closed; it is an item that still needs one of the four forms.
Never batch-close plans or tasks without the user's confirmation. Never delete a plan;
move it to the repo's abandoned/archive convention if it has one.

### 5. Verify once, on the final tree

Run the repo's verification for what changed, once per changed tree: the overlay's
predicate if there is one, otherwise the narrowest build/test/lint the repo declares
(CI config, Makefile, package scripts). Do not replay a green run on an unchanged tree.

The final tree includes any handoff or plan edit this closeout makes. If work remains,
write the Step 7 handoff **before** this run, so the verified tree is the one that is
published; a handoff written afterwards makes the verification stale.

Read the **predicate's own exit code**. `predicate | tail` reports `tail`'s status, so a
printed FAIL can read as green. Run it bare, or capture to a file and filter the copy.

### 6. Report status words separately

- **merged**: `git fetch <remote>` then `git merge-base --is-ancestor <sha> <remote>/<default>`
  exits 0, using the remote and default resolved in Step 3. A squash or rebase merge leaves
  the original sha off the default branch, so ancestry alone will not show it: cite the
  repository-qualified PR as merged plus the landed commit on the default branch.
- **live**: the running checkout or installed runtime contains the commit
  (`git -C <live-root> merge-base --is-ancestor <sha> HEAD`) plus runtime evidence.
- **observed**: evidence of the behavior itself (a log line, a probe output, a rendered page).

Never write "verified end-to-end" without *observed*. Never claim a status above its evidence.

### 7. Hand off only what is unfinished

If work remains, write the handoff into the repo's existing continuation owner (a
handoff file, plan, or issue that already exists): what was done, what is locked, what
the next session picks up first. Do not create a new file or capsule unless the
overlay asks for one. A finished session needs no successor.

Write it before Step 5 verifies the tree. A handoff held only in the working tree or the
conversation is not a record: publish it with the authorized push and read it back from
the remote before Step 8. If publication is not authorized, the item stays unfinished.

### 8. Idempotent fixed point

Step 5's no-replay rule governs verification. The fixed-point check is a separate,
deliberate repeat of the *session predicate*.

- **With an overlay predicate** (the overlay's session-release predicate): run it twice,
  bare, and quote both exit codes. Both must be 0. If the overlay offers only the full
  repository verification, Step 5's run counts as the first and one repeat is the second.
- **With no overlay** the predicate is the Step 3 inventory re-run read-only, and it passes
  on **content, not exit status**. The inventory commands exit 0 precisely when they find
  work, so a clean exit proves nothing. Both passes must show: `git status --short` empty
  (or only paths evidenced as not this session's); no unpushed commits, measured from the
  upstream or a stated session base; no stash this session made; every open PR row carried
  by a Step 4 owner; and the PR inventory *measured*. Any unmeasured row (no upstream and
  no known base, no remote, `gh` unavailable) is a failure, not a skip. Quote what each
  pass showed.

The second pass must create no files, branches, issues, or PRs and leave no process
running or state behind; the short-lived commands that run the predicate itself are
expected and are not a violation.

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
