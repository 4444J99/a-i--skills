# Dotfile Patterns Reference

Patterns for organizing and managing system configuration files.

## Directory Structure

### Recommended Layout

```
~/.dotfiles/
├── README.md           # Documentation
├── install.sh          # Bootstrap script
├── Makefile            # Alternative to shell script
│
├── shell/
│   ├── zshrc           # Zsh configuration
│   ├── bashrc          # Bash configuration
│   ├── aliases         # Shell aliases
│   ├── functions       # Shell functions
│   └── exports         # Environment variables
│
├── git/
│   ├── gitconfig       # Git configuration
│   ├── gitignore       # Global gitignore
│   └── gitmessage      # Commit template
│
├── editor/
│   ├── vimrc           # Vim configuration
│   └── nvim/           # Neovim config directory
│
├── terminal/
│   ├── tmux.conf       # Tmux configuration
│   └── alacritty.yml   # Terminal emulator
│
└── macos/
    └── defaults.sh     # macOS preferences
```

## Symlink Strategies

### Manual Symlinks

```bash
ln -sf ~/.dotfiles/shell/zshrc ~/.zshrc
ln -sf ~/.dotfiles/git/gitconfig ~/.gitconfig
```

### Stow (Recommended)

```bash
# Directory structure for stow
~/.dotfiles/
├── zsh/
│   └── .zshrc          # Will symlink to ~/.zshrc
├── git/
│   └── .gitconfig      # Will symlink to ~/.gitconfig
└── nvim/
    └── .config/
        └── nvim/       # Will symlink to ~/.config/nvim/

# Usage
cd ~/.dotfiles
stow zsh git nvim
```

### Install Script

```bash
#!/usr/bin/env bash
set -euo pipefail

DOTFILES="$HOME/.dotfiles"

link_file() {
  local src="$1"
  local dst="$2"

  if [ -f "$dst" ] || [ -L "$dst" ]; then
    mv "$dst" "$dst.backup"
  fi

  ln -sf "$src" "$dst"
  echo "Linked $src → $dst"
}

# Link configurations
link_file "$DOTFILES/shell/zshrc" "$HOME/.zshrc"
link_file "$DOTFILES/git/gitconfig" "$HOME/.gitconfig"
link_file "$DOTFILES/git/gitignore" "$HOME/.gitignore"
```

## Shell Configuration

### Zsh Modular Setup

```bash
# ~/.zshrc

# Path to dotfiles
export DOTFILES="$HOME/.dotfiles"

# Load modular configs
for file in $DOTFILES/shell/{exports,aliases,functions}; do
  [ -r "$file" ] && source "$file"
done

# Local overrides (not tracked)
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"
```

### Common Aliases

```bash
# ~/.dotfiles/shell/aliases

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

# Safety
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"

# Modern replacements (if installed)
command -v eza &>/dev/null && alias ls="eza"
command -v bat &>/dev/null && alias cat="bat"
command -v rg &>/dev/null && alias grep="rg"
```

## Git Configuration

### Gitconfig Template

```gitconfig
[user]
    name = Your Name
    email = your@email.com

[core]
    editor = nvim
    excludesfile = ~/.gitignore
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

# Include local overrides
[include]
    path = ~/.gitconfig.local
```

### Global Gitignore

```gitignore
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

# Dependencies
node_modules/
vendor/

# Build
dist/
build/
*.log
```

## Environment Management

### Secrets Pattern

```bash
# ~/.dotfiles/shell/exports
export EDITOR="nvim"
export LANG="en_US.UTF-8"

# ~/.secrets (NOT tracked in git)
export API_KEY="secret-value" # allow-secret
export DATABASE_URL="postgres://..."

# In .zshrc
[ -f "$HOME/.secrets" ] && source "$HOME/.secrets"
```

### .env Pattern

```bash
# Project-specific .env files
# Use direnv for automatic loading

# ~/.envrc
export PROJECT_ENV="development"

# Enable with: direnv allow
```

## macOS Defaults

```bash
#!/usr/bin/env bash
# ~/.dotfiles/macos/defaults.sh

# Finder: show hidden files
defaults write com.apple.finder AppleShowAllFiles -bool true

# Dock: auto-hide
defaults write com.apple.dock autohide -bool true

# Keyboard: fast key repeat
defaults write NSGlobalDomain KeyRepeat -int 1
defaults write NSGlobalDomain InitialKeyRepeat -int 10

# Screenshots: save to ~/Screenshots
defaults write com.apple.screencapture location -string "$HOME/Screenshots"

# Restart affected apps
killall Finder Dock
```

## Bootstrap Checklist

New machine setup order:

1. [ ] Install Xcode Command Line Tools
2. [ ] Install Homebrew
3. [ ] Clone dotfiles repo
4. [ ] Run install script
5. [ ] Install packages (Brewfile)
6. [ ] Set up shell (chsh)
7. [ ] Configure macOS defaults
8. [ ] Restore app preferences
9. [ ] Set up SSH keys
10. [ ] Clone work repositories

## Version Control Tips

### What to Track

- Shell configurations
- Git settings
- Editor configurations
- Terminal settings
- Package lists (Brewfile)

### What NOT to Track

- Secrets, API keys
- Machine-specific settings
- Large binary files
- Generated files

### .gitignore for Dotfiles

```gitignore
# Secrets
*.local
.secrets
.env

# Generated
*.zwc
.zcompdump

# Machine-specific
.gitconfig.local
```
