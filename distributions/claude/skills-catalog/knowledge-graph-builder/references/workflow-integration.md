# Workflow Integration: Knowledge Graph Builder

This document describes how `knowledge-graph-builder` integrates with other skills in the Knowledge Management ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `knowledge-architecture` | **Upstream** | Receive schema definitions |
| `research-synthesis-workflow` | **Upstream** | Store research in graph |
| `second-brain-librarian` | **Complementary** | Personal graph implementation |
| `recursive-systems-architect` | **Upstream** | Self-referential patterns |

## Prerequisites

Before invoking `knowledge-graph-builder`, ensure:

1. **Schema defined** - Ontology or architecture exists
2. **Technology chosen** - Neo4j, Neptune, in-memory
3. **Data sources identified** - What will populate the graph

## Handoff Patterns

### From: knowledge-architecture

**Trigger:** Ontology ready to implement.

**What to receive:**
- Entity type definitions
- Relationship specifications
- Constraint rules
- Cardinality limits

**Integration points:**
- Create node labels and properties
- Define relationship types
- Implement constraints
- Set up indexes

### From: research-synthesis-workflow

**Trigger:** Research ready for graph storage.

**What to receive:**
- Entities extracted from research
- Relationships identified
- Source attributions
- Confidence levels

**Integration points:**
- Import research entities
- Create connections
- Link to sources
- Track provenance

### To: second-brain-librarian

**Trigger:** Personal knowledge needs graph.

**What to hand off:**
- Graph query interface
- Connection patterns
- Navigation methods
- Export capabilities

**Expected output from librarian:**
- Personal usage patterns
- Query templates
- Visualization preferences

### From: recursive-systems-architect

**Trigger:** Graph should describe itself.

**What to receive:**
- Meta-node patterns
- Self-reference structures
- Introspection queries
- Evolution mechanisms

**Integration points:**
- Implement meta-schema
- Create reflection capabilities
- Enable schema queries

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Graph Implementation                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. KNOWLEDGE-ARCHITECTURE: Define schema                  │
│           │                                                 │
│           ▼                                                 │
│  2. RECURSIVE-SYSTEMS: Add meta-layer (optional)           │
│           │                                                 │
│           ▼                                                 │
│  3. KNOWLEDGE-GRAPH-BUILDER: Implement graph               │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. RESEARCH-SYNTHESIS         4b. SECOND-BRAIN-LIBRARIAN │
│      (populate graph)               (personal access)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing graph implementation, verify:

- [ ] Schema correctly implements architecture
- [ ] Indexes on frequently queried properties
- [ ] Constraints enforce data integrity
- [ ] Import pipelines tested
- [ ] Query patterns documented
- [ ] Backup strategy defined
- [ ] Performance benchmarked
- [ ] Access patterns understood

## Common Scenarios

### Research Knowledge Graph

1. **Knowledge Architecture:** Domain ontology
2. **Knowledge Graph Builder:** Implement graph schema
3. **Research Synthesis Workflow:** Populate with research

### Personal Knowledge Graph

1. **Second Brain Librarian:** Define personal needs
2. **Knowledge Architecture:** Personal taxonomy
3. **Knowledge Graph Builder:** Implement and connect

### Self-Describing System

1. **Recursive Systems Architect:** Meta-patterns
2. **Knowledge Architecture:** Meta-schema
3. **Knowledge Graph Builder:** Reflective implementation

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No schema | Inconsistent data | Define types first |
| Missing indexes | Slow queries | Index query patterns |
| Over-connected | Dense, slow graph | Meaningful connections only |
| No provenance | Unknown sources | Track data origins |

## Related Resources

- [Knowledge Management Skills Ecosystem Map](../../../docs/guides/knowledge-management-skills-ecosystem.md)
