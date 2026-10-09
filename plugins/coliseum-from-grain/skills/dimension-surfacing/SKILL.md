---
name: dimension-surfacing
description: Surfaces the parallel domain dimensions implicit in a dense or minimal prompt. Use when a user prompt is small on the surface but plainly implies multiple independent domains needing different expertise; when explicitly invoked by the coliseum-orchestrator skill as Phase 1; or when the user asks "what dimensions does this prompt encode" or "what axes does this break into." Produces a named dimension set where each dimension is independently executable and not a paraphrase of another.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, Agent
argument-hint: <path to grain-context.md, or the raw grain inline>
---

# Dimension Surfacing

You are extracting parallel domain dimensions from a grain. A grain is a dense prompt whose surface is small but whose implied scope contains multiple independent domains. Your job is to name those domains so they can be composed as parallel assignments.

## What "dimension" means here

A dimension is an **axis of work the grain implies**, distinct from other axes such that:

- A subagent assigned to dimension A can execute independently of an agent on dimension B (no cross-coupling at execution time).
- Dimension A requires different domain expertise than dimension B (different agent type, different knowledge base, different success criteria).
- Eliminating dimension A from the coliseum would leave the user's grain partially unaddressed.

A dimension is **not**:

- A sub-step within a single domain (that's a sequence, not a dimension).
- A rephrasing of another dimension (that's redundancy).
- A nice-to-have addition the grain didn't actually request (that's scope creep).

## Procedure

### Step 1: Read the grain literally

If invoked from the orchestrator, read `grain-context.md` and extract the verbatim grain from the "literal surface" section.
If invoked directly, treat the argument as the grain.

Do **not** paraphrase before analysis. Paraphrase erases dimensions.

### Step 2: Generate a candidate dimension set

Read the grain through each of these lenses and capture candidate dimensions from each pass. A dimension may emerge from one lens; the strong ones emerge from multiple.

| Lens | Question to ask of the grain |
|---|---|
| **Domain** | What distinct knowledge fields does this implicate? (E.g., legal, security, design, infrastructure, content, ontology) |
| **Stakeholder** | Whose perspectives are implicated? (E.g., user, operator, auditor, contributor, downstream consumer) |
| **Time horizon** | What lives across different temporal scales? (E.g., immediate execution, medium-term architecture, long-term governance) |
| **Substrate layer** | What technical/material layers does it span? (E.g., data model, API, UI, deployment, observability) |
| **Failure mode** | What distinct failure modes need separately mitigating? (E.g., correctness, latency, security, ergonomics) |
| **Forbidden moves** | What does the grain say "not" about, and what dimension does that "not" name by negation? |

Write each candidate dimension as: `<short name> — <one-sentence description> — <expertise type required>`.

### Step 3: Prune for independence

For each pair of candidate dimensions, ask: *can a subagent on dimension A do its work without waiting on dimension B?*

- If yes → both keep.
- If no, and dependency is real → merge into one dimension that includes both, OR split into a sequence (which means one of them is not a peer-dimension, it's a downstream step).
- If they share the same expertise and the same success criterion → collapse into one.

Target dimension count: **3–7**. More than 7 usually means lens-pass output was retained without pruning. Fewer than 3 usually means dimensions were prematurely merged — re-examine.

### Step 4: Write the artifact

Write `phase-1-dimensions.md` in the working directory. Required structure:

```markdown
# Phase 1 — Dimensions surfaced

## Grain (verbatim)

> <quoted grain>

## Dimensions

### D1 — <name>

- **Description**: <one sentence>
- **Expertise required**: <named domain>
- **Why independent**: <one sentence on why this can dispatch in parallel>
- **Implicit success criterion**: <one sentence>

### D2 — <name>

…

## Pruning log

- Candidates considered: <list>
- Merged: <which into which, why>
- Dropped: <which, why>

## Lens coverage

- Domain lens: <which dimensions emerged from this lens>
- Stakeholder lens: …
- Time-horizon lens: …
- Substrate-layer lens: …
- Failure-mode lens: …
- Forbidden-moves lens: …
```

### Step 5: Gate criteria self-check

Before returning, verify:

- [ ] Each dimension is independently executable (no cross-coupling at execution time).
- [ ] No dimension is a paraphrase of another.
- [ ] The dimension set, taken together, covers the grain's implied scope.
- [ ] Dimension count is in [3, 7] OR you have written justification for being outside that range.
- [ ] Each dimension names the required expertise type.

If any check fails, iterate before producing the final artifact.

## Common failure to avoid

The most common failure of this phase is **dimension-as-task-breakdown** — splitting one domain into a sequence of steps and calling those "dimensions." Dimensions are axes, not steps. If your candidates can be ordered into a single workflow, you have a sequence, not a coliseum. Re-read the grain for the true axes.

## Reference material

- [parallel-dimensions.md](../../references/parallel-dimensions.md) — multi-axis reading of prompts
- [assignment-anatomy.md](../../references/assignment-anatomy.md) — anatomy of what each dimension will become
