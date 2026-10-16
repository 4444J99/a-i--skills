# Migration Guide

This guide walks through transitioning from a cluttered home directory to a Minimal Root architecture. Follow these phases in order.

## Phase 1: Preparation (The Audit)

### Step 1: Full Backup

Before making any changes, create a complete backup:

```bash
# Simple backup
tar -czf ~/backup-home-$(date +%Y%m%d).tar.gz ~

# Or use Time Machine / rsync
rsync -av ~ /Volumes/Backup/home-backup/
```

### Step 2: Audit Your Home Directory

List all dotfiles and categorize them:

```bash
ls -la ~ | grep '^\.'
```

Create a categorization list:

| File/Dir | Category | Action |
|----------|----------|--------|
| `.bashrc` | Config | Move to `.config/bash/` |
| `.zshrc` | Config | Move to `.config/zsh/` |
| `.gitconfig` | Config | Move to `.config/git/` |
| `.ssh/` | Data | Symlink or move to `.config/ssh/` |
| `.gnupg/` | Data | Move to `.local/share/gnupg/` |
| `.npm/` | Cache | Delete (regenerates) |
| `.cache/` | Cache | Keep (already correct) |
| `.DS_Store` | Junk | Delete |
| `.vscode/` | Data | Move to `.local/share/vscode/` |

### Step 3: Document What You Have

```bash
# Save current state
ls -la ~ > ~/dotfile-audit.txt
```

---

## Phase 2: Create the Skeleton

### Step 1: Create XDG Directory Structure

```bash
mkdir -p ~/.config
mkdir -p ~/.local/share
mkdir -p ~/.local/state
mkdir -p ~/.cache
```

### Step 2: Initialize the Bare Repository

```bash
# Create the bare repo
git init --bare $HOME/.cfg

# Define the alias (add permanently later)
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# Critical: hide untracked files
config config --local status.showUntrackedFiles no
```

### Step 3: Create Remote Repository

On GitHub, create a new private repository (e.g., `dotfiles`).

```bash
config remote add origin git@github.com:username/dotfiles.git
```

---

## Phase 3: The Migration

### Step 1: Shell Bootstrap

Create the minimal `~/.zshenv`:

```bash
cat > ~/.zshenv << 'EOF'
# ~/.zshenv - The only dotfile in root

# XDG Base Directory specification
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

# Redirect Zsh to XDG location
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"

# Source the real zshenv
[[ -f "$ZDOTDIR/.zshenv" ]] && source "$ZDOTDIR/.zshenv"
EOF
```

### Step 2: Move Zsh Configuration

```bash
mkdir -p ~/.config/zsh

# Move existing zsh files
mv ~/.zshrc ~/.config/zsh/.zshrc
mv ~/.zprofile ~/.config/zsh/.zprofile 2>/dev/null || true
mv ~/.zlogin ~/.config/zsh/.zlogin 2>/dev/null || true
```

Update history location in `~/.config/zsh/.zshrc`:

```bash
# Add to .zshrc
HISTFILE="$XDG_STATE_HOME/zsh/history"
mkdir -p "${HISTFILE:h}"
```

Move existing history:

```bash
mkdir -p ~/.local/state/zsh
mv ~/.zsh_history ~/.local/state/zsh/history
```

### Step 3: Move Git Configuration

```bash
mkdir -p ~/.config/git
mv ~/.gitconfig ~/.config/git/config
mv ~/.gitignore ~/.config/git/ignore 2>/dev/null || true
```

Add to `~/.config/zsh/.zshenv`:

```bash
export GIT_CONFIG_GLOBAL="$XDG_CONFIG_HOME/git/config"
```

### Step 4: Move Other Configurations

```bash
# Neovim (already XDG-compliant, just verify)
# Should be in ~/.config/nvim/

# SSH (symlink strategy)
mkdir -p ~/.config/ssh
mv ~/.ssh/* ~/.config/ssh/
rmdir ~/.ssh
ln -s ~/.config/ssh ~/.ssh
chmod 700 ~/.config/ssh
chmod 600 ~/.config/ssh/id_*

# GnuPG
mkdir -p ~/.local/share/gnupg
mv ~/.gnupg/* ~/.local/share/gnupg/
rmdir ~/.gnupg
chmod 700 ~/.local/share/gnupg
# Add to .zshenv: export GNUPGHOME="$XDG_DATA_HOME/gnupg"

# AWS
mkdir -p ~/.config/aws
mv ~/.aws/* ~/.config/aws/ 2>/dev/null || true
# Add to .zshenv:
# export AWS_CONFIG_FILE="$XDG_CONFIG_HOME/aws/config"
# export AWS_SHARED_CREDENTIALS_FILE="$XDG_CONFIG_HOME/aws/credentials"

# Kubernetes
mkdir -p ~/.config/kube
mv ~/.kube/config ~/.config/kube/ 2>/dev/null || true
# Add to .zshenv: export KUBECONFIG="$XDG_CONFIG_HOME/kube/config"
```

### Step 5: Clean Up Junk

```bash
# Remove macOS cruft
rm -f ~/.DS_Store

# Remove regenerable caches
rm -rf ~/.npm
rm -rf ~/.node_repl_history
rm -rf ~/.python_history

# Remove old empty directories
rmdir ~/.aws 2>/dev/null || true
rmdir ~/.kube 2>/dev/null || true
```

### Step 6: Add Bare Repo Alias

Add to `~/.config/zsh/.zshrc`:

```bash
# Dotfiles management
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
```

---

## Phase 4: Commit and Push

### Step 1: Add Essential Files

```bash
# Start a new shell to load new config
exec zsh

# Add the bootstrap
config add ~/.zshenv

# Add shell configs
config add ~/.config/zsh

# Add git config
config add ~/.config/git

# Add any other configs
config add ~/.config/nvim
config add ~/.config/ssh/config  # NOT private keys
```

### Step 2: Create .gitignore

```bash
cat > ~/.gitignore << 'EOF'
# Ignore everything by default
*

# Track specific paths
!.zshenv
!.gitignore
!.config/
!.config/**

# But not secrets or generated files
.config/ssh/id_*
.config/aws/credentials
*.zwc
.zcompdump*
EOF

config add ~/.gitignore
```

### Step 3: Initial Commit

```bash
config commit -m "Initial dotfiles setup with XDG structure"
```

### Step 4: Push to Remote

```bash
config push -u origin main
```

---

## Phase 5: Restore on New Machine

### Quick Restore Script

Save this as a gist or in your repo's README:

```bash
#!/usr/bin/env bash
set -euo pipefail

DOTFILES_REPO="git@github.com:username/dotfiles.git"

# Clone bare repo
git clone --bare "$DOTFILES_REPO" "$HOME/.cfg"

# Define alias for this session
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# Backup existing dotfiles
mkdir -p ~/.dotfiles-backup
config checkout 2>&1 | grep -E "^\s+" | awk '{print $1}' | while read -r file; do
    mkdir -p "$(dirname ~/.dotfiles-backup/$file)"
    mv "$HOME/$file" ~/.dotfiles-backup/
done

# Checkout
config checkout

# Set config option
config config --local status.showUntrackedFiles no

echo "Dotfiles restored! Start a new shell."
```

### Manual Restore

```bash
# 1. Clone
git clone --bare git@github.com:username/dotfiles.git $HOME/.cfg

# 2. Alias
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# 3. Checkout (may fail if files exist)
config checkout

# 4. If conflicts, backup and retry
mkdir -p ~/.dotfiles-backup
config checkout 2>&1 | grep -E "^\s+" | awk '{print $1}' | xargs -I{} mv {} ~/.dotfiles-backup/
config checkout

# 5. Configure
config config --local status.showUntrackedFiles no
```

---

## Verification Checklist

After migration, verify:

```bash
# Minimal root
ls -a ~ | grep '^\.'
# Should see: . .. .cache .cfg .config .local .zshenv

# XDG variables
echo $XDG_CONFIG_HOME   # ~/.config
echo $XDG_DATA_HOME     # ~/.local/share
echo $ZDOTDIR           # ~/.config/zsh

# Shell history
echo $HISTFILE          # ~/.local/state/zsh/history

# Git config
git config --list --show-origin
# Should reference ~/.config/git/config

# Bare repo status
config status
```

---

## Troubleshooting

### "error: The following untracked working tree files would be overwritten"

Backup and remove the conflicting files:

```bash
config checkout 2>&1 | grep -E "^\s+" | awk '{print $1}' | xargs -I{} mv {} ~/.dotfiles-backup/
config checkout
```

### Zsh Not Loading Config

Check that `~/.zshenv` exists and is readable:

```bash
cat ~/.zshenv
ls -la ~/.zshenv
```

### Git Not Finding Config

Verify the environment variable:

```bash
echo $GIT_CONFIG_GLOBAL
cat "$GIT_CONFIG_HOME/git/config"
```

### SSH Permissions Error

```bash
chmod 700 ~/.config/ssh
chmod 600 ~/.config/ssh/id_*
chmod 644 ~/.config/ssh/id_*.pub
chmod 644 ~/.config/ssh/config
```

---

## Timeline

| Phase | Duration | Notes |
|-------|----------|-------|
| Audit | 30 min | Document everything |
| Skeleton | 10 min | Create directories, init repo |
| Migration | 1-2 hours | Move files, test each step |
| Polish | 30 min | Clean up, verify |
| **Total** | **2-3 hours** | For a typical developer setup |

Take your time. Test after each major change. You can always restore from backup.
