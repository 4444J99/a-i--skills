---
name: technical-writing-guide
description: Produce clear technical documentation — API references, architecture decision records, runbooks, and how-to guides. Covers document structure, audience calibration, and terminology consistency. Triggers on technical documentation, API docs, runbook, or how-to guide requests.
license: MIT
complexity: beginner
time_to_learn: 30min
tags:
  - technical-writing
  - documentation
  - api-reference
  - runbook
  - how-to
inputs:
  - source-code
  - architecture-notes
  - api-spec
outputs:
  - documentation
  - adr
  - runbook
side_effects:
  - creates-files
triggers:
  - user-asks-about-technical-documentation
  - user-asks-about-api-docs
  - user-asks-about-runbooks
  - context:how-to-guide
complements:
  - github-repo-curator
  - github-repository-standards
---

# Technical Writing Guide

Teach clear, usable technical documentation. Focus on structure readers can scan, language matched to the audience, and consistent terms throughout.

## Instructions

### Step 1: Identify document type and audience

| Document type | Primary reader | Success criterion |
|---------------|----------------|-------------------|
| API reference | Integrating developer | Can call endpoints without asking questions |
| ADR | Future maintainers | Understand why a decision was made and what was rejected |
| Runbook | On-call engineer | Can execute steps under pressure |
| How-to guide | Task-focused user | Completes one workflow end to end |

Before writing, state:
- **Audience:** role, experience level, and what they already know
- **Goal:** one sentence describing what the reader can do after reading
- **Scope:** what is in and explicitly out

### Step 2: Choose a structure

**API reference** — one section per resource or endpoint:

```markdown
## POST /v1/widgets

Create a widget.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name  | string | yes | Display name (1–64 chars) |

### Response

`201 Created` — returns the created widget object.

### Errors

| Status | Meaning |
|--------|---------|
| 400 | Invalid `name` length |
| 409 | Widget name already exists |
```

**ADR** — record the decision, not the debate:

```markdown
# ADR-001: Use PostgreSQL for primary storage

**Status:** Accepted
**Date:** YYYY-MM-DD

## Context
What problem or constraint motivates this decision?

## Decision
What we chose, in one or two sentences.

## Consequences
Positive, negative, and neutral outcomes.

## Alternatives considered
What else was evaluated and why it was not chosen.
```

**Runbook** — numbered steps with verification at each stage:

```markdown
# Runbook: Restore read replica lag

## Symptoms
- `replica_lag_seconds` > 300
- Read queries return stale data

## Prerequisites
- kubectl access to `prod` cluster
- PagerDuty incident ID

## Steps
1. Confirm lag: `SELECT pg_last_wal_replay_lsn();`
   - **Expected:** LSN within 1 MB of primary
2. If lag persists, restart replica pod: `kubectl rollout restart ...`
   - **Expected:** Pod `Running` within 2 minutes

## Rollback
Steps to undo if the fix makes things worse.

## Escalation
Contact `#database-oncall` if lag exceeds 15 minutes.
```

**How-to guide** — task title, prerequisites, numbered steps, outcome:

```markdown
# How to rotate API keys

## Prerequisites
- Admin access to the dashboard
- 15 minutes of maintenance window

## Steps
1. Generate a new key in **Settings → API Keys**.
2. Update the key in your deployment secrets.
3. Verify traffic with the new key.
4. Revoke the old key.

## Next steps
Set a calendar reminder for the next rotation date.
```

### Step 3: Calibrate language to the audience

| Audience | Adjust |
|----------|--------|
| New hire | Define acronyms on first use; link to glossary |
| Experienced peer | Skip basics; lead with deltas and edge cases |
| Operator under incident | Imperative verbs, short steps, no background essays |

Rules:
- Use **active voice** and **present tense** for procedures
- Prefer **concrete nouns** over vague labels ("429 response" not "an error")
- One main idea per paragraph; headings every 3–5 paragraphs in long docs

### Step 4: Enforce terminology consistency

1. List key terms before drafting (e.g., "tenant" vs "organization", "job" vs "task")
2. Use the same term for the same concept everywhere — including headings, tables, and code samples
3. When the codebase uses a different name, note the mapping once: "Dashboard calls this `org_id`; API field is `tenant_id`"
4. Keep product names, HTTP methods, and enum values in **code font**

### Step 5: Review before delivery

- [ ] Title states the document type and topic
- [ ] First screen answers "what is this and who is it for?"
- [ ] Every procedure step has an expected result or verification
- [ ] No undefined acronyms
- [ ] Terms match the source code and API spec
- [ ] Links and code examples are copy-paste ready

## Examples

**Input:** OpenAPI spec for `GET /users/{id}` and source handler.

**Output (API excerpt):**

```markdown
## GET /users/{id}

Returns a single user by ID.

### Parameters

| Name | In | Type | Description |
|------|-----|------|-------------|
| id | path | uuid | User identifier |

### Response

`200 OK` — `User` object. Returns `404` if the user does not exist.
```

**Input:** Team chose Redis over Memcached for session storage.

**Output:** ADR with context (session volume, TTL needs), decision (Redis), consequences (ops familiarity vs memory overhead), and rejected alternatives (Memcached, sticky sessions).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Burying the goal below background | Put purpose and audience in the first paragraph |
| Mixing tutorial and reference in one page | Split how-to guides from API reference |
| Steps without verification | Add "Expected:" after each runbook step |
| Synonym drift (`client` / `customer` / `user`) | Pick one term; document exceptions |
| Documenting aspirational behavior | Verify against source code or API spec |
| Missing rollback or escalation in runbooks | Always include both for operational docs |
