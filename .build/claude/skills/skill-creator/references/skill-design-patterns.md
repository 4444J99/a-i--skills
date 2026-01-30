# Skill Design Patterns

Patterns and anti-patterns for effective skill design.

## Pattern 1: Domain Knowledge Encapsulation

Capture specialized knowledge that Claude cannot reliably reproduce from training.

### When to Use

- Company-specific schemas, policies, or workflows
- API documentation that changes frequently
- Domain terminology and relationships
- Business logic rules

### Structure

```
domain-skill/
├── SKILL.md           # Workflows and procedures
└── references/
    ├── schema.md      # Data models and relationships
    ├── glossary.md    # Domain terminology
    └── policies.md    # Business rules
```

### Example: BigQuery Analyst Skill

```markdown
# SKILL.md
---
name: bigquery-analyst
description: Query company data warehouse. This skill should be used when users need to analyze business metrics or generate reports from BigQuery.
license: MIT
---

# BigQuery Analyst

This skill provides guidance for querying the company data warehouse.

## Database Connection

To connect, use the `analytics` project with read-only credentials.

## Common Queries

For user metrics, reference `references/schema.md` for table relationships.
For financial data, apply filters documented in `references/policies.md`.
```

### Anti-Pattern: Duplicated Knowledge

```markdown
# Bad: Schema duplicated in SKILL.md
The users table has columns: id, email, created_at, status...
The orders table has columns: id, user_id, total, created_at...

# Good: Schema in references, procedures in SKILL.md
For table schemas and relationships, see `references/schema.md`.
```

## Pattern 2: Deterministic Operations

Replace repetitive code generation with pre-written scripts.

### When to Use

- Operations that must be 100% reliable
- Complex algorithms that are error-prone to regenerate
- Tasks requiring specific library configurations
- Operations performed frequently

### Structure

```
tool-skill/
├── SKILL.md           # When and how to use scripts
└── scripts/
    ├── process.py     # Main operation
    └── validate.py    # Input validation
```

### Example: PDF Rotation Script

```python
#!/usr/bin/env python3
"""Rotate PDF pages by specified degrees."""

import sys
from pypdf import PdfReader, PdfWriter

def rotate_pdf(input_path: str, output_path: str, degrees: int) -> None:
    """Rotate all pages in a PDF.

    Args:
        input_path: Source PDF file
        output_path: Destination PDF file
        degrees: Rotation angle (90, 180, 270)
    """
    if degrees not in (90, 180, 270):
        raise ValueError(f"Degrees must be 90, 180, or 270, got {degrees}")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: rotate_pdf.py <input> <output> <degrees>")
        sys.exit(1)
    rotate_pdf(sys.argv[1], sys.argv[2], int(sys.argv[3]))
```

### Anti-Pattern: Inline Code Generation

```markdown
# Bad: Script code in SKILL.md that gets regenerated
To rotate a PDF, use this code:
```python
from pypdf import PdfReader, PdfWriter
# ... 50 lines of code ...
```

# Good: Reference pre-written script
To rotate a PDF, run: `scripts/rotate_pdf.py <input> <output> <degrees>`
```

## Pattern 3: Template-Based Generation

Provide starting points for common outputs.

### When to Use

- Standardized document formats
- Boilerplate code structures
- Configuration file templates
- Report formats

### Structure

```
generator-skill/
├── SKILL.md           # Customization guidance
└── assets/
    ├── templates/
    │   ├── report.md
    │   └── config.yaml
    └── examples/
        └── completed-report.md
```

### Example: Project Template

```markdown
# assets/templates/project-readme.md

# {{PROJECT_NAME}}

{{BRIEF_DESCRIPTION}}

## Installation

```bash
{{INSTALL_COMMAND}}
```

## Usage

{{USAGE_EXAMPLES}}

## Configuration

| Option | Description | Default |
|--------|-------------|---------|
{{CONFIG_TABLE}}

## License

{{LICENSE}}
```

### SKILL.md Reference

```markdown
## Creating Project Documentation

To generate a README:

1. Copy `assets/templates/project-readme.md` to the project root
2. Replace placeholders marked with `{{PLACEHOLDER_NAME}}`
3. Remove sections that don't apply
4. Add project-specific sections as needed
```

### Anti-Pattern: Regenerating Boilerplate

```markdown
# Bad: Full template in SKILL.md
When creating a README, include these sections:
# Project Name
Brief description...
## Installation
## Usage
...

# Good: Template file with customization notes
Copy `assets/templates/project-readme.md` and customize placeholders.
```

## Pattern 4: Workflow Orchestration

Guide multi-step processes with clear decision points.

### When to Use

- Complex procedures with branching logic
- Processes requiring user decisions
- Multi-tool coordination
- Quality assurance workflows

### Structure

```
workflow-skill/
├── SKILL.md           # Decision trees and procedures
└── references/
    └── checklist.md   # Validation criteria
```

### Example: Code Review Workflow

```markdown
## Review Process

### Phase 1: Initial Assessment

1. Identify the type of change (feature, bugfix, refactor)
2. Check for test coverage
3. Verify documentation updates

**Decision Point:** If tests are missing, request additions before proceeding.

### Phase 2: Detailed Review

For features:
- Verify acceptance criteria are met
- Check edge case handling
- Review error messages

For bugfixes:
- Confirm root cause is addressed
- Check for regression tests
- Verify related code paths

### Phase 3: Final Checklist

See `references/checklist.md` for sign-off criteria.
```

### Anti-Pattern: Vague Instructions

```markdown
# Bad: No clear steps or decision points
Review the code and provide feedback.

# Good: Structured workflow with decision logic
1. First, check X. If X is missing, request it.
2. Then verify Y according to criteria in references/checklist.md
3. Finally, confirm Z before approval.
```

## Pattern 5: Reference Lookup

Optimize for quick information retrieval.

### When to Use

- Frequently referenced data (codes, mappings, formulas)
- Large reference tables
- Specification documents
- API endpoint catalogs

### Structure

```
reference-skill/
├── SKILL.md           # How to search and use references
└── references/
    ├── codes.md       # Lookup tables
    └── formulas.md    # Calculations
```

### Example: HTTP Status Codes Reference

```markdown
# references/status-codes.md

## Status Code Quick Reference

### 2xx Success

| Code | Name | Use Case |
|------|------|----------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |

### 4xx Client Errors

| Code | Name | Use Case |
|------|------|----------|
| 400 | Bad Request | Malformed syntax |
| 401 | Unauthorized | Missing credentials |
| 403 | Forbidden | Valid credentials, no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | State conflict |
| 422 | Unprocessable | Validation failed |

### 5xx Server Errors

| Code | Name | Use Case |
|------|------|----------|
| 500 | Internal Error | Unexpected server failure |
| 502 | Bad Gateway | Upstream server error |
| 503 | Service Unavailable | Temporary overload |
```

### SKILL.md Search Guidance

```markdown
## Finding Status Codes

For HTTP status codes, see `references/status-codes.md`.

**Search patterns:**
- Grep `2xx` for success codes
- Grep `4xx` for client error codes
- Grep `5xx` for server error codes
- Grep specific code number (e.g., `422`)
```

## Size Guidelines

| Component | Recommended Size | Maximum |
|-----------|-----------------|---------|
| SKILL.md | 1,000-3,000 words | 5,000 words |
| Individual reference | 500-2,000 words | 10,000 words |
| Total references | 5,000-15,000 words | No hard limit |
| Scripts | As needed | No limit |
| Assets | As needed | Consider zip size |

## Decision Matrix

| Scenario | Pattern to Use |
|----------|---------------|
| Need to query company data | Domain Knowledge |
| Same code written repeatedly | Deterministic Operations |
| Generating similar documents | Template-Based Generation |
| Multi-step with decisions | Workflow Orchestration |
| Frequently looking up data | Reference Lookup |

## Combining Patterns

Most effective skills combine multiple patterns:

```
comprehensive-skill/
├── SKILL.md                    # Workflow orchestration
├── scripts/
│   └── process.py              # Deterministic operations
├── references/
│   ├── schema.md               # Domain knowledge
│   └── codes.md                # Reference lookup
└── assets/
    └── templates/              # Template-based generation
        └── output.md
```
