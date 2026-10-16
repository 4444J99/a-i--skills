---
name: prompt-atom-formalization
description: Scan rough markdown, session exports, or pasted prose and isolate each core intent into a structured prompt atom — classified as law, value, directive, constraint, question, or branch-vector — then rewrite it into machine-readable YAML frontmatter per the RAW → CLEANED/FORMALIZED → ELEVATED doctrine. Triggers on "prompt atom extraction pass", "atomize this", "formalize these prompts", or converting loose operator text into registry-grade atoms.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - prompt-engineering
  - atomization
  - formalization
  - governance
  - registry
  - intent-extraction
governance_phases: [build]
organ_affinity: [organ-i, organ-iv]
inputs:
  - source text (rough markdown, session export, transcript excerpt, pasted prose)
  - target atom registry or schema (e.g. prompt-atoms.json shape) if one exists
outputs:
  - structured atoms with YAML frontmatter, one per isolated intent
  - provenance map (atom → source span)
side_effects:
  - reads-filesystem
  - creates-files
triggers: [user-asks-for-atom-extraction, context:atomize, context:formalize-prompts, context:raw-cleaned-elevated]
complements: [prompt-engineering-patterns, corpus-persona-extraction, knowledge-architecture, skill-chain-prompts]
---

# Prompt Atom Extraction & Formalization

Convert loose operator prose into atoms: minimal, classified, machine-readable units of intent that registries can store, pipelines can route, and future sessions can execute without re-interpreting the original wall of text.

## Why this exists

Operator intent arrives packed — one dense paragraph can carry a standing law, two directives, a constraint, and an open question. Left as prose, that intent is executable only by whoever re-reads and re-derives it. Atomized, each unit gets an ID, a class, a lifecycle state, and provenance — it becomes governable. The doctrine: **atoms are permanent**; extraction is additive; nothing in the source is destroyed by being formalized.

## The atom classes

| Class | Nature | Lifetime | Example |
|-------|--------|----------|---------|
| **law** | standing rule; governs all future behavior | permanent until amended | "nothing local-only — every artifact git-tracked AND pushed" |
| **value** | weighting/preference; shapes choices without mandating one | durable | "prefer user coinages over standard vocabulary" |
| **directive** | one concrete executable action | until DONE | "register the 5 bench agents in fleet.yaml" |
| **constraint** | boundary on how any action may be done | scoped or permanent | "never chezmoi add over existing source without diffing" |
| **question** | open decision owned by a human | until answered | "GCP_SA_KEY provisioning — enable CI deploys?" |
| **branch-vector** | a fork in possible futures; options held in superposition | until collapsed | "skills live in domus OR a-i--skills — decide before next install" |

## The three states

- **RAW** — verbatim source span, untouched. Always preserved (quoted or referenced by span), never edited.
- **CLEANED / FORMALIZED** — the intent restated minimally in normalized language, classified, given frontmatter.
- **ELEVATED** — the atom generalized to its standing form: stripped of incident-specific detail, linked to related atoms, ready for constitutional or registry placement. Only laws, values, and constraints elevate; directives and questions resolve instead.

Every atom records which state it is in; an extraction pass may legitimately stop at CLEANED.

## Workflow

### 1. Segment the source
- Split the text at intent boundaries, not sentence boundaries — an intent is one irreducible "do/never/prefer/decide" unit.
- Dense prompts pack abstractions: expect 3–10 atoms per operator paragraph. Under-segmentation (one atom per message) is the dominant failure.
- Assign each segment a provenance span: `{file, line-range}` or `{session-id, message-index}`.

### 2. Classify
- Apply the class table. Disambiguation tests:
  - Would it still bind next month? → law/value/constraint, not directive.
  - Does it command an action or bound an action? → directive vs constraint.
  - Can the agent resolve it alone? If no → question.
  - Are multiple mutually-exclusive futures named without choosing? → branch-vector.
- When torn between law and value: laws are violated, values are traded off. If you can imagine a sanctioned trade-off, it's a value.

### 3. Formalize into frontmatter

```yaml
- id: ATM-NNNNNN            # mint from the registry's counter — never invent ranges
  class: constraint
  state: CLEANED
  text: "Never `chezmoi add` over existing source without `chezmoi diff` first."
  raw: "…also for god's sake diff before you chezmoi add anything again…"
  provenance: {session: 8bb8f846, message: 41}
  captured: 2026-06-07
  status: OPEN              # OPEN | DONE | ANSWERED | COLLAPSED | SUPERSEDED-BY:{id}
  links: [ATM-013811]       # related atoms; liberal linking
  tags: [chezmoi, destructive-ops]
```

Rules:
- **Mint IDs from the registry's own counter surface** — read it, claim the range, write back; never guess the next ID.
- `raw` is mandatory: the verbatim or span-referenced source. Formalization without provenance is paraphrase, not extraction.
- One intent per atom. If the `text` field needs "and", split it.

### 4. Elevate (when warranted)
For laws/values/constraints that recur across ≥2 independent sources:
- Strip incident detail ("in the limen repo" → gone, unless scope-bound).
- Link the supporting atoms as evidence.
- Mark `state: ELEVATED` and route to the appropriate standing surface (constitution tier, reliquary, registry) **by pointer** — the atom stays in the registry; the surface cites it.

### 5. Append and report
- Append atoms to the registry surface (append-only; existing atoms are never edited by an extraction pass — supersession is a new atom with `SUPERSEDED-BY` back-link).
- Emit the provenance map and counts: atoms by class, by state, plus the segments deliberately *not* atomized (conversational filler) so reviewers can audit the discard decisions.

## Anti-patterns

- **Atomizing the assistant's restatement instead of the operator's words.** Extract from source turns only.
- **Editing RAW.** The verbatim layer is evidence; all normalization happens in CLEANED.
- **Minting IDs by pattern-matching the last seen ID.** Registry counters exist precisely because parallel sessions race; read-claim-write.
- **Eliding the boring atoms.** Constraints embedded in rants ("never do X again") are the highest-value extractions and the most commonly skipped.
- **Elevating from a single occurrence.** One strong statement is a CLEANED constraint; elevation requires recurrence.
