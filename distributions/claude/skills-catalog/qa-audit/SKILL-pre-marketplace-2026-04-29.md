---
name: qa-audit
description: Verify claims in a session/PR/transcript against on-disk reality. Produce a verification report (verified / false-positive / false-negative / partial) with explicit owners. STOP at verification — do not execute remediation without explicit approval.
---

# QA Audit

1. Read referenced session transcripts/artifacts fresh from disk
2. Verify each claim against on-disk reality (file exists, content matches, commit landed)
3. Mark each as: verified / false-positive / false-negative / partial
4. Produce remediation list with explicit owners
5. Stop at verification — do NOT execute remediation without explicit approval

<!--
HISTORICAL FORM — pre-marketplace, dated 2026-04-29 18:58.
Preserved 2026-05-17 per the additive-preservation principle.
Source: ~/Workspace/.claude/skills/qa-audit/SKILL.md (657 B).
Diff from canonical: missing `license: MIT` in frontmatter (canonical adds it).
Content otherwise byte-identical (5 numbered steps, same description).

This file is HISTORICAL and SHOULD NOT BE LOADED AS A SKILL — its filename
deliberately differs from SKILL.md so skill-loading globs skip it.

Plan: ~/.claude/plans/plan-for-completions-for-stateful-dove.md §5
-->
