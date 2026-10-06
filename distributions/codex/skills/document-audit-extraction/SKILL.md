---
name: document-audit-extraction
description: Audit document collections to extract features, identify patterns, assess quality, and build structured inventories. Covers metadata extraction, content classification, gap analysis, and coverage mapping. Triggers on document audit, content inventory, or document feature extraction requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - document-audit
  - content-inventory
  - metadata-extraction
  - gap-analysis
  - quality-assessment
governance_phases: [shape, prove]
governance_norm_group: documentation-standard
organ_affinity: [all]
triggers: [user-asks-about-document-audit, context:content-inventory, context:doc-quality, context:document-review]
complements: [stranger-test-protocol, technical-analytical-writing, knowledge-architecture]
---

# Document Audit & Feature Extraction

Systematically inventory, evaluate, and extract structured data from document collections.

## Audit Framework

### Four-Phase Audit

```
Phase 1: Inventory    → What exists?
Phase 2: Classify     → What type is each document?
Phase 3: Evaluate     → What's the quality?
Phase 4: Extract      → What structured data can we pull?
```

## Phase 1: Inventory

### Automated Inventory

```python
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DocumentEntry:
    path: str
    name: str
    extension: str
    size_bytes: int
    modified: str
    word_count: int
    has_frontmatter: bool

def inventory_documents(root: str, patterns: list[str] = ["*.md", "*.txt", "*.yaml"]) -> list[DocumentEntry]:
    entries = []
    for pattern in patterns:
        for path in Path(root).rglob(pattern):
            content = path.read_text(errors="ignore")
            entries.append(DocumentEntry(
                path=str(path.relative_to(root)),
                name=path.stem,
                extension=path.suffix,
                size_bytes=path.stat().st_size,
                modified=path.stat().st_mtime,
                word_count=len(content.split()),
                has_frontmatter=content.startswith("---"),
            ))
    return entries
```

### Inventory Report

```markdown
## Document Inventory

| Path | Type | Words | Frontmatter | Modified |
|------|------|-------|-------------|----------|
| skills/dev/testing/SKILL.md | skill | 1,245 | Yes | 2026-03-20 |
| docs/CHANGELOG.md | changelog | 890 | No | 2026-03-19 |
| README.md | readme | 450 | No | 2026-03-18 |

**Total:** 142 documents | **With frontmatter:** 105 | **Total words:** 185,000
```

## Phase 2: Classification

### Document Type Taxonomy

| Type | Signal | Example |
|------|--------|---------|
| **Skill** | YAML frontmatter with `name:`, in skills/ | SKILL.md |
| **Configuration** | YAML/JSON schema | seed.yaml, registry.json |
| **Guide** | Tutorial structure, step-by-step | getting-started.md |
| **Reference** | API docs, schema docs | api-spec.md |
| **Decision** | ADR format, options + decision | adr-001.md |
| **Changelog** | Date-ordered entries | CHANGELOG.md |
| **Policy** | Rules, constraints | CONTRIBUTING.md |

### Automated Classification

```python
def classify_document(path: str, content: str) -> str:
    if "skills/" in path and content.startswith("---"):
        return "skill"
    if path.endswith("seed.yaml") or path.endswith("registry.json"):
        return "configuration"
    if "## Step" in content or "### Step" in content:
        return "guide"
    if "## Decision" in content or "## Alternatives" in content:
        return "decision"
    if "## [" in content and any(d in content for d in ["Added", "Fixed", "Changed"]):
        return "changelog"
    return "general"
```

## Phase 3: Quality Evaluation

### Quality Scorecard

| Criterion | Weight | Score (0-3) | Notes |
|-----------|--------|-------------|-------|
| **Completeness** | 30% | | All required sections present? |
| **Accuracy** | 25% | | Information correct and current? |
| **Clarity** | 20% | | Understandable without prior context? |
| **Structure** | 15% | | Logical organization, headings, formatting? |
| **Maintenance** | 10% | | Updated date, versioned, no stale links? |

### Automated Quality Checks

```python
def quality_check(path: str, content: str) -> dict:
    checks = {
        "has_title": content.startswith("#") or content.startswith("---"),
        "has_sections": content.count("\n##") >= 2,
        "reasonable_length": 100 < len(content.split()) < 10000,
        "no_todo_left": "TODO" not in content and "FIXME" not in content,
        "no_broken_links": not re.search(r'\[.*?\]\(\s*\)', content),
        "has_code_examples": "```" in content,
        "frontmatter_complete": check_frontmatter_fields(content),
    }
    score = sum(checks.values()) / len(checks)
    return {"checks": checks, "score": round(score, 2)}
```

## Phase 4: Feature Extraction

### Metadata Extraction

```python
import yaml
import re

def extract_frontmatter(content: str) -> dict | None:
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None

def extract_features(content: str) -> dict:
    return {
        "headings": re.findall(r'^#+\s+(.+)$', content, re.MULTILINE),
        "code_blocks": len(re.findall(r'```', content)) // 2,
        "links": re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content),
        "images": re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content),
        "tables": content.count("\n|"),
        "todos": re.findall(r'- \[ \]\s+(.+)', content),
    }
```

### Cross-Reference Mapping

```python
def build_reference_graph(documents: list[dict]) -> dict:
    graph = {}
    for doc in documents:
        links = extract_features(doc["content"])["links"]
        graph[doc["path"]] = {
            "outgoing": [link[1] for link in links if not link[1].startswith("http")],
            "incoming": [],
        }

    # Build incoming links
    for source, data in graph.items():
        for target in data["outgoing"]:
            if target in graph:
                graph[target]["incoming"].append(source)

    return graph
```

## Gap Analysis

```python
def gap_analysis(inventory: list[dict], expected: dict) -> dict:
    existing = {doc["path"] for doc in inventory}
    gaps = {
        "missing_required": [p for p in expected.get("required", []) if p not in existing],
        "missing_recommended": [p for p in expected.get("recommended", []) if p not in existing],
        "orphaned": [p for p in existing if p not in expected.get("all_known", existing)],
        "empty_files": [doc["path"] for doc in inventory if doc["word_count"] < 10],
    }
    return gaps
```

## Anti-Patterns

- **Manual-only audits** — Automate what you can; reserve human judgment for quality assessment
- **Audit without action** — Every finding should map to a remediation action
- **One-time audit** — Build continuous monitoring, not point-in-time snapshots
- **Counting without evaluating** — Document count is vanity; quality score is actionable
- **No baseline** — Establish quality benchmarks before auditing
- **Ignoring cross-references** — Orphaned documents and broken links indicate structural problems
