---
name: code-review-checklist
description: Guide an AI agent through a structured code review — correctness, security, performance, readability, and test coverage — producing a summary with actionable, prioritized feedback. Triggers on pull-request review, diff review, or "review this code" requests.
license: MIT
complexity: beginner
time_to_learn: 30min
tags:
  - code-review
  - quality
  - security
  - checklist
  - pull-request
governance_phases: [prove]
organ_affinity: [all]
triggers: [user-asks-about-code-review, context:pull-request, context:diff-review, file-type:*.diff, file-type:*.patch]
complements: [code-refactoring-patterns, verification-loop, testing-patterns, coding-standards-enforcer]
---

# Code Review Checklist

A structured checklist for reviewing code changes — whether a diff, a pull request, or a
single file — that keeps feedback consistent, prioritized, and actionable instead of
scattered or stylistic-only.

## When to Use

- Reviewing a pull request or diff before merge
- A human or another agent asks "review this code"
- Self-review before opening a PR
- Auditing an existing file for latent issues

## The Five Dimensions

Work through each dimension in order. Skip a dimension only if it is genuinely inapplicable
(e.g. "performance" for a docs-only change) — say so explicitly rather than silently omitting it.

### 1. Correctness

- Does the change do what it claims to do? Trace the logic against the stated intent (PR
  description, issue, commit message).
- Are edge cases handled: empty input, null/None, zero, negative numbers, empty collections,
  concurrent access, off-by-one boundaries?
- Do error paths actually handle errors, or just swallow/log and continue silently?
- Does it introduce a regression? Diff against prior behavior, not just the new code in isolation.
- Are there any logic inversions (`==` vs `!=`, `&&` vs `||`, inclusive vs exclusive bounds)?

### 2. Security

- Untrusted input: is anything from a user, network request, file, or environment variable
  interpolated into a shell command, SQL query, HTML template, or file path without sanitization?
- Secrets: any hardcoded credentials, tokens, or keys — including in test fixtures or comments?
- Authorization: does the change check permissions/ownership before acting, or does it trust a
  client-supplied ID?
- Dependency risk: does it add a new third-party dependency, and if so, is it maintained and
  reasonably scoped?
- Injection classes to scan for explicitly: command injection, SQL injection, path traversal,
  SSRF, log injection (unsanitized values written to logs an operator later greps/pastes), and
  unpinned/mutable CI Action tags used as a supply-chain vector.

### 3. Performance

- Any obviously quadratic-or-worse operation on a collection that could be large in production
  (nested loops over the same dataset, repeated linear scans)?
- N+1 query patterns (a loop issuing one DB/API call per iteration instead of batching)?
- Unbounded growth: does the change introduce a cache, buffer, or accumulator with no eviction
  or size cap?
- Are expensive operations (network calls, disk I/O, crypto) on a hot path that could be
  memoized, batched, or moved off it?

### 4. Readability & Maintainability

- Can a stranger to this code understand the change from the diff and its names alone, without
  needing the author's context?
- Is the change scoped to one concern, or does it mix refactoring with new behavior (making the
  diff harder to review and revert)?
- Are names accurate and specific (not `data`, `temp`, `handleStuff`)?
- Is there dead code, commented-out blocks, or leftover debug output (`console.log`, `print`,
  `pdb.set_trace()`) left in?
- Does it follow the file's/repo's existing conventions (formatting, error-handling style,
  module layout) rather than introducing a new one inconsistently?

### 5. Test Coverage

- Does the change include tests for the new behavior, or only for the happy path?
- Are the edge cases identified in "Correctness" above actually covered by a test, not just
  mentioned in a comment?
- If a bug is being fixed, is there a regression test that would have caught it — i.e. does the
  new test fail against the old code and pass against the new code?
- Do existing tests still pass, and did the change quietly weaken an assertion to make them pass
  (e.g. loosening a strict equality check, or adding a broad `try/except: pass`)?

## Output Format

Produce a summary, not a transcript of every line examined:

```
## Code Review: <file/PR>

**Correctness**: <finding or "no issues found">
**Security**: <finding or "no issues found">
**Performance**: <finding or "no issues found">
**Readability**: <finding or "no issues found">
**Test Coverage**: <finding or "no issues found">

### Priority Actions
1. <highest-priority fix, with file:line>
2. <next priority>
...
```

- Order findings by actual risk/impact, not by which dimension they came from.
- Cite `file:line` for every finding — a review comment without a location is not actionable.
- Distinguish a **blocking** issue (correctness bug, security hole, missing critical test) from a
  **suggestion** (style, minor readability nit) — do not let nits drown out real defects.
- Never comment on formatting a linter/formatter already enforces automatically.

## Anti-Patterns to Avoid

- **Rubber-stamping**: approving without tracing at least the changed logic paths against their
  stated intent.
- **Style-only reviews**: flagging naming/formatting while missing a real correctness or security
  defect in the same diff.
- **Vague feedback**: "this could be cleaner" without a concrete alternative.
- **Reviewing in isolation**: judging a diff hunk without reading enough surrounding context to
  know whether it's actually correct in situ.
