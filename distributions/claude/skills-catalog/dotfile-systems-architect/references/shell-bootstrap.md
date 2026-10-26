# Shell Bootstrap Strategy

The shell is the entry point for the user session. It initializes the XDG environment variables that all subsequent applications rely on. Therefore, cleaning the shell configuration is the first step in achieving a Minimal Root.

## The Zsh ZDOTDIR Mechanism

By default, Zsh looks for its configuration files (`.zshrc`, `.zprofile`, `.zlogin`, `.zshenv`) in `$HOME`. This contributes four files to root clutter.

Zsh supports the `ZDOTDIR` environment variable. When set, Zsh looks for configuration files in that directory instead of `$HOME`.

**The Catch:** Zsh must know where `ZDOTDIR` is *before* it can load config from it. The only file Zsh reads from `$HOME` unconditionally is `~/.zshenv`.

## The Minimal ~/.zshenv Strategy

Place a single file in root that acts as the bootstrapper:

```bash
# ~/.zshenv
# This is the ONLY dotfile in the home directory root

# 1. Define XDG Base Directory variables
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

# 2. Redirect Zsh configuration to XDG location
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"

# 3. Source the 'real' zshenv if it exists in the new location
if [[ -f "$ZDOTDIR/.zshenv" ]]; then
    source "$ZDOTDIR/.zshenv"
fi
```

## Result

- Root directory contains only `.zshenv`
- All other Zsh files move to `~/.config/zsh/`:
  - `.zshrc`
  - `.zprofile`
  - `.zlogin`
  - `.zlogout`

## Moving .zsh_history

Shell history needs explicit reconfiguration. Add to `~/.config/zsh/.zshrc`:

```bash
# Move history to STATE directory (not CONFIG - history is state data)
HISTFILE="$XDG_STATE_HOME/zsh/history"
HISTSIZE=50000
SAVEHIST=50000

# Ensure directory exists
[[ -d "${HISTFILE:h}" ]] || mkdir -p "${HISTFILE:h}"
```

## Complete ~/.config/zsh/.zshrc Template

```bash
# ~/.config/zsh/.zshrc

# History configuration
HISTFILE="$XDG_STATE_HOME/zsh/history"
HISTSIZE=50000
SAVEHIST=50000
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY

# Create history directory if needed
[[ -d "${HISTFILE:h}" ]] || mkdir -p "${HISTFILE:h}"

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

# The bare repo alias
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# Modular config loading
for config_file in "$ZDOTDIR"/{aliases,functions,completions}.zsh(N); do
    source "$config_file"
done

# Local overrides (machine-specific, not tracked)
[[ -f "$ZDOTDIR/.zshrc.local" ]] && source "$ZDOTDIR/.zshrc.local"
```

## Bash Compatibility

Bash is less flexible than Zsh. It hardcodes lookups for `~/.bashrc` and `~/.bash_profile`.

### Strategy: Shim Files

Create thin shim files in root that source the XDG location:

```bash
# ~/.bashrc (shim)
[[ -f "$HOME/.config/bash/bashrc" ]] && . "$HOME/.config/bash/bashrc"
```

```bash
# ~/.bash_profile (shim)
[[ -f "$HOME/.config/bash/bash_profile" ]] && . "$HOME/.config/bash/bash_profile"
```

### Actual Config Location

Place the real configuration in `~/.config/bash/`:

```bash
~/.config/bash/
├── bashrc           # Interactive shell config
├── bash_profile     # Login shell config
├── aliases          # Bash aliases
└── functions        # Bash functions
```

## Directory Structure After Setup

```
~/
├── .zshenv          # Only root dotfile (bootstrap)
├── .bashrc          # Shim (optional, for Bash compat)
├── .bash_profile    # Shim (optional)
│
├── .config/
│   ├── zsh/
│   │   ├── .zshrc
│   │   ├── .zprofile
│   │   ├── aliases.zsh
│   │   └── functions.zsh
│   ├── bash/
│   │   ├── bashrc
│   │   └── bash_profile
│   └── git/
│       └── config
│
├── .local/
│   ├── share/       # XDG_DATA_HOME
│   └── state/
│       └── zsh/
│           └── history
│
└── .cache/          # XDG_CACHE_HOME
```

## Verifying the Setup

After configuring, verify with:

```bash
# Should show minimal dotfiles
ls -a ~ | grep '^\.'

# Expected: . .. .cache .config .local .zshenv (maybe .bashrc .bash_profile)

# Verify ZDOTDIR
echo $ZDOTDIR
# Expected: /Users/username/.config/zsh

# Verify history location
echo $HISTFILE
# Expected: /Users/username/.local/state/zsh/history
```

## Troubleshooting

### Zsh Not Finding Config

Ensure `~/.zshenv` has correct permissions:

```bash
chmod 644 ~/.zshenv
```

### Oh-My-Zsh Compatibility

If using Oh-My-Zsh, set `ZSH` variable in `.zshenv`:

```bash
export ZSH="$XDG_DATA_HOME/oh-my-zsh"
```

Then install to that location:

```bash
ZSH="$XDG_DATA_HOME/oh-my-zsh" sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### PATH Not Set Correctly

Remember that `.zshenv` is sourced for all shell types (interactive, non-interactive, login, non-login). Put PATH modifications there or in `.zprofile`.
