---
name: coliseum-reconciliation
description: Merges the parallel returns from a dispatched coliseum into a single composed whole — alchemy, not concatenation. Resolves tensions between returns explicitly, surfaces any BLOCKED records as named gaps, ensures no return is silently discarded. Use when invoked by the coliseum-orchestrator as Phase 4; when all (or recorded) returns from a Phase-3 dispatch are in and the next step is composition; or when the user asks to "reconcile," "compose the returns," or "merge into a whole." Produces the final artifact — phase-4-composed-whole.md — that closes the grain-to-coliseum loop.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: <path to the working directory containing phase-3-dispatch-log.md and returns/>
---

# Coliseum Reconciliation

You are composing N parallel returns into one coherent artifact. This is the alchemy step. Stapling returns together is failure; the user explicitly forbade flattening (the grain itself said "resist flattening"). Composition means structural integration, named tensions, resolved disagreements, no silent discards.

## What composition is (and is not)

| Composition | Concatenation |
|---|---|
| Returns are integrated structurally into a whole that has its own architecture | Returns are appended one after another |
| Tensions between returns are named and resolved | Tensions are hidden or averaged away |
| Overlapping content is unified | Overlapping content is duplicated |
| Each return contributes to the final shape | Each return is preserved as a section |
| The whole exceeds the sum of parts | The whole equals the sum of parts |

If the output of this phase reads like a concatenation, the phase failed.

## Procedure

### Step 1: Take inventory

Read `phase-3-dispatch-log.md` to enumerate expected returns. For each return path:

- Check whether the return artifact exists at the expected path.
- If absent, record as "missing" in the inventory.
- If present, read the entire artifact.
- Note whether the return contains a `BLOCKED` block (and the blocker's content).

Write an inventory section in your working notes before composing.

### Step 2: Extract claims

For each return, extract its **claims** — the substantive output the subagent produced. A claim is anything that would be lost if you summarized the return in one sentence and discarded the rest. Capture:

- Concrete artifacts produced (file paths, code, schema entries, decisions).
- Substantive recommendations.
- Surfaced risks or unknowns.
- Disagreements with peer returns (if the return explicitly references peer dimensions — most won't, by design).

### Step 3: Identify tensions

A tension is a place where two returns produce outputs that are not directly compatible:

- They name the same entity differently.
- They make incompatible structural choices.
- They each cover a region but with different assumptions about that region's interface.
- They each propose to handle a failure mode the same way (overlap, redundancy).

For each tension, name it explicitly and decide how to resolve in the composed whole:

- **Adopt one side** — name which return prevailed and why.
- **Synthesize** — produce a third option that integrates both. Note where this synthesis lives in the composed whole.
- **Surface to user** — when the tension is a genuine design decision rather than a technical reconciliation. Mark the tension as `PENDING-DECISION` in the composed whole, with both options spelled out.

Do not resolve tensions by averaging or hand-waving. Either pick one, synthesize a third, or surface as PENDING-DECISION.

### Step 4: Identify gaps

A gap is a place where:

- The grain implied coverage that no return delivered.
- A `BLOCKED` block in a return identified work that was not completable.
- Cross-cutting concerns emerged that no single return addressed (most common — emerges precisely because dimensions were independent at dispatch time).

For each gap:

- Name what was implied but unaddressed.
- Decide whether it is closeable within the current pass (you address it directly in the composed whole) or requires another assignment (record as a follow-up).

### Step 5: Compose the artifact

Write `phase-4-composed-whole.md`. The structure adapts to the grain — there is no one-size template — but always includes these sections:

```markdown
# Phase 4 — Composed whole

## Grain (verbatim)

> <quoted grain>

## What this composes

<one paragraph: what the coliseum produced as a unified output. Not "we dispatched N assignments" — what is the *thing* that resulted.>

## The composed output

<the actual integrated artifact. This is the bulk. Structure it as the grain required, not as the dispatch happened. The user reading this section should not be able to reverse-engineer which return contributed which sentence — that's the test of true composition.>

## Tensions resolved

| Tension | Returns involved | Resolution | Rationale |
|---|---|---|---|
| … | assignment-001, assignment-003 | adopt assignment-001's version | … |
| … | assignment-002, assignment-004 | synthesized — see <section above> | … |

## Pending decisions

<any tension surfaced to user as PENDING-DECISION, with both options spelled out>

## Gaps and follow-ups

<named gaps, with disposition: closed-here | follow-up-assignment-recommended>

## BLOCKED records

<any BLOCKED blocks from returns, surfaced verbatim, with disposition>

## Returns inventory

<the inventory from Step 1, for audit trail>
```

### Step 6: Reconciliation self-check

Before returning to the orchestrator, verify:

- [ ] Every return is referenced somewhere in the composed whole (no silent discards)
- [ ] Every tension is named and disposed (resolved, synthesized, or PENDING-DECISION)
- [ ] Every gap is named and disposed (closed-here, follow-up, or noted as unaddressed)
- [ ] Every BLOCKED record is surfaced
- [ ] The "composed output" section reads as one artifact, not as N stitched sections
- [ ] The composed whole addresses the grain — re-read the grain after reading the composed output, and confirm coverage

### Step 6a: Mechanical composition gate (MANDATORY)

After the self-check, compute two metrics and record them in `phase-4-composed-whole.md` under a `## Composition metrics` section:

1. **Compression ratio** — `wc -w` the composed output section divided by the sum of `wc -w` across all returns.
   - **Target**: ≤ 0.50 (the composed whole is at most half the mass of the inputs combined).
   - **Acceptable**: 0.50 – 0.80 (compression present but weaker; note why in the metrics section).
   - **STAPLED** (failure): > 0.80. The composed output is a concatenation. Recompose before returning.

2. **PENDING-DECISION count** — number of items in the Pending-decisions section.
   - **Minimum**: 1 across N≥3 returns, OR an explicit justification ("All N returns aligned on every load-bearing choice — no tensions detected because <specific reason>").
   - Zero PENDING-DECISIONs without justification is a failure signal — three or more independent subagent returns almost always disagree somewhere; a zero count usually means the orchestrator didn't look.

The metrics section is required. If compression is > 0.80, do not return the artifact — recompose. If PENDING-DECISION count is 0 without justification, surface the most plausible candidate tension as PENDING-DECISION before returning.

```markdown
## Composition metrics

- Returns total word count: <sum>
- Composed output word count: <count>
- Compression ratio: <ratio> (target ≤ 0.50, stapled if > 0.80)
- PENDING-DECISIONs surfaced: <count> (minimum 1 or explicit justification)
- Justification (if zero PENDING-DECISIONs): <text or N/A>
```

### Step 7: Close the loop

Notify the orchestrator (or the user, if invoked directly) that Phase 4 is complete. Pass the path to `phase-4-composed-whole.md`. If PENDING-DECISIONs exist, surface them explicitly — these are the only legitimate items returning to the user as questions.

## The legitimate question category

The protocol forbids ping-pong — recipients bouncing mid-execution. But this phase legitimately surfaces decisions to the user when:

- Two returns disagreed on a genuine design choice (not a technical conflict).
- A blocker exists that cannot be unblocked without the user's authority (e.g., access to a system, authorization for a destructive op).
- The grain itself was load-bearing-ambiguous and the dispatch revealed the ambiguity rather than resolving it.

These are not ping-pong. They are surfacing the *exact* points where the system genuinely needs the user, having done everything the system can do on its own. This is the conductor principle: the human directs vision; the system does everything else. PENDING-DECISIONs are where vision must be directed.

## Common failure to avoid

**Composition-as-table-of-contents.** Producing an artifact whose structure is "return 1, return 2, return 3, …" with no integration. The reader sees the dispatch architecture rather than the composed result. The user does not want to read the seams; the user wants the coliseum. The seams belong in the dispatch log, not the composed whole.

## Reference material

- [assignment-anatomy.md](../../references/assignment-anatomy.md) — what each return embodies
- [handoff-envelope-spec.md](../../references/handoff-envelope-spec.md) — the envelope contract returns were written against
