# OWASP Top 10 Quick Reference

Practical mitigations for the most critical web application security risks.

## A01: Broken Access Control

### The Risk

Users can act outside their intended permissions.

### Common Vulnerabilities

```
Insecure Direct Object Reference (IDOR):
GET /api/users/123/profile → Access user 123's profile
Attacker changes to: /api/users/456/profile → Accesses user 456

Missing Function Level Access Control:
Regular user discovers: /admin/users/delete
No server-side check if user is admin

Path Traversal:
GET /files?name=report.pdf
Attacker tries: /files?name=../../../etc/passwd
```

### Mitigations

```typescript
// 1. Always check ownership/permissions server-side
async function getProfile(userId: string, currentUser: User) {
  const profile = await db.profiles.findById(userId);

  if (profile.ownerId !== currentUser.id && !currentUser.isAdmin) {
    throw new ForbiddenError('Access denied');
  }

  return profile;
}

// 2. Use indirect references
// Instead of: /orders/12345
// Use: /orders/abc-def-ghi (maps to 12345 for this user only)

// 3. Deny by default
function authorize(user: User, resource: Resource, action: string) {
  const permission = getPermission(user.role, resource.type, action);

  if (permission !== 'allow') {
    throw new ForbiddenError();
  }
}
```

---

## A02: Cryptographic Failures

### The Risk

Sensitive data exposed due to weak or missing cryptography.

### Common Vulnerabilities

- Transmitting data over HTTP instead of HTTPS
- Using weak algorithms (MD5, SHA1 for passwords)
- Hardcoded encryption keys
- Missing encryption at rest
- Storing passwords in plaintext

### Mitigations

```typescript
// Password hashing - use bcrypt or Argon2
import bcrypt from 'bcrypt';  // allow-secret

const SALT_ROUNDS = 12;

async function hashPassword(password: string): Promise<string> {  // allow-secret
  return bcrypt.hash(password, SALT_ROUNDS);  // allow-secret
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {  // allow-secret
  return bcrypt.compare(password, hash);  // allow-secret
}

// Encryption at rest - use AES-256-GCM
import crypto from 'crypto';

function encrypt(plaintext: string, key: Buffer): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}

// Key management - use environment variables or secrets manager
const encryptionKey = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex');
// NEVER hardcode: const key = 'my-secret-key';
```

### Checklist

- [ ] All sensitive data transmitted over HTTPS
- [ ] TLS 1.2+ with strong cipher suites
- [ ] Passwords hashed with bcrypt/Argon2 (cost 12+)
- [ ] Sensitive data encrypted at rest with AES-256
- [ ] Keys stored in secrets manager, rotated regularly
- [ ] No sensitive data in logs or error messages

---

## A03: Injection

### The Risk

Untrusted data sent to an interpreter as part of a command or query.

### Common Vulnerabilities

```sql
-- SQL Injection
SELECT * FROM users WHERE name = 'admin'--' AND password = 'x' -- allow-secret
-- The -- comments out the password check

-- Command Injection
ping -c 1 google.com; rm -rf /

-- NoSQL Injection
{ "username": {"$gt": ""}, "password": {"$gt": ""} }
-- Returns first user regardless of credentials
```

### Mitigations

```typescript
// SQL: Always use parameterized queries
// WRONG
const query = `SELECT * FROM users WHERE email = '${email}'`;

// CORRECT
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);

// ORM: Use query builders properly
// WRONG - raw query with interpolation
await User.query().whereRaw(`name = '${name}'`);

// CORRECT - parameterized
await User.query().where('name', name);

// Command execution: Avoid shell, use argument arrays
// WRONG
exec(`convert ${filename} output.png`);

// CORRECT
execFile('convert', [sanitizedFilename, 'output.png']);

// NoSQL: Validate input types
// WRONG - passes object directly
const user = await User.findOne({ email: req.body.email });

// CORRECT - ensure string type
const email = String(req.body.email);
const user = await User.findOne({ email });
```

---

## A04: Insecure Design

### The Risk

Flaws in the design that cannot be fixed by better implementation.

### Common Vulnerabilities

- No rate limiting on authentication
- Security questions instead of MFA
- Unlimited failed login attempts
- No account lockout
- Trusting client-side validation

### Mitigations

```typescript
// Rate limiting on sensitive endpoints
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many attempts, try again later'
});

app.post('/api/login', loginLimiter, loginHandler);

// Account lockout
async function handleFailedLogin(userId: string) {
  await db.users.increment(userId, 'failedAttempts', 1);

  const user = await db.users.findById(userId);

  if (user.failedAttempts >= 5) {
    await db.users.update(userId, {
      lockedUntil: new Date(Date.now() + 30 * 60 * 1000) // 30 min
    });
  }
}

// Secure workflows - require re-authentication for sensitive ops
async function changeEmail(userId: string, newEmail: string, password: string) {  // allow-secret
  // Verify current password before allowing change  // allow-secret
  const user = await db.users.findById(userId);

  if (!await verifyPassword(password, user.passwordHash)) {  // allow-secret
    throw new UnauthorizedError('Current password required');  // allow-secret
  }

  await db.users.update(userId, { email: newEmail });
}
```

---

## A05: Security Misconfiguration

### The Risk

Insecure default configurations, incomplete setups, open cloud storage.

### Common Vulnerabilities

- Default credentials unchanged
- Unnecessary features enabled
- Error messages reveal system info
- Missing security headers
- Outdated software

### Mitigations

```typescript
// Security headers middleware
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      frameSrc: ["'none'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));

// Error handling - don't expose details
app.use((err, req, res, next) => {
  // Log full error for debugging
  logger.error('Unhandled error', { error: err, stack: err.stack });

  // Return generic message to client
  res.status(500).json({
    error: 'An unexpected error occurred',
    requestId: req.id // For support reference
  });
});

// Disable server version headers
app.disable('x-powered-by');
```

### Configuration Checklist

- [ ] Remove/change default credentials
- [ ] Disable unnecessary features/endpoints
- [ ] Configure appropriate security headers
- [ ] Use different configs for dev/prod
- [ ] Automate configuration verification
- [ ] Keep all software updated

---

## A06: Vulnerable and Outdated Components

### The Risk

Using components with known vulnerabilities.

### Mitigations

```bash
# Regular dependency audits
npm audit
npm audit fix

# Or for more thorough scanning
npx snyk test

# Pin dependencies to specific versions
# package.json
{
  "dependencies": {
    "express": "4.18.2",  // Exact version
    "lodash": "^4.17.21" // At least check for patches
  }
}

# Use lock files
npm ci  # Install from lock file exactly
```

### Process

```
1. Inventory all components and versions
2. Subscribe to security bulletins (CVE, NVD)
3. Automate scanning in CI/CD (Dependabot, Snyk)
4. Establish patching SLAs:
   - Critical: 24 hours
   - High: 1 week
   - Medium: 1 month
5. Remove unused dependencies
```

---

## A07: Identification and Authentication Failures

### The Risk

Weak authentication allows attackers to compromise user accounts.

### Common Vulnerabilities

- Permits automated attacks (credential stuffing)
- Weak or default passwords allowed
- Missing or ineffective MFA
- Session IDs in URL
- Session not invalidated on logout

### Mitigations

```typescript
// Strong password requirements
function validatePassword(password: string): ValidationResult {  // allow-secret
  const requirements = [
    { test: password.length >= 12, message: 'At least 12 characters' },  // allow-secret
    { test: /[A-Z]/.test(password), message: 'At least one uppercase' },  // allow-secret
    { test: /[a-z]/.test(password), message: 'At least one lowercase' },  // allow-secret
    { test: /[0-9]/.test(password), message: 'At least one number' },  // allow-secret
    { test: !commonPasswords.includes(password), message: 'Not a common password' }  // allow-secret
  ];

  const failures = requirements.filter(r => !r.test);

  return {
    valid: failures.length === 0,
    errors: failures.map(f => f.message)
  };
}

// Secure session management
app.use(session({
  secret: process.env.SESSION_SECRET, // allow-secret
  name: 'sessionId', // Don't use default name
  cookie: {
    httpOnly: true,
    secure: true, // HTTPS only
    sameSite: 'strict',
    maxAge: 30 * 60 * 1000 // 30 minutes
  },
  resave: false,
  saveUninitialized: false
}));

// Regenerate session on login
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);

  req.session.regenerate((err) => {
    req.session.userId = user.id;
    res.json({ success: true });
  });
});

// Invalidate on logout
app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    res.clearCookie('sessionId');
    res.json({ success: true });
  });
});
```

---

## A08: Software and Data Integrity Failures

### The Risk

Code and infrastructure that doesn't protect against integrity violations.

### Common Vulnerabilities

- CI/CD pipeline without integrity verification
- Auto-update without signature verification
- Insecure deserialization
- Untrusted CDN resources

### Mitigations

```html
<!-- Subresource Integrity for CDN resources -->
<script
  src="https://cdn.example.com/lib.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
  crossorigin="anonymous">
</script>
```

```typescript
// Avoid deserializing untrusted data
// WRONG - arbitrary code execution risk
const data = JSON.parse(untrustedInput);
eval(data.code); // Never do this

// CORRECT - validate and sanitize
const data = JSON.parse(untrustedInput);
const validated = schema.validate(data);
if (!validated.success) {
  throw new ValidationError();
}

// Signed updates
import crypto from 'crypto';

function verifyUpdate(update: Buffer, signature: Buffer, publicKey: string): boolean {
  const verify = crypto.createVerify('SHA256');
  verify.update(update);
  return verify.verify(publicKey, signature);
}
```

---

## A09: Security Logging and Monitoring Failures

### The Risk

Without logging and monitoring, attacks go undetected.

### What to Log

```typescript
// Security events to log
interface SecurityLog {
  timestamp: Date;
  eventType: 'AUTH_SUCCESS' | 'AUTH_FAILURE' | 'ACCESS_DENIED' |
             'PERMISSION_CHANGE' | 'SENSITIVE_ACCESS' | 'RATE_LIMIT';
  userId?: string;
  ipAddress: string;
  userAgent: string;
  resource: string;
  action: string;
  outcome: 'success' | 'failure';
  details?: Record<string, any>; // No PII or secrets
}

// Example logging
async function logSecurityEvent(event: SecurityLog) {
  await securityLogger.info('Security event', {
    ...event,
    // Ensure no sensitive data
    details: sanitize(event.details)
  });
}

// Usage
await logSecurityEvent({
  timestamp: new Date(),
  eventType: 'AUTH_FAILURE',
  userId: undefined, // Unknown at this point
  ipAddress: req.ip,
  userAgent: req.headers['user-agent'],
  resource: '/api/login',
  action: 'login_attempt',
  outcome: 'failure',
  details: { reason: 'invalid_credentials' }
});
```

### Alerting Thresholds

| Event | Threshold | Action |
|-------|-----------|--------|
| Failed logins (single IP) | 10 in 5 min | Block IP, alert |
| Failed logins (single user) | 5 in 15 min | Lock account, alert |
| Access denied | 20 in 5 min | Alert |
| Admin action | Any | Log |
| Sensitive data access | Any | Log |

---

## A10: Server-Side Request Forgery (SSRF)

### The Risk

Application fetches remote resources based on user-supplied URLs.

### Common Vulnerabilities

```
// User provides URL, server fetches it
POST /api/fetch-url
{ "url": "http://internal-service/admin" }

// Attacker accesses internal services
{ "url": "http://169.254.169.254/latest/meta-data/" }  // AWS metadata
{ "url": "http://localhost:6379/" }  // Redis
```

### Mitigations

```typescript
import { URL } from 'url';
import dns from 'dns/promises';

// Validate and sanitize URLs
async function validateExternalUrl(urlString: string): Promise<URL> {
  const url = new URL(urlString);

  // 1. Protocol allowlist
  if (!['http:', 'https:'].includes(url.protocol)) {
    throw new Error('Invalid protocol');
  }

  // 2. Block internal hostnames
  const blockedHosts = ['localhost', '127.0.0.1', '0.0.0.0', '169.254.169.254'];
  if (blockedHosts.includes(url.hostname)) {
    throw new Error('Internal hosts not allowed');
  }

  // 3. Resolve DNS and check for internal IPs
  const addresses = await dns.resolve4(url.hostname);
  for (const addr of addresses) {
    if (isPrivateIP(addr)) {
      throw new Error('Internal IP not allowed');
    }
  }

  return url;
}

function isPrivateIP(ip: string): boolean {
  const parts = ip.split('.').map(Number);

  return (
    parts[0] === 10 ||
    (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) ||
    (parts[0] === 192 && parts[1] === 168) ||
    parts[0] === 127 ||
    (parts[0] === 169 && parts[1] === 254)
  );
}

// Use validated URL for fetching
async function fetchExternalResource(userUrl: string) {
  const validatedUrl = await validateExternalUrl(userUrl);

  // Use timeout and size limits
  const response = await fetch(validatedUrl.toString(), {
    signal: AbortSignal.timeout(5000),
    headers: {
      'User-Agent': 'MyApp/1.0'
    }
  });

  // Limit response size
  const maxSize = 10 * 1024 * 1024; // 10MB
  const contentLength = response.headers.get('content-length');

  if (contentLength && parseInt(contentLength) > maxSize) {
    throw new Error('Response too large');
  }

  return response;
}
```

### Network-Level Protection

- [ ] Segment internal networks from application servers
- [ ] Use firewall rules to restrict outbound connections
- [ ] Implement egress proxy with allowlist
- [ ] Disable unnecessary URL schemes
- [ ] Use metadata service v2 (AWS) with session tokens
