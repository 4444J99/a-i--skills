# Secrets Management

When moving dotfiles to GitHub, the risk of leaking secrets (SSH private keys, API tokens) is paramount. This reference covers secure strategies for managing secrets in a version-controlled environment.

## What NOT to Commit

Never commit these to a public (or even private) repository without encryption:

- SSH private keys (`id_rsa`, `id_ed25519`)
- API tokens and keys
- Database credentials
- OAuth client secrets
- `.env` files with real values
- AWS credentials
- Kubernetes secrets

## Strategy 1: Private Repository

The simplest security layer is a **Private GitHub Repository**.

**Pros:**
- GitHub Free allows unlimited private repos
- Obscures configs from public internet
- Zero additional tooling

**Cons:**
- Not encrypted at rest on GitHub's servers
- If your GitHub account is compromised, secrets are exposed
- Insufficient for high-security environments

**Best for:** Personal configs without highly sensitive data.

---

## Strategy 2: git-crypt

Transparently encrypts files on `git push` and decrypts on `git pull`.

### Setup

```bash
# Install
brew install git-crypt  # macOS
apt install git-crypt   # Debian/Ubuntu

# Initialize in your repo
cd ~/.cfg  # or wherever your dotfiles are
git-crypt init

# Export the key (store this safely!)
git-crypt export-key ~/dotfiles-key.gpg
```

### Configure Encrypted Files

Create `.gitattributes`:

```gitattributes
# Encrypt secrets
secrets/** filter=git-crypt diff=git-crypt
.config/aws/credentials filter=git-crypt diff=git-crypt
.config/ssh/id_* filter=git-crypt diff=git-crypt
*.secret filter=git-crypt diff=git-crypt
```

### Usage

```bash
# Add files - they encrypt automatically on commit
config add .config/aws/credentials
config commit -m "Add AWS credentials (encrypted)"

# On new machine, after cloning
git-crypt unlock ~/dotfiles-key.gpg
```

### Pros & Cons

**Pros:**
- Seamless workflow
- Files appear as plain text locally
- Works with any Git hosting

**Cons:**
- Binary diffs on GitHub (can't review changes in UI)
- Key rotation is complex
- Need to distribute unlock key securely

---

## Strategy 3: SOPS (Secrets OPerationS)

Mozilla's tool encrypts *values* inside JSON/YAML files while leaving keys readable.

### Example

Original:
```yaml
database:
  host: localhost
  password: supersecret  # allow-secret (example placeholder)
```

Encrypted with SOPS:
```yaml
database:
  host: localhost
  password: ENC[AES256_GCM,data:abc123...,type:str]  # allow-secret (example)
sops:
  kms: ...
  version: 3.7.0
```

### Setup

```bash
brew install sops

# Create config
cat > ~/.sops.yaml << 'EOF'
creation_rules:
  - path_regex: \.secret\.yaml$
    age: >-
      age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
EOF
```

### Pros & Cons

**Pros:**
- Better cloud KMS integration (AWS KMS, GCP KMS, Azure Key Vault)
- Can diff file structure (only values are encrypted)
- Supports multiple key formats

**Cons:**
- Higher setup complexity
- Requires `sops` binary everywhere
- Overkill for personal dotfiles

---

## Strategy 4: Runtime Injection (Recommended)

The most secure approach: **don't store secrets in Git at all**. Store them in a password manager and inject at runtime.

### 1Password + direnv

```bash
# Install
brew install 1password-cli direnv

# Login
op signin

# Create .envrc for a project
# ~/.config/aws/.envrc
export AWS_ACCESS_KEY_ID=$(op read "op://Private/AWS/access-key")
export AWS_SECRET_ACCESS_KEY=$(op read "op://Private/AWS/secret-key")
```

When you `cd` into the directory, direnv loads the secrets from 1Password.

### Bitwarden + direnv

```bash
# Install
brew install bitwarden-cli direnv

# Login
bw login
export BW_SESSION=$(bw unlock --raw)

# .envrc
export API_KEY=$(bw get password "My API Key")
```

### Benefits

- **Zero secrets in Git** — not even encrypted
- **Single source of truth** — password manager
- **Automatic rotation** — update in password manager, applies everywhere
- **Audit trail** — password managers log access

---

## Strategy 5: Separate Private Repo

Maintain two repositories:

1. **Public dotfiles** — Shell configs, editor settings, aliases
2. **Private secrets** — Credentials, API keys, SSH keys

### Structure

```
# Public repo: github.com/user/dotfiles
~/.config/
├── zsh/
├── git/
├── nvim/
└── ...

# Private repo: github.com/user/secrets (private)
~/.secrets/
├── aws/
│   └── credentials
├── ssh/
│   ├── id_ed25519
│   └── config
└── api-keys.env
```

### Bootstrap Script

```bash
#!/usr/bin/env bash

# Clone public dotfiles
git clone --bare git@github.com:user/dotfiles.git ~/.cfg

# Clone private secrets
git clone git@github.com:user/secrets.git ~/.secrets

# Symlink secrets to expected locations
ln -s ~/.secrets/ssh ~/.ssh
ln -s ~/.secrets/aws ~/.config/aws
```

---

## Hybrid Approach (Recommended)

Combine strategies for defense in depth:

1. **Private repository** for obscurity
2. **git-crypt** for secrets that must be in the repo
3. **1Password/direnv** for high-rotation credentials (API keys, tokens)
4. **Separate private repo** for SSH keys

### Example .gitattributes

```gitattributes
# Encrypt with git-crypt
.config/ssh/config filter=git-crypt diff=git-crypt

# These should be in separate repo or 1Password
# Never commit:
# - id_rsa, id_ed25519 (SSH private keys)
# - AWS credentials
# - API tokens
```

---

## Checklist Before Pushing

Before pushing dotfiles to any remote:

```bash
# Search for potential secrets
grep -r "PRIVATE KEY" ~/.config
grep -r "sk-" ~/.config          # OpenAI keys
grep -r "ghp_" ~/.config         # GitHub tokens
grep -r "AKIA" ~/.config         # AWS access keys

# Check git-crypt status
git-crypt status

# Review what's being committed
config diff --cached
```

---

## Emergency: Leaked Secret

If you accidentally commit a secret:

1. **Rotate the secret immediately** — Assume it's compromised
2. **Remove from Git history**:
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/secret' \
     HEAD
   git push --force
   ```
3. **Use BFG Repo-Cleaner** for large repos:
   ```bash
   bfg --delete-files secret.key
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```
4. **GitHub**: Request cache purge from support

---

## Summary

| Strategy | Security Level | Complexity | Best For |
|----------|----------------|------------|----------|
| Private Repo | Low | Very Low | Non-sensitive configs |
| git-crypt | Medium | Low | Personal dotfiles with some secrets |
| SOPS | High | Medium | Team/enterprise secrets |
| Runtime Injection | Very High | Medium | API keys, rotating credentials |
| Separate Private Repo | High | Low | SSH keys, certificates |
