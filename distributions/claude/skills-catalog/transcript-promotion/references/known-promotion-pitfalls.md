# Known Promotion Pitfalls — Silent-Failure Class Register

Append-only register of silent-failure classes encountered during transcript promotion.
Each row describes a way Phase 3 (propagate) can succeed-from-the-skill's-perspective
while actually failing-to-satisfy-Universal-Rule-#2.

The skill's prevention surface grows by appending here, not by editing the SKILL.md
protocol.

## Class register

| ID | Class | Symptom | Root cause | Detection | Mitigation |
|---|---|---|---|---|---|
| TP-01 | bash-redirect bypasses auto-sync | runtime file exists; chezmoi-source missing it | `domus-memory-sync` hook is PostToolUse on `Write\|Edit` tool — bash heredoc / `cat >` doesn't invoke either | `ls <chezmoi-source>/<mirror-path>` returns "No such file" after Phase 2 | Phase 3 manually runs `chezmoi add` per `propagate-via-chezmoi.sh`; never assume auto-sync fires |
| TP-02 | closeout-*.md files silently skip auto-sync | runtime closeout file exists; chezmoi-source missing it; root-cause-unknown | filename predicate match presumed-but-broken in `domus-memory-sync` for closeout pattern | manual `chezmoi add` works fine; only auto-fire is broken | run `chezmoi add` manually after closeout writes (precedent: [[2026-05-22-resumed-closeout-audit]]) |
| TP-03 | INDEX.md regenerator stale | promoted files don't appear in `~/.claude/plans/INDEX.md` even after propagation | INDEX.md is a generated artifact whose regeneration script is not running on a regular cadence (≥5 weeks stale as of 2026-05-22) | `tail INDEX.md` shows date months in the past while plans directory has recent files | rely on plan-file presence + frontmatter cross-links for discoverability; do not treat INDEX.md absence as Phase 3 failure |

## How to add a row

1. During or after a promotion, you observe a way the artifact failed-to-fully-propagate.
2. Reproduce or confirm the cause (do not guess — Universal Rule #12).
3. Append a row with the next `TP-NN` ID.
4. If the class warrants tracking in corpvs IRF, surface an IRF row proposal to the user
   with `surfaced_by: transcript-promotion`.

## Why this register exists

The first promotion (2026-05-22, session `beeff468`) discovered TP-01 unprompted, by
verifying chezmoi-source after Phase 2 and finding the mirror absent. Without that
verification step, the skill would have reported success while leaving Universal Rule #2
unmet. The verify-then-claim pattern is now mandatory in Phase 3 (see SKILL.md and
`propagate-via-chezmoi.sh`).

Subsequent promotions should run the same verification and append here when new
failure modes appear. The skill is stronger every time it encounters new drift.
