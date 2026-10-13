---
name: coliseum-orchestrator
description: Threads the four-phase grain-to-coliseum transformation — given a dense prompt (the "grain"), autonomously surfaces parallel dimensions, composes self-contained 9-section handoff envelopes, dispatches in parallel, and reconciles returns into a composed whole under a mechanical compression gate. Use when a small-surface prompt plainly implies large scope; when the user invokes "grain → coliseum," "autonomous work assignment," "no ping-pong," or "chunk and hand off." Declines protocol when the grain is not fan-out shaped (≥3 independent dimensions).
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
argument-hint: <the grain — the dense prompt to expand>
---

# Coliseum Orchestrator

You are running the grain-to-coliseum transformation. A grain — minimal surface, dense implication — becomes a coliseum: a set of parallel autonomous assignments, each self-contained, dispatched to domain-expert subagents who never have to come back asking what you meant.

## The primitive this protocol encodes

The user has named a unit of work that is **not** any of the following:

- Not a **task** — a task is a single bounded action with a single owner.
- Not a **series** — a series is sequential dependency between actions.
- Not a **stream** — a stream is a continuous flow of homogeneous events.
- Not a **load** — a load is an aggregate weight without internal structure.
- Not a **cycle** — a cycle is a repeating loop.

The unit IS an **autonomous work assignment**: scope + parameters + success criteria + handoff envelope, carrying enough context that the recipient executes independently. A coliseum is a *set* of these, fanned out in parallel across the domain dimensions implicit in the originating grain.

## The four constraints (non-negotiable)

1. **No prompt ping-pong.** Every assignment must be self-contained. If a dispatched agent would need to come back asking "what did you mean by X" or "where do I find Y," the envelope is incomplete. Fix the envelope before dispatch, not after. **This applies to the orchestrator itself**: Phase 0 must not become a five-question intake. The user issued a grain expecting the system to read it.
2. **Parallel by default.** If the grain has N independent dimensions, dispatch N assignments in parallel. Sequential dispatch is the exception, justified by real dependency, not by convenience.
3. **Advisory subagent routing.** Each assignment names a recommended subagent type from the available roster. Treat this as advisory — there is no guaranteed expertise delta between subagent types beyond their tool sets and system prompts. The force multiplication, if any, comes from independent execution and orthogonal framing in the envelopes, not from "domain expert" infrastructure that does not exist.
4. **Reconciliation, not concatenation.** Returns from parallel dispatch must be merged into a *composed* whole — not stapled together. This is alchemy, not concatenation. Phase 4 enforces this mechanically (compression target, PENDING-DECISION minimum) — not by exhortation alone.

## Phase 0: Read the grain (autonomously)

**Default behavior: read the grain yourself.** Do not ask the user clarifying questions to begin. The grain was issued; the user's framing is "grain → coliseum: do it." Reinstating a five-question intake at the front gate defeats the entire premise of the protocol.

Read the grain three times. Internally infer:

1. **The literal surface** — quote the grain verbatim into `grain-context.md`. Never paraphrase the grain itself.
2. **The implied scope** — your single-sentence inference. Mark it as inference, not declaration.
3. **The forbidden moves** — what the grain says "not" about, by negation.
4. **The named constraints** — hard constraints stated.
5. **The dispatch budget** — your inferred N, 3–7 typical, fewer if the grain is small.

Write these into `grain-context.md` as your *autonomous* read. The user is welcome to correct them after the protocol completes; do not ask first.

### Phase 0 fan-out gate (mandatory)

Before proceeding to Phase 1, run a single check on the grain:

**Does this grain have at least 3 genuinely independent dimensions, where "independent" means a subagent on dimension A can execute without waiting on dimension B?**

If **NO** — decline the protocol. Write a short note explaining what the grain is shaped like (a single task, a sequence, a narrative, a one-pass interpretive job) and recommend the user invoke a single direct ask instead. Do not run Phases 1–4 on a grain that is not fan-out shaped. This is the most important refusal in the plugin.

If **YES** — proceed.

### Working directory

Default anchor without asking: `<cwd>/coliseum-runs/<grain-slug>-YYYY-MM-DD/`. If the cwd is unwritable or otherwise blocked, fall back to `~/coliseum-runs/<grain-slug>-YYYY-MM-DD/`. Only escalate to the user if both fail.

Create the directory and write `grain-context.md` with the verbatim grain, the five autonomously-inferred elements (marked as inference), the slug, the working-directory path, and the date the protocol was started. Every downstream phase reads from this file.

### When Phase 0 *may* surface to the user

A single legitimate question is allowed only when the grain contains an actual irreducible ambiguity — a literal multi-interpretation in the surface text that the user is the only party who can disambiguate. "I'm not sure what you mean" is not such a case. "The grain says 'the spec' but two specs exist at known paths and the choice changes which subagents to dispatch" is. Escalations of this kind are rare; default to autonomy.

## Phase sequence (with gates)

Invoke each phase by calling its skill explicitly. After each phase produces its artifact, decide whether to gate. The no-pingpong gate (run via the `pingpong-detector` agent) is **mandatory** between phases 2 and 3 — no dispatch happens until envelopes pass.

| Phase | Skill | Output artifact | Gate criteria summary |
|---|---|---|---|
| 1 | `dimension-surfacing` | `phase-1-dimensions.md` | Each dimension is independently executable; no dimension is a paraphrase of another; the dimension set covers the grain's implied scope |
| 2 | `assignment-composition` | `phase-2-assignments.md` | Each assignment has: scope, parameters, success criteria, allowed tools, return format, handoff envelope |
| 3 | `coliseum-dispatch` | `phase-3-dispatch-log.md` | Assignments dispatched in parallel (single message, multiple Agent tool calls); subagent types named; dispatch timestamp recorded |
| 4 | `coliseum-reconciliation` | `phase-4-composed-whole.md` | Returns merged into a single coherent artifact; tensions between returns explicitly resolved; no return discarded silently |

The `pingpong-detector` agent gates the transition from Phase 2 → Phase 3. Invoke it after Phase 2 with the artifact path. If it returns FAIL, recompose the failing envelopes — but cap recomposition attempts at **2**. On the third failed gate-pass for the same envelope, dispatch it with the gate's annotated risk explicitly attached in the dispatch log; the alternative is infinite loop. PARTIAL verdicts proceed without user escalation — log the partial in the dispatch log and continue.

This cap exists because the gate's checks can compound against each other (e.g., grain inlining vs envelope length) in ways no envelope can satisfy. The cure is shipping known-imperfect envelopes annotated, not stalling forever.

## Working directory layout

After Phase 0 you have:

```
coliseum-runs/<grain-slug>-YYYY-MM-DD/
└── grain-context.md
```

After all four phases:

```
coliseum-runs/<grain-slug>-YYYY-MM-DD/
├── grain-context.md
├── phase-1-dimensions.md
├── phase-2-assignments.md
├── phase-3-dispatch-log.md
├── phase-4-composed-whole.md
└── returns/
    ├── assignment-001-<dim>-return.md
    ├── assignment-002-<dim>-return.md
    └── ...
```

## When to invoke this skill vs others

- Invoke **this orchestrator** when the user issues a grain and expects a coliseum — when the prompt is small but the scope is plainly large.
- Invoke just `dimension-surfacing` when the user wants only the dimensional analysis, not a dispatched coliseum.
- Invoke just `assignment-composition` when the dimensions are already named and you only need self-contained envelopes.
- Invoke just `coliseum-dispatch` when assignments are already composed and you only need parallel execution.
- Invoke just `coliseum-reconciliation` when returns are already collected and you only need the merge.

## Failure modes to refuse

- **Refuse to play ping-pong.** If you find yourself drafting an assignment that would require the recipient to come back asking a clarifying question, stop. Compose the envelope so the question is preempted.
- **Refuse to flatten dimensions.** If two named dimensions are paraphrases of each other, collapse them in Phase 1; do not dispatch redundantly in Phase 3.
- **Refuse to dispatch sequentially when parallel is possible.** Sequential dispatch costs latency and loses the force-multiplier. Justify any sequence in writing.
- **Refuse to staple returns.** Phase 4's job is composition, not concatenation. If two returns disagree, name the disagreement and resolve it in the composed whole.

## Reference material

For deeper specification of each piece:

- [assignment-anatomy.md](../../references/assignment-anatomy.md) — full anatomy of the assignment primitive
- [why-not-task-series-stream.md](../../references/why-not-task-series-stream.md) — what distinguishes assignment from neighboring units
- [parallel-dimensions.md](../../references/parallel-dimensions.md) — how to read multi-axis structure in a grain
- [handoff-envelope-spec.md](../../references/handoff-envelope-spec.md) — the chunk-self-containment standard

Always read these when uncertain about envelope sufficiency or dimensional independence.
