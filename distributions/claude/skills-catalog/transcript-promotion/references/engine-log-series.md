# Engine Log Series — Register

Living register of the "LOG #N" engine-reference series. Append-only. Each row points
at a durable plan file produced by the `transcript-promotion` skill.

## What the series is

A user-driven pattern: substantive dense references to Claude Code surfaces (statusLine,
hooks, subagents, etc.) delivered inline as "engine logs", then promoted to plan files
under the standard `~/.claude/plans/YYYY-MM-DD-{slug}-options-reference.md` slug.

Each entry follows the same internal shape:
- Settings block / configuration surface
- Payload fields / schema details
- Execution behavior / lifecycle semantics
- Environment variables
- Gap analysis vs the session-author's current setup
- Troubleshooting cheatsheet
- One closing `★ Insight ─────────────────` block

## Register

| # | Date | Topic | Slug | Genesis session | Promotion session |
|---|---|---|---|---|---|
| 1 | 2026-05-20 | statusLine | `2026-05-20-statusline-options-reference.md` | `9cb55c4d` | same (user persisted in-flow) |
| 2 | 2026-05-20 | Hooks | `2026-05-20-hooks-options-reference.md` | `9cb55c4d` | `beeff468` (2026-05-22) |
| 3 | 2026-05-20 | Subagents | `2026-05-20-subagents-options-reference.md` | `9cb55c4d` | `beeff468` (2026-05-22) |

## Candidate LOG #4+ topics

Surfaced from session `9cb55c4d` cross-agent handoff as natural next branches:

- **settings.json complete schema** — the umbrella holding statusLine + hooks + permissions + MCP + agent setting
- **Skills** — SKILL.md spec, frontmatter fields, the Skill tool, namespacing, plugin-scoped skills
- **Plugin manifest** — `.claude-plugin/plugin.json`, marketplace, namespacing
- **MCP server configuration** — types (stdio/http/sse/ws), `.mcp.json`, server-name namespacing
- **Slash commands** — built-in vs user vs plugin, frontmatter

Each is a natural LOG #4. Series-index assignment is first-come-first-claimed at the
moment of promotion, not pre-allocated.

## Series invariants

- **Verbatim from transcript** — Phase 1 of `transcript-promotion` slices the JSONL by
  anchor; the body is canonical.
- **Same shape** — each member has the same internal sections, making cross-series grep
  workable.
- **Cross-linked** — each plan file's frontmatter `related:` block names the other
  members so a reader landing on LOG #5 can walk back to LOG #1.
- **Open** — N grows monotonically; no compaction or supersession.

## Adding a new entry

1. Invoke `transcript-promotion` with `--series engine-log --series-index <N>`.
2. The Phase 2 frontmatter generator auto-includes prior siblings in `related:`.
3. After promotion succeeds, append a row to this register.
4. Commit the register update alongside any other skill-repo changes in the same PR.

Do NOT pre-allocate slots in this register before promotion succeeds. The register
records *what happened*, not *what is planned*.
