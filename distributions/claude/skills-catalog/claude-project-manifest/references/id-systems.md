# ID Systems

Strategies for generating and managing unique identifiers in manifests.

## Standard ID Formats

### Project IDs

Format: `PROJ-{YEAR}-{SEQ}`

```
PROJ-2024-001  # First project of 2024
PROJ-2024-042  # 42nd project of 2024
PROJ-2025-001  # First project of 2025
```

Rationale:
- Year prefix provides natural grouping
- Sequence resets annually (prevents unbounded growth)
- Three-digit sequence supports 999 projects per year

### File IDs

Format: `FILE-{SEQ}`

```
FILE-001  # First file
FILE-042  # 42nd file
FILE-100  # 100th file
```

Rationale:
- Simple sequential numbering
- Three digits support up to 999 files per project
- Extend to four digits if needed: `FILE-1000`

### Thread IDs

Format: `THR-{SEQ}`

```
THR-001  # First thread
THR-015  # 15th thread
```

### Relation IDs

Format: `REL-{SEQ}`

```
REL-001  # First relation
REL-050  # 50th relation
```

## ID Generation Strategies

### Sequential (Default)

Simply increment from the highest existing ID.

```python
def next_file_id(existing_ids):
    if not existing_ids:
        return "FILE-001"
    max_seq = max(int(id.split('-')[1]) for id in existing_ids)
    return f"FILE-{max_seq + 1:03d}"
```

Pros:
- Simple to implement
- Easy to understand
- Natural ordering

Cons:
- Requires knowing existing IDs
- Can have gaps if entries are deleted

### Timestamp-Based

Include timestamp for uniqueness without coordination.

```
FILE-20240115-103045  # YYYYMMDD-HHMMSS
FILE-1705318245       # Unix timestamp
```

Pros:
- No collision risk
- Self-documenting creation time
- Works in distributed scenarios

Cons:
- Longer IDs
- Less human-readable
- Ordering by time, not logical sequence

### UUID-Based

Use UUIDs for guaranteed uniqueness.

```
FILE-a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

Pros:
- Globally unique
- No coordination needed
- Good for distributed systems

Cons:
- Long and unwieldy
- Not human-friendly
- No natural ordering

### Hybrid Approach

Combine sequential with hash suffix for uniqueness.

```
FILE-001-a7f3    # Sequential + 4-char hash
FILE-042-b2e1
```

Pros:
- Short but unique
- Human-readable prefix
- Collision-resistant

## ID Assignment Rules

### Never Reuse IDs

Once an ID is assigned, never reassign it even if the entity is deleted.

```yaml
# File deleted but ID preserved in history
files:
  - id: "FILE-001"
    status: removed
    path: "old/deprecated.py"
    removed_in: "THR-015"
```

### Maintain Gaps

If FILE-005 is deleted, the next file is still FILE-006, not FILE-005.

### Cross-Reference Integrity

When referencing IDs, verify they exist:

```yaml
# Bad: dangling reference
files:
  - id: "FILE-001"
    thread_id: "THR-999"  # This thread doesn't exist!

# Good: validated reference
files:
  - id: "FILE-001"
    thread_id: "THR-003"  # Verified to exist
```

## ID Registry Pattern

For complex projects, maintain a central registry:

```yaml
# _registry.yaml
id_sequences:
  project: 1
  file: 42
  thread: 15
  relation: 28

deleted_ids:
  files: ["FILE-010", "FILE-023"]
  threads: []
  relations: ["REL-005"]
```

## Migration Strategies

### Adding IDs to Existing Files

When manifesting an existing project:

1. List all files in logical order
2. Assign sequential IDs
3. Document the mapping

```yaml
# Initial manifest of existing project
files:
  - id: "FILE-001"
    path: "README.md"
    notes: "Pre-existing file, manifested in THR-001"
  - id: "FILE-002"
    path: "src/main.py"
    notes: "Pre-existing file, manifested in THR-001"
```

### Merging Manifests

When combining projects:

1. Prefix IDs with project identifier
2. Or resequence with new IDs
3. Maintain a mapping table

```yaml
# Merged from PROJ-A and PROJ-B
files:
  - id: "FILE-001"  # Was PROJ-A:FILE-001
    original_id: "PROJ-A:FILE-001"
  - id: "FILE-050"  # Was PROJ-B:FILE-001
    original_id: "PROJ-B:FILE-001"
```

## Validation Checklist

- [ ] All IDs follow the standard format
- [ ] No duplicate IDs within category
- [ ] All references point to existing IDs
- [ ] Deleted entities have `status: removed`
- [ ] ID sequences are documented
- [ ] No ID reuse after deletion
