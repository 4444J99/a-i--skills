# Workflow Integration

How to integrate manifests into development workflows.

## Git Integration

### Commit Hooks

Update manifest on commit:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if manifest needs updating
python3 scripts/check_manifest.py

# Auto-update file modification times
python3 scripts/update_manifest_timestamps.py
```

### Manifest in Version Control

```
project/
├── manifest.yaml     # Track in git
├── .manifest/        # Optional: manifest-related scripts
│   ├── validate.py
│   └── report.py
└── ...
```

### Branch Strategy

```yaml
# manifest.yaml in feature branch
manifest:
  branch: feature/new-auth
  parent_branch: main

threads:
  - id: "THR-020"
    title: "Implementing OAuth support"
    branch: feature/new-auth
```

## Session Workflow

### Starting a Session

1. Open or create manifest
2. Create new thread entry
3. Note current state

```yaml
threads:
  - id: "THR-021"
    started: "2024-01-20T09:00:00Z"
    title: "Session: Refactoring auth module"
    goals:
      - "Extract common auth logic"
      - "Add unit tests"
```

### During Session

Update as you work:

```yaml
threads:
  - id: "THR-021"
    # ... existing fields ...
    files_created:
      - "FILE-045"  # Added new file
    files_modified:
      - "FILE-012"  # Updated existing
    notes: |
      In progress: extracted BaseAuthenticator.
      Next: migrate OAuthHandler to use base class.
```

### Ending Session

Complete the thread entry:

```yaml
threads:
  - id: "THR-021"
    started: "2024-01-20T09:00:00Z"
    ended: "2024-01-20T12:30:00Z"
    title: "Session: Refactoring auth module"
    summary: "Extracted common auth logic, added tests"
    accomplishments:
      - "Created BaseAuthenticator abstract class"
      - "Migrated OAuthHandler to new base"
      - "Added 15 unit tests (90% coverage)"
    files_created: ["FILE-045", "FILE-046"]
    files_modified: ["FILE-012", "FILE-013"]
    decisions:
      - "Used ABC over Protocol: need runtime isinstance checks"
    next_steps:
      - "Migrate remaining auth handlers"
      - "Update integration tests"
```

## Automation Scripts

### Generate Manifest from Directory

```python
#!/usr/bin/env python3
"""Generate initial manifest from directory structure."""

import os
import yaml
from datetime import datetime

def generate_manifest(root_dir, project_name):
    files = []
    file_id = 1

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            filepath = os.path.relpath(
                os.path.join(dirpath, filename),
                root_dir
            )
            files.append({
                'id': f'FILE-{file_id:03d}',
                'path': filepath,
                'title': filename,
                'summary': 'TODO: Add summary',
                'type': get_file_type(filename)
            })
            file_id += 1

    manifest = {
        'manifest': {
            'id': f'PROJ-{datetime.now().year}-001',
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'project': {
                'name': project_name,
                'description': 'TODO: Add description',
                'status': 'active'
            }
        },
        'files': files,
        'threads': [{
            'id': 'THR-001',
            'started': datetime.now().isoformat(),
            'title': 'Initial manifest creation',
            'summary': 'Auto-generated manifest from existing files'
        }]
    }

    return manifest
```

### Validate Manifest

```python
#!/usr/bin/env python3
"""Validate manifest integrity."""

import yaml
import sys

def validate_manifest(manifest_path):
    with open(manifest_path) as f:
        data = yaml.safe_load(f)

    errors = []

    # Check required fields
    if 'manifest' not in data:
        errors.append("Missing 'manifest' section")

    # Check ID uniqueness
    file_ids = [f['id'] for f in data.get('files', [])]
    if len(file_ids) != len(set(file_ids)):
        errors.append("Duplicate file IDs found")

    # Check reference integrity
    valid_file_ids = set(file_ids)
    for rel in data.get('relations', []):
        if rel['source'] not in valid_file_ids:
            errors.append(f"Invalid source reference: {rel['source']}")
        if rel['target'] not in valid_file_ids:
            errors.append(f"Invalid target reference: {rel['target']}")

    return errors
```

### Generate Markdown Report

```python
#!/usr/bin/env python3
"""Generate markdown report from manifest."""

import yaml

def generate_report(manifest_path):
    with open(manifest_path) as f:
        data = yaml.safe_load(f)

    m = data['manifest']
    report = f"""# {m['project']['name']}

{m['project']['description']}

**Status:** {m['project']['status']}
**Created:** {m['created']}
**Manifest Version:** {m['version']}

## Files ({len(data['files'])})

| ID | Path | Type | Summary |
|----|------|------|---------|
"""

    for f in data['files']:
        report += f"| {f['id']} | `{f['path']}` | {f.get('type', '-')} | {f['summary']} |\n"

    if data.get('threads'):
        report += f"\n## Threads ({len(data['threads'])})\n\n"
        for t in data['threads']:
            report += f"### {t['id']}: {t['title']}\n\n"
            report += f"{t.get('summary', 'No summary')}\n\n"

    return report
```

## IDE Integration

### VS Code Tasks

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate Manifest",
      "type": "shell",
      "command": "python3 scripts/validate_manifest.py manifest.yaml"
    },
    {
      "label": "Generate Report",
      "type": "shell",
      "command": "python3 scripts/generate_report.py manifest.yaml > MANIFEST_REPORT.md"
    }
  ]
}
```

### Snippets

```json
// .vscode/snippets/yaml.json
{
  "New File Entry": {
    "prefix": "mfile",
    "body": [
      "- id: \"FILE-${1:001}\"",
      "  path: \"${2:path/to/file}\"",
      "  type: ${3|source,config,doc,asset,generated|}",
      "  title: \"${4:Title}\"",
      "  summary: \"${5:Summary}\"",
      "  notes: |",
      "    ${6:Notes}"
    ]
  },
  "New Thread Entry": {
    "prefix": "mthread",
    "body": [
      "- id: \"THR-${1:001}\"",
      "  started: \"${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}T${CURRENT_HOUR}:${CURRENT_MINUTE}:00Z\"",
      "  title: \"${2:Thread Title}\"",
      "  summary: \"${3:Summary}\"",
      "  accomplishments:",
      "    - \"${4:What was done}\""
    ]
  }
}
```

## CI/CD Integration

### Manifest Validation in CI

```yaml
# .github/workflows/validate.yml
name: Validate Manifest

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pyyaml
      - run: python scripts/validate_manifest.py manifest.yaml
```

### Auto-update on PR

```yaml
# .github/workflows/manifest-update.yml
name: Update Manifest

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update file timestamps
        run: python scripts/update_manifest_timestamps.py
      - name: Commit if changed
        run: |
          git diff --quiet || (git add manifest.yaml && git commit -m "Update manifest timestamps")
```
