# {{PROJECT_NAME}} - Project Manifest Report

> Generated from `manifest.yaml` on {{GENERATED_DATE}}

## Project Overview

| Field | Value |
|-------|-------|
| **Project ID** | `{{PROJECT_ID}}` |
| **Status** | {{PROJECT_STATUS}} |
| **Created** | {{PROJECT_CREATED}} |
| **Last Modified** | {{PROJECT_MODIFIED}} |
| **Manifest Version** | {{MANIFEST_VERSION}} |

### Description

{{PROJECT_DESCRIPTION}}

### Tags

{{PROJECT_TAGS}}

---

## File Inventory

**Total Files:** {{FILE_COUNT}}

### By Type

| Type | Count |
|------|-------|
| Source | {{SOURCE_COUNT}} |
| Config | {{CONFIG_COUNT}} |
| Documentation | {{DOC_COUNT}} |
| Assets | {{ASSET_COUNT}} |
| Generated | {{GENERATED_COUNT}} |

### File List

| ID | Path | Type | Summary |
|----|------|------|---------|
{{#FILES}}
| `{{ID}}` | `{{PATH}}` | {{TYPE}} | {{SUMMARY}} |
{{/FILES}}

---

## Development History

**Total Threads:** {{THREAD_COUNT}}

### Thread Timeline

{{#THREADS}}
#### {{ID}}: {{TITLE}}

**Started:** {{STARTED}}
{{#ENDED}}**Ended:** {{ENDED}}{{/ENDED}}

{{SUMMARY}}

{{#ACCOMPLISHMENTS}}
**Accomplishments:**
{{#ITEMS}}
- {{.}}
{{/ITEMS}}
{{/ACCOMPLISHMENTS}}

{{#DECISIONS}}
**Decisions:**
{{#ITEMS}}
- {{.}}
{{/ITEMS}}
{{/DECISIONS}}

{{#FILES_CREATED}}
**Files Created:** {{ITEMS}}
{{/FILES_CREATED}}

{{#FILES_MODIFIED}}
**Files Modified:** {{ITEMS}}
{{/FILES_MODIFIED}}

---

{{/THREADS}}

## Relationships

**Total Relations:** {{RELATION_COUNT}}

### Dependency Graph

```mermaid
graph LR
{{#RELATIONS}}
    {{SOURCE}}{{ARROW}}{{TARGET}}
{{/RELATIONS}}
```

### Relation Details

| ID | Type | Source | Target | Description |
|----|------|--------|--------|-------------|
{{#RELATIONS}}
| `{{ID}}` | {{TYPE}} | `{{SOURCE}}` | `{{TARGET}}` | {{ANNOTATION}} |
{{/RELATIONS}}

---

## Quick Reference

### Files by Tag

{{#TAGS}}
#### {{TAG_NAME}}
{{#TAG_FILES}}
- `{{ID}}`: {{PATH}}
{{/TAG_FILES}}
{{/TAGS}}

### Recent Activity

| Date | Thread | Summary |
|------|--------|---------|
{{#RECENT_THREADS}}
| {{DATE}} | `{{ID}}` | {{TITLE}} |
{{/RECENT_THREADS}}

---

## Appendix

### ID Registry

| Category | Last ID | Total |
|----------|---------|-------|
| Files | `{{LAST_FILE_ID}}` | {{FILE_COUNT}} |
| Threads | `{{LAST_THREAD_ID}}` | {{THREAD_COUNT}} |
| Relations | `{{LAST_RELATION_ID}}` | {{RELATION_COUNT}} |

### Validation Status

- [ ] All file paths exist
- [ ] No duplicate IDs
- [ ] All references valid
- [ ] Timestamps in ISO 8601
- [ ] Required fields present

---

*This report was generated from the project manifest. For the authoritative source, see `manifest.yaml`.*
