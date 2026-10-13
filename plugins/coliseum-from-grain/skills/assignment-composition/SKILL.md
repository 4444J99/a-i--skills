---
name: assignment-composition
description: Wraps each surfaced dimension as a self-contained 9-section autonomous-work-assignment envelope — scope, context, success criteria, allowed tools, return format, handoff — all the recipient subagent needs to execute without coming back. Use when invoked by coliseum-orchestrator as Phase 2; when dimensions are named and the next step is to make each independently dispatchable; or when the user asks "compose this as an assignment." The no-pingpong gate validates each envelope before dispatch.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: <path to phase-1-dimensions.md>
---

# Assignment Composition

You are turning each named dimension into a self-contained autonomous-work-assignment envelope. After this phase, each envelope must be dispatch-ready — a recipient subagent reads only that envelope and executes, without needing to come back asking questions.

## The envelope standard

Every assignment envelope MUST contain all of the following sections. Missing any section means the envelope is incomplete and the no-pingpong gate will reject it.

### 1. Identifier

A short slug: `assignment-NNN-<dimension-slug>`. Stable across the rest of the protocol.

### 2. Scope (positive)

What the recipient is being asked to produce. One paragraph. Concrete, not abstract. If you cannot write this in one paragraph, the dimension is probably not yet pruned enough.

### 3. Scope (negative)

What the recipient is **not** being asked to produce. Lists adjacent work this assignment explicitly omits. This is where you preempt the "should I also do X?" question.

### 4. Context the recipient needs

Everything the recipient must know to execute. This is the section that, if incomplete, causes ping-pong. Include:

- Background the recipient cannot derive from the prompt alone.
- File paths, system names, link references, where to read upstream artifacts.
- Domain conventions specific to the user's environment.
- Any previously-rejected approaches and the reason they were rejected.

If the recipient is a fresh subagent with no memory of this conversation (assume so — they have none), they must be able to start work after reading this section alone.

### 5. Success criteria

A checklist of what makes this assignment "done." Each item must be:

- Observable (yes/no after looking at the return).
- Independently verifiable (does not require asking the originator).
- Sufficient — together, all checks being yes means the work is complete.

### 6. Allowed tools

Explicit list of tools the recipient may use. Default to a minimal set. If you list "all tools," that is a flag that scope is too broad.

### 7. Recommended subagent type (advisory)

The agent type from the available roster (Explore, general-purpose, code-reviewer, etc.) you recommend dispatching this envelope to. **Treat this as advisory, not load-bearing.** There is no guaranteed expertise delta between subagent types beyond their tool sets and system prompts — all are general Claude underneath. Calling a subagent an "epistemologist" does not make it think like one; it makes it talk like one.

Justify the choice in one sentence on the basis of tool fit (does the subagent have the tools the work needs?) or system-prompt fit (does the subagent's prompt frame the work in a useful direction?), NOT on the basis of imagined domain expertise. If the most honest choice is `general-purpose` or `claude`, write that.

If a dimension would genuinely benefit from a domain expert that does not exist in the roster, name the gap explicitly in this section. Do not invent a subagent that does not exist; do not paper over the gap with a generic dispatch labeled as expert.

### 8. Return format

What the recipient writes back, and where. Be explicit about:

- File path (absolute) for the return artifact.
- Required structure (headings, sections).
- Required length budget (e.g., "≤ 400 words" or "≤ 2 pages").
- What the return must NOT contain (e.g., "no executive summary," "no recommendations beyond the scope").

### 9. Handoff envelope (the no-pingpong guarantee)

A final block stating:

- The verbatim grain that started the coliseum (so the recipient has the originating intent).
- The dimension this assignment serves (so the recipient knows their place in the coliseum).
- A pointer to `phase-1-dimensions.md` for full context (so the recipient can read peer dimensions if relevant).
- An explicit statement: "If you reach a point where you cannot continue without clarification, write a `BLOCKED` block in your return artifact rather than coming back to the originator. Continue with the rest of the assignment if any part remains executable."

The `BLOCKED` exception is not ping-pong — it is a logged blocker, recorded in the artifact, surfaced at reconciliation. Ping-pong is the recipient bouncing back mid-dispatch asking for clarification before producing anything. The envelope must prevent that.

## Procedure

### Step 1: Read Phase 1 output

Read `phase-1-dimensions.md`. For each dimension, extract:

- Name and description
- Required expertise
- Implicit success criterion (from Phase 1)

### Step 2: Compose each envelope

For each dimension, write a full envelope using the 9-section standard. Do not skip sections. Do not abbreviate. Length is fine — completeness is what matters.

### Step 3: Cross-check independence

After all envelopes are drafted, read them as a set. Verify:

- No envelope references "the return from assignment-NNN" (that would mean a sequential dependency, not parallel).
- No two envelopes have overlapping success criteria (that would mean redundant dispatch).
- The union of scopes (positive) covers the grain's implied scope as named in `grain-context.md`.

If you find a sequential dependency, decide: either it's a real sequence (downgrade one envelope to Phase-4 follow-up, not Phase-3 parallel dispatch), or the dimensions need re-pruning (back to Phase 1).

### Step 4: Write the artifact

Write `phase-2-assignments.md` in the working directory. Required structure:

```markdown
# Phase 2 — Assignment envelopes composed

## Grain (verbatim)

> <quoted grain>

## Envelope set

### assignment-001-<dim-slug>

**Scope (positive)**: …
**Scope (negative)**: …
**Context the recipient needs**: …
**Success criteria**:
- [ ] …
- [ ] …
**Allowed tools**: …
**Recommended subagent type**: …
**Return format**: …
**Handoff envelope**: …

### assignment-002-<dim-slug>

…

## Cross-check log

- Sequential dependencies found: <list, with resolution>
- Overlapping success criteria found: <list, with resolution>
- Scope-union coverage check: <pass/partial/fail, with note>
```

### Step 5: Gate self-check

Before returning, verify for each envelope:

- [ ] All 9 sections present and non-trivial
- [ ] Scope is one paragraph, not a list
- [ ] Negative scope explicitly names adjacent work being excluded
- [ ] Context section would let a fresh subagent start without questions
- [ ] Success criteria are observable and sufficient
- [ ] Allowed tools is minimal, not a blank check
- [ ] Subagent type is named with one-sentence justification
- [ ] Return format includes path, structure, length budget
- [ ] Handoff envelope includes grain, dimension, references, and BLOCKED clause

The next step in the protocol invokes the `pingpong-detector` agent against this artifact. The detector will fail any envelope that misses these. Better to self-check now than to be sent back.

## Common failure to avoid

The most common failure of this phase is **assuming the recipient shares your context**. They do not. A fresh subagent has none of the conversation history. Every assumption you carry from the conversation must be made explicit in the envelope, or the recipient will either ping-pong back or — worse — execute on their own assumptions and return work that misses the mark.

## Reference material

- [handoff-envelope-spec.md](../../references/handoff-envelope-spec.md) — full envelope spec with examples
- [assignment-anatomy.md](../../references/assignment-anatomy.md) — anatomy of the primitive being composed
