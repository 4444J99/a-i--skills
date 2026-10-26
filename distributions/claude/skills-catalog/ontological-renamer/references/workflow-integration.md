# Workflow Integration

How to integrate ontological naming into development workflows.

## Naming Sessions

### Pre-Naming Checklist

Before starting a naming session:

```yaml
preparation:
  - [ ] Understand the thing being named
  - [ ] Identify target audience
  - [ ] List existing naming conventions in ecosystem
  - [ ] Gather stakeholder preferences
  - [ ] Define constraints (length, characters allowed)
```

### Session Structure

```yaml
naming_session:
  duration: 30-60 minutes

  phases:
    - name: "Discovery"
      time: 10min
      activities:
        - Identify essence (what IS it)
        - Identify function (what does it DO)
        - Identify domain (what CONTEXT)

    - name: "Generation"
      time: 15min
      activities:
        - Generate 10+ candidates
        - Apply naming patterns
        - Create compound forms

    - name: "Translation"
      time: 10min
      activities:
        - Translate top candidates to Latin
        - Translate to Greek
        - Verify translations

    - name: "Evaluation"
      time: 10min
      activities:
        - Score against criteria
        - Check for conflicts
        - Select recommendation

    - name: "Documentation"
      time: 5min
      activities:
        - Document rationale
        - Record alternatives
        - Note translations
```

## Evaluation Criteria

### Scoring Matrix

| Criterion | Weight | 1 (Poor) | 3 (Good) | 5 (Excellent) |
|-----------|--------|----------|----------|---------------|
| Clarity | 25% | Confusing | Clear enough | Immediately clear |
| Memorability | 20% | Forgettable | Decent recall | Highly memorable |
| Domain Fit | 20% | Wrong domain | Acceptable | Perfect fit |
| Uniqueness | 15% | Common/conflicts | Somewhat unique | Fully unique |
| Pronounceable | 10% | Difficult | Manageable | Easy to say |
| Extensible | 10% | Dead end | Some room | Highly extensible |

### Evaluation Template

```yaml
candidate:
  name: "skill-codex--agent-mastery"

  scores:
    clarity: 5
    memorability: 4
    domain_fit: 5
    uniqueness: 4
    pronounceable: 4
    extensible: 5

  weighted_score: 4.55

  notes:
    strengths:
      - "Codex implies curated knowledge"
      - "Mastery conveys expertise acquisition"
    weaknesses:
      - "Codex may sound old-fashioned"
```

## Integration with Project Lifecycle

### At Project Creation

```yaml
project_creation:
  steps:
    - "Define project purpose"
    - "Run naming session"
    - "Document name rationale"
    - "Register in namespace"
```

### During Development

```yaml
development_naming:
  modules:
    apply_pattern: "[project-name]-[module-name]"
    example: "skill-codex--auth-module"

  components:
    apply_pattern: "[module]-[component]"
    example: "auth-handler"
```

### At Release

```yaml
release_naming:
  versioned_names:
    pattern: "[name]-v[major]"
    example: "skill-codex-v2"

  codenames:
    pattern: "[adjective]-[noun]"
    example: "swift-falcon"
```

## Namespace Management

### Registry Structure

```yaml
namespace_registry:
  global:
    - skill-codex
    - agent-mastery

  by_team:
    platform:
      - infra--logging
      - infra--monitoring
    product:
      - feature--auth
      - feature--payments

  reserved:
    - core-*
    - internal-*
```

### Conflict Resolution

```yaml
conflict_handling:
  on_conflict:
    - Check if same concept (merge)
    - Check if different scope (namespace)
    - Rename one with differentiator

  differentiators:
    - Add domain prefix
    - Add version suffix
    - Add team prefix

  examples:
    conflict: "auth-handler"
    resolution: "api--auth-handler" vs "cli--auth-handler"
```

## Tooling Integration

### Git Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check new file/folder names follow conventions
for file in $(git diff --cached --name-only --diff-filter=A); do
    if ! validate_name "$file"; then
        echo "Error: '$file' does not follow naming conventions"
        echo "See: docs/naming-conventions.md"
        exit 1
    fi
done
```

### CI Validation

```yaml
# .github/workflows/naming-check.yml
name: Naming Conventions

on: [pull_request]

jobs:
  check-names:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate naming
        run: |
          python scripts/check_naming.py \
            --pattern "^[a-z]+(-[a-z]+)*(--[a-z]+(-[a-z]+)*)?$" \
            --path src/
```

### IDE Snippets

```json
// .vscode/snippets/naming.json
{
  "Ontological Name": {
    "prefix": "oname",
    "body": [
      "/**",
      " * Name: ${1:name}",
      " * Pattern: ${2:domain-function}",
      " * Latin: ${3:latin-translation}",
      " * Greek: ${4:greek-translation}",
      " */"
    ]
  }
}
```

## Documentation Integration

### Name Documentation Template

```markdown
# {{NAME}}

## Etymology

**English:** {{ENGLISH_NAME}}
**Latin:** {{LATIN_NAME}}
**Greek:** {{GREEK_NAME}}

## Components

| Component | Meaning | Role |
|-----------|---------|------|
| {{COMP_1}} | {{MEANING_1}} | {{ROLE_1}} |
| {{COMP_2}} | {{MEANING_2}} | {{ROLE_2}} |

## Rationale

{{WHY_THIS_NAME}}

## Alternatives Considered

| Name | Pros | Cons | Score |
|------|------|------|-------|
| {{ALT_1}} | {{PROS_1}} | {{CONS_1}} | {{SCORE_1}} |
| {{ALT_2}} | {{PROS_2}} | {{CONS_2}} | {{SCORE_2}} |

## Related Names

- {{RELATED_1}}
- {{RELATED_2}}
```

### Change Log

```markdown
# Naming Changelog

## [2024-01-15] Project Renamed

**Old Name:** my-project
**New Name:** skill-codex--agent-mastery

**Reason:** Original name was too generic. New name better reflects:
- The curated nature of the content (codex)
- The skill/expertise focus
- The agent enhancement purpose (mastery)

**Migration:** All references updated in:
- [ ] README.md
- [ ] package.json
- [ ] Documentation
- [ ] CI/CD pipelines
```

## Batch Renaming

### For Legacy Projects

```yaml
migration_plan:
  phase1:
    - Audit current names
    - Identify non-compliant names
    - Generate new names

  phase2:
    - Create mapping document
    - Update internal references
    - Update documentation

  phase3:
    - Update external references
    - Redirect old names
    - Communicate changes
```

### Bulk Rename Script

```python
#!/usr/bin/env python3
"""Apply naming conventions to directory structure."""

import os
import re

PATTERN = r'^[a-z]+(-[a-z]+)*(--[a-z]+(-[a-z]+)*)?$'

def validate_name(name):
    return bool(re.match(PATTERN, name))

def suggest_fix(name):
    # Convert camelCase to kebab-case
    fixed = re.sub(r'([a-z])([A-Z])', r'\1-\2', name).lower()
    # Convert underscores to hyphens
    fixed = fixed.replace('_', '-')
    return fixed

def audit_directory(path):
    issues = []
    for root, dirs, files in os.walk(path):
        for name in dirs + files:
            if not validate_name(name.split('.')[0]):
                issues.append({
                    'path': os.path.join(root, name),
                    'current': name,
                    'suggested': suggest_fix(name.split('.')[0])
                })
    return issues
```
