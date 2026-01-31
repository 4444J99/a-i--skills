# Workflow Integration: Second Brain Librarian

This document describes how `second-brain-librarian` integrates with other skills in the Knowledge Management ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `knowledge-architecture` | **Upstream** | Receive categories and structure |
| `knowledge-graph-builder` | **Complementary** | Graph-based personal knowledge |
| `research-synthesis-workflow` | **Upstream** | Receive synthesized research |
| `recursive-systems-architect` | **Complementary** | System self-improvement |

## Prerequisites

Before invoking `second-brain-librarian`, ensure:

1. **Tool chosen** - Obsidian, Notion, Roam, etc.
2. **Workflow needs understood** - How you work
3. **Existing notes audited** - What's already there

## Handoff Patterns

### From: knowledge-architecture

**Trigger:** Structure ready for personal system.

**What to receive:**
- Tagging taxonomy
- Folder organization
- Note templates
- Link types

**Integration points:**
- Set up folder structure
- Create template library
- Configure tagging system

### From: research-synthesis-workflow

**Trigger:** Research ready for personal capture.

**What to receive:**
- Key insights and findings
- Source references
- Actionable items
- Connection suggestions

**Integration points:**
- Create research notes
- Link to existing knowledge
- Tag and categorize
- Queue actions

### To: knowledge-graph-builder

**Trigger:** Personal knowledge needs graph.

**What to hand off:**
- Notes and connections
- Tag relationships
- Backlink patterns
- Query needs

**Expected output from graph:**
- Visualization of connections
- Graph queries for retrieval
- Pattern discovery

### To: knowledge-architecture

**Trigger:** Usage patterns suggest improvements.

**What to hand off:**
- Categories that work
- Relationships that emerge
- Pain points in structure
- Suggested refinements

**Expected output from architecture:**
- Improved taxonomy
- New category definitions
- Structure evolution

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Personal Knowledge System                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. KNOWLEDGE-ARCHITECTURE: Define personal structure      │
│           │                                                 │
│           ▼                                                 │
│  2. SECOND-BRAIN-LIBRARIAN: Set up system                  │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. RESEARCH-SYNTHESIS         3b. KNOWLEDGE-GRAPH        │
│      (feed insights in)             (visualize connections)│
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. Continuous use and refinement                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing second brain setup, verify:

- [ ] Capture workflow frictionless
- [ ] Categorization intuitive
- [ ] Retrieval effective
- [ ] Connections discoverable
- [ ] Review system in place
- [ ] Archive strategy defined
- [ ] Mobile access working
- [ ] Backup configured

## Common Scenarios

### Zettelkasten Implementation

1. **Knowledge Architecture:** Slip-box structure
2. **Second Brain Librarian:** Note workflow
3. **Knowledge Graph Builder:** Link visualization

### Getting Things Done (GTD)

1. **Second Brain Librarian:** Capture system
2. **Knowledge Architecture:** Project/context taxonomy
3. **Research Synthesis Workflow:** Reference collection

### Learning Management

1. **Research Synthesis Workflow:** Study materials
2. **Second Brain Librarian:** Personal notes
3. **Knowledge Graph Builder:** Concept maps

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Over-organizing | Friction in capture | Start simple |
| Never reviewing | Dead knowledge | Regular review ritual |
| No connections | Just a filing cabinet | Active linking |
| Tool obsession | Process over content | Focus on knowledge |

## Related Resources

- [Knowledge Management Skills Ecosystem Map](../../../docs/guides/knowledge-management-skills-ecosystem.md)
