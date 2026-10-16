# Web Application Security Checklist

Comprehensive security review checklist for web applications.

## Authentication Security

### Password Handling

- [ ] Passwords hashed with bcrypt, Argon2, or scrypt (NOT MD5/SHA1)
- [ ] Salt is unique per password (not a global salt)
- [ ] Work factor is appropriate (bcrypt cost 12+)
- [ ] Passwords never logged or exposed in errors
- [ ] Password reset tokens are single-use and time-limited
- [ ] Password reset doesn't reveal if account exists
- [ ] Minimum password length enforced (12+ characters)
- [ ] Common password blocklist implemented

### Session Management

- [ ] Session tokens are cryptographically random (256+ bits entropy)
- [ ] Session tokens transmitted only via HTTPS
- [ ] Session tokens in cookies with proper flags:
  - [ ] `HttpOnly` (prevents JS access)
  - [ ] `Secure` (HTTPS only)
  - [ ] `SameSite=Strict` or `Lax`
- [ ] Session timeout implemented (idle and absolute)
- [ ] Session invalidated on logout
- [ ] Session regenerated after authentication
- [ ] Concurrent session limits enforced (if required)

### Multi-Factor Authentication

- [ ] MFA option available for all users
- [ ] MFA required for privileged accounts
- [ ] Recovery codes generated and stored securely
- [ ] TOTP secrets encrypted at rest
- [ ] Backup authentication method available
- [ ] MFA bypass requires strong verification

### OAuth/OIDC Implementation

- [ ] State parameter used to prevent CSRF
- [ ] PKCE implemented for public clients
- [ ] Token storage is secure (not localStorage)
- [ ] Redirect URIs strictly validated
- [ ] Scopes follow principle of least privilege
- [ ] ID token signature verified

---

## Authorization Security

### Access Control

- [ ] Role-based or attribute-based access control implemented
- [ ] Authorization checked on every request (not just UI)
- [ ] Default deny: access blocked unless explicitly granted
- [ ] Horizontal access controls tested (user A can't access user B data)
- [ ] Vertical access controls tested (user can't access admin functions)
- [ ] API endpoints enforce same authorization as UI

### Object-Level Authorization

```
Common vulnerability pattern:
GET /api/invoices/12345  ← Does the user own invoice 12345?

Required check:
if (invoice.ownerId !== currentUser.id) {
  throw new ForbiddenError();
}
```

- [ ] Every data access includes ownership/permission check
- [ ] ID parameters treated as user input (not trusted)
- [ ] Bulk operations check permissions on each item
- [ ] File access includes authorization check

### Function-Level Authorization

- [ ] Admin functions restricted to admin roles
- [ ] API endpoints match documented authorization requirements
- [ ] Feature flags don't bypass authorization
- [ ] Debug/diagnostic endpoints protected or removed

---

## Input Validation

### General Validation

- [ ] All input validated on the server (not just client)
- [ ] Whitelist validation preferred over blacklist
- [ ] Input length limits enforced
- [ ] Input type validation (numbers, dates, etc.)
- [ ] File upload validation (type, size, content)
- [ ] Reject request if validation fails (don't sanitize and continue)

### SQL Injection Prevention

```typescript
// WRONG: String concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// CORRECT: Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);
```

- [ ] All database queries use parameterized statements
- [ ] No string concatenation for SQL
- [ ] ORM properly configured for parameterization
- [ ] Stored procedures use parameters
- [ ] Database user has minimum required permissions

### XSS Prevention

- [ ] Output encoded based on context:
  - [ ] HTML context: HTML entity encoding
  - [ ] JavaScript context: JavaScript encoding
  - [ ] URL context: URL encoding
  - [ ] CSS context: CSS encoding
- [ ] User input never inserted into `<script>` tags
- [ ] `dangerouslySetInnerHTML` (React) avoided or sanitized
- [ ] Content-Security-Policy header configured
- [ ] X-XSS-Protection header set (for older browsers)

### Command Injection Prevention

- [ ] User input never passed to shell commands
- [ ] If shell required, use allowlist of commands
- [ ] Arguments passed as array, not string
- [ ] Input validated against strict pattern

```typescript
// WRONG
exec(`convert ${userFilename} output.png`);

// CORRECT
execFile('convert', [userFilename, 'output.png']);
// Better: validate userFilename against allowlist
```

---

## Data Protection

### Encryption at Rest

- [ ] Sensitive data encrypted in database
- [ ] Encryption keys managed securely (not in code)
- [ ] Key rotation process defined
- [ ] Backups encrypted
- [ ] Logs don't contain sensitive data

### Encryption in Transit

- [ ] TLS 1.2+ required for all connections
- [ ] TLS 1.0/1.1 disabled
- [ ] Strong cipher suites only
- [ ] HSTS header configured
- [ ] Certificate chain valid and complete
- [ ] Internal service-to-service communication encrypted

### Sensitive Data Handling

| Data Type | Storage | Logging | Display |
|-----------|---------|---------|---------|
| Passwords | Hashed only | Never | Masked |
| API keys | Encrypted | Never | Masked |
| SSN/Tax ID | Encrypted | Never | Masked |
| Credit cards | Tokenized or encrypted | Never | Last 4 only |
| PII | Encrypted if possible | Anonymized | As needed |

---

## Security Headers

### Required Headers

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

### Header Checklist

- [ ] Content-Security-Policy configured
- [ ] Strict-Transport-Security with long max-age
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY or SAMEORIGIN
- [ ] Referrer-Policy restrictive
- [ ] Permissions-Policy limits browser features
- [ ] No sensitive headers exposed to client (Server, X-Powered-By)

---

## CSRF Protection

### Token-Based CSRF

- [ ] CSRF token generated per session or per request
- [ ] Token validated on all state-changing requests
- [ ] Token is cryptographically random
- [ ] Token comparison is timing-safe
- [ ] Token not in URL (log exposure risk)

### SameSite Cookie Protection

- [ ] `SameSite=Strict` for sensitive cookies
- [ ] `SameSite=Lax` acceptable for less sensitive
- [ ] Fallback CSRF protection for older browsers

### Additional CSRF Measures

- [ ] Re-authentication for sensitive operations
- [ ] CORS configured restrictively
- [ ] Origin header validated on state-changing requests

---

## API Security

### Rate Limiting

- [ ] Rate limits on authentication endpoints
- [ ] Rate limits on expensive operations
- [ ] Rate limits by IP and/or user
- [ ] Rate limit responses include Retry-After header
- [ ] Distributed rate limiting for scaled deployments

### API Authentication

- [ ] API keys rotatable
- [ ] API keys not in URLs
- [ ] JWT tokens properly validated (signature, expiry, issuer)
- [ ] JWT tokens short-lived with refresh flow
- [ ] API versioning doesn't expose deprecated security

### API Design Security

- [ ] Error messages don't leak implementation details
- [ ] Pagination limits enforced
- [ ] Query complexity limits (for GraphQL)
- [ ] Field-level authorization on responses
- [ ] No mass assignment vulnerabilities

---

## Dependency Security

### Package Management

- [ ] Dependencies pinned to specific versions
- [ ] Lock file committed (package-lock.json, yarn.lock)
- [ ] Regular dependency updates scheduled
- [ ] Automated vulnerability scanning (npm audit, Snyk, Dependabot)
- [ ] Transitive dependencies reviewed

### Vulnerability Management

- [ ] Critical vulnerabilities patched within 24 hours
- [ ] High vulnerabilities patched within 1 week
- [ ] Medium vulnerabilities patched within 1 month
- [ ] Vulnerability review in PR/merge process

---

## Error Handling & Logging

### Error Handling

- [ ] Generic error messages to users (no stack traces)
- [ ] Detailed errors logged server-side only
- [ ] Custom error pages configured (404, 500)
- [ ] No sensitive data in error messages
- [ ] Failed authentication logged with limited detail

### Security Logging

Events to log:
- [ ] Authentication attempts (success and failure)
- [ ] Authorization failures
- [ ] Password changes
- [ ] Permission changes
- [ ] Sensitive data access
- [ ] Admin actions
- [ ] Rate limit triggers

Log requirements:
- [ ] Timestamp (UTC)
- [ ] User identifier (if available)
- [ ] IP address
- [ ] Action attempted
- [ ] Success/failure
- [ ] No sensitive data in logs

---

## Infrastructure Security

### Configuration

- [ ] Secrets not in code or config files
- [ ] Secrets managed via environment variables or secrets manager
- [ ] Debug mode disabled in production
- [ ] Verbose errors disabled in production
- [ ] Admin interfaces not publicly accessible
- [ ] Development endpoints removed in production

### Network Security

- [ ] Web application firewall (WAF) configured
- [ ] DDoS protection enabled
- [ ] Firewall rules follow least privilege
- [ ] Database not directly accessible from internet
- [ ] Internal services not exposed publicly

---

## Security Testing

### Pre-Deployment

- [ ] Static analysis (SAST) run on code
- [ ] Dependency vulnerability scan
- [ ] Security unit tests for auth/authz
- [ ] Input validation tests

### Post-Deployment

- [ ] Dynamic analysis (DAST) run
- [ ] Penetration testing (annual minimum)
- [ ] Bug bounty program (if applicable)
- [ ] Security regression tests in CI

### Test Cases

```
Authentication:
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (rate limited)
- [ ] Session timeout works
- [ ] Password reset flow secure

Authorization:
- [ ] User cannot access other users' data
- [ ] User cannot access admin functions
- [ ] API enforces same rules as UI

Input validation:
- [ ] SQL injection attempts blocked
- [ ] XSS attempts escaped/blocked
- [ ] Large inputs rejected
- [ ] Invalid types rejected
```
