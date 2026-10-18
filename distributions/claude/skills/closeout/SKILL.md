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
- Before a non-trivial `git push`: prepare and inventory only. Final closure follows authorized publication and remote readback, including any newly updated handoff.
- The session produced files, commits, branches, plans, or tasks and the user signals the end.
- A quiet session still uses the read-only ownership check; an empty measured inventory is valid.

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
4. A "Closeout" (or "Session end") section in `<root>/AGENTS.md` or `<root>/CLAUDE.md`
5. A committed predicate: `scripts/closeout*`, `done.sh`, or a `closeout` Makefile / package script

Skip only the invoked file or a byte-identical copy of it in items 1, 2 and 3.
An unchanged description does not make a customized overlay generic. A generic installed
copy is not the repo's protocol, and finding one must not end discovery before items 4
and 5 are checked.

If one exists, **it governs the repo-specific steps and the final predicate**; the steps
below are the floor it must not drop. If none exists, the floor stands alone. If a repo
points at an overlay you cannot read or run, report that precisely rather than guessing.

Repos that keep an ORGANVM-style plan ledger (a `CLAUDE.md` with the `ORGANVM:AUTO`
sentinel in a tracked root instruction file, or actual DONE-NNN / IRF-XXX-NNN ledger
conventions in repository-owned plan locations) opt into the preserved ritual in
`references/organvm-plan-ledger-overlay.md`. It is an example overlay, not a default. Ignore sentinel/ledger mentions in bundled
skills, distributions, documentation and examples; `scripts/closeout_check.py` implements
this bounded discovery.

### 3. Inventory (read-only)

Use the bundled [ownership checker](references/ownership-check.md):

```bash
python3 <skill>/scripts/closeout_check.py inventory --evidence <existing-session-evidence.json>
```

The evidence document projects existing owners; it is not another task registry. Name
the native session, scoped roots, exact bases and declared non-file obligations. The
helper inventories content-bound files, commits, stashes and retained worktrees. An
unknown item requires a verified owner or a remote evidenced exclusion from this session.
The following commands are exploratory inventory, never a completion predicate.

```bash
git status --short                      # modified, staged, untracked
# Unpushed commits: empty with an upstream means none; missing upstream is an inventory state, not failure
if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git log @{u}.. --oneline
else
  echo "(no upstream configured; remote commit ownership unverified — inspect session base if known)"
fi
git stash list                          # work parked outside any branch
gh pr list --head "$(git branch --show-current)" 2>/dev/null   # only if gh and a remote exist
```

With no upstream, an empty `git log` proves nothing. Inspect from a known session base
(using the actual selected remote and its measured default branch) or report remote commit ownership as unverified.

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

Read the **predicate's own exit code**. `predicate | tail` reports `tail`'s status, so a
printed FAIL can read as green. Run it bare, or capture to a file and filter the copy.

### 6. Report status words separately

- **merged**: resolve the actual remote/default, fetch, then prove ancestry to that
  measured branch. A squash landing needs authenticated repository-qualified PR
  evidence linking the original commit to the PR and its landed commit on that default.
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

Step 5's no-replay rule governs verification. The fixed-point check is a separate,
deliberate repeat of the *session predicate* (the overlay's session-release predicate, or
the bundled ownership checker when there is no repository predicate). Successful
inventory commands cannot establish ownership. Run the read-only ownership check
with `check --evidence <existing-session-evidence.json> --twice`; both fresh passes
must return 0 with unchanged inventory and evidence fingerprints. Quote both exit codes. If the
overlay offers only the full repository verification as its predicate, Step 5's run counts
as the first and one read-only repeat is the second; reuse unchanged verification
receipts and never replay a mutating verification as a fixed-point check. Both must be 0, and the second run must
create no files, branches, issues, PRs, or processes.

Only then emit, as the last line:

`CLOSEOUT COMPLETE — idempotent fixed point, zero dangling items`

Nothing follows it. If any step failed, report the real outcome and the precise owner
of what remains; do not emit the statement.

## Effects

The helper reads files and Git objects and invokes bounded Git/gh network reads. It
disables optional Git index refresh writes and creates no artifacts. The surrounding
workflow may create/update owner records and modify Git only within granted authority.
Missing helper, unsupported evidence or inaccessible remote readback is unmeasured
(exit 2); dangling obligations exit 1; complete measured ownership exits 0. Ownership
alone never overrides a repository session predicate, including Limen.

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
