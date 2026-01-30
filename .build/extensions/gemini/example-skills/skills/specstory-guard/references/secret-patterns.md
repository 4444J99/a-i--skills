# Secret Detection Patterns

Common patterns for detecting secrets in code and chat history.

## High-Confidence Patterns

These patterns strongly indicate real secrets.

### API Keys & Tokens

| Pattern | Regex | Description |
|---------|-------|-------------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | AWS access key ID |
| AWS Secret Key | `aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}` | AWS secret key |
| GitHub PAT | `ghp_[A-Za-z0-9]{36}` | GitHub personal access token |
| GitHub OAuth | `gho_[A-Za-z0-9]{36}` | GitHub OAuth token |
| GitHub App | `(ghu|ghs)_[A-Za-z0-9]{36}` | GitHub App tokens |
| Slack Token | `xox[baprs]-[0-9A-Za-z\-]{10,}` | Slack bot/user/app tokens |
| Stripe Key | `(sk|pk)_(live|test)_[0-9a-zA-Z]{24,}` | Stripe API keys |
| OpenAI Key | `sk-[A-Za-z0-9]{48}` | OpenAI API key |
| Anthropic Key | `sk-ant-[A-Za-z0-9\-]{95}` | Anthropic API key |

### Private Keys

| Pattern | Description |
|---------|-------------|
| `-----BEGIN RSA PRIVATE KEY-----` | RSA private key |
| `-----BEGIN OPENSSH PRIVATE KEY-----` | OpenSSH private key |
| `-----BEGIN EC PRIVATE KEY-----` | EC private key |
| `-----BEGIN DSA PRIVATE KEY-----` | DSA private key |
| `-----BEGIN PGP PRIVATE KEY BLOCK-----` | PGP private key |

### Generic Secrets

| Pattern | Regex | Description |
|---------|-------|-------------|
| Password assignment | `password\s*[=:]\s*["'][^"']+["']` | Password in config |
| Secret assignment | `secret\s*[=:]\s*["'][^"']+["']` | Secret value |
| API key assignment | `api[_-]?key\s*[=:]\s*["'][^"']+["']` | Generic API key |
| Token assignment | `token\s*[=:]\s*["'][^"']+["']` | Generic token |
| Connection string | `(mongodb|postgres|mysql|redis):\/\/[^\s]+` | Database URL with creds |

---

## Medium-Confidence Patterns

May be secrets or may be placeholders/examples.

### Bearer Tokens

```regex
Authorization:\s*Bearer\s+[A-Za-z0-9\-._~+/]+=*
```

Context matters: in error logs, often a real token.

### Base64 Encoded Values

```regex
[A-Za-z0-9+/]{40,}={0,2}
```

Only flag if appears in:
- Header values
- Environment variables
- Config files

### JWT Tokens

```regex
eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*
```

Always real JWTs, but may be expired test tokens.

---

## Low-Confidence Patterns

Often false positives but worth checking.

### Hex Strings

```regex
[a-f0-9]{32,}
```

Could be: hashes, commit SHAs, session IDs, or secrets.

### UUID-like Values

```regex
[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}
```

Usually IDs, rarely secrets.

---

## Allowlist Patterns

Common false positives to exclude.

### Documentation Placeholders

```regex
(your-api-key|YOUR_API_KEY|<API_KEY>|PLACEHOLDER|example|test-key)
```

### Truncated/Redacted

```regex
(\.{3,}|xxx+|\*{3,}|REDACTED|HIDDEN)
```

### Known Safe Patterns

```regex
# Version strings
v[0-9]+\.[0-9]+\.[0-9]+

# Commit SHAs in typical contexts
commit [a-f0-9]{40}

# File hashes
sha256:[a-f0-9]{64}
md5:[a-f0-9]{32}
```

---

## Environment-Specific Patterns

### Node.js / npm

| Pattern | Description |
|---------|-------------|
| `NPM_TOKEN` | npm publish token |
| `NODE_AUTH_TOKEN` | npm registry auth |
| `npm_[A-Za-z0-9]{36}` | npm token format |

### Python / pip

| Pattern | Description |
|---------|-------------|
| `PYPI_TOKEN` | PyPI publish token |
| `pypi-[A-Za-z0-9]{56}` | PyPI token format |

### Docker / Kubernetes

| Pattern | Description |
|---------|-------------|
| `DOCKER_AUTH_CONFIG` | Docker registry auth |
| `KUBECONFIG` contents | Kubernetes credentials |

### Cloud Providers

| Provider | Patterns |
|----------|----------|
| **Google Cloud** | Service account JSON, `gcloud auth` output |
| **Azure** | `AZURE_CLIENT_SECRET`, tenant credentials |
| **Heroku** | `HEROKU_API_KEY`, app tokens |
| **Vercel** | `VERCEL_TOKEN` |
| **Netlify** | `NETLIFY_AUTH_TOKEN` |

---

## Remediation Patterns

### Replace with Placeholder

```
# Before
API_KEY=sk-live-abc123xyz # allow-secret

# After
API_KEY=[REDACTED] # allow-secret
```

### Environment Variable Reference

```
# Before
api_key: "actual-secret-value" # allow-secret

# After
api_key: ${API_KEY}
```

### Truncation

```
# Before
token: "eyJhbGciOiJIUzI1NiIs..." # allow-secret

# After
token: "eyJhbG...[truncated]" # allow-secret
```

---

## Severity Classification

| Severity | Impact | Examples |
|----------|--------|----------|
| **Critical** | Account compromise | AWS keys, GitHub PATs, private keys |
| **High** | Service access | API keys, database URLs |
| **Medium** | Limited exposure | Expired tokens, test credentials |
| **Low** | Minimal risk | Truncated secrets, obvious placeholders |

---

## Testing Patterns

Use these safe patterns to test detection.

```
# Should match (but are fake)
AKIAIOSFODNN7EXAMPLE                          # allow-secret
wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY      # allow-secret
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx       # allow-secret

# Should NOT match
password=<your-password-here>                  # allow-secret
api_key=YOUR_API_KEY                           # allow-secret
token=...                                      # allow-secret
```
