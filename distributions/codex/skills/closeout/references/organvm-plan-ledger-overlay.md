# ORGANVM plan-ledger overlay (preserved ritual)

> **This is an overlay, not the skill.** `closeout` is repo-agnostic; see `../SKILL.md`.
> This file preserves the original six-step ritual with current path corrections
> and so the cross-skill references that cite its Step numbers (`artifact-resurfacing`,
> `transcript-promotion` → `references/composition-with-closeout.md`) stay true.
>
> **Apply it only when a repo-owned instruction explicitly selects this procedure.**
> A generated context marker or ledger alone is not an opt-in. Its maintenance steps
> apply only within the accepted task scope; native conversation archiving remains
> separate. Paths below (`.gemini/plans`, `data/prompt-registry/`,
> `.conductor/`) are ORGANVM conventions, not universal ones.
>
> **The generic floor still binds this overlay.** Files under `.gemini/plans` are local to
> the host. Per `../SKILL.md` Step 4, nothing counts as homed until it also has a remotely
> visible owner (a pushed plan, filed issue, or PR); Step 6's summary is a convenience view,
> not the record.

## When to invoke

- User explicitly says: `/closeout`, "close out", "wrap up", "end the session"
- When explicitly selected for session closeout; never recursively before a push
- When the session has produced 3+ files, plans, or atoms and the user is signaling end

## Six-step protocol

### Step 1 — Inventory session outputs

Run, in parallel where possible:

```bash
# What files did this session create or modify?
git status --short

# What plans were authored in this session?
ls -t .gemini/plans/*.md 2>/dev/null | head -10

# What's the current branch and where does it stand vs origin?
git branch --show-current
git log @{u}.. 2>/dev/null || echo "(no upstream tracking)"
```

Surface a brief inventory table to the user:
- N files modified, M created
- K plans authored this session
- L commits ahead of origin

### Step 2 — Walk back through plans

For each plan authored this session (filter `.gemini/plans/*.md` by mtime within session window):

For each plan, classify it as one of:
- **EXECUTED**: contains `DONE-NNN` reference. No action.
- **IN-PROGRESS**: contains `IRF-XXX-NNN` reference but no DONE-NNN. Update its frontmatter to confirm continued status.
- **ABANDONED**: no closure reference, no follow-on commits. Move to `.gemini/plans/abandoned/` with a brief abandonment-reason only when abandonment is established, not inferred from missing metadata.

Ask the user for ambiguous cases. Do NOT bulk-classify without confirmation — the home-scope AGENTS.md rule "Atoms are permanent — never batch-close" applies to plans-as-artifacts too.

### Step 3 — Walk back through atoms (if applicable)

If `data/prompt-registry/prompt-atoms.json` was touched this session, identify atoms that were closed in this session and confirm their `status` field is updated.

If not (most sessions), skip.

### Step 4 — Verify git state

Cross-check:
- Working tree is clean (no uncommitted changes meant for this session)
- Local main is in sync with origin (or branch tracks correctly)
- No stray exports/temp files in the workspace root (for example, auto-named `2026-MM-DD-NNNNNN-*.txt` session exports should be relocated or absent)

If stray exports exist (the auto-named `2026-MM-DD-NNNNNN-this-session-being-continued-from-a-previous-c.txt` pattern), move them to `~/Documents/session-exports/` or delete if duplicative.

### Step 4.5 — Verify CLAUDE.md autogen freshness (hall-monitor gate)

Only when generated-context maintenance is part of the accepted task, and the active
repo has a `CLAUDE.md` carrying `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->`
sentinels, run the gate. Markers alone do not add maintenance to session closeout:

```bash
~/.local/bin/claude-md-autogen-gate
```

If it exits non-zero, record the maintenance finding with its existing owner. It
does not invalidate independently verified session delivery. When refreshing is
within the accepted task, refresh through its existing owner:

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

### Step 5 — Update active-handoff (if exists)

If `.conductor/active-handoff.md` exists in any active repo, update it with:
- What this session accomplished
- What's locked / not-yet-attempted
- What the next session should pick up

This is the cross-session continuity gate.

### Step 6 — Write CLOSEOUT_SUMMARY.md

Produce a session-close-out summary at `.gemini/plans/closeout-{date}.md` with:

Use that path only when it is the repository's tracked plan convention. Otherwise
update the existing tracked session owner; never create a second local-only plan
root. Publish the required summary with the already-authorized delivery before the
generic final-tree verification. A summary is not a new permission checkpoint and
does not replace completing the requested work. If no publication authority exists,
report that artifact as retained and unfinished rather than claiming release.

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
- **Complete authorized publication as part of delivery.** Existing authorization to finish and land work carries through ordinary commits, pushes and permitted merges; do not ask again merely because closeout was invoked.
- **If the session produced no notable artifacts**, say so and exit cleanly. Closeout is fast on quiet sessions.

## Why this exists

Per `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md`:

> 90.4% of plans are ORPHANED. Of 427 plans in `~/.Codex/plans/`, 386 contain neither a DONE-NNN nor IRF reference. Only 20 (4.7%) are EXECUTED, 21 (4.9%) are IN-PROGRESS.

The orphan rate is a direct artifact of the absence of a close-out ritual. This skill is the ritual.

The cost of skipping is invisible bookkeeping debt: plans accumulate, atoms stay open against doctrine that already encodes them, the system can't programmatically answer "what was done?". The cost of doing it is ~3-5 minutes per session.

## Related

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Pathology #4: plan-author cadence vastly exceeds plan-execution cadence (21:1)
- `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md` — full data behind the 90.4% orphan rate
- Universal Rule #2: "Nothing local only" — close-out is what makes "nothing local only" achievable per session
