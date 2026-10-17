# Composition with /closeout

The `/closeout` skill discovers candidates for promotion; `transcript-promotion` executes
the promotion. They are sequential, not redundant.

## How closeout flags candidates

The `/closeout` skill walks back through deliverables and marks each with a closure
status. Some deliverables don't fit the standard closure classes (DONE-NNN executed,
IRF-XXX-NNN in-progress, abandoned/) because they're substantive references delivered
inline that have no on-disk artifact yet. Closeout flags these as:

> "Inline only; not file-persisted by Claude"

The closeout summary table for the genesis session looked like:

```
| Log | Topic | Disposition |
|---|---|---|
| #1 | statusLine | Persisted by user to `response.md` |
| #2 | Hooks | Inline only; not file-persisted |
| #3 | Subagents | Inline only; not file-persisted |
```

The "inline only" rows are the candidates. They survive in the JSONL transcript but
are invisible to the plan-file pipeline.

## When to invoke promotion

Two valid invocation patterns:

**Same-session promotion** — user invokes `transcript-promotion` directly in the same
session that delivered the inline content. The transcript path is the active session's
`.jsonl`; anchors are still warm in the assistant's working memory.

**Cross-session promotion** — user resumes a later session (or a different agent reads
the prior session's transcript) and invokes `transcript-promotion` with the explicit
JSONL path. This is the more common case because closeout naturally bundles "make
durable" decisions for a later, calmer pass.

The genesis case (LOG #2 + #3, 2026-05-22 session `beeff468`) was the cross-session
variant: original delivery 2026-05-20 in `9cb55c4d`; promotion two days later when the
user asked "all unique data survives present context upon exit?" The audit table
exposed the candidate; the promotion protocol made it durable.

## Why closeout doesn't do the promotion itself

Closeout is broad and ritualized — it does plan walkback, atom walkback, git
verification, autogen freshness gate, working-state capture, summary write. Adding
extraction-and-frontmatter mechanics would balloon the skill and conflate "audit" with
"reconstruct." The split honors single-responsibility:

- Closeout: *Do all the audit work and surface candidates.*
- Promotion: *Take a named candidate and make it durable.*

The handoff between them is a flagged row in the closeout summary, not an automatic
invocation.

## Sequence diagram

```
user invokes /closeout
  └─ closeout walks back deliverables
       └─ flags inline-only candidates in summary
            └─ user reviews summary
                 └─ user invokes transcript-promotion with a named candidate
                      └─ Phase 1: extract from JSONL
                           └─ Phase 2: prepend frontmatter
                                └─ Phase 3: propagate via chezmoi
                                     └─ Phase 4: register in series (if applicable)
```

Both skills are propose-not-apply for constitutional surfaces. Neither silently mutates
`CLAUDE.md` or `MEMORY.md` based on what it surfaces; both defer to the conductor.

## When NOT to invoke promotion

- Closeout flagged something but the user didn't name it — wait for the user to confirm
  the candidate. (Universal Rule #21: do what is asked.)
- The transcript JSONL has rotated out and the canonical source is gone — surface this
  rather than reconstruct from memory.
- The "inline content" is actually a `<system-reminder>` or `<command-message>` block —
  these are infrastructure, not deliverables.
- The deliverable was code that's already in a file — there's nothing to promote.
