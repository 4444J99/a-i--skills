# Constitutional-Doc Policy

Rules for what may and may not be auto-edited by this skill. Read alongside `../SKILL.md` Phase 3 (Polish).

The skill's core discipline is **propose-not-apply** for constitutional surfaces. This file enumerates which surfaces are constitutional, why, and what the proposal-vs-application boundary looks like in practice.

## What is "constitutional"

A file is **constitutional** when its content shapes the behavior of future sessions or the routing of future work. Editing it changes the rules, not just the data.

Constitutional files in this workspace include:

- All `CLAUDE.md` at any scope (home, workspace, organ, repo)
- All `MEMORY.md` in `~/.claude/projects/*/memory/`
- All `seed.yaml` (each repo's automation contract)
- `governance-rules.json` (dependency rules in ORGAN-IV)
- `registry-v2.json` (~2,200 lines, single source of truth for ~97 repos)
- `system-metrics.json` (computed metrics)
- All SOP-prefixed docs in `standards/` directories (process specifications)

A file is **operational** when it tracks state but does not change rules. Operational files include:

- `INST-INDEX-RERUM-FACIENDARUM.md` (work registry — adds/closes rows but doesn't change rule schema)
- `polish-log.md` (this skill's own append-only log)
- `outreach-log.yaml`, `network.yaml`, `contacts.yaml`, `signal-actions.yaml` (signal logs)
- `ratings/*.json` (rater outputs)
- Plan files in `~/.claude/plans/*.md` (work artifacts, versioned via `-v2` suffix not edited in place)

This skill freely writes to operational files (with the constraints noted below). It never writes to constitutional files without same-session conductor authorization.

## Why the distinction matters

Constitutional drift is hard to detect. A misplaced rule in `CLAUDE.md` routes future sessions in subtly wrong directions for weeks. A misplaced row in `outreach-log.yaml` is visible the next time the file is read.

Constitutional edits also tend to be **multi-scope**: changing one CLAUDE.md often implies changing related CLAUDE.md files at sibling scopes. Coordinated multi-file edits need authorization more than single-file edits do.

This skill's discovery of drift in a constitutional file generates a *proposal*. The proposal includes:

- The exact unified diff
- The class of finding (stale-citation, missing-never-written, missing-lost, orphan-plan)
- The evidence (`find` output, `grep` output, mtime check)
- A one-line authorization request: "May I apply this diff to <file>?"

The conductor reads the proposal and either:

- Authorizes the diff (skill applies via Edit tool)
- Rejects the diff (skill records rejection in polish-log)
- Modifies the diff (conductor edits the proposal, skill applies the modified version)
- Defers (skill records "deferred to next session" and moves on)

## What may be auto-edited without authorization

These are explicit carve-outs from the propose-not-apply rule:

1. **Polish-log entries** in the affected repo. This is the skill's own log; appending is mechanical.
2. **IRF row proposals** in `polish-log.md` (proposal text, not the IRF file itself).
3. **Deep-search command emission** to stdout. Running `find` and `grep` is read-only.
4. **Citation audit JSONL output** to stdout. Also read-only.
5. **Genesis case study addition** to `examples/` in this skill's own source dir. Additive, not modifying constitutional content.

These exceptions are narrow. They cover the skill's own logging and its own bundled-resource maintenance. Everything else is propose-only.

## What may NEVER be auto-edited

Per memory rule #21 ("Do what is asked — never preempt") and the home-level CLAUDE.md "Executing actions with care" guidance:

- `CLAUDE.md` at any scope — even when the autogen footer is the cited authority, the body still needs conductor sign-off
- `MEMORY.md` and any of its companion `<type>_<slug>.md` memory files
- `seed.yaml`
- `governance-rules.json`
- `registry-v2.json`
- `system-metrics.json`
- Production data files protected by `save_registry()` 50-repo guard
- `prompt-atoms.json` (24,599+ atoms, 73 MB — protected by atom-permanence rule)

Even when this skill is invoked on a session where the conductor has previously authorized similar edits to similar files, each new constitutional edit needs its own authorization. Previous authorization does not transfer.

## What "proposal" looks like in practice

A proposed diff for a stale-citation looks like:

```diff
--- a/Users/4jp/Workspace/4444J99/application-pipeline/CLAUDE.md
+++ b/Users/4jp/Workspace/4444J99/application-pipeline/CLAUDE.md
@@ -298,3 +298,3 @@
 - Authority dissertation: `meta-organvm/praxis-perpetua/research/dissertation-institutional-authority/`
+- Authority dissertation: `~/Code/organvm/praxis-perpetua/research/dissertation-institutional-authority/`
```

The proposal is emitted to stdout by `scripts/propose-citation-fix.py`. The conductor sees it and decides. The skill **never** pipes the diff to `patch` or to the Edit tool without an authorization step.

## The autogen-block exception

CLAUDE.md files often carry autogen sections delimited by `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->` sentinels. Content inside the autogen block is re-written by `organvm refresh` (or `organvm context sync --write`) on each invocation.

For autogen content, the polish action is different:

- **Do NOT** edit the autogen block directly. The next `organvm refresh` overwrites the edit.
- **Do** propose updating the *source* that the autogen block reads from. The source might be `seed.yaml`, `registry-v2.json`, or an `organvm-engine` data file.
- **Do** flag autogen-block drift as a separate finding class (root cause in the source data, symptom in the autogen output). Universal Rule #6 applies: fix bases, not outputs.

If a citation appears in the autogen block (e.g., the workspace `CLAUDE.md` System Library section that cites `~/Code/organvm/praxis-perpetua/library`), and the citation is correct (which the genesis session confirmed it is), the finding is **not stale** — the autogen knows the truth even when the body lags. Cross-check autogen content against body content before declaring drift.

## When the conductor authorizes a batch

The conductor may say "yes, apply all of those" after reading a multi-finding polish-log. This is a same-session batch authorization and is allowed. The skill then runs Edit for each proposal, but:

- One Edit per file (do not chain Edits across multiple files in one tool call)
- Verify each Edit succeeded before moving to the next
- If any Edit fails, stop and surface the failure — do not continue applying the remaining proposals

Batch authorization does not transfer to future sessions. The next session starts fresh.

## Recovery from a misapplied edit

If this skill applies an edit and the conductor later rejects it, recovery is:

1. `git diff HEAD` to confirm the misapplied content
2. `git checkout -- <file>` to revert the working tree
3. Append a polish-log entry recording the misapplication and the recovery
4. Surface the failure mode to the conductor for future-fixing (perhaps Phase 4 codification needed on this skill itself)

This skill never uses `git reset --hard`, `git push --force`, or any destructive git operation as part of recovery. Those require explicit conductor authorization per workspace CLAUDE.md.

## Summary

| Surface | Read | Propose | Apply without auth | Apply with auth |
|---|---|---|---|---|
| Constitutional (CLAUDE.md, MEMORY.md, seed.yaml, etc.) | ✓ | ✓ | ✗ | ✓ (one diff at a time) |
| Operational (polish-log, IRF proposals, ratings) | ✓ | ✓ | ✓ (append-only) | ✓ |
| Autogen blocks (between ORGANVM:AUTO sentinels) | ✓ | propose edit to source | ✗ | propose edit to source then organvm refresh |
| This skill's own bundled resources (examples/, references/) | ✓ | ✓ | ✓ (additive only) | ✓ |
| Production data files (registry-v2.json, prompt-atoms.json, system-metrics.json) | ✓ | ✓ | ✗ | propose only; mutations route through canonical CLIs |

The rule is simple: read freely, propose freely, apply carefully.
