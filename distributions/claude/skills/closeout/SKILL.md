---
name: closeout
description: Finish authorized session work and release its owned resources using the repository's scoped protocol. Use for closeout, wrap-up, or session-end requests. Keep task delivery, session release, native conversation archiving, and worktree retirement separate.
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
- A push uses the repository's scoped verification and publication procedure. It does
  not invoke this skill recursively. Existing authorization to finish and land work
  carries through ordinary commits, pushes, review fixes and permitted merges.
- The session produced files, commits, branches, plans, or tasks and the user signals the end.
- A quiet session with no artifacts: complete Step 2 first, because the repo's protocol may
  still require something; if it does not, say so and exit. Closeout is fast when there is
  nothing to home.

## Steps

First classify the requested result. Finish-and-land requests require completing
the authorized delivery; an open PR or handoff does not substitute for a requested
merge or deployment. Session release may retain unfinished work with its existing
owner. Explicit native conversation archive/unarchive uses the provider operation:
record any unfinished work in the conversation or its existing owner, then archive.
It does not require Git publication, a broker release, or worktree deletion. A
readiness question must say whether it assesses unfinished work or safe worktree
removal; do not silently turn native history organization into filesystem retirement.

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

A repo opts into `references/organvm-plan-ledger-overlay.md` only through an explicit
repo-owned instruction selecting that procedure. An `ORGANVM:AUTO` marker or a ledger
identifier alone does not authorize broader maintenance, context regeneration, or
new summary files. Preserve existing ledgers without turning their presence into
new session obligations. The overlay is an example, not a default.

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
# Repeat for every session-owned branch identified in Step 1, including branches no longer checked out.
# Use its repository explicitly; a failed call is not an empty inventory.
gh pr list --repo <owner/repo> --head <session-owned-branch> --state all
```

Reconcile known session outputs against ignored paths as well as `git status`:
use `git status --short --ignored -- <known-output-paths>` for each scoped output.
Include session-owned ignored deliverables in homing; preserve private data through
its authorized custody owner rather than committing secrets or generated caches.
Do not turn unrelated ignored files into new session obligations.

With no upstream, an empty `git log` proves nothing. Inspect from a known session base
(for example `git log <remote>/<default>..`) or report remote commit ownership as unverified.

Resolve the remote and default branch instead of assuming `origin/main`: use the remote
the branch tracks (`git config branch.<name>.remote`), else the only remote, else name
the remote you chose; take its default from `git symbolic-ref --short refs/remotes/<remote>/HEAD`.
Use that `<remote>/<default>` wherever Step 6 or the session base needs one. With no
remote at all, report remote ownership as unverified rather than passing it. A PR
inventory that is unmeasured is a dangling row, not an empty one.

Add whatever the session touched in the repo's *own* plan, task, or issue locations,
found by looking, not by assuming a path. Persist a conversation deliverable when the
accepted task requires a saved artifact or the repository contract requires one.
Do not automatically turn an ordinary answer into a new file, promotion task, or PR.
Present a short table when it helps:
files changed, commits ahead of upstream, open PRs, plans or tasks touched, stashes,
inline-only deliverables.

### 4. Home every item

Complete the accepted delivery first. Homing is how remaining obligations retain an
owner, not permission to stop authorized work early. Do not ask again for permission
already granted by the task or repository charter.

Each item ends in exactly one durable form:

- merged to the default branch, or the landing branch explicitly named by the repo's delivery protocol, with the SHA;
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

- **merged**: `git fetch <remote>` then `git merge-base --is-ancestor <sha> <remote>/<landing>`
  exits 0. Use the default resolved in Step 3 unless the repo's delivery protocol explicitly
  names another landing branch; report that branch. A squash or rebase merge leaves
  the original SHA off that branch, so cite the repository-qualified PR as merged
  plus ancestry of its landed commit on the authorized landing branch.
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
  bare, and quote both exit codes when that protocol requires an idempotence check.
  Both must be 0. Full repository verification is not a session-release predicate;
  reuse its unchanged passing result and inspect the owned inventory separately.
- **With no session-release predicate**, including an overlay that defines only steps
  or repository verification, use the Step 3 inventory re-run read-only. It passes
  on **content, not exit status**. The inventory commands exit 0 precisely when they find
  work, so a clean exit proves nothing. Both passes must show: `git status --short` empty
  (or only paths evidenced as not this session's); no unpushed commits, measured from the
  upstream or a stated session base, except commits proven published by the exact
  repository-qualified PR head and its squash/rebase merge on the default branch;
  no stash this session made; every open PR row carried
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
- **Freeze the verified head.** Successful CI, review completion, and status changes
  are observations, not reasons to commit new success notes or polish. Change source
  only for an actual defect or requested scope change; record run evidence in the
  existing PR or external receipt. Submit the permitted exact head for landing once.
- **Bound failed checks.** Retry only after relevant evidence or state changes. A
  broker outage or quota failure leaves release unmeasured; it does not undo verified
  task delivery or require a fresh repair of the whole estate. Continue independent
  authorized work and preserve the existing owner of the unavailable check.
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
