# GDPR & CCPA Compliance Checklist

Comprehensive checklist for privacy regulation compliance.

## Data Collection Requirements

### Consent (GDPR Article 7)

- [ ] Consent is freely given, specific, informed, and unambiguous
- [ ] Consent request is clearly distinguishable from other matters
- [ ] Pre-ticked boxes are NOT used
- [ ] Consent can be withdrawn as easily as it was given
- [ ] Records of consent are maintained (when, how, what)
- [ ] Separate consent obtained for different processing purposes
- [ ] Consent is obtained before processing begins

### Lawful Basis (GDPR Article 6)

| Basis | When to Use | Documentation Required |
|-------|-------------|------------------------|
| Consent | Marketing, analytics, non-essential cookies | Consent records |
| Contract | Order fulfillment, account management | Service terms |
| Legal obligation | Tax records, employment law | Legal reference |
| Vital interests | Emergency health situations | Rare, document carefully |
| Public interest | Government functions | Legal authority |
| Legitimate interest | Fraud prevention, security | LIA documentation |

### Legitimate Interest Assessment (LIA)

- [ ] Purpose identified and documented
- [ ] Necessity test: Is this processing necessary?
- [ ] Balancing test: Do individual rights override?
- [ ] Safeguards implemented to minimize impact
- [ ] Opt-out mechanism available
- [ ] LIA documented and reviewed periodically

---

## Cookie & Tracking Compliance

### Cookie Categories

| Category | GDPR Consent | CCPA Disclosure | Examples |
|----------|--------------|-----------------|----------|
| Essential | Not required | Required | Auth, security, cart |
| Functional | Required | Required | Language, preferences |
| Analytics | Required | Required | Google Analytics |
| Marketing | Required | Required | Ad tracking, retargeting |

### Cookie Banner Requirements (GDPR)

- [ ] Banner appears before non-essential cookies are set
- [ ] "Reject All" option as prominent as "Accept All"
- [ ] Granular control by cookie category available
- [ ] No dark patterns (colors, sizing to push acceptance)
- [ ] Banner doesn't block content access
- [ ] Choice remembered and not re-prompted excessively
- [ ] Preference center accessible from footer

### Technical Implementation

```javascript
// DO NOT load analytics before consent
// Wrong:
<script src="google-analytics.js"></script>

// Correct: Load only after consent
if (hasConsent('analytics')) {
  loadAnalytics();
}
```

---

## User Rights Implementation

### Right to Access (GDPR Article 15 / CCPA 1798.100)

- [ ] Process to receive and verify access requests
- [ ] Respond within 30 days (GDPR) / 45 days (CCPA)
- [ ] Provide data in machine-readable format
- [ ] Include categories of data, purposes, recipients
- [ ] No fee for reasonable requests
- [ ] Identity verification before disclosure

### Right to Erasure (GDPR Article 17)

- [ ] "Delete my account" clearly accessible
- [ ] Deletion request process documented
- [ ] Data actually deleted (not just soft-deleted)
- [ ] Third-party processors notified
- [ ] Backups handled (rotate out within retention period)
- [ ] Exceptions documented (legal holds, regulatory)

### Erasure Checklist

```
User deletion request received:

Primary Database:
- [ ] User profile deleted
- [ ] User content deleted (or anonymized)
- [ ] Associated files deleted

Third-Party Services:
- [ ] Analytics user ID deleted
- [ ] Email marketing list updated
- [ ] Payment processor records checked
- [ ] Support ticket history handled

Backups:
- [ ] Backup retention period documented
- [ ] Automated expiry in place
- [ ] No manual restore of deleted users

Logs:
- [ ] User identifiers removed/hashed
- [ ] IP addresses anonymized
- [ ] Session data purged
```

### Right to Portability (GDPR Article 20)

- [ ] Export function available to users
- [ ] Common machine-readable format (JSON, CSV)
- [ ] Includes all user-provided data
- [ ] Includes derived data where feasible
- [ ] Direct transfer to another controller if requested

### Right to Object (GDPR Article 21)

- [ ] Marketing opt-out immediately effective
- [ ] Profiling opt-out available
- [ ] Legitimate interest processing can be objected to
- [ ] Objection mechanism documented

---

## CCPA-Specific Requirements

### "Do Not Sell" (CCPA 1798.120)

- [ ] "Do Not Sell My Personal Information" link in footer
- [ ] Link leads to functional opt-out mechanism
- [ ] Sale stopped within 15 days of request
- [ ] Third-party data sharing disclosed
- [ ] Opt-out honored for at least 12 months

### Categories Disclosure (CCPA 1798.110)

Required disclosures in privacy policy:
- [ ] Categories of PI collected in past 12 months
- [ ] Categories of sources
- [ ] Business purpose for collection
- [ ] Categories of third parties shared with
- [ ] Specific pieces of PI collected (upon request)

### Financial Incentives (CCPA 1798.125)

- [ ] Loyalty programs disclosed as financial incentive
- [ ] Opt-in consent for incentive programs
- [ ] Value of data explained
- [ ] Easy withdrawal from incentive programs

---

## Technical Security Requirements

### Data Minimization

- [ ] Only necessary data collected (not "nice to have")
- [ ] Retention periods defined for each data type
- [ ] Automated deletion when retention expires
- [ ] Audit of data fields performed annually

### Data Inventory

| Data Field | Purpose | Legal Basis | Retention | Encryption |
|------------|---------|-------------|-----------|------------|
| Email | Account, marketing | Consent/Contract | Account life + 30 days | At rest |
| Name | Account display | Contract | Account life | At rest |
| IP Address | Security, fraud | Legitimate interest | 90 days | Hashed after 24h |
| Payment | Transactions | Contract | 7 years (legal) | PCI-DSS |

### Encryption Requirements

- [ ] Data encrypted at rest (AES-256 or equivalent)
- [ ] Data encrypted in transit (TLS 1.2+)
- [ ] Database encryption enabled
- [ ] Backup encryption enabled
- [ ] Key management documented

### Access Controls

- [ ] Role-based access implemented
- [ ] Principle of least privilege applied
- [ ] Access logs maintained
- [ ] Regular access reviews conducted
- [ ] MFA required for PII access

---

## Third-Party & Processor Requirements

### Data Processing Agreements (DPA)

Required DPA contents (GDPR Article 28):
- [ ] Subject matter and duration of processing
- [ ] Nature and purpose of processing
- [ ] Type of personal data processed
- [ ] Categories of data subjects
- [ ] Processor obligations and rights
- [ ] Instructions from controller
- [ ] Confidentiality obligations
- [ ] Security measures required
- [ ] Sub-processor requirements
- [ ] Audit rights
- [ ] Deletion/return upon termination

### Third-Party Audit

| Vendor | Data Shared | DPA Signed | Last Review | Compliant |
|--------|-------------|------------|-------------|-----------|
| AWS | All hosting | Yes | 2024-01 | Yes |
| Stripe | Payment | Yes | 2024-01 | Yes |
| SendGrid | Email | Yes | 2024-01 | Yes |
| Google Analytics | Behavior | Yes | 2024-01 | Check |

---

## Privacy Policy Requirements

### GDPR Required Contents

- [ ] Identity and contact details of controller
- [ ] DPO contact details (if applicable)
- [ ] Purposes and legal basis for processing
- [ ] Legitimate interests pursued (if applicable)
- [ ] Categories of recipients
- [ ] International transfer safeguards
- [ ] Retention periods
- [ ] User rights explained
- [ ] Right to withdraw consent
- [ ] Right to lodge complaint with supervisory authority
- [ ] Whether provision of data is required/optional
- [ ] Automated decision-making details

### CCPA Required Contents

- [ ] Categories of PI collected (past 12 months)
- [ ] Business/commercial purpose for collection
- [ ] Categories sold or disclosed for business purpose
- [ ] User rights under CCPA
- [ ] "Do Not Sell" instructions
- [ ] Non-discrimination statement
- [ ] Contact information for requests

---

## Breach Response Requirements

### Timeline (GDPR)

| Action | Timeline |
|--------|----------|
| Internal discovery | Document immediately |
| Risk assessment | Within hours |
| Supervisory authority notification | 72 hours if high risk |
| User notification | Without undue delay if high risk |

### Breach Documentation

- [ ] Nature of breach documented
- [ ] Categories of data affected
- [ ] Approximate number of individuals
- [ ] Likely consequences assessed
- [ ] Measures taken to address breach
- [ ] Measures to mitigate effects
- [ ] Decision on notification documented

---

## Audit Frequency

| Area | Frequency | Owner |
|------|-----------|-------|
| Cookie consent implementation | Quarterly | Dev team |
| Third-party DPAs | Annually | Legal |
| Data inventory | Annually | DPO |
| Access controls | Quarterly | Security |
| Privacy policy accuracy | Bi-annually | Legal |
| User rights process testing | Quarterly | Ops |
| Training completion | Annually | HR |
