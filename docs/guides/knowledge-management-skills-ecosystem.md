# Knowledge Management Skills Ecosystem

This guide maps the relationships between knowledge management skills in this repository and provides workflow guidance for using them together effectively.

## Skill Overview

| Skill | Category | Focus Area |
|-------|----------|------------|
| [`knowledge-architecture`](../../skills/knowledge/knowledge-architecture/) | knowledge | Ontological design and structure |
| [`knowledge-graph-builder`](../../skills/knowledge/knowledge-graph-builder/) | knowledge | Graph implementation and queries |
| [`research-synthesis-workflow`](../../skills/knowledge/research-synthesis-workflow/) | knowledge | Research systematization |
| [`second-brain-librarian`](../../skills/knowledge/second-brain-librarian/) | knowledge | Personal knowledge management |
| [`recursive-systems-architect`](../../skills/knowledge/recursive-systems-architect/) | knowledge | Self-referential systems design |

## Ecosystem Diagram

```mermaid
flowchart TB
    subgraph Meta["Meta Layer"]
        RSA[recursive-systems-architect]
    end

    subgraph Structure["Structural Layer"]
        KA[knowledge-architecture]
        KGB[knowledge-graph-builder]
    end

    subgraph Practice["Practice Layer"]
        RSW[research-synthesis-workflow]
        SBL[second-brain-librarian]
    end

    RSA -->|"Informs design of"| KA
    RSA -->|"Patterns for"| KGB
    KA -->|"Schemas for"| KGB
    KA -->|"Categories for"| SBL
    KGB -->|"Stores research in"| RSW
    RSW -->|"Outputs to"| SBL
    SBL -->|"Personal use of"| KGB
    RSA -.->|"Self-describes"| RSA
    RSW -.->|"Improves"| KA
    SBL -.->|"Refines"| KA

    style RSA fill:#f3e5f5
    style KA fill:#e3f2fd
    style KGB fill:#e3f2fd
    style RSW fill:#e8f5e9
    style SBL fill:#fff3e0
```

## Workflow Scenarios

### Scenario 1: Research Project

**Goal:** Systematically research and synthesize knowledge into a personal system.

```mermaid
sequenceDiagram
    participant Res as Researcher
    participant RSW as research-synthesis-workflow
    participant KA as knowledge-architecture
    participant KGB as knowledge-graph-builder
    participant SBL as second-brain-librarian

    Res->>RSW: 1. Design research workflow
    RSW-->>Res: Collection, processing, synthesis
    Res->>KA: 2. Define ontology for domain
    KA-->>Res: Concepts, relationships
    Res->>KGB: 3. Build knowledge graph
    KGB-->>Res: Connected knowledge
    Res->>SBL: 4. Integrate into second brain
    SBL-->>Res: Personal knowledge system
```

**Skill Sequence:**
1. **`research-synthesis-workflow`** - Design systematic research approach
2. **`knowledge-architecture`** - Define domain ontology
3. **`knowledge-graph-builder`** - Implement as connected graph
4. **`second-brain-librarian`** - Integrate into personal system

### Scenario 2: Knowledge Base Creation

**Goal:** Design and build an organizational knowledge base.

```mermaid
sequenceDiagram
    participant Arch as Architect
    participant KA as knowledge-architecture
    participant RSA as recursive-systems-architect
    participant KGB as knowledge-graph-builder
    participant SBL as second-brain-librarian

    Arch->>KA: 1. Design knowledge structure
    KA-->>Arch: Taxonomy, ontology
    Arch->>RSA: 2. Make system self-describing
    RSA-->>Arch: Meta-knowledge layer
    Arch->>KGB: 3. Implement graph database
    KGB-->>Arch: Query-able knowledge
    Arch->>SBL: 4. Define access patterns
    SBL-->>Arch: User interaction design
```

**Skill Sequence:**
1. **`knowledge-architecture`** - Design organizational structure
2. **`recursive-systems-architect`** - Add meta-layer for system evolution
3. **`knowledge-graph-builder`** - Implement graph storage
4. **`second-brain-librarian`** - Design user access patterns

### Scenario 3: Self-Referential System

**Goal:** Create a system that can describe and improve itself.

```mermaid
sequenceDiagram
    participant Des as Designer
    participant RSA as recursive-systems-architect
    participant KA as knowledge-architecture
    participant KGB as knowledge-graph-builder

    Des->>RSA: 1. Design recursive patterns
    RSA-->>Des: Self-reference structures
    Des->>KA: 2. Create meta-ontology
    KA-->>Des: Schema that describes schemas
    Des->>KGB: 3. Implement with reflection
    KGB-->>Des: Graph that queries itself
```

**Skill Sequence:**
1. **`recursive-systems-architect`** - Design self-referential patterns
2. **`knowledge-architecture`** - Create meta-level ontology
3. **`knowledge-graph-builder`** - Implement with introspection

## Decision Tree: Which Skill to Use?

```mermaid
flowchart TD
    Start([What do you need?]) --> Q1{Scope?}

    Q1 -->|Personal| Q2{Activity?}
    Q2 -->|Research| RSW[research-synthesis-workflow]
    Q2 -->|Organization| SBL[second-brain-librarian]
    Q2 -->|Connections| KGB[knowledge-graph-builder]

    Q1 -->|Organizational| Q3{Phase?}
    Q3 -->|Design| KA[knowledge-architecture]
    Q3 -->|Implementation| KGB
    Q3 -->|Meta-design| RSA[recursive-systems-architect]

    Q1 -->|Meta/Philosophical| RSA

    Q1 -->|Domain-specific| Q4{Existing structure?}
    Q4 -->|No| KA
    Q4 -->|Yes| KGB

    style RSA fill:#f3e5f5
    style KA fill:#e3f2fd
    style KGB fill:#e3f2fd
    style RSW fill:#e8f5e9
    style SBL fill:#fff3e0
```

## Cross-Reference Matrix

This matrix shows when each skill might invoke or reference another:

| Primary Skill | Invokes | For |
|---------------|---------|-----|
| `knowledge-architecture` | `knowledge-graph-builder` | Implementing the ontology |
| `knowledge-architecture` | `recursive-systems-architect` | Meta-level design |
| `knowledge-graph-builder` | `knowledge-architecture` | Schema guidance |
| `knowledge-graph-builder` | `second-brain-librarian` | Personal use patterns |
| `research-synthesis-workflow` | `knowledge-architecture` | Domain structure |
| `research-synthesis-workflow` | `knowledge-graph-builder` | Knowledge storage |
| `second-brain-librarian` | `knowledge-architecture` | Organizational categories |
| `second-brain-librarian` | `knowledge-graph-builder` | Connection implementation |
| `recursive-systems-architect` | `knowledge-architecture` | Meta-ontology design |
| `recursive-systems-architect` | `knowledge-graph-builder` | Self-referential implementation |

## Common Handoff Patterns

### Architecture → Graph Builder
When ontology is defined, implement it:
- Entity definitions
- Relationship types
- Constraints and rules
- Query patterns

### Research Workflow → Second Brain
When research is synthesized, internalize it:
- Key insights
- Source references
- Connection points
- Actionable knowledge

### Recursive Architect → Architecture
When meta-patterns are designed, apply them:
- Schema of schemas
- Evolution patterns
- Self-improvement mechanisms

### Second Brain → Knowledge Architecture
When personal patterns emerge, formalize them:
- Emerging categories
- Usage patterns
- Natural connections

## Best Practices

### Sequential vs. Parallel Usage
- **Sequential:** New knowledge base (architecture → graph → librarian)
- **Parallel:** Research + second brain maintenance can coexist

### Avoiding Overlap
- **Structural concerns:** `knowledge-architecture` owns ontology design
- **Implementation concerns:** `knowledge-graph-builder` owns graph technology
- **Research concerns:** `research-synthesis-workflow` owns research process
- **Personal concerns:** `second-brain-librarian` owns personal knowledge
- **Meta concerns:** `recursive-systems-architect` owns self-reference

### When to Combine Skills
Some projects benefit from multiple skills:
- **Research to knowledge:** workflow + architecture + graph + brain
- **Organizational KB:** architecture + graph + recursive
- **Personal system:** brain + architecture + graph

## Flexible Relationships

Unlike linear ecosystems, knowledge management has fluid relationships:

```mermaid
flowchart LR
    RSW[Research] <--> KA[Architecture]
    KA <--> KGB[Graph]
    KGB <--> SBL[Brain]
    SBL <--> RSW
    RSA[Recursive] --> KA
    RSA --> KGB
    RSA -.-> RSA

    style RSA fill:#f3e5f5
    style KA fill:#e3f2fd
    style KGB fill:#e3f2fd
    style RSW fill:#e8f5e9
    style SBL fill:#fff3e0
```

Knowledge flows in all directions, with each skill enriching the others. The recursive architect provides meta-patterns that can be applied anywhere.

## Related Resources

- [Creating Skills Guide](./creating-skills.md)
- [Skill Specification](../api/skill-spec.md)
- [Getting Started](./getting-started.md)
