# XDG Base Directory Specification

The XDG Base Directory Specification is the foundation for achieving directory hygiene. Originally designed for Linux desktop environments, it has been widely adopted by command-line tools and is the gold standard for cross-platform directory management.

## Core Variables

| Variable | Default Path | Purpose | Backup Policy |
|----------|--------------|---------|---------------|
| `XDG_CONFIG_HOME` | `$HOME/.config` | Configuration files (user-specific `/etc`). Read-only for apps, writable by user. | **Critical:** Version-control via Git |
| `XDG_DATA_HOME` | `$HOME/.local/share` | User-specific data (keyrings, fonts, desktop entries). User analogue to `/usr/share`. | **Selective:** Back up distinct subdirectories |
| `XDG_CACHE_HOME` | `$HOME/.cache` | Non-essential data (thumbnails, browser cache, package buffers). Apps must handle absence gracefully. | **None:** Exclude from backups. Safe to `rm -rf`. |
| `XDG_STATE_HOME` | `$HOME/.local/state` | State data persisting between restarts (logs, history files). Not configuration. | **None:** Generally excluded from config backups |
| `XDG_RUNTIME_DIR` | `/run/user/$UID` | Non-essential runtime files (sockets, pipes). Managed by OS, cleared on reboot. | **None:** Volatile system area |

## Understanding STATE vs DATA vs CACHE

The introduction of `XDG_STATE_HOME` is a relatively recent refinement. Historically, applications dumped logs and history into `XDG_DATA_HOME` or `XDG_CACHE_HOME`.

**Separating State allows granular backup policies:**
- Shell history → STATE (valuable, but not configuration)
- Browser cache → CACHE (regenerable, exclude from backups)
- Fonts → DATA (selective backup)
- Git config → CONFIG (version-controlled)

## Compliance Landscape

### Fully Compliant

These tools respect XDG out of the box:
- Neovim
- Git (recent versions)
- Helix
- Yarn
- Fish Shell
- Most Rust and Go CLI tools

### Partially Compliant

These require environment variable hints:
- **Zsh** → Set `ZDOTDIR`
- **GnuPG** → Set `GNUPGHOME`
- **Bash** → Requires sourcing workarounds

### Non-Compliant (Hostile Apps)

These require shim strategies:
- **OpenSSH** → Hardcoded `~/.ssh`
- **AWS CLI** → Defaults to `~/.aws`
- **Kubernetes** → Defaults to `~/.kube`
- **macOS GUI apps** → Prefer `~/Library`

## Shim Strategies

### Environment Variable Shims

Set these in `~/.zshenv` before other apps load:

```bash
# Git (for versions that don't auto-detect)
export GIT_CONFIG_GLOBAL="$XDG_CONFIG_HOME/git/config"

# AWS CLI
export AWS_CONFIG_FILE="$XDG_CONFIG_HOME/aws/config"
export AWS_SHARED_CREDENTIALS_FILE="$XDG_CONFIG_HOME/aws/credentials"

# Kubernetes
export KUBECONFIG="$XDG_CONFIG_HOME/kube/config"

# GnuPG
export GNUPGHOME="$XDG_DATA_HOME/gnupg"
```

### Symlink Shims

When environment variables aren't respected:

```bash
# AWS (for SDKs that ignore env vars)
ln -s "$XDG_CONFIG_HOME/aws" "$HOME/.aws"

# SSH (no env var available)
ln -s "$XDG_CONFIG_HOME/ssh" "$HOME/.ssh"
```

### Alias Shims

For CLI tools that accept flags:

```bash
# VS Code extensions
alias code='code --extensions-dir "$XDG_DATA_HOME/vscode/extensions"'
```

## Practical Setup

### 1. Create the Directory Structure

```bash
mkdir -p ~/.config ~/.local/share ~/.local/state ~/.cache
```

### 2. Set Variables in ~/.zshenv

```bash
# XDG Base Directories
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
```

### 3. Verify Compliance

Check where apps store their data:

```bash
# List visible dotfiles (should be minimal)
ls -a ~ | grep '^\.'

# Expected: .cache, .config, .local, .zshenv (and maybe .ssh, .gnupg if using symlinks)
```

## Further Reading

- [freedesktop.org XDG specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [Arch Wiki: XDG Base Directory](https://wiki.archlinux.org/title/XDG_Base_Directory)
