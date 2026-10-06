---
name: transcript-promotion
description: Use when substantive inline content delivered during a session lives only in the JSONL transcript and needs promotion to a durable, surface-discoverable, remote-backed artifact. Triggers on "persist this", "promote to a plan", "make this survive context exit", "engine log N", or when closeout flags a deliverable as "inline only — not file-persisted". Provides the four-phase extract → frontmatter → propagate → register protocol. Sibling to artifact-resurfacing (which reconciles citations pointing at nothing); this one rescues content that exists without citation.
license: MIT
complexity: intermediate
time_to_learn: 30min
tier: core
tags:
  - transcript-extraction
  - artifact-promotion
  - durability-restoration
  - engine-log-series
  - silent-failure-class
  - propose-then-propagate
inputs:
  - jsonl-transcript-path
  - section-anchor-or-line-range
  - artifact-slug
outputs:
  - plan-file-in-claude-plans
  - chezmoi-source-mirror
  - remote-commit-pushed
  - series-register-entry
side_effects:
  - reads-filesystem
  - creates-files
  - runs-commands
  - modifies-git
triggers:
  - user-says-persist-this
  - user-says-promote-to-plan
  - user-says-make-this-survive
  - user-says-engine-log
  - closeout-flagged-inline-only
  - all-unique-data-survives-exit-question
complements:
  - closeout
  - artifact-resurfacing
  - cross-agent-handoff
governance_phases: [prove, ship]
governance_norm_group: repo-hygiene
organ_affinity: [all]
---

# Transcript Promotion

Lift substantive inline content from the ephemeral transcript surface to the durable plan-file surface. Extract verbatim, prepend canonical frontmatter, propagate to chezmoi-source so the autoCommit+autoPush cascade fires, and register the artifact in any series it belongs to.

## Why this exists

Sessions produce two kinds of substantive output:

1. **File-bound** — code edits, plan writes, IRF rows, memory entries. These propagate via `Write|Edit` tool hooks and naturally land on disk + remote.
2. **Conversation-bound** — dense reference deliveries, "engine logs", inline analyses, multi-section walkthroughs the user reads and reacts to in-chat.

Class (2) is durable in the JSONL transcript but invisible to `~/.claude/plans/INDEX.md`, `MEMORY.md`, and the chezmoi-source mirror. The transcript is on disk, but the content is buried inside conversation text rather than promoted to a discoverable artifact. A future session reading the plans index sees nothing; the content effectively dies with context exit.

Genesis case (2026-05-20 session `9cb55c4d`): three engine reference docs (LOG #1 statusLine, LOG #2 Hooks, LOG #3 Subagents) delivered inline. LOG #1 was persisted to a plan file by the same session. LOG #2 and #3 were marked "inline only — not file-persisted" in the closeout. Two days later (2026-05-22), under explicit prompt to verify durability, they were extracted from the JSONL and promoted via the protocol now codified in this skill.

Pairs with `artifact-resurfacing` as the inverse motion:
- `artifact-resurfacing` — citation points at nothing → reconcile the citation
- `transcript-promotion` — content exists with no citation → mint the citation

Both clear different sides of the same drift entropy.

## Authority boundary (read first)

This skill is **propagate-with-explicit-cascade** for routine plan files, **propose-not-apply** for any constitutional surface.

- Plan files in `~/.claude/plans/` may be written directly; the chezmoi auto-sync hook fails for bash-redirect file creation, so the skill manually runs `chezmoi add` to bring source into sync and let autoCommit+autoPush fire. This is the documented chezmoi gotcha protocol from home-scope CLAUDE.md.
- `CLAUDE.md`, `MEMORY.md`, `governance-rules.json`, `registry-v2.json`, any `seed.yaml`, `INST-INDEX-RERUM-FACIENDARUM.md` — never written by this skill. If transcript content names changes to a constitutional surface, defer to the conductor.
- Cross-organ push to a public ORGANVM `main` branch requires explicit per-session push authorization. This skill commits but surfaces the push decision to the user when the target is a public-main branch.

Discovery → propose-frontmatter → propagate via chezmoi → register in series. Four phases, last two require user-derived authorization for non-routine targets.

## When to use

- "Persist LOG #N to `~/.claude/plans/...`"
- "Promote this inline reference to a plan file"
- "Make sure this survives context exit"
- "Save the engine log to disk"
- "Another log for the engine" (canonically followed by promotion in the same or next turn)
- Closeout walks back and finds ≥1 deliverable flagged "inline only"
- User asks "all unique data survives present context upon exit?" and the audit table shows artifacts with `JSONL ✓ / plan file ✗`
- A `qa-audit` of substantive deliverables finds class-(2) content with no on-disk citation

## Four-phase protocol

### Phase 1 — Extract (verbatim from the JSONL)

The JSONL transcript is the canonical source. Extract assistant text and locate the content boundary by section anchor (preferred) or line range (fallback).

```bash
bash scripts/extract-anchor-range.sh \
  --jsonl ~/.claude/projects/<scope>/<project-uuid>.jsonl \
  --start-anchor "^## LOG #2 — Hooks: Complete Reference" \
  --end-anchor "^## LOG #3 — Subagents: Complete Reference" \
  --output "$CLAUDE_JOB_DIR/extracted-log-2.md"
```

The script:
1. Filters `assistant`-type entries, concatenates `.message.content[].text` via `jq`.
2. Greps for the start anchor; bails with non-zero exit if not found (Universal Rule #12: verify before acting).
3. Greps for the end anchor; if absent, falls back to EOF.
4. Writes verbatim slice to `$CLAUDE_JOB_DIR` (background-session safe path).

**Verbatim is non-negotiable.** The transcript is the canonical version; re-authoring breaks the audit trail. Future drift-reconciliation by `artifact-resurfacing` should be able to grep the transcript for the same string and find it.

### Phase 2 — Frontmatter (canonical, mirrors LOG #1 precedent)

Prepend the standard frontmatter block. Required fields:

```yaml
---
title: <Subject> — <Reference-Type>
date: <YYYY-MM-DD of original delivery, not promotion date>
scope: home (~/.claude/plans/) | repo (<path>) | organ (<organ>)
status: reference
extracted_from: <jsonl-path>
extraction_date: <YYYY-MM-DD of promotion>
related:
  - <sibling-artifact-paths>
  - <upstream-doc-urls>
  - <series-siblings if part of a series>
---

# <Title>

## Why this file exists

<One-paragraph rationale: who delivered it, when, why it's being promoted now, what precedent it mirrors.>

---

<verbatim extracted content>
```

For series content (LOG #N), the `related:` block includes all siblings in the series, allowing later members to grep-discover earlier ones via the cross-link.

```bash
python3 scripts/propose-frontmatter.py \
  --title "Claude Code Hooks — Complete Options Reference" \
  --date 2026-05-20 \
  --scope home \
  --extracted-from ~/.claude/projects/-Users-4jp/9cb55c4d-3191-4b61-a8e8-192e4710affb.jsonl \
  --series engine-log \
  --series-index 2 \
  --body "$CLAUDE_JOB_DIR/extracted-log-2.md" \
  --output ~/.claude/plans/2026-05-20-hooks-options-reference.md
```

The script enforces the schema, prepends frontmatter, prints the resulting file path. Slug convention: `YYYY-MM-DD-<topic-slug>-options-reference.md` for engine-log series; `YYYY-MM-DD-<topic-slug>.md` for one-offs.

### Phase 3 — Propagate (the chezmoi gotcha workaround)

Bash-redirect / `cat >` file creation bypasses the PostToolUse `Write|Edit` hook that fires `domus-memory-sync`. The runtime file exists but never reaches chezmoi-source or remote. **This is a documented silent-failure class** — see `references/known-promotion-pitfalls.md`.

Manual recovery is the chezmoi-documented protocol:

```bash
bash scripts/propagate-via-chezmoi.sh ~/.claude/plans/2026-05-20-hooks-options-reference.md ~/.claude/plans/2026-05-20-subagents-options-reference.md
```

The script:
1. Runs `chezmoi add <runtime-paths>` to copy runtime → source.
2. autoCommit+autoPush fires from chezmoi config (no separate `git push` needed for the chezmoi-source repo).
3. Verifies parity: `git -C <chezmoi-source> log @{u}..HEAD --oneline` should be empty.
4. If parity check fails, surfaces the divergence to the user and stops.

For non-chezmoi-managed plan files (per-repo `.claude/plans/`), the script falls back to `git add` + manual-commit-and-push surfacing.

### Phase 4 — Register (in any applicable series)

A solitary promoted artifact is durable. A *series* member needs registration so future members can discover the canonical series register.

For the engine-log series (`LOG #N` pattern), update `references/engine-log-series.md` in this skill with the new entry:

```markdown
| N | YYYY-MM-DD | Topic | Slug | Genesis session |
|---|---|---|---|---|
| 1 | 2026-05-20 | statusLine | 2026-05-20-statusline-options-reference | 9cb55c4d |
| 2 | 2026-05-20 | Hooks | 2026-05-20-hooks-options-reference | 9cb55c4d (extracted 2026-05-22 in beeff468) |
| 3 | 2026-05-20 | Subagents | 2026-05-20-subagents-options-reference | 9cb55c4d (extracted 2026-05-22 in beeff468) |
| ... | ... | ... | ... | ... |
```

For ad-hoc one-off promotions (not part of a series), no register update needed — the artifact's frontmatter `related:` cross-links suffice.

If promotion exposes a new silent-failure class (e.g., a new way auto-sync gets bypassed), append a row to `references/known-promotion-pitfalls.md` and surface an IRF row proposal. The skill's prevention surface grows monotonically.

## What this skill explicitly does NOT do

- Edit `CLAUDE.md`, `MEMORY.md`, `governance-rules.json`, `registry-v2.json`, any `seed.yaml`, or `INST-INDEX-RERUM-FACIENDARUM.md` directly. IRF row proposals surface to the user.
- Re-author or paraphrase transcript content (verbatim only — see Phase 1).
- Promote content that lives in `<system-reminder>` blocks or `<command-message>` blocks (those are infrastructure, not deliverable content).
- Cross-organ push to public ORGANVM `main` without explicit per-session push authorization.
- Run as a background daemon, cron, or LaunchAgent (Universal Rule #9 — HARD RULE).
- Batch-promote without per-artifact frontmatter (each promoted file is independently citable).
- Auto-fire on every closeout (closeout walks back and *suggests*; user invokes this skill).

## Scripts

- `scripts/extract-anchor-range.sh` — anchor-bounded transcript extractor; verifies anchors exist (Rule #12) before slicing.
- `scripts/propose-frontmatter.py` — frontmatter generator with schema validation and series-aware `related:` linking.
- `scripts/propagate-via-chezmoi.sh` — chezmoi-add wrapper with parity verification; surfaces non-chezmoi targets for manual push.

## References

- `references/engine-log-series.md` — register of the LOG #N series; living document, append-only.
- `references/known-promotion-pitfalls.md` — silent-failure classes encountered during promotion; append-only.
- `references/composition-with-closeout.md` — how this skill chains with `/closeout` (closeout flags candidates; this skill executes the promotion).
- `references/composition-with-artifact-resurfacing.md` — the inverse-motion pair; when to invoke which.

## Examples

- `examples/2026-05-20-engine-logs-2-and-3.md` — the genesis case: LOG #2 (Hooks) and LOG #3 (Subagents) extracted from JSONL `9cb55c4d` and promoted to plan files in session `beeff468` (2026-05-22). Full protocol trace including the silent-failure discovery for bash-redirect bypass of auto-sync.

## Anti-patterns

- Re-authoring transcript content from memory (Phase 1 must be verbatim grep+slice; if anchors don't match, fix anchors or use line-range fallback)
- Promoting `<system-reminder>` infrastructure as if it were substantive content
- Skipping Phase 3 because "the file is on disk already" (without chezmoi propagation, Universal Rule #2 is unmet)
- Promoting before the closeout has flagged candidates (close out first, then promote what closeout surfaces; reverses the dependency)
- Treating series register as ceremony — it's the discovery surface for the next session
- Inventing the `extracted_from:` field when the transcript has rotated out (if the JSONL is gone, the canonical source is gone; surface this rather than backfill)
- Cross-organ push to public main without explicit per-session authorization (surface the push decision)

## Universal rules this skill is built around

- **Universal Rule #2** — Nothing local only. Phase 3 is the literal operationalization: runtime file → chezmoi-source → remote.
- **Universal Rule #6** — Fix bases, not outputs. Phase 4's series register is the base for "next LOG"; codification grows the prevention surface, not just the symptom fix.
- **Universal Rule #8** — Plans are artifacts. Promoted content becomes a plan file under the standard `~/.claude/plans/YYYY-MM-DD-{slug}.md` discipline.
- **Universal Rule #9** — No LaunchAgents. Promotion is on-demand only.
- **Universal Rule #12** — Memory is hypothesis. Phase 1 requires anchor-verification before slicing; never trust a remembered anchor without grep-verifying it in the current transcript.

## Composition with other tools/ skills

| Skill | Role | When |
|---|---|---|
| `closeout` | discovers candidates | end of session; flags "inline only" deliverables |
| `transcript-promotion` (this) | executes the promotion | when user invokes or when closeout candidates need durability |
| `artifact-resurfacing` | inverse motion | when promoted content's *citation* later goes stale and needs reconciliation |
| `cross-agent-handoff` | carries the register | promotion register travels in the handoff to the next session |
| `qa-audit` | verifies promotion success | after promotion, audits whether all candidates actually landed on disk + remote |
| memory consolidation (platform tool, if available) | indexes new artifacts | promoted plan files referenced from memory via `[[name]]` links get curated here |

## Why "ongoing unfurling expansion"

The skill is designed to grow monotonically without ever overwriting itself:

- **Series register** (`references/engine-log-series.md`) — append-only; LOG #N grows to N+1, N+2, ad infinitum.
- **Pitfall register** (`references/known-promotion-pitfalls.md`) — append-only; each new silent-failure class discovered during promotion gets a row.
- **Examples** — append-only; each genesis case becomes a worked example for future invocations.
- **Scripts** — versioned; new extraction patterns (anchor regex variants, multi-section windowing) extend rather than replace the base extractor.

The skill ages well because every new use case enriches the prevention surface. Drift is detected, codified, and surfaced — not papered over.
