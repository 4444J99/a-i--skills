---
name: json-schema-design
description: Design and validate JSON Schemas for API contracts, configuration files, and data exchange formats. Covers schema composition, conditional validation, and code generation from schemas. Triggers on JSON Schema creation, data validation, or API contract design requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - json-schema
  - validation
  - api-contracts
  - data-modeling
governance_phases: [shape, build]
organ_affinity: [meta]
triggers: [user-asks-about-json-schema, context:data-validation, context:api-contract, file-type:*.schema.json]
complements: [api-design-patterns, configuration-management]
---

# JSON Schema Design

Define precise data contracts with JSON Schema for validation, documentation, and code generation.

## Schema Fundamentals

### Basic Types

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://organvm.dev/schemas/repo.json",
  "title": "Repository",
  "description": "An ORGANVM repository entry",
  "type": "object",
  "required": ["name", "organ", "tier", "status"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]*$",
      "minLength": 2,
      "maxLength": 64
    },
    "organ": {
      "type": "string",
      "enum": ["I", "II", "III", "IV", "V", "VI", "VII", "META"]
    },
    "tier": {
      "type": "string",
      "enum": ["flagship", "standard", "infrastructure"]
    },
    "status": {
      "type": "string",
      "enum": ["LOCAL", "CANDIDATE", "PUBLIC_PROCESS", "GRADUATED", "ARCHIVED"]
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true
    }
  },
  "additionalProperties": false
}
```

### Numeric Constraints

```json
{
  "priority": {
    "type": "integer",
    "minimum": 1,
    "maximum": 10
  },
  "score": {
    "type": "number",
    "exclusiveMinimum": 0,
    "maximum": 1.0
  }
}
```

## Composition

### $ref (Reuse)

```json
{
  "$defs": {
    "organ": {
      "type": "string",
      "enum": ["I", "II", "III", "IV", "V", "VI", "VII", "META"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  },
  "properties": {
    "source_organ": { "$ref": "#/$defs/organ" },
    "target_organ": { "$ref": "#/$defs/organ" },
    "created_at": { "$ref": "#/$defs/timestamp" }
  }
}
```

### allOf (Intersection / Extension)

```json
{
  "allOf": [
    { "$ref": "#/$defs/base-entity" },
    {
      "properties": {
        "extra_field": { "type": "string" }
      }
    }
  ]
}
```

### oneOf (Discriminated Union)

```json
{
  "oneOf": [
    {
      "properties": {
        "type": { "const": "skill" },
        "category": { "type": "string" }
      },
      "required": ["type", "category"]
    },
    {
      "properties": {
        "type": { "const": "bundle" },
        "includes": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["type", "includes"]
    }
  ],
  "discriminator": { "propertyName": "type" }
}
```

### if/then/else (Conditional)

```json
{
  "if": {
    "properties": { "tier": { "const": "flagship" } }
  },
  "then": {
    "required": ["ci_url", "docs_url"]
  }
}
```

## Patterns for Common Needs

### Extensible Enums

```json
{
  "status": {
    "anyOf": [
      { "enum": ["active", "archived", "draft"] },
      { "type": "string", "pattern": "^x-" }
    ]
  }
}
```

### Maps / Dictionaries

```json
{
  "metadata": {
    "type": "object",
    "additionalProperties": { "type": "string" },
    "propertyNames": { "pattern": "^[a-z_]+$" }
  }
}
```

### Nullable Fields

```json
{
  "description": {
    "oneOf": [
      { "type": "string" },
      { "type": "null" }
    ]
  }
}
```

## Validation in Python

```python
import jsonschema
import json
from pathlib import Path

def validate_entry(data: dict, schema_path: str) -> list[str]:
    schema = json.loads(Path(schema_path).read_text())
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    return [f"{'.'.join(str(p) for p in e.path)}: {e.message}" for e in errors]
```

## Schema Evolution

| Change | Safe? | Strategy |
|--------|-------|----------|
| Add optional field | Yes | No version bump needed |
| Add required field | No | Major version, provide default |
| Remove field | No | Deprecate first, then remove |
| Widen type (string → string\|number) | Yes | Backward compatible |
| Narrow type | No | Major version |
| Add enum value | Yes | Consumers should handle unknown |
| Remove enum value | No | Deprecate first |

## Anti-Patterns

- **No `additionalProperties: false`** — Typos in field names pass silently
- **Overly permissive types** — Use specific types and constraints
- **Inline definitions everywhere** — Extract to `$defs` for reuse
- **No `$id` or `$schema`** — Always specify schema version and identity
- **Validating only on write** — Validate on both read and write boundaries
