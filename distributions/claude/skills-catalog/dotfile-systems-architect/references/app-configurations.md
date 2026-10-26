# Application Configuration Strategies

Many applications defy XDG standards. This reference documents specific intervention strategies for common tools.

## Visual Studio Code

VS Code is an Electron app that maintains strict separation between "User Data" and "Extensions."

### The Extensions Directory Problem

By default, VS Code creates `~/.vscode` in root to store extensions. This directory can grow to gigabytes.

### Solution 1: CLI Flags (Transient)

```bash
code --extensions-dir "$XDG_DATA_HOME/vscode/extensions"
```

**Limitation:** Only works when launching from terminal. Dock/Spotlight launches revert to `~/.vscode`.

### Solution 2: Symlink (Robust)

```bash
# Create destination
mkdir -p "$XDG_DATA_HOME/vscode/extensions"

# Move existing extensions
mv ~/.vscode/extensions/* "$XDG_DATA_HOME/vscode/extensions/"

# Remove root folder
rm -rf ~/.vscode

# Create symlink
ln -s "$XDG_DATA_HOME/vscode" ~/.vscode
```

**Note:** This leaves a symlink in root, but prevents creation of a physical directory.

### Settings Synchronization

VS Code stores user settings in platform-specific paths:

| Platform | Location |
|----------|----------|
| macOS | `~/Library/Application Support/Code/User/settings.json` |
| Linux | `~/.config/Code/User/settings.json` |
| Windows | `%APPDATA%\Code\User\settings.json` |

**Strategy:** Keep `settings.json` and `keybindings.json` in your dotfiles repo, symlink to OS location:

```bash
# macOS example
mkdir -p "$XDG_CONFIG_HOME/vscode"
# Store your settings.json in $XDG_CONFIG_HOME/vscode/

# Symlink to VS Code's expected location
ln -sf "$XDG_CONFIG_HOME/vscode/settings.json" \
       "$HOME/Library/Application Support/Code/User/settings.json"
ln -sf "$XDG_CONFIG_HOME/vscode/keybindings.json" \
       "$HOME/Library/Application Support/Code/User/keybindings.json"
```

---

## Claude (Anthropic)

Configuration is split between the Desktop Application and CLI.

### Claude Desktop (Electron)

Stores MCP server configurations in a JSON file:

| Platform | Location |
|----------|----------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Strategy:**

```bash
# Create version-controlled config
mkdir -p "$XDG_CONFIG_HOME/claude"
# Edit $XDG_CONFIG_HOME/claude/claude_desktop_config.json

# Symlink to system location (macOS)
ln -sf "$XDG_CONFIG_HOME/claude/claude_desktop_config.json" \
       "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
```

**Warning:** Ensure this file does not contain raw API keys if your repo is public.

### Claude Code (CLI)

- **Legacy:** Stored configs in `~/.claude`
- **Current (v1.0.29+):** Moving toward XDG compliance (`~/.config/claude`)
- **CLAUDE.md:** Project-specific instructions, intended for project repos

**Cleanup:**

1. Check if `~/.claude` exists
2. Verify if your version supports `XDG_CONFIG_HOME`
3. If not, add to `.gitignore` and accept as temporary violation

---

## AWS CLI

**Default:** `~/.aws/config` and `~/.aws/credentials`

### XDG Fix

```bash
export AWS_CONFIG_FILE="$XDG_CONFIG_HOME/aws/config"
export AWS_SHARED_CREDENTIALS_FILE="$XDG_CONFIG_HOME/aws/credentials"
```

### Caveat

Third-party SDKs (older Boto3, Terraform providers) might fall back to `~/.aws` if environment variables aren't propagated. For robust compatibility:

```bash
# Belt-and-suspenders approach
ln -s "$XDG_CONFIG_HOME/aws" "$HOME/.aws"
```

---

## Kubernetes

**Default:** `~/.kube/config`

### XDG Fix

```bash
export KUBECONFIG="$XDG_CONFIG_HOME/kube/config"
```

Create the directory:

```bash
mkdir -p "$XDG_CONFIG_HOME/kube"
```

Tools that respect `KUBECONFIG`:
- kubectl
- helm
- k9s
- lens

---

## SSH

**Default:** `~/.ssh/` (hardcoded, no env var)

### Strategy: Symlink

```bash
mkdir -p "$XDG_CONFIG_HOME/ssh"
mv ~/.ssh/* "$XDG_CONFIG_HOME/ssh/"
rmdir ~/.ssh
ln -s "$XDG_CONFIG_HOME/ssh" ~/.ssh
```

**Note:** SSH is security-critical. Ensure permissions remain correct:

```bash
chmod 700 "$XDG_CONFIG_HOME/ssh"
chmod 600 "$XDG_CONFIG_HOME/ssh/id_*"
chmod 644 "$XDG_CONFIG_HOME/ssh/id_*.pub"
chmod 644 "$XDG_CONFIG_HOME/ssh/config"
```

---

## GnuPG

**Default:** `~/.gnupg/`

### XDG Fix

```bash
export GNUPGHOME="$XDG_DATA_HOME/gnupg"
```

Move existing:

```bash
mkdir -p "$XDG_DATA_HOME/gnupg"
mv ~/.gnupg/* "$XDG_DATA_HOME/gnupg/"
chmod 700 "$XDG_DATA_HOME/gnupg"
```

---

## Cargo/Rust

```bash
export CARGO_HOME="$XDG_DATA_HOME/cargo"
export RUSTUP_HOME="$XDG_DATA_HOME/rustup"
```

Add to PATH:

```bash
export PATH="$CARGO_HOME/bin:$PATH"
```

---

## Node/npm

```bash
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"
export NODE_REPL_HISTORY="$XDG_STATE_HOME/node/history"
```

---

## Go

```bash
export GOPATH="$XDG_DATA_HOME/go"
export PATH="$GOPATH/bin:$PATH"
```

---

## Docker

**Default:** `~/.docker/`

```bash
export DOCKER_CONFIG="$XDG_CONFIG_HOME/docker"
```

---

## Complete Shims Block

Add to `~/.zshenv` or `~/.config/zsh/.zshrc`:

```bash
# XDG Shims for non-compliant apps
export GIT_CONFIG_GLOBAL="$XDG_CONFIG_HOME/git/config"
export AWS_CONFIG_FILE="$XDG_CONFIG_HOME/aws/config"
export AWS_SHARED_CREDENTIALS_FILE="$XDG_CONFIG_HOME/aws/credentials"
export KUBECONFIG="$XDG_CONFIG_HOME/kube/config"
export GNUPGHOME="$XDG_DATA_HOME/gnupg"
export CARGO_HOME="$XDG_DATA_HOME/cargo"
export RUSTUP_HOME="$XDG_DATA_HOME/rustup"
export GOPATH="$XDG_DATA_HOME/go"
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"
export NODE_REPL_HISTORY="$XDG_STATE_HOME/node/history"
export DOCKER_CONFIG="$XDG_CONFIG_HOME/docker"

# PATH additions
export PATH="$CARGO_HOME/bin:$GOPATH/bin:$PATH"
```

---

## Cross-Platform Setup Script

```bash
#!/usr/bin/env bash
set -euo pipefail

# Detect OS
case "$(uname -s)" in
    Darwin)
        CODE_USER="$HOME/Library/Application Support/Code/User"
        CLAUDE_CONFIG="$HOME/Library/Application Support/Claude"
        ;;
    Linux)
        CODE_USER="$XDG_CONFIG_HOME/Code/User"
        CLAUDE_CONFIG="$XDG_CONFIG_HOME/claude"
        ;;
esac

# VS Code settings
ln -sf "$XDG_CONFIG_HOME/vscode/settings.json" "$CODE_USER/settings.json"
ln -sf "$XDG_CONFIG_HOME/vscode/keybindings.json" "$CODE_USER/keybindings.json"

# Claude Desktop
mkdir -p "$CLAUDE_CONFIG"
ln -sf "$XDG_CONFIG_HOME/claude/claude_desktop_config.json" \
       "$CLAUDE_CONFIG/claude_desktop_config.json"

echo "Application symlinks created"
```
