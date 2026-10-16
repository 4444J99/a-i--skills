# Secret Remediation Guide

Step-by-step guide for handling secrets found in SpecStory history.

## Immediate Actions

When Guard finds a secret, follow this priority order:

### 1. Assess the Risk

| Question | If Yes |
|----------|--------|
| Is this a production credential? | High priority - continue immediately |
| Was the file ever pushed to a remote? | May already be exposed |
| Is the secret still active? | Must be rotated |
| Can the secret access sensitive data? | Document scope of exposure |

### 2. Redact the Secret

**In the history file:**

```markdown
# Before
The API key is sk-live-abc123xyz789

# After
The API key is [REDACTED]
```

**Preserve context:**
- Keep the surrounding text
- Indicate what type of secret was removed
- Leave enough info to understand the conversation

### 3. Rotate the Credential

**Never assume a secret is safe just because you redacted it.**

| Service | Rotation Steps |
|---------|----------------|
| **AWS** | IAM Console > Users > Security credentials > Create access key |
| **GitHub** | Settings > Developer settings > Personal access tokens > Regenerate |
| **OpenAI** | API Keys page > Create new secret key |
| **Stripe** | Dashboard > Developers > API keys > Roll keys |
| **Database** | Change password, update connection strings |

---

## Remediation Patterns

### Pattern 1: Simple Replacement

Best for: isolated secrets in text

```markdown
# Original
I set the API key to sk-ant-abc123...

# Redacted
I set the API key to [REDACTED API_KEY]
```

### Pattern 2: Contextual Replacement

Best for: secrets in code blocks

```markdown
# Original
```bash
export OPENAI_API_KEY="sk-abc123xyz"
```

# Redacted
```bash
export OPENAI_API_KEY="[REDACTED]"
```
```

### Pattern 3: Truncation with Indicator

Best for: long tokens where partial visibility helps debugging

```markdown
# Original
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (example JWT) <!-- allow-secret -->

# Redacted
Authorization: Bearer eyJhbG...[REDACTED JWT]
```

### Pattern 4: Environment Variable Hint

Best for: config file examples

```markdown
# Original
database_url: "postgres://admin:secretpass@db.example.com/prod"

# Redacted
database_url: "${DATABASE_URL}" # Set this in your environment
```

---

## Bulk Remediation

For multiple secrets across many files:

### Scripted Approach

```bash
# Create a redaction script
find .specstory/history -name "*.md" -exec grep -l "sk-ant-" {} \; | \
  xargs sed -i '' 's/sk-ant-[A-Za-z0-9-]*/[REDACTED]/g'
```

### Manual Review Checklist

- [ ] Run Guard scan to get full list
- [ ] Group secrets by type
- [ ] Redact all instances of each secret
- [ ] Verify with another scan
- [ ] Rotate all affected credentials

---

## Preventing Future Exposure

### Pre-Chat Hygiene

Before pasting into chat:
1. Remove actual values from configs
2. Use placeholders in examples
3. Sanitize error messages
4. Redact logs before sharing

### Good Practices

| Do This | Not This |
|---------|----------|
| `export API_KEY="your-key-here"` | `export API_KEY="sk-live-abc123"` |
| `{"password": "[YOUR_PASSWORD]"}` | `{"password": "hunter2"}` |
| Use `.env.example` with placeholders | Paste actual `.env` contents |

### Guardrail Installation

```bash
# Install the pre-commit hook
/specstory-guard install

# Verify it's active
ls -la .git/hooks/pre-commit
```

---

## Secret Rotation Checklists

### AWS Keys

- [ ] Create new access key in IAM Console
- [ ] Update all systems using the old key
- [ ] Test with new key
- [ ] Deactivate old key
- [ ] Delete old key after grace period

### GitHub PAT

- [ ] Generate new token with same scopes
- [ ] Update GitHub Actions secrets
- [ ] Update local git credential manager
- [ ] Update any CI/CD systems
- [ ] Revoke old token

### Database Credentials

- [ ] Create new user or change password
- [ ] Update connection strings in:
  - [ ] Environment variables
  - [ ] Secret managers
  - [ ] CI/CD configs
  - [ ] Application configs
- [ ] Test connectivity
- [ ] Remove old credentials

### API Keys (Generic)

- [ ] Generate new key in service dashboard
- [ ] Update environment variables
- [ ] Update secret manager
- [ ] Deploy updated config
- [ ] Monitor for old key usage
- [ ] Revoke old key

---

## Post-Remediation Verification

### Run Guard Scan

```bash
/specstory-guard scan
```

Expected output:
```
All clear! No secrets detected in 47 files.
```

### Check Git History

If files were committed before remediation:

```bash
# Check if secret exists in git history
git log -p --all -S "sk-live-" -- .specstory/

# If found, consider:
# 1. BFG Repo-Cleaner to rewrite history
# 2. Notifying team about exposure
# 3. Mandatory credential rotation
```

### Audit Log

Keep a record of remediation:

```markdown
## Secret Remediation Log

| Date | File | Secret Type | Action | Rotated |
|------|------|-------------|--------|---------|
| 2026-01-22 | api-setup.md | AWS Key | Redacted | Yes |
| 2026-01-22 | debug-auth.md | JWT | Truncated | N/A (expired) |
```

---

## Escalation Criteria

Escalate to security team if:

- Production credentials were exposed
- Secrets may have been pushed to public repos
- Multiple high-value credentials in one session
- Evidence of unauthorized access after exposure
- Regulatory implications (PII, healthcare, finance)
