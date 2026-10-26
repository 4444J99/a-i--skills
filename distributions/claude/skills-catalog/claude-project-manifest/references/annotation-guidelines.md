# Annotation Guidelines

How to write effective annotations for files, threads, and relations.

## Principles

### 1. Future Self Test

Write annotations for someone who:
- Has never seen this project
- Needs to understand it in 6 months
- Might be you, having forgotten everything

### 2. Why Over What

Code shows **what**. Annotations explain **why**.

**Bad**: "This function validates input"
**Good**: "Validates input because the external API returns malformed JSON 10% of the time"

### 3. Context is King

Include the circumstances that led to decisions:
- What problem prompted this?
- What alternatives were considered?
- Why was this approach chosen?

## File Annotations

### Structure Template

```yaml
notes: |
  PURPOSE: What this file does and why it exists

  APPROACH: Key implementation decisions
  - Decision 1 and rationale
  - Decision 2 and rationale

  CONTEXT: What prompted its creation

  CAVEATS: Known limitations or gotchas

  TODO: Future work if any
```

### Good Examples

```yaml
# Example 1: Configuration file
notes: |
  Central configuration with environment-based overrides.
  Uses YAML over JSON for inline comments and multi-line strings.
  Loads from CONFIG_PATH env var, falls back to ./config.yaml.

  CAVEAT: Secrets must use environment variables, not this file.
  See security-guidelines.md for secret management.

# Example 2: Utility module
notes: |
  Rate limiter using token bucket algorithm.
  Chose token bucket over sliding window because:
  - Better handles burst traffic (our main use case)
  - Lower memory overhead for high-cardinality keys

  Created during THR-003 after API overload incident.

  TODO: Add Redis backend for distributed deployments.

# Example 3: Test file
notes: |
  Integration tests for payment processing.
  Uses mock payment gateway (see fixtures/mock_gateway.py).

  IMPORTANT: These tests require TEST_STRIPE_KEY env var.
  Never use production keys - tests make real API calls to test mode.

  Coverage gaps: Refund edge cases not yet tested (see ISSUE-42).
```

### Bad Examples

```yaml
# Too vague
notes: "Handles user authentication"

# Describes what, not why
notes: "Uses bcrypt to hash passwords"

# No context
notes: "Added retry logic"
```

### Improved Versions

```yaml
# Specific and contextual
notes: |
  Handles user authentication with session-based tokens.
  Chose sessions over JWT because:
  - Need immediate revocation capability
  - Server-side state acceptable for our scale

  Password hashing uses bcrypt with cost factor 12.
  Cost factor tuned for ~250ms on target hardware.

# Explains the why
notes: |
  Uses bcrypt for password hashing (not argon2) because:
  - Native Python implementation available
  - Argon2 C extension caused deployment issues on Alpine

  Cost factor 12 chosen to balance security vs. UX.

# Provides context
notes: |
  Retry logic added after THR-015 discovered intermittent
  timeouts to payment processor. Uses exponential backoff
  with jitter. Max 3 retries, 30s total timeout.
```

## Thread Annotations

### Summary Writing

A good thread summary answers:
1. What was the goal?
2. What was accomplished?
3. What's the current state?

```yaml
# Good
summary: |
  Migrated database from SQLite to PostgreSQL.
  All data transferred successfully.
  Performance improved 3x on complex queries.

# Bad
summary: "Worked on database stuff"
```

### Accomplishments

Use specific, verifiable statements:

```yaml
# Good
accomplishments:
  - "Migrated 50k user records to new schema"
  - "Added indexes reducing query time from 2s to 50ms"
  - "Implemented connection pooling (max 20 connections)"

# Bad
accomplishments:
  - "Fixed database"
  - "Made it faster"
  - "Updated code"
```

### Decisions

Document choices and rationale:

```yaml
# Good
decisions:
  - "PostgreSQL over MySQL: better JSON support, needed for flexible metadata"
  - "pgBouncer for connection pooling: lower memory than built-in pooling"
  - "Kept SQLite for tests: faster CI, production parity via integration tests"

# Bad
decisions:
  - "Used PostgreSQL"
  - "Added pooling"
```

## Relation Annotations

### Dependency Annotations

Explain the nature of the dependency:

```yaml
# Good
- id: "REL-001"
  type: depends_on
  source: "FILE-001"
  target: "FILE-002"
  annotation: |
    Main imports Config for database connection settings.
    Tight coupling - changes to Config schema require Main updates.

# Bad
- id: "REL-001"
  type: depends_on
  source: "FILE-001"
  target: "FILE-002"
  annotation: "imports"
```

### Interface Annotations

```yaml
- id: "REL-005"
  type: implements
  source: "FILE-010"
  target: "FILE-003"
  annotation: |
    PostgresRepository implements StorageInterface.
    Must implement: save(), load(), delete(), list().
    Currently missing: list() pagination (tracked in ISSUE-55).
```

## Quick Reference

### Do

- Explain rationale and context
- Include relevant timestamps and references
- Mention known issues and limitations
- Link to related threads and decisions
- Use concrete, specific language

### Don't

- Describe what the code does (read the code)
- Use vague language ("stuff", "things", "misc")
- Assume future readers have context
- Skip the "why" behind decisions
- Leave placeholders ("TODO: add description")

### Annotation Length Guide

| Element | Target Length |
|---------|---------------|
| Summary (one-line) | 50-100 characters |
| File notes | 3-10 lines |
| Thread summary | 2-5 lines |
| Accomplishment item | 1 line, specific |
| Decision item | 1-2 lines with rationale |
| Relation annotation | 1-3 lines |
