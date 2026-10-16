# URL Categorization Guide

Patterns for categorizing and analyzing URLs from AI coding sessions.

## Domain Categories

### Documentation Sites

| Category | Domains | Notes |
|----------|---------|-------|
| **Official Docs** | `docs.*`, `*.readthedocs.io`, `developer.*` | Primary reference |
| **MDN** | `developer.mozilla.org` | Web standards |
| **Language Docs** | `docs.python.org`, `doc.rust-lang.org`, `go.dev/doc` | Language reference |
| **Framework Docs** | `react.dev`, `nextjs.org/docs`, `vuejs.org` | Framework guides |

### Q&A / Community

| Category | Domains | Notes |
|----------|---------|-------|
| **Stack Overflow** | `stackoverflow.com` | Community answers |
| **GitHub Issues** | `github.com/*/issues/*` | Bug reports, discussions |
| **Reddit** | `reddit.com/r/*` | Community discussion |
| **Discord** | Links to discord threads | Real-time help |

### Code Repositories

| Category | Domains | Notes |
|----------|---------|-------|
| **GitHub** | `github.com` | Source code |
| **GitLab** | `gitlab.com` | Source code |
| **npm** | `npmjs.com` | Package info |
| **PyPI** | `pypi.org` | Python packages |
| **crates.io** | `crates.io` | Rust packages |

### API References

| Category | Patterns | Notes |
|----------|----------|-------|
| **API Docs** | `*/api/*`, `*/reference/*` | Endpoint docs |
| **OpenAPI/Swagger** | `*/swagger/*`, `*/openapi/*` | API specs |
| **Postman** | `postman.com` | API collections |

### Tools & Services

| Category | Examples | Notes |
|----------|----------|-------|
| **Cloud Providers** | AWS, GCP, Azure docs | Infrastructure |
| **Databases** | PostgreSQL, MongoDB docs | Data storage |
| **CI/CD** | GitHub Actions, CircleCI docs | Deployment |

---

## URL Pattern Analysis

### Research Indicators

High documentation fetch count suggests:
- Learning new technology
- Debugging unfamiliar code
- Architectural decisions

```
Pattern: 5+ docs.* URLs in one session
Interpretation: Deep research phase
```

### Debugging Indicators

Stack Overflow + GitHub Issues suggests:
- Encountering errors
- Looking for workarounds
- Known issues

```
Pattern: stackoverflow.com + github.com/issues
Interpretation: Troubleshooting session
```

### Implementation Indicators

Package registry + framework docs suggests:
- Active development
- Dependency evaluation
- Integration work

```
Pattern: npmjs.com + react.dev
Interpretation: Building React feature
```

---

## Fetch Status Analysis

### Success Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Content retrieved |
| 301/302 | Redirect | Followed to destination |
| 304 | Not Modified | Cached content used |

### Failure Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 403 | Forbidden | Auth required, rate limited |
| 404 | Not Found | Dead link, moved content |
| 429 | Rate Limited | Too many requests |
| 500+ | Server Error | Temporary outage |

### Retry Recommendations

| Status | Should Retry | When |
|--------|--------------|------|
| 403 | Maybe | If auth token expired |
| 404 | No | Link is dead |
| 429 | Yes | After waiting |
| 500 | Yes | After brief delay |
| Timeout | Yes | Immediately |

---

## Session Pattern Templates

### Documentation Deep Dive

```
Session: "Learning GraphQL"
URLs fetched: 12
Domain breakdown:
  - graphql.org: 4
  - apollographql.com: 3
  - github.com: 3
  - stackoverflow.com: 2

Pattern: Documentation-heavy research
Insight: Comprehensive learning session
```

### Debugging Session

```
Session: "Fix auth bug"
URLs fetched: 8
Domain breakdown:
  - stackoverflow.com: 4
  - github.com/issues: 2
  - docs.auth0.com: 2

Pattern: Troubleshooting
Insight: Error investigation
```

### Quick Reference

```
Session: "Add date formatting"
URLs fetched: 2
Domain breakdown:
  - developer.mozilla.org: 1
  - docs.python.org: 1

Pattern: Targeted lookup
Insight: Efficient, focused work
```

---

## Report Enrichment

### Domain Reputation

Add context to domains:

```markdown
## Fetched URLs with Context

- **developer.mozilla.org** (MDN - trusted web reference)
  - /en-US/docs/Web/JavaScript/Reference/...

- **stackoverflow.com** (Community Q&A - verify answers)
  - /questions/12345/...

- **medium.com** (Blog - varies in quality)
  - /@author/article-name
```

### Temporal Patterns

Track when research happens:

```markdown
## Research Timeline

09:15 - Started with official docs (react.dev)
09:32 - Hit a problem (stackoverflow.com)
09:45 - Found related issue (github.com/issues)
09:58 - Solution in docs (react.dev/reference)
10:05 - Implementation complete
```

---

## Privacy Considerations

### URLs That May Contain Sensitive Data

| Pattern | Risk | Recommendation |
|---------|------|----------------|
| `*/api/users/*` | May contain user IDs | Truncate path |
| `*?token=*` | May contain auth tokens | Remove query params | <!-- allow-secret -->
| `*/admin/*` | Internal URLs | Flag for review |
| `localhost:*` | Local dev URLs | Skip in reports |

### Safe URL Cleaning

```python
# Remove query parameters
from urllib.parse import urlparse, urlunparse
parsed = urlparse(url)
clean = urlunparse(parsed._replace(query=''))

# Truncate sensitive paths
if '/users/' in url:
    url = url.split('/users/')[0] + '/users/[id]'
```

---

## Aggregation Patterns

### By Domain

```markdown
## Domain Summary

| Domain | Fetches | Success Rate |
|--------|---------|--------------|
| github.com | 15 | 100% |
| stackoverflow.com | 8 | 100% |
| docs.internal.com | 3 | 0% (403) |
```

### By Category

```markdown
## Category Summary

| Category | Fetches | Top Domain |
|----------|---------|------------|
| Documentation | 23 | react.dev |
| Q&A | 12 | stackoverflow.com |
| Source Code | 8 | github.com |
| Internal | 3 | (all failed) |
```

### By Session

```markdown
## Session Summary

| Session | Fetches | Pattern |
|---------|---------|---------|
| auth-bug | 8 | Debugging |
| new-feature | 15 | Research |
| quick-fix | 2 | Reference |
```
