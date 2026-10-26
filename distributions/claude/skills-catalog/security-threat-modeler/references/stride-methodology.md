# STRIDE Threat Modeling Methodology

Complete reference for systematic threat identification.

## STRIDE Categories

### S - Spoofing Identity

**Question:** Can an attacker pretend to be someone or something else?

**Targets:**
- Users (impersonating another user)
- Processes (malicious process pretending to be legitimate)
- Data sources (fake data appearing to be from trusted source)
- External systems (man-in-the-middle)

**Example Threats:**

| Target | Threat | Attack Vector |
|--------|--------|---------------|
| User account | Credential theft | Phishing, password spray |
| API endpoint | Token forgery | Weak JWT implementation |
| Certificate | Fake certificate | Compromised CA, self-signed |
| IP address | IP spoofing | Network-level attack |

**Mitigations:**
- Strong authentication (MFA)
- Certificate pinning
- Token validation (signature, expiry, issuer)
- Network authentication (mTLS)

---

### T - Tampering with Data

**Question:** Can an attacker modify data they shouldn't?

**Targets:**
- Data in transit (network communications)
- Data at rest (databases, files)
- Data in memory (runtime manipulation)
- Configuration data

**Example Threats:**

| Target | Threat | Attack Vector |
|--------|--------|---------------|
| Database | SQL injection | Malicious input modifies queries |
| Network traffic | MITM modification | Unencrypted communication |
| Session data | Cookie manipulation | Client-side tampering |
| Files | Unauthorized modification | Insufficient access controls |

**Mitigations:**
- Input validation (parameterized queries)
- Encryption in transit (TLS)
- Integrity verification (checksums, signatures)
- Access controls (RBAC, file permissions)
- Audit logging (detect tampering)

---

### R - Repudiation

**Question:** Can a user deny performing an action?

**Targets:**
- User actions (claims they didn't do it)
- System events (no proof of occurrence)
- Transactions (dispute without evidence)

**Example Threats:**

| Target | Threat | Attack Vector |
|--------|--------|---------------|
| Financial transaction | User denies purchase | No audit trail |
| Document approval | User denies signing | No signature verification |
| Access attempt | User denies access | Insufficient logging |
| Configuration change | Admin denies modification | No change tracking |

**Mitigations:**
- Comprehensive audit logging
- Immutable log storage
- Digital signatures (non-repudiation)
- Timestamps from trusted source
- User activity monitoring

---

### I - Information Disclosure

**Question:** Can an attacker access data they shouldn't see?

**Targets:**
- Sensitive data (PII, credentials, business data)
- System information (versions, paths, configurations)
- Source code (intellectual property)
- Error messages (stack traces, database errors)

**Example Threats:**

| Target | Threat | Attack Vector |
|--------|--------|---------------|
| User data | Unauthorized access | IDOR, broken access control |
| Credentials | Password exposure | Logs, error messages |
| Database | Data extraction | SQL injection |
| Network | Traffic sniffing | Unencrypted communication |
| Files | Path traversal | `../../../etc/passwd` |

**Mitigations:**
- Encryption at rest and in transit
- Access control enforcement
- Data classification and handling
- Error message sanitization
- Secure coding practices

---

### D - Denial of Service

**Question:** Can an attacker make the system unavailable?

**Targets:**
- Application (crash, hang)
- Infrastructure (exhaust resources)
- Network (flood traffic)
- Dependencies (attack third-party services)

**Example Threats:**

| Target | Threat | Attack Vector |
|--------|--------|---------------|
| Server | Resource exhaustion | Memory/CPU exhaustion |
| Network | Traffic flood | DDoS attack |
| Application | Algorithmic complexity | ReDoS, hash collision |
| Database | Connection exhaustion | Connection pool starvation |
| Disk | Storage exhaustion | Log flooding, file upload |

**Mitigations:**
- Rate limiting
- Input validation (size limits)
- Resource quotas
- Circuit breakers
- Auto-scaling
- CDN/DDoS protection
- Timeout configuration

---

### E - Elevation of Privilege

**Question:** Can an attacker gain permissions they shouldn't have?

**Targets:**
- User roles (user becomes admin)
- Process privileges (code execution as root)
- System access (container escape)
- Data access (accessing other users' data)

**Example Threats:**

| Target | Threat | Attack Vector |
|--------|--------|---------------|
| Admin functions | Unauthorized access | Missing authorization check |
| OS privileges | Privilege escalation | Kernel exploit |
| Container | Escape to host | Container misconfiguration |
| Database | Admin access | SQL injection with admin creds |

**Mitigations:**
- Principle of least privilege
- Role-based access control
- Authorization on every request
- Sandboxing and isolation
- Regular privilege audits

---

## STRIDE Per Element Analysis

### Data Flow Diagram Elements

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  External   │────▶│   Process   │────▶│  Data Store │
│   Entity    │     └─────────────┘     └─────────────┘
└─────────────┘            │
                           │
                    ┌──────┴──────┐
                    │ Trust       │
                    │ Boundary    │
                    └─────────────┘
```

### Threat Mapping by Element

| Element | S | T | R | I | D | E |
|---------|---|---|---|---|---|---|
| External Entity | X | | | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | | X | X | |
| Data Flow | | X | | X | X | |
| Trust Boundary | X | X | | X | | X |

---

## Threat Modeling Worksheet

### Per-Component Analysis

```markdown
## Component: [Name]

### Description
[Brief description of the component]

### Trust Level
[What trust level does this component operate at?]

### Data Handled
[What sensitive data does this component process?]

### Entry Points
- [Entry point 1]
- [Entry point 2]

### STRIDE Analysis

| Category | Applicable? | Threats Identified | Mitigations |
|----------|-------------|-------------------|-------------|
| Spoofing | Yes/No | | |
| Tampering | Yes/No | | |
| Repudiation | Yes/No | | |
| Info Disclosure | Yes/No | | |
| Denial of Service | Yes/No | | |
| Elevation of Priv | Yes/No | | |
```

### Example: Web API Component

```markdown
## Component: REST API Gateway

### Description
Public-facing API handling user authentication and data requests.

### Trust Level
Boundary between untrusted (internet) and internal network.

### Data Handled
- User credentials (authentication)
- Session tokens
- User PII (profile data)
- Business data (orders, transactions)

### Entry Points
- POST /api/auth/login
- POST /api/auth/register
- GET/POST /api/users/*
- GET/POST /api/orders/*

### STRIDE Analysis

| Category | Applicable? | Threats Identified | Mitigations |
|----------|-------------|-------------------|-------------|
| Spoofing | Yes | Session hijacking, token theft | MFA, secure token handling, HTTPS |
| Tampering | Yes | Request manipulation, parameter tampering | Input validation, signatures |
| Repudiation | Yes | User denies actions | Audit logging with timestamps |
| Info Disclosure | Yes | Error messages leak details, IDOR | Error handling, authz checks |
| Denial of Service | Yes | Rate limit bypass, large payloads | Rate limiting, input size limits |
| Elevation of Priv | Yes | Admin function access | RBAC, authz on every endpoint |
```

---

## Risk Ranking with DREAD

### DREAD Scoring

| Factor | 1 (Low) | 2 (Medium) | 3 (High) |
|--------|---------|------------|----------|
| **D**amage | Minor inconvenience | Data exposure | Complete system compromise |
| **R**eproducibility | Rare conditions | Requires specific setup | Always reproducible |
| **E**xploitability | Requires expertise | Moderate skill | Easy, automated |
| **A**ffected Users | Single user | Subset of users | All users |
| **D**iscoverability | Hidden, unlikely | Requires research | Obvious, documented |

### Risk Score Calculation

```
Risk Score = (D + R + E + A + D) / 5

Score Range:
- 1.0 - 1.9: Low risk
- 2.0 - 2.4: Medium risk
- 2.5 - 2.9: High risk
- 3.0: Critical risk
```

### Example DREAD Assessment

```markdown
## Threat: SQL Injection in Search Endpoint

| Factor | Score | Justification |
|--------|-------|---------------|
| Damage | 3 | Full database access/modification |
| Reproducibility | 3 | Always works if vulnerability exists |
| Exploitability | 3 | Well-documented, automated tools |
| Affected Users | 3 | All users' data at risk |
| Discoverability | 2 | Requires probing, not obvious |

**Risk Score:** (3+3+3+3+2) / 5 = 2.8 (High)

**Priority:** Immediate remediation required
```

---

## Common Threat Patterns

### Authentication Threats

```
1. Brute Force Attack
   - STRIDE: Spoofing
   - Vector: Automated password guessing
   - Mitigation: Rate limiting, account lockout, MFA

2. Credential Stuffing
   - STRIDE: Spoofing
   - Vector: Leaked credential reuse
   - Mitigation: MFA, breach detection, password policies

3. Session Fixation
   - STRIDE: Spoofing
   - Vector: Attacker sets session ID before auth
   - Mitigation: Regenerate session on authentication

4. Session Hijacking
   - STRIDE: Spoofing, Information Disclosure
   - Vector: Stealing session tokens
   - Mitigation: Secure cookies, HTTPS, token binding
```

### Authorization Threats

```
1. Insecure Direct Object Reference (IDOR)
   - STRIDE: Information Disclosure, Tampering
   - Vector: Accessing /user/456 when user is /user/123
   - Mitigation: Object-level authorization checks

2. Privilege Escalation
   - STRIDE: Elevation of Privilege
   - Vector: User accessing admin functions
   - Mitigation: Role-based access control on all endpoints

3. Parameter Tampering
   - STRIDE: Tampering, Elevation of Privilege
   - Vector: Modifying role=admin in request
   - Mitigation: Server-side validation, ignore client role claims
```

### Data Security Threats

```
1. SQL Injection
   - STRIDE: Tampering, Information Disclosure
   - Vector: Malicious SQL in user input
   - Mitigation: Parameterized queries, input validation

2. Path Traversal
   - STRIDE: Information Disclosure
   - Vector: ../../../etc/passwd in file path
   - Mitigation: Input validation, chroot, whitelist paths

3. Sensitive Data Exposure
   - STRIDE: Information Disclosure
   - Vector: PII in logs, unencrypted storage
   - Mitigation: Encryption, log sanitization, access controls
```

### Infrastructure Threats

```
1. DDoS Attack
   - STRIDE: Denial of Service
   - Vector: Traffic flood overwhelming resources
   - Mitigation: CDN, rate limiting, auto-scaling

2. Resource Exhaustion
   - STRIDE: Denial of Service
   - Vector: Memory/CPU exhaustion via complex operations
   - Mitigation: Timeouts, resource limits, input validation

3. Container Escape
   - STRIDE: Elevation of Privilege
   - Vector: Breaking out of container isolation
   - Mitigation: Non-root containers, security profiles, updates
```

---

## Threat Model Report Template

```markdown
# Threat Model Report

**Application:** [Name]
**Version:** [Version]
**Date:** [Date]
**Authors:** [Names]
**Status:** [Draft/Review/Final]

---

## Executive Summary

[2-3 sentences summarizing the system, key findings, and overall risk]

---

## System Overview

### Architecture Diagram
[Include DFD or architecture diagram]

### Components
| Component | Description | Trust Level |
|-----------|-------------|-------------|
| [Name] | [Description] | [High/Medium/Low] |

### Data Classification
| Data Type | Classification | Storage | Protection |
|-----------|----------------|---------|------------|
| [Type] | [Public/Internal/Confidential/Restricted] | [Where] | [How] |

### Trust Boundaries
1. [Boundary 1]: [Description]
2. [Boundary 2]: [Description]

---

## Threat Catalog

### [Threat ID]: [Threat Name]

**Category:** [STRIDE category]
**Component:** [Affected component]
**Description:** [Detailed description]
**Attack Vector:** [How the attack works]
**DREAD Score:** [Score] ([Risk level])
**Status:** [Open/Mitigated/Accepted]

**Mitigations:**
- [Mitigation 1]
- [Mitigation 2]

---

## Risk Summary

| Risk Level | Count | Mitigated | Open |
|------------|-------|-----------|------|
| Critical | [N] | [N] | [N] |
| High | [N] | [N] | [N] |
| Medium | [N] | [N] | [N] |
| Low | [N] | [N] | [N] |

---

## Recommendations

### Immediate (Critical/High)
1. [Recommendation]
2. [Recommendation]

### Short-term (Medium)
1. [Recommendation]
2. [Recommendation]

### Long-term (Low/Improvements)
1. [Recommendation]
2. [Recommendation]

---

## Appendix

### A. Data Flow Diagrams
### B. Threat Analysis Worksheets
### C. References
```
