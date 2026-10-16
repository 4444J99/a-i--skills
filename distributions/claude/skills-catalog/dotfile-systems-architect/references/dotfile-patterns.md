# Dotfile Patterns Reference

Patterns for organizing configuration files within an XDG-compliant structure.

## XDG Directory Layout

```
~/
├── .zshenv                 # Only root dotfile (bootstrap)
├── .bashrc                 # Shim (optional)
│
├── .config/                # XDG_CONFIG_HOME
│   ├── zsh/
│   │   ├── .zshrc
│   │   ├── .zprofile
│   │   ├── aliases.zsh
│   │   └── functions.zsh
│   ├── git/
│   │   ├── config
│   │   └── ignore
│   ├── nvim/
│   │   └── init.lua
│   ├── ssh/
│   │   └── config
│   ├── aws/
│   │   └── config
│   └── vscode/
│       ├── settings.json
│       └── keybindings.json
│
├── .local/
│   ├── share/              # XDG_DATA_HOME
│   │   ├── gnupg/
│   │   ├── cargo/
│   │   ├── go/
│   │   └── vscode/
│   │       └── extensions/
│   └── state/              # XDG_STATE_HOME
│       └── zsh/
│           └── history
│
└── .cache/                 # XDG_CACHE_HOME (not backed up)
```

## Shell Configuration

### Modular Zsh Setup

```bash
# ~/.config/zsh/.zshrc

# Load modular configs
for config_file in "$ZDOTDIR"/{aliases,functions,completions}.zsh(N); do
    source "$config_file"
done

# Local overrides (machine-specific, not tracked)
[[ -f "$ZDOTDIR/.zshrc.local" ]] && source "$ZDOTDIR/.zshrc.local"
```

### Common Aliases

```bash
# ~/.config/zsh/aliases.zsh

# Navigation
alias ..="cd .."
alias ...="cd ../.."
alias ~="cd ~"

# ls alternatives
alias ll="ls -la"
alias la="ls -A"

# Git shortcuts
alias g="git"
alias gs="git status"
alias gd="git diff"
alias gc="git commit"
alias gp="git push"

# Dotfiles management (bare repo)
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# Safety
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"

# Modern replacements (if installed)
command -v eza &>/dev/null && alias ls="eza"
command -v bat &>/dev/null && alias cat="bat"
command -v rg &>/dev/null && alias grep="rg"
```

### Shell Functions

```bash
# ~/.config/zsh/functions.zsh

# Create directory and cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Extract any archive
extract() {
    case "$1" in
        *.tar.bz2) tar xjf "$1" ;;
        *.tar.gz)  tar xzf "$1" ;;
        *.tar.xz)  tar xJf "$1" ;;
        *.zip)     unzip "$1" ;;
        *.gz)      gunzip "$1" ;;
        *)         echo "Unknown archive: $1" ;;
    esac
}

# Quick dotfiles commit
dotcommit() {
    config add -u
    config commit -m "${1:-Update dotfiles}"
    config push
}
```

## Git Configuration

### XDG-Compliant Gitconfig

```gitconfig
# ~/.config/git/config

[user]
    name = Your Name
    email = your@email.com

[core]
    editor = nvim
    excludesfile = ~/.config/git/ignore
    autocrlf = input
    pager = delta

[init]
    defaultBranch = main

[pull]
    rebase = true

[push]
    default = current
    autoSetupRemote = true

[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --decorate

[diff]
    colorMoved = default

[merge]
    conflictstyle = diff3

# Include machine-specific overrides
[include]
    path = ~/.config/git/config.local
```

### Global Gitignore

```gitignore
# ~/.config/git/ignore

# OS
.DS_Store
Thumbs.db

# Editors
*.swp
*.swo
.idea/
.vscode/
*.sublime-*

# Environment
.env
.env.local
.envrc

# Dependencies
node_modules/
vendor/

# Build
dist/
build/
*.log
```

## Environment Management

### XDG Exports

```bash
# ~/.config/zsh/.zshenv (sourced from ~/.zshenv)

# XDG shims for non-compliant apps
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

# PATH
export PATH="$CARGO_HOME/bin:$GOPATH/bin:$HOME/.local/bin:$PATH"
```

### Secrets Pattern

```bash
# Use direnv for runtime injection
# ~/.config/project/.envrc

export API_KEY=$(op read "op://Private/API/key")
export DATABASE_URL=$(op read "op://Private/DB/url")
```

## macOS Defaults

```bash
#!/usr/bin/env bash
# ~/.config/macos/defaults.sh

# Finder: show hidden files
defaults write com.apple.finder AppleShowAllFiles -bool true

# Dock: auto-hide
defaults write com.apple.dock autohide -bool true

# Keyboard: fast key repeat
defaults write NSGlobalDomain KeyRepeat -int 1
defaults write NSGlobalDomain InitialKeyRepeat -int 10

# Screenshots: save to ~/Screenshots
mkdir -p "$HOME/Screenshots"
defaults write com.apple.screencapture location -string "$HOME/Screenshots"

# Restart affected apps
killall Finder Dock
```

## Bootstrap Script

```bash
#!/usr/bin/env bash
# ~/.config/scripts/bootstrap.sh

set -euo pipefail

DOTFILES_REPO="git@github.com:username/dotfiles.git"

echo "Creating XDG directories..."
mkdir -p ~/.config ~/.local/share ~/.local/state ~/.cache

echo "Cloning dotfiles..."
git clone --bare "$DOTFILES_REPO" "$HOME/.cfg"

alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

echo "Checking out..."
config checkout || {
    echo "Backing up existing files..."
    mkdir -p ~/.dotfiles-backup
    config checkout 2>&1 | grep -E "^\s+" | awk '{print $1}' | \
        xargs -I{} mv {} ~/.dotfiles-backup/
    config checkout
}

config config --local status.showUntrackedFiles no

echo "Done! Restart your shell."
```

## What to Track vs Ignore

### Track (Version Control)

- Shell configurations (`.zshrc`, aliases, functions)
- Editor settings (`nvim/init.lua`, `settings.json`)
- Git configuration
- Tool configs (tmux, starship, etc.)
- SSH config (NOT keys)
- Setup scripts

### Ignore (Never Commit)

- Private keys (`id_rsa`, `id_ed25519`)
- API keys and tokens
- Credentials files
- `.local` machine-specific overrides
- Generated files (`.zwc`, `.zcompdump`)
- Cache directories

### .gitignore for Dotfiles Repo

```gitignore
# ~/.gitignore

# Ignore everything by default (opt-in tracking)
*

# Track XDG config
!.zshenv
!.gitignore
!.config/
!.config/**

# Exclude secrets and generated files
.config/ssh/id_*
.config/aws/credentials
.config/**/*.local
*.zwc
.zcompdump*
```

## Bare Repo Quick Reference

```bash
# Status
config status

# Add file
config add ~/.config/nvim/init.lua

# Commit
config commit -m "Update neovim config"

# Push
config push

# Pull
config pull

# See what's tracked
config ls-files
```
