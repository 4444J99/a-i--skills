# Bare Git Repository Setup

The Bare Git Repository is the most elegant solution for users prioritizing a minimal toolchain. Unlike standard git repositories, which place a `.git` folder inside the working directory, a bare repository stores the git metadata in a separate folder and treats the home directory (`~`) as its working tree.

## Why Bare Repos?

### The Problem with Standard Git in Home

If you run `git init` in your home directory:
- Every subdirectory becomes part of the repo search path
- System performance degrades significantly
- Interferes with other git repos in `~/src`
- `git status` is overwhelmed by noise

### The Bare Repo Solution

The Bare Repo decouples the database from the files:
1. **Repository Storage:** A hidden directory (`~/.cfg`) holds the object database
2. **Working Tree:** `$HOME` is defined as the checkout location
3. **Command Alias:** A shell alias wraps git to reference these locations

## Implementation Guide

### Step 1: Initialize the Bare Repository

```bash
git init --bare $HOME/.cfg
```

### Step 2: Define the Alias

```bash
# Add to ~/.zshenv or ~/.config/zsh/.zshrc
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
```

### Step 3: Hide Untracked Files (Critical!)

```bash
config config --local status.showUntrackedFiles no
```

**This is the linchpin of the strategy.** Without it, `git status` would list thousands of files (every photo, download, and code file) as "untracked." With this setting, the repository ignores everything in home *unless explicitly added*.

This creates an **opt-in version control system**.

### Step 4: Start Tracking Files

```bash
config add ~/.zshenv
config add ~/.config/zsh
config add ~/.config/git
config commit -m "Initial dotfiles setup"
```

### Step 5: Push to Remote

```bash
config remote add origin git@github.com:username/dotfiles.git
config push -u origin main
```

## Restoring on a New Machine

```bash
# 1. Clone the bare repo
git clone --bare git@github.com:username/dotfiles.git $HOME/.cfg

# 2. Define the alias (temporary)
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# 3. Checkout the files
config checkout

# 4. If checkout fails due to existing files
config checkout 2>&1 | grep -E "^\s+" | awk '{print $1}' | xargs -I{} rm {}
config checkout

# 5. Set the config option
config config --local status.showUntrackedFiles no
```

**Note:** Checkout will fail if files already exist (like default `.bashrc`). You must move or delete conflicting files first.

## Comparison: Bare Repo vs Stow vs Chezmoi

| Feature | Bare Git Repo | GNU Stow | Chezmoi |
|---------|---------------|----------|---------|
| **Mechanism** | Git working tree at `$HOME` | Symlinks from `~/dotfiles` to `~` | Generates files from templates |
| **Root Cleanliness** | Excellent (no visible repo folder) | Good (requires `~/dotfiles`) | Excellent (source in `~/.local/share`) |
| **Dependencies** | Git only (universal) | Perl/Stow | Go binary |
| **Cross-Platform** | Requires manual branching/shell logic | Difficult (path differences) | **Superior** (native templating) |
| **Secrets** | Requires git-crypt or sops | Difficult to integrate | Native password manager support |
| **Complexity** | High initial concept, low maintenance | Low | High setup, powerful automation |

### When to Use Each

**Bare Git Repository:**
- Single platform (or minor variations)
- Want "native" Git experience
- Prefer minimal dependencies
- Comfortable with Git internals

**GNU Stow:**
- Simple needs
- Don't mind `~/dotfiles` directory visible
- Want easy per-package enable/disable

**Chezmoi:**
- Multiple heterogeneous machines (macOS + Linux + Windows)
- Need templating for platform differences
- Want password manager integration for secrets
- Managing a "fleet" of machines

## Advanced Usage

### Branching for Different Machines

```bash
config checkout -b work-laptop
# Make work-specific changes
config commit -m "Work laptop configs"

config checkout -b personal-desktop
# Make personal changes
config commit -m "Personal desktop configs"
```

### Partial Checkout (Sparse)

For very large dotfiles repos:

```bash
config config core.sparseCheckout true
echo ".config/git" >> ~/.cfg/info/sparse-checkout
config checkout
```

## Common Commands Reference

```bash
# Status
config status

# Add a file
config add ~/.config/nvim/init.lua

# Commit
config commit -m "Update neovim config"

# Push
config push

# Pull updates
config pull

# Diff
config diff

# Log
config log --oneline
```

## Troubleshooting

### "Please commit or stash your changes"

```bash
config stash
config pull
config stash pop
```

### Accidentally Tracking Wrong File

```bash
config rm --cached <file>
config commit -m "Stop tracking <file>"
```

### Want to See Untracked Files Temporarily

```bash
config status -u
# or
config status --untracked-files=normal
```
