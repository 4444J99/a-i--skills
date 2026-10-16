# Manifest Schema Specification

Complete YAML/JSON schema for Claude project manifests.

## Root Structure

```yaml
manifest:
  id: string           # Required: Unique project identifier
  version: string      # Required: Manifest version (semver)
  created: datetime    # Required: ISO 8601 timestamp
  modified: datetime   # Optional: Last modification timestamp

  project:
    name: string       # Required: Project name
    description: string # Required: Brief description
    status: enum       # Required: active | archived | dormant
    tags: [string]     # Optional: Project-level tags
    repository: string # Optional: Git repository URL

files: [FileEntry]     # Required: List of file entries
threads: [ThreadEntry] # Optional: List of conversation threads
relations: [Relation]  # Optional: List of relationships
```

## FileEntry Schema

```yaml
FileEntry:
  id: string           # Required: Unique file ID (FILE-XXX)
  path: string         # Required: Relative file path
  type: enum           # Optional: source | config | doc | asset | generated
  thread_id: string    # Optional: Thread that created this file
  title: string        # Required: Human-readable title
  summary: string      # Required: One-line description
  notes: string        # Optional: Extended annotation (multiline)
  tags: [string]       # Optional: File-level tags
  depends_on: [string] # Optional: List of file IDs this depends on
  created: datetime    # Optional: Creation timestamp
  modified: datetime   # Optional: Last modification timestamp
  status: enum         # Optional: current | deprecated | removed
```

### File Types

| Type | Description | Examples |
|------|-------------|----------|
| `source` | Source code files | `.py`, `.ts`, `.go` |
| `config` | Configuration files | `.yaml`, `.json`, `.toml` |
| `doc` | Documentation | `.md`, `.rst`, `.txt` |
| `asset` | Static assets | images, fonts, data files |
| `generated` | Auto-generated files | build outputs, compiled files |

## ThreadEntry Schema

```yaml
ThreadEntry:
  id: string           # Required: Unique thread ID (THR-XXX)
  started: datetime    # Required: Start timestamp
  ended: datetime      # Optional: End timestamp
  title: string        # Required: Thread title
  summary: string      # Required: Brief summary of conversation
  accomplishments: [string]  # Optional: List of what was achieved
  files_created: [string]    # Optional: File IDs created
  files_modified: [string]   # Optional: File IDs modified
  decisions: [string]  # Optional: Key decisions made
  blockers: [string]   # Optional: Issues encountered
  next_steps: [string] # Optional: Planned follow-up work
  tags: [string]       # Optional: Thread-level tags
  parent_id: string    # Optional: Parent thread for continuations
```

## Relation Schema

```yaml
Relation:
  id: string           # Required: Unique relation ID (REL-XXX)
  type: enum           # Required: Relation type (see below)
  source: string       # Required: Source entity ID
  target: string       # Required: Target entity ID
  annotation: string   # Optional: Description of relationship
  strength: enum       # Optional: strong | weak | optional
  created: datetime    # Optional: When relation was established
```

### Relation Types

| Type | Direction | Meaning |
|------|-----------|---------|
| `depends_on` | Source → Target | Source requires target to function |
| `extends` | Source → Target | Source builds upon target |
| `implements` | Source → Target | Source implements target interface |
| `references` | Source → Target | Source refers to target |
| `supersedes` | Source → Target | Source replaces target |
| `tests` | Source → Target | Source contains tests for target |
| `documents` | Source → Target | Source documents target |

## Validation Rules

### ID Uniqueness

- All IDs must be unique within their category
- File IDs: `FILE-{SEQ}` where SEQ is zero-padded 3 digits
- Thread IDs: `THR-{SEQ}`
- Relation IDs: `REL-{SEQ}`
- Project IDs: `PROJ-{YEAR}-{SEQ}`

### Required Fields

```yaml
# Minimum valid manifest
manifest:
  id: "PROJ-2024-001"
  version: "1.0.0"
  created: "2024-01-15T00:00:00Z"
  project:
    name: "Project Name"
    description: "Description"
    status: active
files: []
```

### Path Conventions

- All file paths are relative to project root
- Use forward slashes regardless of OS
- No leading slash
- Case-sensitive

### Timestamp Format

All timestamps use ISO 8601 format:
- Full: `2024-01-15T10:30:00Z`
- Date only: `2024-01-15`
- With timezone: `2024-01-15T10:30:00-05:00`

## JSON Schema

For validation tools, use this JSON Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["manifest", "files"],
  "properties": {
    "manifest": {
      "type": "object",
      "required": ["id", "version", "created", "project"],
      "properties": {
        "id": { "type": "string", "pattern": "^PROJ-\\d{4}-\\d{3}$" },
        "version": { "type": "string" },
        "created": { "type": "string", "format": "date-time" },
        "project": {
          "type": "object",
          "required": ["name", "description", "status"],
          "properties": {
            "name": { "type": "string" },
            "description": { "type": "string" },
            "status": { "enum": ["active", "archived", "dormant"] }
          }
        }
      }
    },
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "path", "title", "summary"],
        "properties": {
          "id": { "type": "string", "pattern": "^FILE-\\d{3}$" },
          "path": { "type": "string" },
          "type": { "enum": ["source", "config", "doc", "asset", "generated"] },
          "title": { "type": "string" },
          "summary": { "type": "string" }
        }
      }
    }
  }
}
```
