---
name: shell-history-hygiene
description: Dry-run audit + targeted cleanup for shell command history. Currently wraps atuin (stats today, prune, dedup with dated preview artifacts); extensible to zsh/bash/mcfly backends. Always previews before applying — apply commands are echoed for the human to run, never auto-executed. Triggers on "/shell-history-hygiene", "audit atuin", "audit shell history", "clean shell history", "atuin prune", "atuin dedup", "shell history hygiene", "history cleanup". Replaces ad-hoc one-liners (e.g. `... | tee cmd > file.txt` which wrote two files, swallowed dedup output, and left a junk `cmd` file).
license: MIT
complexity: beginner
time_to_learn: 5min
tags:
  - shell
  - history
  - atuin
  - hygiene
  - audit
  - dry-run
  - preview-then-apply
inputs:
  - atuin-history-state
  - optional-dedup-cutoff-date
outputs:
  - prune-preview-file
  - dedup-preview-file
  - headline-summary
  - echoed-apply-commands
side_effects:
  - creates-files
  - runs-commands
triggers:
  - user-says-audit-atuin
  - user-says-clean-shell-history
  - user-says-atuin-prune
  - user-says-atuin-dedup
  - user-says-shell-history-hygiene
  - before-history-store-migration
---

# shell-history-hygiene — Shell-History Audit + Targeted Cleanup

## When to invoke

- User explicitly asks to audit / clean / dedup / prune their shell history (atuin or otherwise)
- User pasted an ad-hoc `atuin stats / prune / dedup` one-liner and asked for review or improvement
- Before any history-store migration (atuin → atuin v2, zsh-only → atuin, etc.) where you want a clean baseline
- During machine-setup audits where the history corpus is being inspected for size or quality

## Backends

- **atuin** (current): `atuin stats today`, `atuin history prune`, `atuin history dedup`
- **zsh native** (future): `.zsh_history` line dedup, size limits
- **bash native** (future): `.bash_history` line dedup
- **mcfly** (future): mcfly's own pruning

This skill currently ships the atuin backend at `scripts/atuin-audit.sh`. Add sibling scripts under `scripts/` as backends are added.

## How it works (preview-then-apply)

The audit is **dry-run only**. It produces three things:

1. A headline summary on the terminal — `atuin stats today` + counts.
2. Two dated preview artifacts on disk — one per operation (prune, dedup) — for human inspection.
3. Echoed apply commands at the end — copy/paste shapes that the human runs manually.

The skill never runs the apply commands itself. Separation of audit from apply is deliberate — it's the kill-switch against accidental history destruction.

## Running the audit

```bash
${CLAUDE_SKILL_ROOT}/scripts/atuin-audit.sh           # dedup --before defaults to today
${CLAUDE_SKILL_ROOT}/scripts/atuin-audit.sh 2026-05-01  # dedup --before <date>
```

If `${CLAUDE_SKILL_ROOT}` isn't resolved by the harness, use the absolute path:

```bash
/Users/4jp/Code/organvm/a-i--skills/skills/tools/shell-history-hygiene/scripts/atuin-audit.sh
```

Preview artifacts land alongside the script:
- `atuin-prune-preview-YYYY-MM-DD.txt`
- `atuin-dedup-preview-YYYY-MM-DD.txt`

Dated filenames preserve a trail — re-runs don't clobber prior previews.

## Interpreting output

| Headline | Meaning |
|---|---|
| `prune entries: N` | atuin's own "Found N entries to prune" — structural no-ops (empty commands, repeated `clear`, paste-glitch duplicates). Almost always safe to prune. |
| `dedup duplicates: M` | atuin's own "Found M duplicates to delete" — exact-string repeats older than `--before`. Inspect a sample before applying; large M (10K+) is normal across months of history. |
| `(N lines in preview, multi-line commands expand)` | The preview file may have more lines than the entity count because multi-line commands (HEREDOCs, `for` loops) take multiple lines each. Trust the headline number, use the line count for file-size context. |

## Applying the cleanup

After the human eyeballs the preview and approves:

```bash
atuin history prune                                          # apply prune
atuin history dedup --before "$BEFORE_DATE" --dupkeep 1     # apply dedup (keep 1 copy per duplicate string)
```

Run in that order. Prune first removes the structural no-ops; dedup then collapses the remaining exact-string repeats. Reverse order works but does redundant scanning.

`--dupkeep 0` is destructive (removes ALL copies). Never recommend it — `--dupkeep 1` is the right default.

## Safety / failure modes

- **Script preserves dry-run guarantee** — `set -euo pipefail`, never invokes apply commands.
- **`atuin` not on PATH** — script exits 1 with clear error. No partial action.
- **Multi-line commands in atuin** — the script's headline parses atuin's own "Found N" lines (not `wc -l`) so the count is accurate even when multi-line commands inflate the line total.
- **`--before` date in the future** — atuin accepts it; dedup just considers all history. Inspect preview before applying.

## Heritage / why this skill exists

Triggered by a 2026-05-21 review of an ad-hoc one-liner that had a `tee cmd > file.txt` bug — wrote two files, swallowed dedup output. The fix evolved into a dated-preview script, then into this skill so the workflow lives somewhere discoverable rather than as scratch material under `~/_dot-config/scratch/`. Per Rule #34 ("merge into ideal form") the function clarified beyond `scratch/`'s purpose, so it migrated here.

Original artifact birthplace: `~/_dot-config/scratch/atuin-audit.sh` (worktree commit `6d6ef39` on `_dot-config` main). This skill's `scripts/atuin-audit.sh` is the canonical-from-here copy.
