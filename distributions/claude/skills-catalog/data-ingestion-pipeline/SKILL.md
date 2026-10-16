---
name: data-ingestion-pipeline
description: Build data ingestion pipelines for batch and streaming data from multiple sources. Covers extraction strategies, format normalization, deduplication, validation gates, and staging patterns. Triggers on data ingestion, ETL pipeline, or data import architecture requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - data-ingestion
  - etl
  - data-pipeline
  - batch-processing
  - streaming
governance_phases: [build]
organ_affinity: [meta]
triggers: [user-asks-about-data-ingestion, context:etl, context:data-import, context:data-pipeline]
complements: [data-pipeline-architect, data-backup-patterns, configuration-management]
---

# Data Ingestion Pipeline

Extract, validate, and load data from diverse sources into target systems.

## Pipeline Architecture

```
Sources → Extract → Validate → Transform → Stage → Load → Verify
  │          │          │          │          │       │        │
  │          │          │          │          │       │        └─ Row counts match
  │          │          │          │          │       └─ Write to target
  │          │          │          │          └─ Staging table/file
  │          │          │          └─ Normalize, enrich, deduplicate
  │          │          └─ Schema validation, business rules
  │          └─ Pull from source
  └─ APIs, files, databases, streams
```

## Source Extraction

### File-Based Sources

```python
from pathlib import Path
import json
import csv
import yaml

class FileExtractor:
    PARSERS = {
        ".json": lambda p: json.loads(p.read_text()),
        ".yaml": lambda p: yaml.safe_load(p.read_text()),
        ".yml": lambda p: yaml.safe_load(p.read_text()),
        ".csv": lambda p: list(csv.DictReader(p.open())),
    }

    def extract(self, path: Path) -> list[dict]:
        parser = self.PARSERS.get(path.suffix)
        if not parser:
            raise ValueError(f"Unsupported format: {path.suffix}")
        data = parser(path)
        return data if isinstance(data, list) else [data]
```

### API Extraction with Pagination

```python
import httpx

async def extract_paginated(base_url: str, params: dict = {}) -> list[dict]:
    all_records = []
    page = 1
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(base_url, params={**params, "page": page, "per_page": 100})
            response.raise_for_status()
            data = response.json()
            records = data.get("items", data.get("results", data))
            if not records:
                break
            all_records.extend(records)
            page += 1
    return all_records
```

### Database Extraction

```python
import asyncpg

async def extract_from_db(dsn: str, query: str, batch_size: int = 1000):
    conn = await asyncpg.connect(dsn)
    try:
        async for batch in conn.cursor(query, prefetch=batch_size):
            yield dict(batch)
    finally:
        await conn.close()
```

## Validation

### Schema Validation

```python
from dataclasses import dataclass

@dataclass
class ValidationResult:
    valid: list[dict]
    invalid: list[tuple[dict, str]]  # (record, error_message)

def validate_records(records: list[dict], schema: dict) -> ValidationResult:
    result = ValidationResult(valid=[], invalid=[])
    required_fields = schema.get("required", [])

    for record in records:
        errors = []
        for field in required_fields:
            if field not in record or record[field] is None:
                errors.append(f"Missing required field: {field}")

        for field, rules in schema.get("fields", {}).items():
            if field in record and record[field] is not None:
                value = record[field]
                if "type" in rules and not isinstance(value, rules["type"]):
                    errors.append(f"{field}: expected {rules['type'].__name__}")
                if "max_length" in rules and len(str(value)) > rules["max_length"]:
                    errors.append(f"{field}: exceeds max length {rules['max_length']}")

        if errors:
            result.invalid.append((record, "; ".join(errors)))
        else:
            result.valid.append(record)

    return result
```

### Business Rule Validation

```python
def apply_business_rules(records: list[dict]) -> ValidationResult:
    result = ValidationResult(valid=[], invalid=[])
    for record in records:
        errors = []

        # Example: organ must be valid
        if record.get("organ") not in {"I", "II", "III", "IV", "V", "VI", "VII", "META"}:
            errors.append(f"Invalid organ: {record.get('organ')}")

        # Example: status must follow promotion state machine
        valid_statuses = {"LOCAL", "CANDIDATE", "PUBLIC_PROCESS", "GRADUATED", "ARCHIVED"}
        if record.get("status") not in valid_statuses:
            errors.append(f"Invalid status: {record.get('status')}")

        if errors:
            result.invalid.append((record, "; ".join(errors)))
        else:
            result.valid.append(record)
    return result
```

## Deduplication

```python
def deduplicate(records: list[dict], key_fields: list[str]) -> list[dict]:
    seen = set()
    unique = []
    for record in records:
        key = tuple(record.get(f) for f in key_fields)
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique
```

### Merge Strategy

```python
from enum import Enum

class MergeStrategy(str, Enum):
    KEEP_FIRST = "keep_first"
    KEEP_LATEST = "keep_latest"
    MERGE_FIELDS = "merge_fields"

def merge_duplicates(records: list[dict], key_fields: list[str], strategy: MergeStrategy) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for record in records:
        key = tuple(record.get(f) for f in key_fields)
        groups.setdefault(key, []).append(record)

    merged = []
    for key, group in groups.items():
        if strategy == MergeStrategy.KEEP_FIRST:
            merged.append(group[0])
        elif strategy == MergeStrategy.KEEP_LATEST:
            merged.append(group[-1])
        elif strategy == MergeStrategy.MERGE_FIELDS:
            result = {}
            for record in group:
                for k, v in record.items():
                    if v is not None:
                        result[k] = v
            merged.append(result)
    return merged
```

## Staging Pattern

```python
from pathlib import Path
from datetime import datetime

class StagingArea:
    def __init__(self, base_dir: str):
        self.base = Path(base_dir)

    def stage(self, batch_id: str, records: list[dict]) -> Path:
        stage_dir = self.base / batch_id
        stage_dir.mkdir(parents=True, exist_ok=True)

        data_path = stage_dir / "data.json"
        meta_path = stage_dir / "metadata.json"

        data_path.write_text(json.dumps(records, indent=2, default=str))
        meta_path.write_text(json.dumps({
            "batch_id": batch_id,
            "record_count": len(records),
            "staged_at": datetime.now().isoformat(),
            "status": "staged",
        }))
        return stage_dir

    def promote(self, batch_id: str) -> list[dict]:
        stage_dir = self.base / batch_id
        data = json.loads((stage_dir / "data.json").read_text())
        meta = json.loads((stage_dir / "metadata.json").read_text())
        meta["status"] = "promoted"
        meta["promoted_at"] = datetime.now().isoformat()
        (stage_dir / "metadata.json").write_text(json.dumps(meta, indent=2))
        return data
```

## Pipeline Orchestration

```python
class IngestionPipeline:
    def __init__(self, extractor, validator, transformer, loader):
        self.extractor = extractor
        self.validator = validator
        self.transformer = transformer
        self.loader = loader

    async def run(self, source: str) -> dict:
        # Extract
        raw = await self.extractor.extract(source)

        # Validate
        validation = self.validator.validate(raw)
        if validation.invalid:
            log.warning("validation_failures", count=len(validation.invalid))

        # Transform
        transformed = self.transformer.transform(validation.valid)

        # Deduplicate
        unique = deduplicate(transformed, key_fields=["id"])

        # Load
        loaded = await self.loader.load(unique)

        return {
            "extracted": len(raw),
            "valid": len(validation.valid),
            "invalid": len(validation.invalid),
            "loaded": loaded,
        }
```

## Anti-Patterns

- **No validation gate** — Always validate before loading; corrupt data is worse than missing data
- **Loading directly from source** — Stage first; staging enables inspection and rollback
- **No deduplication** — Sources often contain duplicates; handle at ingestion
- **Silent data loss** — Log and report every skipped/invalid record
- **Monolithic pipeline** — Break into composable stages for testing and reuse
- **No idempotency** — Pipeline re-runs should produce the same result
