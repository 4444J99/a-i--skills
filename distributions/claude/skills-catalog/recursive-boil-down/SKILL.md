---
name: recursive-boil-down
description: Decompose a system, repository, or architecture into four tiers — Macro (whole system), Bricks (components), Elements (conceptual primitives), Primitives (base operations) — reading target source plus its seed.yaml, then output a comparison table of the new system against existing substrates to expose reuse and overlap before anything new is built. Triggers on "boil down", "decompose into primitives", "recursive boil-down", or analyzing a new repo/architecture against what already exists.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - architecture
  - decomposition
  - primitives
  - substrate-analysis
  - reuse
  - ontology
governance_phases: [frame, shape]
organ_affinity: [organ-i, organ-iv]
inputs:
  - target source tree (repo or subsystem)
  - target seed.yaml (read-only; if absent, that absence is a finding)
  - inventory of existing substrates to compare against (registry, sibling repos)
outputs:
  - four-tier decomposition document
  - substrate comparison table (new vs existing, per tier)
  - reuse verdict (build / extend / absorb)
side_effects:
  - reads-filesystem
  - creates-files
triggers: [user-asks-to-decompose-system, context:boil-down, context:primitives-analysis, context:new-repo-audit]
complements: [knowledge-architecture, modular-synthesis-philosophy, domain-ideal-whole-substrate, ecosystem-autopsy]
---

# Recursive Boil-Down Protocol

Strip a system down to what it *is made of*, tier by tier, until it can be compared honestly against everything that already exists — so the verdict "build new" is earned rather than assumed.

## Why this exists

Delegated agents reinvent existing tools because they meet a system at its surface (the Macro tier) where everything looks unique. Two systems that look unrelated at the surface usually share most of their Elements and nearly all of their Primitives. Decomposing before building converts "this is new" into a precise statement of *which tier* is actually new — and routes everything below that tier to reuse.

## The four tiers

| Tier | Question | Granularity | Example (a prompt-registry system) |
|------|----------|-------------|-----------------------------------|
| **Macro** | What is the whole thing for? | 1 system | "durable registry of every prompt issued across sessions" |
| **Bricks** | What components compose it? | 3–12 components | capture hook, session parser, index generator, archive store |
| **Elements** | What concepts do the bricks manipulate? | 5–20 concepts | session, prompt-atom, capture-event, index-entry, archive-path |
| **Primitives** | What base operations recur beneath the concepts? | small closed set | append-only write, content-hash dedupe, frontmatter parse, glob-walk, ID-mint |

Decomposition is **recursive**: any Brick too large to state in one sentence gets its own four-tier pass.

## Workflow

### 1. Read the declared intent
- Read `seed.yaml` (or the repo's manifest/charter equivalent) **read-only** — it declares what the system believes itself to be.
- If no seed exists, record that as a governance finding (undeclared system), and reconstruct intent from README + entry points.
- Capture the declared Macro statement verbatim before forming your own.

### 2. Walk the source top-down
- Entry points → major modules → data files. At each level ask the tier question, not "what does this code do" but "what is this *made of*".
- Derive the Bricks list from actual structure (directories, services, scripts), not from documentation claims; diff against the seed's claims and note divergence.

### 3. Extract Elements and Primitives bottom-up
- Elements: nouns that survive across multiple Bricks — the shared conceptual vocabulary. If a noun appears in only one Brick it's internal detail, not an Element.
- Primitives: verbs/operations that recur beneath Elements. Test for primitive-hood: could this operation be lifted into a library with no domain knowledge? If yes, it's a Primitive.
- Keep the Primitive set small and closed; a sprawling primitive list means you stopped one tier too high.

### 4. Build the substrate comparison table
For each existing substrate in scope (sibling repos, platform services, prior systems), compare per tier:

```markdown
| Tier | New system | Substrate A | Substrate B | Verdict |
|------|-----------|-------------|-------------|---------|
| Macro | prompt registry | session archive | atom pipeline | distinct |
| Bricks | capture hook | ✅ has (PostToolUse) | ❌ | reuse A's |
| Elements | prompt-atom | ≈ message-atom | ✅ identical | absorb into B |
| Primitives | ID-mint | ✅ | ✅ | reuse, never re-mint |
```

Cell vocabulary: `✅ identical` / `≈ overlapping (name the delta)` / `❌ absent`.

### 5. Issue the reuse verdict
The highest tier with genuine novelty determines the build posture:
- Novel **Macro**, shared below → thin composition over existing substrates. Build only the composition.
- Novel **Bricks** → new components inside an existing system; extend, don't fork.
- Novel **Elements/Primitives only** → almost always a misreading; re-examine before believing it.
- Nothing novel → **absorb**: the "new system" is a view over an existing one; route the requirement there.

State the verdict explicitly with the tier that justifies it. Commit the decomposition + table as an artifact; it is the evidence the build decision cites.

## Anti-patterns

- **Decomposing from documentation alone.** READMEs describe aspiration; walk the source.
- **Stopping at Bricks.** Brick-level comparison hides reuse — most theft happens at Elements and Primitives.
- **Comparing against zero substrates.** A boil-down without a comparison table is a diagram, not a protocol; the table is the deliverable.
- **Treating the seed as ground truth.** It's the system's self-image; divergence between seed and source is itself a top-tier finding.
- **Open-ended primitive lists.** If Primitives exceed ~12, you've mixed tiers; promote the domain-specific ones back up to Elements.
