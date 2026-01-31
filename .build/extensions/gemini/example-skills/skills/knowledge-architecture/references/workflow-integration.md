# Workflow Integration: Knowledge Architecture

This document describes how `knowledge-architecture` integrates with other skills in the Knowledge Management ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `knowledge-graph-builder` | **Downstream** | Implement the designed ontology |
| `research-synthesis-workflow` | **Upstream** | Domain patterns from research |
| `second-brain-librarian` | **Downstream** | Categories for personal system |
| `recursive-systems-architect` | **Complementary** | Meta-ontology design |

## Prerequisites

Before invoking `knowledge-architecture`, ensure:

1. **Domain scope defined** - What knowledge area to structure
2. **Use cases known** - How the structure will be used
3. **Existing knowledge audited** - What already exists

## Handoff Patterns

### From: research-synthesis-workflow

**Trigger:** Research reveals domain structure.

**What to receive:**
- Key concepts identified
- Natural categories emerging
- Relationships observed
- Hierarchies discovered

**Integration points:**
- Formalize discovered patterns
- Create explicit ontology
- Define relationship types

### To: knowledge-graph-builder

**Trigger:** Ontology ready for implementation.

**What to hand off:**
- Entity type definitions
- Relationship type specifications
- Cardinality constraints
- Validation rules

**Expected output from graph:**
- Implemented schema
- Query patterns
- Data import mappings

### To: second-brain-librarian

**Trigger:** Categories ready for personal use.

**What to hand off:**
- Tagging taxonomy
- Folder structure
- Link type definitions
- Note templates

**Expected output from librarian:**
- Personal system structure
- Capture workflows
- Retrieval patterns

### To/From: recursive-systems-architect

**Trigger:** Meta-level design needed.

**What to exchange:**
- Meta-ontology patterns (from recursive)
- Domain ontology (to recursive)
- Evolution mechanisms (from recursive)
- Refinement feedback (to recursive)

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Knowledge Architecture                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. RESEARCH-SYNTHESIS: Discover domain patterns           │
│           │                                                 │
│           ▼                                                 │
│  2. RECURSIVE-SYSTEMS: Design meta-layer (optional)        │
│           │                                                 │
│           ▼                                                 │
│  3. KNOWLEDGE-ARCHITECTURE: Design ontology                │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. KNOWLEDGE-GRAPH-BUILDER   4b. SECOND-BRAIN-LIBRARIAN  │
│      (implement schema)            (personal use)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing architecture, verify:

- [ ] All core concepts defined
- [ ] Relationships have clear semantics
- [ ] Hierarchy levels appropriate
- [ ] Edge cases considered
- [ ] Evolution path possible
- [ ] Documentation complete
- [ ] Example instances provided
- [ ] Validation rules specified

## Common Scenarios

### Domain Ontology

1. **Research Synthesis Workflow:** Study the domain
2. **Knowledge Architecture:** Design formal ontology
3. **Knowledge Graph Builder:** Implement in graph DB

### Personal Knowledge Structure

1. **Knowledge Architecture:** Design personal taxonomy
2. **Second Brain Librarian:** Apply to note system
3. **Knowledge Graph Builder:** Enable connections

### Meta-Knowledge System

1. **Recursive Systems Architect:** Design meta-patterns
2. **Knowledge Architecture:** Apply to specific domain
3. **Knowledge Graph Builder:** Self-describing implementation

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Over-classification | Too many categories | Start simple, refine |
| Rigid hierarchy | Can't adapt | Allow multiple parents |
| No relationships | Just a list | Define explicit links |
| Missing evolution | Outdated quickly | Build in change mechanism |

## Related Resources

- [Knowledge Management Skills Ecosystem Map](../../../docs/guides/knowledge-management-skills-ecosystem.md)
