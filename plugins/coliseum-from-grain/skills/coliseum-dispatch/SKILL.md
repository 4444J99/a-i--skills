---
name: coliseum-dispatch
description: Dispatches a composed set of assignment envelopes to domain-expert subagents in parallel, in a single message with multiple Agent tool calls. Enforces the no-pingpong gate via the pingpong-detector agent before any dispatch fires. Use when invoked by the coliseum-orchestrator as Phase 3; when envelopes are already composed and the next step is parallel execution; or when the user asks to "fan out" or "dispatch in parallel." Produces a dispatch log capturing what was sent, when, and where returns land.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
argument-hint: <path to phase-2-assignments.md>
---

# Coliseum Dispatch

You are firing the assignment envelopes at their target subagents — in parallel, in a single message, with one Agent tool call per envelope. This is where the force-multiplication happens. Sequential dispatch is a failure mode here.

## The hard rule of this phase

**Parallel by default.** Use a single message with multiple Agent tool calls. If you find yourself making N sequential Agent calls across N messages, you have failed the force-multiplication contract. The only acceptable reason for sequential dispatch is a *real* dependency between envelopes — and if real dependency exists, that envelope should have been demoted to a Phase-4 follow-up during Phase 2, not dispatched here.

## Procedure

### Step 1: Run the no-pingpong gate

Before any dispatch:

1. Invoke the `pingpong-detector` agent with `phase-2-assignments.md` as the input.
2. Wait for the verdict.

Possible verdicts:

- **PASS** → proceed to Step 2.
- **PARTIAL** → fix the flagged envelopes (or surface to user and proceed only on explicit approval).
- **FAIL** → return to Phase 2 to repair envelopes. Do not dispatch.

The gate is non-optional. A dispatched ping-pong-prone envelope wastes both the subagent's tokens and the user's. Catching it here is cheap.

### Step 2: Pre-flight per envelope

For each envelope, confirm:

- The recommended subagent type exists in the agent roster available at runtime.
- If the recommended type does not exist, substitute the closest available type and note the substitution in the dispatch log.
- The return-file path's parent directory exists; create it if not (`returns/` under the working directory).

### Step 3: Compose the parallel dispatch

In a SINGLE message, issue ONE Agent tool call per envelope. Each call:

- `description`: short, e.g., `"Assignment-NNN-<dim-slug>"`.
- `subagent_type`: from envelope's "Recommended subagent type" section (or substituted type).
- `prompt`: the full envelope content, self-contained, including the handoff block. The recipient subagent must read **only** this prompt — no implicit reference to conversation context.

The prompt must end with the explicit instruction:

> Write your return artifact to `<absolute path from envelope>`. Use the structure required by the envelope's Return format section. If you reach an unresolvable blocker, write a `BLOCKED` block in the return artifact rather than coming back to ask. Continue with any remaining executable portion of the assignment.

### Step 4: Decide foreground vs background

Two modes for the parallel dispatch:

- **Foreground** (default): the orchestrator waits for all subagents to complete before proceeding to Phase 4. Right when reconciliation is the immediate next step.
- **Background** (`run_in_background: true`): use when subagent work is long-running and the orchestrator has independent work to do meanwhile. The harness notifies on completion.

For the standard grain-to-coliseum flow, foreground is correct — reconciliation can't begin until returns are in.

### Step 5: Write the dispatch log

Immediately after the dispatch message goes out (not after returns arrive), write `phase-3-dispatch-log.md`:

```markdown
# Phase 3 — Dispatch log

## Grain (verbatim)

> <quoted grain>

## Dispatch summary

- Total envelopes dispatched: <N>
- Dispatch mode: foreground | background
- Dispatch timestamp: <ISO 8601>
- No-pingpong gate verdict: PASS | PARTIAL (notes…) | (would not be FAIL — we'd have returned to Phase 2)

## Dispatch table

| Assignment ID | Dimension | Subagent type | Substitution? | Return path |
|---|---|---|---|---|
| assignment-001-… | … | … | none | returns/assignment-001-…-return.md |
| assignment-002-… | … | … | (general-purpose substituted for absent specialist X) | returns/… |

## Returns expected

- <list each return-path with checkbox for arrival status>

## Substitutions and rationale

<for each substitution made in Step 2, one paragraph>
```

### Step 6: Track return arrivals

After the dispatch message, the orchestrator's next action is to wait for returns (foreground) or to be notified (background). When each return arrives, update the dispatch log's "Returns expected" checklist.

If any return arrives with a `BLOCKED` block, that is a signal — not a failure. The reconciliation phase handles blockers explicitly.

### Step 7: Hand off to reconciliation

When all returns are in (or all returns + recorded blockers), invoke the `coliseum-reconciliation` skill with the working directory as argument.

## Gate self-check before Step 3

Before composing the parallel dispatch message, verify:

- [ ] All envelopes passed the no-pingpong gate (or PARTIAL was explicitly approved by user)
- [ ] Each envelope's prompt is fully self-contained (you could send it to a stranger who has no conversation history)
- [ ] All envelopes are dispatched in a single message (not split across messages)
- [ ] The single message has exactly N Agent tool calls for N envelopes
- [ ] Each subagent's return path is unique and parent-dir-existent

## Common failure to avoid

**Sequential dispatch dressed up as parallel.** It is easy to write a single message containing multiple Agent calls but secretly intend them to run in sequence (e.g., one waits on another's return). The Agent tool does not enforce that — if you call N agents in one message, they all start at roughly the same time. If you've baked in a sequence by way of envelope content (e.g., assignment-002's prompt references assignment-001's return artifact), you've collapsed the coliseum into a series. Refactor before dispatch.

## Reference material

- [handoff-envelope-spec.md](../../references/handoff-envelope-spec.md) — what the dispatched prompt must contain
- [parallel-dimensions.md](../../references/parallel-dimensions.md) — what makes dimensions truly parallel
