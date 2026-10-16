# Genesis Case — LOG #2 (Hooks) + LOG #3 (Subagents)

Worked example: the session that exercised the protocol that became this skill.

## Setting

- **Delivery session**: `9cb55c4d-3191-4b61-a8e8-192e4710affb` (2026-05-20)
  - User invoked an "engine logs" pattern: dense reference deliveries to Claude Code
    surfaces, persisted by the user into a `response.md` file.
  - LOG #1 (statusLine) was promoted to a plan file in the same session.
  - LOG #2 (Hooks) and LOG #3 (Subagents) were delivered inline only.
- **Closeout** flagged the gap explicitly: "Inline only; not file-persisted".
- **Promotion session**: `beeff468` (2026-05-22, background-session shape)
  - Triggered by user question "all unique data survives present context upon exit?"
  - The audit table showed LOG #2 + #3 as `JSONL ✓ / plan file ✗`.
  - User issued the "find their gravitational logical center" cascade directive.

## Phase 1 — Extract

Transcript: `/Users/4jp/.claude/projects/-Users-4jp/9cb55c4d-3191-4b61-a8e8-192e4710affb.jsonl`
(2008 lines of JSONL).

```bash
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="text") | .text' \
  "$JSONL" > "$CLAUDE_JOB_DIR/assistant_text.md"
# → 1399 lines of assistant text
```

Anchors located:
- LOG #2 start: line 629 (`## LOG #2 — Hooks: Complete Reference`)
- LOG #3 start: line 991 (`## LOG #3 — Subagents: Complete Reference`)
- LOG #3 end: line 1274 (closing three-engine-stack Insight)

Slice boundaries:
- LOG #2: lines 629–989 (cut at `---` separator on line 990)
- LOG #3: lines 991–1274 (includes closing Insight that cross-references LOG #1+#2+#3)

```bash
sed -n '629,989p' assistant_text.md > hooks_body.md      # 361 lines
sed -n '991,1274p' assistant_text.md > subagents_body.md # 284 lines
```

## Phase 2 — Frontmatter

Standard frontmatter prepended via `cat <frontmatter> <body>`:

```yaml
---
title: Claude Code Hooks — Complete Options Reference
date: 2026-05-20
scope: home (~/.claude/settings.json)
status: reference
extracted_from: /Users/4jp/.claude/projects/-Users-4jp/9cb55c4d-3191-4b61-a8e8-192e4710affb.jsonl
extraction_date: 2026-05-22
related:
  - ~/.claude/settings.json (34-hook census; PreToolUse/SessionStart/etc.)
  - https://code.claude.com/docs/en/hooks.md
  - 2026-05-20-statusline-options-reference.md (LOG #1 sibling)
  - 2026-05-20-subagents-options-reference.md (LOG #3 sibling)
---
```

LOG #3 used the same shape with reciprocal cross-links.

Output files:
- `~/.claude/plans/2026-05-20-hooks-options-reference.md` (14294 bytes)
- `~/.claude/plans/2026-05-20-subagents-options-reference.md` (16298 bytes)

Both comparable in scale to the prior LOG #1 reference (13583 bytes). Pattern matches.

## Phase 3 — Propagate (the silent-failure discovery)

Verification step exposed the silent-failure: `ls <chezmoi-source>/<mirror>` returned
"No such file". The auto-sync hook had NOT fired.

Root cause analysis:
- `domus-memory-sync` is a `PostToolUse` hook on `Write|Edit` tools.
- Phase 2 used bash heredoc (`cat <frontmatter> <body> > <output>`), which doesn't invoke
  the `Write` tool.
- The hook predicate is correct; the *tool*-class invocation was wrong.

This is structurally distinct from a previously-known silent-failure class
([[2026-05-22-resumed-closeout-audit]]) where `closeout-*.md` files mysteriously skip
auto-sync. Same symptom (file local-only), different cause. Recorded as TP-01 in
`references/known-promotion-pitfalls.md`.

Recovery (the chezmoi-documented protocol):

```bash
chezmoi add ~/.claude/plans/2026-05-20-hooks-options-reference.md \
            ~/.claude/plans/2026-05-20-subagents-options-reference.md
# → [master f231c37] Add .claude/plans/...
#    2 files changed, 693 insertions(+)
# → To https://github.com/4444J99/domus-semper-palingenesis.git
#    3a86ccd..f231c37  master -> master
```

Parity verification:

```bash
git -C ~/Workspace/4444J99/domus-semper-palingenesis log @{u}..HEAD --oneline
# → (empty — 0/0 parity confirmed)
```

Universal Rule #2 ("nothing local only") satisfied.

## Phase 4 — Register

Series register at `references/engine-log-series.md` updated with rows for LOG #2 and
LOG #3, linking both back to genesis session `9cb55c4d` and promotion session
`beeff468`.

The closing three-engine-stack Insight from the original transcript (`statusLine +
hooks + subagents form a stack`) was preserved at the tail of LOG #3's plan file
because it's the *cross-reference between all three logs* — it has no other natural
home.

## Outcomes

After promotion:
- Local disk: 3/3 engine logs durable in `~/.claude/plans/`
- Chezmoi-source: 3/3 mirrored
- Remote (`origin/master`): 3/3 pushed
- Cross-referenced in `2026-05-20-cross-agent-handoff.md`'s `related:` block
- Two findings filed for future codification (bash-redirect bypass; INDEX.md stale)

User's original question — "all unique data survives present context upon exit?" —
answered yes, after the protocol now codified in this skill ran end-to-end.

## What this case taught the skill

1. **Phase 1 verbatim is non-negotiable.** Re-authoring would break audit grep against
   the transcript.
2. **Phase 3 must verify, not assume.** `ls <chezmoi-source>` after Phase 2 is the
   verification step that exposed TP-01.
3. **Anchor extraction needs both start and end anchors verified before slicing.**
   `extract-anchor-range.sh` enforces this; the genesis case used manual `awk` for the
   same effect.
4. **The closing Insight (or other cross-reference content) belongs in the *last*
   member of a series**, not the first or in a separate file. It anchors the cross-link
   for readers landing on any one member.
5. **Series register is the discovery surface for LOG #4+.** Without it, future
   promotions would re-discover the same patterns from scratch.
