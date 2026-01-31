# Workflow Integration: Research Synthesis Workflow

This document describes how `research-synthesis-workflow` integrates with other skills in the Knowledge Management ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `knowledge-architecture` | **Downstream** | Informs domain structure |
| `knowledge-graph-builder` | **Downstream** | Store research in graph |
| `second-brain-librarian` | **Downstream** | Personal knowledge capture |
| `recursive-systems-architect` | **Complementary** | Research about research |

## Prerequisites

Before invoking `research-synthesis-workflow`, ensure:

1. **Research question defined** - What you want to learn
2. **Sources identified** - Where to gather information
3. **Output format known** - How to use the synthesis

## Handoff Patterns

### To: knowledge-architecture

**Trigger:** Research reveals domain structure.

**What to hand off:**
- Discovered concepts
- Natural categorizations
- Relationship patterns
- Hierarchies observed

**Expected output from architecture:**
- Formal ontology
- Category definitions
- Relationship types

### To: knowledge-graph-builder

**Trigger:** Research ready for structured storage.

**What to hand off:**
- Extracted entities
- Identified relationships
- Source citations
- Confidence assessments

**Expected output from graph:**
- Populated knowledge graph
- Queryable connections
- Source traceability

### To: second-brain-librarian

**Trigger:** Research insights for personal system.

**What to hand off:**
- Key findings
- Source references
- Actionable insights
- Connection opportunities

**Expected output from librarian:**
- Integrated into personal system
- Connected to existing knowledge
- Retrievable when needed

### From/To: recursive-systems-architect

**Trigger:** Research process improvement.

**What to exchange:**
- Meta-research patterns (from recursive)
- Research process observations (to recursive)
- Improvement suggestions (from recursive)

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Research Synthesis                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. RESEARCH-SYNTHESIS-WORKFLOW: Systematic research       │
│           │                                                 │
│           ├─────────────────────────────────────────┐       │
│           │             │             │             │       │
│           ▼             ▼             ▼             ▼       │
│      KNOWLEDGE     KNOWLEDGE-GRAPH  SECOND-BRAIN  RECURSIVE│
│      ARCHITECTURE     BUILDER       LIBRARIAN     SYSTEMS  │
│      (structure)    (store)        (personal)    (improve) │
│           │             │             │             │       │
│           └─────────────┴─────────────┴─────────────┘       │
│                          │                                  │
│                          ▼                                  │
│  2. Knowledge synthesized and actionable                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing research synthesis, verify:

- [ ] Research question answered
- [ ] Sources properly cited
- [ ] Key findings extracted
- [ ] Connections identified
- [ ] Gaps acknowledged
- [ ] Synthesis coherent
- [ ] Actionable insights clear
- [ ] Next steps defined

## Common Scenarios

### Academic Research

1. **Research Synthesis Workflow:** Literature review
2. **Knowledge Architecture:** Domain taxonomy
3. **Knowledge Graph Builder:** Citation network

### Market Research

1. **Research Synthesis Workflow:** Competitive analysis
2. **Second Brain Librarian:** Strategic insights
3. **Knowledge Architecture:** Market structure

### Learning Project

1. **Research Synthesis Workflow:** Topic exploration
2. **Second Brain Librarian:** Personal notes
3. **Knowledge Graph Builder:** Concept connections

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No system | Chaotic collection | Use structured workflow |
| No synthesis | Just summaries | Connect and conclude |
| Missing sources | Can't verify | Track all citations |
| No action | Knowledge hoarded | Extract actionable insights |

## Related Resources

- [Knowledge Management Skills Ecosystem Map](../../../docs/guides/knowledge-management-skills-ecosystem.md)
