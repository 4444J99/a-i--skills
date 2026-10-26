---
name: source-evaluation-bibliography
description: Evaluate source quality, build annotated bibliographies, and maintain curated reference collections. Covers the CRAAP test, source classification, citation management, and research documentation patterns. Triggers on source evaluation, bibliography creation, or research documentation requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - bibliography
  - source-evaluation
  - research
  - citations
  - curation
governance_phases: [shape]
organ_affinity: [all]
triggers: [user-asks-about-source-evaluation, context:research, context:bibliography, context:citations]
complements: [research-synthesis-workflow, technical-analytical-writing, second-brain-librarian]
---

# Source Evaluation & Bibliography

Evaluate, document, and maintain curated collections of references and sources.

## Source Evaluation Framework

### The CRAAP Test

| Criterion | Questions | Weight |
|-----------|-----------|--------|
| **Currency** | When was it published/updated? Is the information still valid? | Medium |
| **Relevance** | Does it address the specific question? Who is the intended audience? | High |
| **Authority** | Who is the author? What credentials/affiliations? | High |
| **Accuracy** | Is it evidence-based? Can claims be verified? Peer-reviewed? | Critical |
| **Purpose** | Is it informative, persuasive, or commercial? Any bias? | Medium |

### Source Tier Classification

| Tier | Source Type | Reliability | Example |
|------|-----------|-------------|---------|
| **S** | Primary research, official specs | Highest | Peer-reviewed papers, RFC documents, official API docs |
| **A** | Authoritative secondary | High | Textbooks, reputable technical blogs, conference proceedings |
| **B** | Community knowledge | Moderate | Stack Overflow answers (high-vote), well-maintained wikis |
| **C** | Informal | Variable | Blog posts, tutorials, forum discussions |
| **D** | Unverified | Low | Social media, anonymous posts, undated content |

### Evaluation Record

```yaml
source:
  title: "Designing Data-Intensive Applications"
  author: "Martin Kleppmann"
  type: book
  year: 2017
  url: "https://dataintensive.net/"
  tier: A
  evaluation:
    currency: Good (concepts still current despite 2017 publication)
    relevance: High (directly addresses distributed systems patterns)
    authority: Strong (researcher at Cambridge, industry experience)
    accuracy: Peer-reviewed content, extensively cited
    purpose: Educational, no commercial bias
  notes: "Definitive reference for distributed data systems. Chapter 5-9 most relevant."
  tags: [distributed-systems, databases, architecture]
  last_verified: 2026-03-20
```

## Annotated Bibliography Format

### Entry Structure

```markdown
## {Author Last}, {First}. "{Title}." *{Publication}*, {Year}. {URL}

**Tier:** {S/A/B/C/D} | **Relevance:** {High/Medium/Low} | **Last verified:** {Date}

**Summary:** {2-3 sentences describing the content and main argument}

**Key contributions:**
- {Specific idea, framework, or finding #1}
- {Specific idea, framework, or finding #2}

**Limitations:** {Any caveats, biases, or gaps}

**Connection:** {How this source relates to other sources or the project}
```

### Example Entry

```markdown
## Kleppmann, Martin. "Designing Data-Intensive Applications." O'Reilly, 2017.

**Tier:** A | **Relevance:** High | **Last verified:** 2026-03-20

**Summary:** Comprehensive guide to distributed data systems covering replication,
partitioning, transactions, and stream processing. Bridges theoretical CS concepts
with practical engineering tradeoffs.

**Key contributions:**
- Clear taxonomy of consistency models (linearizability, causal, eventual)
- Practical comparison of batch vs. stream processing architectures
- The "unbundling the database" framing for microservice data patterns

**Limitations:** Pre-dates serverless and edge computing patterns. Some implementation
details are framework-specific and may be dated.

**Connection:** Foundation for resilience-patterns and data-pipeline-architect skills.
Complements the CAP theorem discussion in redis-patterns.
```

## Bibliography Management

### Collection Structure

```
references/
├── bibliography.yaml          # Machine-readable catalog
├── by-topic/
│   ├── distributed-systems.md # Topic-organized annotations
│   ├── security.md
│   └── ai-agents.md
├── by-tier/
│   ├── tier-s.md              # Primary sources only
│   └── tier-a.md              # Authoritative secondary
└── reading-log.md             # Chronological reading notes
```

### Machine-Readable Catalog

```yaml
bibliography:
  - id: kleppmann2017
    title: "Designing Data-Intensive Applications"
    author: "Martin Kleppmann"
    year: 2017
    type: book
    tier: A
    topics: [distributed-systems, databases]
    cited_by: [resilience-patterns, data-pipeline-architect]

  - id: fowler2002
    title: "Patterns of Enterprise Application Architecture"
    author: "Martin Fowler"
    year: 2002
    type: book
    tier: A
    topics: [architecture, patterns]
    cited_by: [backend-implementation-patterns]
```

### Citation in Documents

```markdown
The circuit breaker pattern [kleppmann2017, ch.8] provides fault isolation
between services. This aligns with the bulkhead pattern described in
[nygard2018, ch.5], which isolates failure domains at the resource level.
```

## Curation Workflow

### Adding New Sources

1. **Discover** — Find source through research, recommendation, or citation chain
2. **Evaluate** — Apply CRAAP test and assign tier
3. **Annotate** — Write summary, key contributions, limitations
4. **Connect** — Link to existing sources and project skills
5. **Catalog** — Add to bibliography.yaml and topic files

### Periodic Review

```markdown
## Quarterly Review Checklist

- [ ] Verify URLs still resolve (automated: link-checker script)
- [ ] Check for updated editions or superseding publications
- [ ] Re-evaluate tier for sources whose domains have evolved
- [ ] Remove or demote sources that are no longer current
- [ ] Add newly discovered sources from recent research
```

## Anti-Patterns

- **Uncritical acceptance** — Every source needs evaluation, even authoritative ones
- **Recency bias** — Older sources can be foundational; evaluate on merit, not date alone
- **Single-source reliance** — Triangulate claims across multiple independent sources
- **No annotation** — A bibliography without annotations is just a link list
- **Stale references** — Sources need periodic re-verification
- **Collecting without connecting** — Always link sources to the questions they help answer
