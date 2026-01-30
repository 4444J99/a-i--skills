# Implementation Patterns for Knowledge Architecture

## File Naming Patterns

### Entity Files

```
# Format: [type]-[identifier].md

project-in-midst-my-life.md
concept-modular-synthesis.md
tool-claude-desktop.md
work-welcome-to-spiral.md
person-self.md
```

### Relation Files

```
# Format: [domain]-[relation-type].md

projects-dependencies.md
concepts-contradictions.md
tools-integrations.md
```

### Index Files

```
# Format: index-[dimension].md

index-by-type.md
index-by-state.md
index-by-date.md
index-by-domain.md
```

---

## Linking Patterns

### Wikilink Style

```markdown
This project [[depends-on::project-alpha]] for its core functionality.

The concept [[contradicts::concept-legacy-approach]] established thinking.

See [[tool-claude-desktop]] for implementation details.
```

### Typed Links

```markdown
- depends-on:: [[project-alpha]]
- extends:: [[concept-base]]
- exemplifies:: [[pattern-feedback-loop]]
```

### Bidirectional Awareness

When linking A → B, consider:
- Should B → A exist?
- What is the inverse relation name?
- Should both be explicit or one inferred?

---

## Frontmatter Schema

### Minimal Schema

```yaml
---
type: project | concept | tool | work | person | event
title: Human-readable name
created: YYYY-MM-DD
---
```

### Standard Schema

```yaml
---
type: project
title: In Midst My Life
created: 2024-01-15
modified: 2024-12-01
state: active
phase: development

# Essential nature
nature: |
  Full-stack portfolio system serving as both 
  professional showcase and experimental platform.

# Relations
depends-on:
  - tool-next-js
  - tool-supabase
extends:
  - concept-modular-architecture
exemplifies:
  - pattern-recursive-self-reference

# Contexts
contexts:
  - professional
  - technical
  - creative

# Accidental properties (for filtering)
tags:
  - typescript
  - web
  - portfolio
---
```

### Event Schema

```yaml
---
type: event
title: Portfolio Launch Decision
date: 2024-06-15
event-type: decision

# Causes
triggered-by:
  - event-job-search-begin
efficient-cause: self
final-cause: establish professional presence

# Effects
resulted-in:
  - project-in-midst-my-life
changed:
  - state of professional-identity
---
```

---

## Directory Structures

### Flat with Metadata

```
knowledge/
├── project-alpha.md
├── project-beta.md
├── concept-x.md
├── concept-y.md
├── tool-a.md
└── _indices/
    ├── projects.md
    ├── concepts.md
    └── tools.md
```

**Pros**: Simple, no nesting decisions, relies on links/metadata
**Cons**: Large folders, harder visual scanning

### Type-Based Hierarchy

```
knowledge/
├── projects/
│   ├── project-alpha.md
│   └── project-beta.md
├── concepts/
│   ├── concept-x.md
│   └── concept-y.md
├── tools/
│   └── tool-a.md
└── indices/
    └── master.md
```

**Pros**: Clear type separation, familiar structure
**Cons**: Cross-type entities awkward, folder navigation required

### Context-Based Hierarchy

```
knowledge/
├── technical/
│   ├── projects/
│   └── tools/
├── creative/
│   ├── works/
│   └── concepts/
├── personal/
│   └── reflections/
└── meta/
    └── indices/
```

**Pros**: Grouped by domain of relevance
**Cons**: Same entity may need multiple placements

### Hybrid (Recommended)

```
knowledge/
├── entities/              # All primary substances
│   ├── project-alpha.md
│   ├── concept-x.md
│   └── tool-a.md
├── relations/             # Explicit relation maps
│   └── dependencies.md
├── views/                 # Computed/curated indices
│   ├── by-type.md
│   ├── by-state.md
│   └── by-domain.md
├── contexts/              # Domain-specific overlays
│   ├── technical/
│   └── creative/
└── meta/                  # System documentation
    ├── ontology.md
    └── conventions.md
```

---

## Query Patterns

### Dataview (Obsidian)

```dataview
TABLE state, phase, modified
FROM "entities"
WHERE type = "project" AND state = "active"
SORT modified DESC
```

### Tag-Based Queries

```
Find all entities that:
- Have tag #typescript
- Are in state "active"
- Depend on project-alpha
```

### Graph Queries

```
Starting from: concept-modular-synthesis
Find: All entities reachable via "exemplifies" relation
Depth: 2
```

---

## Evolution Patterns

### Append-Only History

```
entities/
└── concept-x.md           # Current version

history/
└── concept-x/
    ├── 2024-01-v1.md      # First version
    ├── 2024-03-v2.md      # Major revision
    └── changelog.md       # Summary of changes
```

### Inline History

```markdown
# Concept X

Current understanding as of 2024-06.

## History

### 2024-06 Revision
Changed understanding of relation to Y.

### 2024-03 Revision  
Added connection to Z.

### 2024-01 Original
Initial formulation.
```

### Git-Based History

Use version control on the knowledge base itself:
- Commits = conceptual changes
- Branches = exploratory thinking
- Tags = stable states

---

## Cross-System Integration

### External References

```yaml
---
external-refs:
  github: https://github.com/user/repo
  figma: https://figma.com/file/xyz
  notion: https://notion.so/page
  gdrive: https://drive.google.com/file/xyz
---
```

### Sync Patterns

```
External System → Importer → Knowledge Base → Exporter → External System

# Examples:
GitHub Issues → issue-tracker.py → entities/ → (manual review)
Google Docs → gdoc-import.py → entities/ → (link back via frontmatter)
```

### API Integrations

```python
# Conceptual: Query knowledge base programmatically
def find_dependencies(entity_id):
    """Return all entities this one depends on."""
    entity = load_entity(entity_id)
    return entity.frontmatter.get('depends-on', [])

def find_dependents(entity_id):
    """Return all entities that depend on this one."""
    all_entities = load_all_entities()
    return [e for e in all_entities 
            if entity_id in e.frontmatter.get('depends-on', [])]
```
