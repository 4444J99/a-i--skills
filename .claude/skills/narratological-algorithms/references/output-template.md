# Narratological Algorithm Output Template

Canonical structure for distilled narratological algorithm documents.

---

## Document Header

```markdown
# [Creator Name]'s Narratological Algorithms

> Systematic distillation of [Creator]'s [methodology name] into formal, implementable 
> principles for narrative construction. Derived from [primary source(s)].

---
```

## Table of Contents

Always include numbered sections:

```markdown
## Table of Contents

0. [Meta-Principles (Axioms)](#0-meta-principles-axioms)
1. [Structural Hierarchy](#1-structural-hierarchy)
2. [Core Algorithm Name](#2-core-algorithm-name)
...
N. [Quick Reference Card](#n-quick-reference-card)
```

---

## Section 0: Meta-Principles (Axioms)

Format axioms as table with unique identifiers:

```markdown
## 0. Meta-Principles (Axioms)

| Axiom | Formulation |
|-------|-------------|
| XX-A0 | **"Direct quote or paraphrase."** Explanation of principle. |
| XX-A1 | Description of foundational assumption or rule. |
| XX-A2 | Another core principle that shapes all other decisions. |

### Source Quotes

> "Verbatim quote from primary source" —Attribution
```

---

## Section 1: Structural Hierarchy

Visualize the structural units using ASCII trees:

```markdown
## 1. Structural Hierarchy

```
HIGHEST_UNIT
  └── MID_LEVEL_UNIT (quantity, characteristics)
        └── LOWER_UNIT (definition, constraints)
              └── ATOMIC_UNIT (smallest element)
```

### Definition Table

| Unit | Definition | Constraint |
|------|------------|------------|
| **Unit Name** | What it is | What rules govern it |
```

---

## Core Algorithm Sections

Each major algorithm/technique gets its own section:

```markdown
## N. Algorithm Name

### N.1 Subsection (Phase/Step/Component)

```
ALGORITHM_NAME:
├── Step or component 1
│     SUBTYPE_A   - description
│     SUBTYPE_B   - description
├── Step or component 2
│     Constraint or rule
└── Final step or output
```

### N.2 Decision Table

| Condition | Action |
|-----------|--------|
| IF X | THEN Y |
| IF NOT X | THEN Z |

### N.3 Pseudocode

```python
def algorithm_name(input):
    """Docstring explaining purpose"""
    # Step 1
    intermediate = process(input)
    
    # Step 2: Constraint check
    if not valid(intermediate):
        raise StructuralError("Constraint violated")
    
    return output
```
```

---

## Diagnostic Questions Section

Frame as binary yes/no tests:

```markdown
## N. Diagnostic Questions

Answer YES/NO for structural validation:

**[Category Name]**
1. Does [specific testable condition]?
2. Is [measurable property] present?
3. Can [operation] be performed?

**Scoring:**
- All YES → Structure is sound
- Any NO → Identify and address weakness
```

---

## Quick Reference Card

Condensed operational summary:

```markdown
## N. Quick Reference Card

### [Test/Formula Name]
```
IF condition: ACTION
```

### [Core Formula]
```
INPUT → PROCESS → OUTPUT
```

### [Key Constraint]
```
✓ Do this
✗ Don't do this
✗ NEVER do this at [specific point]
```

### [Template]
```
"[VARIABLE] is [state] because [CAUSE]"
```
```

---

## Optional: Theoretical Correspondence Table

Map terminology to other systems:

```markdown
## Appendix: Theoretical Correspondences

| This Framework | McKee | Aristotle | Field | Other |
|----------------|-------|-----------|-------|-------|
| Term A | Equivalent | Greek term | Equivalent | — |
| Term B | Related concept | — | Different usage | Note |
```

---

## Optional: Source Cross-Reference

Map chapters/interviews to principles:

```markdown
## Appendix: Source Cross-Reference

| Source Section | Key Principles |
|----------------|----------------|
| Chapter 1 / Interview Date | Principle X; Concept Y |
| Chapter 2 / Documentary | Algorithm Z; Rule W |
```

---

## Footer

```markdown
---

*Document generated from [full source citation]. All principles extracted 
and formalized for practical narrative construction.*
```

---

## Formatting Conventions

- Use `CAPS_WITH_UNDERSCORES` for algorithm/process names
- Use **bold** for key terms on first introduction
- Use `code blocks` for:
  - Pseudocode
  - Formulas
  - Decision trees
  - ASCII diagrams
- Use tables for:
  - Taxonomies
  - Comparisons
  - Definition lists
  - Decision matrices
- Use blockquotes `>` for direct source quotes
- Include attribution with em-dash: `—Source Name`
