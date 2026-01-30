# Privacy by Design Implementation Guide

Practical patterns for building privacy into software from the start.

## Seven Foundational Principles

### 1. Proactive Not Reactive

Build privacy in from the start; don't retrofit.

**Implementation:**
```
Before starting any feature:
- [ ] What personal data does this feature need?
- [ ] What's the minimum data required?
- [ ] How long must we keep it?
- [ ] Who needs access to it?
- [ ] How will users control it?
```

### 2. Privacy as the Default

Users shouldn't have to take action to protect privacy.

**Anti-patterns:**
- Opt-out checkboxes for marketing
- Public by default profiles
- Analytics enabled before consent
- Sharing on by default

**Correct patterns:**
- Opt-in for marketing
- Private by default profiles
- Analytics blocked until consent
- Explicit sharing decisions

### 3. Privacy Embedded into Design

Privacy is a core feature, not a bolt-on.

**Architecture questions:**
- Where is PII stored? (Minimize locations)
- Who has access? (Minimize access)
- How does it flow? (Minimize copies)
- When is it deleted? (Automate retention)

### 4. Full Functionality (Positive-Sum)

Privacy AND functionality, not privacy OR functionality.

**Example - Analytics without surveillance:**
```javascript
// Instead of tracking individual users:
// track("user_123", "clicked_button")

// Use aggregate, anonymized data:
incrementCounter("button_clicks", {
  page: "/pricing",
  variant: "A"
});
```

### 5. End-to-End Security

Protect data throughout its entire lifecycle.

```
Lifecycle stage → Security measure

Collection    → TLS, input validation, consent
Processing    → Access controls, encryption, logging
Storage       → Encryption at rest, backups encrypted
Sharing       → DPAs, minimum necessary, secure transfer
Retention     → Defined periods, automated deletion
Disposal      → Secure deletion, certificate of destruction
```

### 6. Visibility and Transparency

Be open about data practices.

**User-facing:**
- Clear privacy policy
- Real-time privacy dashboard
- Data download/export
- Processing logs visible

**Internal:**
- Documented data flows
- Audit trails
- Compliance monitoring

### 7. Respect for User Privacy

User interests come first.

**Design questions:**
- Would I be comfortable if this was my data?
- Is this the minimum intrusion for the feature?
- Can users easily opt out?
- Are we being manipulative (dark patterns)?

---

## Data Minimization Patterns

### Field-Level Minimization

| Instead of | Collect | Because |
|------------|---------|---------|
| Full DOB | Age range or birth year | Reduces PII exposure |
| Full address | City/postal code only | Unless shipping required |
| Full name | First name or username | Unless legal identity needed |
| Phone number | Only if 2FA required | Email often sufficient |
| Government ID | Never store, verify only | Extreme liability |

### Collection Timing

```
Don't collect everything at signup.
Collect data when you need it.

Signup:
- Email (required for account)
- Password

First purchase:
- Shipping address (required for fulfillment)
- Payment (required for transaction)

Later, if requested:
- Phone (optional 2FA)
- Profile info (optional personalization)
```

### Derived Data Strategy

```
Instead of storing: "User viewed products A, B, C, D, E"
Store derived: "User interested in category: Electronics"

Instead of storing: "GPS location every 5 minutes"
Store derived: "User typically in timezone: PST"
```

---

## Consent Implementation Patterns

### Granular Consent UI

```
PRIVACY PREFERENCES

Essential cookies (always on)
These cookies are required for the site to function.
[Cannot be disabled]

□ Analytics cookies
Help us understand how visitors use our site.
[Enable] [Disable]

□ Marketing cookies
Used to show relevant ads on other sites.
[Enable] [Disable]

□ Personalization
Remember your preferences and customize your experience.
[Enable] [Disable]

[Save preferences] [Reject all] [Accept all]
```

### Consent Storage

```typescript
interface ConsentRecord {
  userId: string;
  timestamp: Date;
  ipAddress: string;  // Hashed after 24h
  consentVersion: string;

  consents: {
    analytics: boolean;
    marketing: boolean;
    personalization: boolean;
  };

  source: 'banner' | 'settings' | 'api';
  userAgent: string;  // For audit trail
}

// Store consent before setting any cookies
async function recordConsent(consent: ConsentRecord) {
  await db.consents.insert(consent);

  // Only then enable services
  if (consent.consents.analytics) {
    enableAnalytics();
  }
}
```

### Consent Withdrawal

```typescript
// Withdrawal must be as easy as giving consent
async function withdrawConsent(userId: string, category: string) {
  // 1. Update consent record
  await db.consents.update(userId, { [category]: false });

  // 2. Immediately stop processing
  disableCategory(category);

  // 3. Notify third parties
  await notifyProcessors(userId, category, 'withdrawn');

  // 4. Audit log
  await logConsentChange(userId, category, 'withdrawn');
}
```

---

## User Rights Implementation

### Data Access Request Flow

```
Request received
    ↓
Verify identity (email confirmation, security questions)
    ↓
Gather data from all systems:
  - Primary database
  - Analytics (user ID lookup)
  - Email service
  - Support tickets
  - Payment processor
  - Third-party integrations
    ↓
Compile into machine-readable format (JSON)
    ↓
Review for third-party PII (redact others' data)
    ↓
Deliver via secure channel
    ↓
Log request completion
```

### Data Export Format

```json
{
  "export_date": "2024-01-15T10:30:00Z",
  "data_controller": "Acme Inc",
  "user_id": "user_12345",

  "profile": {
    "email": "user@example.com",
    "name": "Jane Doe",
    "created_at": "2023-06-01",
    "last_login": "2024-01-14"
  },

  "activity": {
    "orders": [...],
    "support_tickets": [...],
    "preferences": {...}
  },

  "consent_history": [
    {
      "date": "2023-06-01",
      "action": "granted",
      "categories": ["analytics", "marketing"]
    },
    {
      "date": "2023-09-15",
      "action": "withdrawn",
      "categories": ["marketing"]
    }
  ],

  "third_party_sharing": [
    {
      "recipient": "Stripe",
      "purpose": "Payment processing",
      "data_categories": ["payment_info"]
    }
  ]
}
```

### Deletion Implementation

```typescript
async function deleteUserData(userId: string): Promise<DeletionReport> {
  const report: DeletionReport = {
    userId,
    requestDate: new Date(),
    deletions: [],
    exceptions: []
  };

  // 1. Primary database
  await db.users.hardDelete(userId);
  report.deletions.push('primary_database');

  // 2. Anonymize activity logs (don't delete - compliance)
  await db.activityLogs.anonymize(userId);
  report.deletions.push('activity_logs_anonymized');

  // 3. Third-party services
  await stripe.customers.delete(userId);
  report.deletions.push('stripe');

  await sendgrid.contacts.delete(userId);
  report.deletions.push('sendgrid');

  // 4. Analytics - delete or anonymize
  await analytics.deleteUser(userId);
  report.deletions.push('analytics');

  // 5. Document exceptions
  // Legal holds, regulatory requirements
  if (hasLegalHold(userId)) {
    report.exceptions.push({
      system: 'legal_hold',
      reason: 'Active legal matter',
      retention: 'Until hold lifted'
    });
  }

  // Tax records must be kept 7 years
  report.exceptions.push({
    system: 'tax_records',
    reason: 'Legal requirement',
    retention: '7 years from transaction'
  });

  return report;
}
```

---

## Anonymization Techniques

### Data Anonymization Methods

| Technique | Description | Use Case | Reversible? |
|-----------|-------------|----------|-------------|
| Deletion | Remove entirely | No longer needed | No |
| Hashing | One-way transformation | IPs in logs | No* |
| Encryption | Two-way with key | Sensitive storage | Yes |
| Tokenization | Replace with token | Payment data | Yes (with vault) |
| Generalization | Reduce precision | Age: 35 → 30-40 | No |
| Pseudonymization | Replace identifiers | Analytics | Yes (with mapping) |

### K-Anonymity Implementation

Ensure each record is indistinguishable from at least k-1 others.

```sql
-- Check if dataset is 5-anonymous for quasi-identifiers
SELECT age_range, gender, zip_prefix, COUNT(*) as count
FROM anonymized_users
GROUP BY age_range, gender, zip_prefix
HAVING COUNT(*) < 5;

-- If any results, further generalize those combinations
```

### Log Anonymization

```typescript
// Before: Identifiable log
// "User user_123 (IP: 192.168.1.100) purchased item_456"

// After: Anonymized log (after 24 hours)
function anonymizeLog(log: LogEntry): AnonymizedLog {
  return {
    timestamp: log.timestamp,
    action: log.action,
    userId: hash(log.userId + dailySalt()),  // Pseudonymized
    ipAddress: anonymizeIP(log.ipAddress),   // 192.168.1.0
    metadata: log.metadata  // Keep non-PII metadata
  };
}

function anonymizeIP(ip: string): string {
  // Zero out last octet for IPv4
  const parts = ip.split('.');
  parts[3] = '0';
  return parts.join('.');
}
```

---

## Secure Development Checklist

### Pre-Development

- [ ] Data protection impact assessment (DPIA) for high-risk processing
- [ ] Privacy requirements in user stories
- [ ] Data flow documented
- [ ] Retention periods defined

### Development

- [ ] Input validation on all PII fields
- [ ] Output encoding to prevent leakage
- [ ] Encryption implemented correctly
- [ ] Access controls in place
- [ ] Logging excludes sensitive data (or redacts it)
- [ ] Consent checked before processing

### Code Review

- [ ] No PII in URLs/query strings
- [ ] No PII in client-side storage (localStorage)
- [ ] No PII logged inappropriately
- [ ] Encryption keys not hardcoded
- [ ] Third-party SDKs reviewed for privacy

### Testing

- [ ] Test data uses synthetic PII, not real
- [ ] Deletion actually deletes (verify in DB)
- [ ] Access controls tested (role-based)
- [ ] Consent flows tested end-to-end

### Deployment

- [ ] Environment variables for secrets
- [ ] Production data isolated from dev/staging
- [ ] Monitoring excludes PII from alerts
- [ ] Backup encryption verified
