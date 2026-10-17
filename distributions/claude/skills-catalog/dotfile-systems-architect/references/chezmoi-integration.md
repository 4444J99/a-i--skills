# Chezmoi Integration

Chezmoi is an enterprise-grade dotfiles manager that fully supports the XDG philosophy. Unlike the Bare Git approach, Chezmoi generates files from templates, enabling powerful cross-platform support and native secrets management.

## Why Choose Chezmoi

| Scenario | Bare Git | Chezmoi |
|----------|----------|---------|
| Single platform | ✓ Simpler | Works fine |
| macOS + Linux | Shell conditionals | ✓ Native templating |
| macOS + Linux + Windows | Difficult | ✓ Superior |
| Password manager secrets | Requires direnv setup | ✓ Native integration |
| Machine-specific configs | `.local` files | ✓ Template variables |

**Choose Chezmoi when:**
- Managing multiple machines with different OSes
- Needing native 1Password/Bitwarden/LastPass integration
- Wanting declarative, reproducible configuration
- Preferring a single tool over shell scripts + git-crypt + direnv

## Installation

```bash
# macOS
brew install chezmoi

# Linux
sh -c "$(curl -fsLS get.chezmoi.io)"

# Initialize (creates ~/.local/share/chezmoi)
chezmoi init
```

Chezmoi stores its source in `~/.local/share/chezmoi` by default—already XDG-compliant.

## XDG-Compliant Directory Structure

```
~/.local/share/chezmoi/          # Chezmoi source (XDG_DATA_HOME)
├── .chezmoi.toml.tmpl           # Config template
├── .chezmoiignore               # Files to ignore
├── dot_zshenv                   # → ~/.zshenv
├── dot_config/                  # → ~/.config/
│   ├── zsh/
│   │   ├── dot_zshrc
│   │   └── aliases.zsh
│   ├── git/
│   │   └── config
│   ├── nvim/
│   │   └── init.lua
│   └── private_ssh/             # private_ prefix for permissions
│       └── config
└── private_dot_config/          # Alternative: entire .config as private
    └── aws/
        └── config
```

### Naming Conventions

| Prefix | Effect |
|--------|--------|
| `dot_` | Creates file/dir starting with `.` |
| `private_` | Sets permissions to `0600`/`0700` |
| `executable_` | Sets executable bit |
| `readonly_` | Sets read-only |
| `.tmpl` suffix | Process as template |

## The Bootstrap: ~/.zshenv

Create the XDG bootstrap file:

```bash
chezmoi add ~/.zshenv
```

Or create from scratch:

```bash
# ~/.local/share/chezmoi/dot_zshenv.tmpl

# XDG Base Directory specification
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

# Redirect Zsh to XDG location
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"

# Source the real zshenv
[[ -f "$ZDOTDIR/.zshenv" ]] && source "$ZDOTDIR/.zshenv"
```

## Cross-Platform Templating

### Platform Detection

Chezmoi provides built-in variables:

```
{{ .chezmoi.os }}        # "darwin", "linux", "windows"
{{ .chezmoi.arch }}      # "amd64", "arm64"
{{ .chezmoi.hostname }}  # Machine hostname
{{ .chezmoi.username }}  # Current user
```

### Platform-Specific Paths

```bash
# ~/.local/share/chezmoi/dot_config/zsh/dot_zshrc.tmpl

# XDG shims for non-compliant apps
export GIT_CONFIG_GLOBAL="$XDG_CONFIG_HOME/git/config"
export KUBECONFIG="$XDG_CONFIG_HOME/kube/config"
export GNUPGHOME="$XDG_DATA_HOME/gnupg"

{{- if eq .chezmoi.os "darwin" }}
# macOS-specific
export BROWSER="open"
eval "$(/opt/homebrew/bin/brew shellenv)"
{{- else if eq .chezmoi.os "linux" }}
# Linux-specific
export BROWSER="xdg-open"
{{- end }}
```

### Conditional File Inclusion

```
# ~/.local/share/chezmoi/.chezmoiignore

# Ignore macOS files on Linux
{{ if ne .chezmoi.os "darwin" }}
dot_config/karabiner/
dot_config/rectangle/
{{ end }}

# Ignore Linux files on macOS
{{ if ne .chezmoi.os "linux" }}
dot_config/i3/
dot_config/polybar/
{{ end }}
```

## Handling Hostile Apps

### VS Code

VS Code settings live in different places per OS. Use templates:

```bash
# ~/.local/share/chezmoi/dot_config/vscode/settings.json
# (Your actual settings - not a template)
```

Then use a script to symlink:

```bash
# ~/.local/share/chezmoi/run_onchange_vscode-symlink.sh.tmpl

#!/usr/bin/env bash
set -euo pipefail

{{- if eq .chezmoi.os "darwin" }}
CODE_USER="$HOME/Library/Application Support/Code/User"
{{- else if eq .chezmoi.os "linux" }}
CODE_USER="${XDG_CONFIG_HOME:-$HOME/.config}/Code/User"
{{- end }}

mkdir -p "$CODE_USER"
ln -sf "$XDG_CONFIG_HOME/vscode/settings.json" "$CODE_USER/settings.json"
ln -sf "$XDG_CONFIG_HOME/vscode/keybindings.json" "$CODE_USER/keybindings.json"
```

### Claude Desktop

```bash
# ~/.local/share/chezmoi/run_onchange_claude-symlink.sh.tmpl

#!/usr/bin/env bash
set -euo pipefail

{{- if eq .chezmoi.os "darwin" }}
CLAUDE_DIR="$HOME/Library/Application Support/Claude"
{{- else if eq .chezmoi.os "linux" }}
CLAUDE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/claude"
{{- end }}

mkdir -p "$CLAUDE_DIR"
ln -sf "$XDG_CONFIG_HOME/claude/claude_desktop_config.json" \
       "$CLAUDE_DIR/claude_desktop_config.json"
```

### Git Configuration

```gitconfig
# ~/.local/share/chezmoi/dot_config/git/config.tmpl

[user]
    name = {{ .name }}
    email = {{ .email }}

[core]
    editor = nvim
    excludesfile = ~/.config/git/ignore
{{- if eq .chezmoi.os "darwin" }}
    pager = delta
{{- end }}

[init]
    defaultBranch = main
```

## Secrets Management

Chezmoi has native integration with password managers—no git-crypt needed.

### 1Password Integration

```bash
# Enable in ~/.config/chezmoi/chezmoi.toml
[onepassword]
    command = "op"
```

Use in templates:

```bash
# ~/.local/share/chezmoi/dot_config/aws/credentials.tmpl

[default]
aws_access_key_id = {{ onepasswordRead "op://Private/AWS/access-key" }}
aws_secret_access_key = {{ onepasswordRead "op://Private/AWS/secret-key" }}
```

### Bitwarden Integration

```bash
# ~/.config/chezmoi/chezmoi.toml
[bitwarden]
    command = "bw"
```

```bash
# Template usage
{{ (bitwarden "item" "my-api-key").login.password }}
```

### LastPass Integration

```bash
{{ (lastpassRaw "my-secret").password }}
```

### Age Encryption (Local)

For secrets without a password manager:

```bash
# Generate key
age-keygen -o ~/.config/chezmoi/key.txt

# Configure chezmoi
chezmoi init --config-format=toml
```

```toml
# ~/.config/chezmoi/chezmoi.toml
encryption = "age"
[age]
    identity = "~/.config/chezmoi/key.txt"
    recipient = "age1xxxxxxxxx..."
```

```bash
# Add encrypted file
chezmoi add --encrypt ~/.config/ssh/id_ed25519
```

## Machine-Specific Configuration

### Using chezmoi.toml

```toml
# ~/.config/chezmoi/chezmoi.toml

[data]
    name = "Your Name"
    email = "your@email.com"

[data.work]
    email = "your@work.com"
```

### Prompting for Data

```toml
# ~/.local/share/chezmoi/.chezmoi.toml.tmpl

{{- $email := promptStringOnce . "email" "Email address" -}}
{{- $isWork := promptBoolOnce . "isWork" "Is this a work machine" -}}

[data]
    email = {{ $email | quote }}
    isWork = {{ $isWork }}
```

### Using in Templates

```bash
# dot_config/git/config.tmpl

[user]
{{- if .isWork }}
    email = {{ .work.email }}
{{- else }}
    email = {{ .email }}
{{- end }}
```

## Migration from Bare Git

If you have an existing Bare Git setup:

```bash
# 1. Initialize chezmoi
chezmoi init

# 2. Add existing files
chezmoi add ~/.zshenv
chezmoi add ~/.config/zsh
chezmoi add ~/.config/git
chezmoi add ~/.config/nvim

# 3. Convert to templates where needed
chezmoi edit ~/.config/zsh/.zshrc
# Add {{ }} templating for platform-specific parts

# 4. Test
chezmoi diff
chezmoi apply --dry-run

# 5. Push to GitHub
chezmoi cd
git remote add origin git@github.com:username/dotfiles.git
git push -u origin main
```

## Daily Workflow

```bash
# Check what would change
chezmoi diff

# Apply changes
chezmoi apply

# Add a new file
chezmoi add ~/.config/starship.toml

# Edit a managed file
chezmoi edit ~/.config/zsh/.zshrc

# Re-apply after editing
chezmoi apply

# Update from remote
chezmoi update

# Push changes
chezmoi cd && git add -A && git commit -m "Update" && git push
```

## New Machine Setup

```bash
# One-liner bootstrap
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply username

# Or step by step
chezmoi init https://github.com/username/dotfiles.git
chezmoi diff
chezmoi apply
```

## Directory Structure Comparison

| Bare Git | Chezmoi |
|----------|---------|
| `~/.cfg/` (bare repo) | `~/.local/share/chezmoi/` (source) |
| Files directly in `~` | Generated/copied to `~` |
| `config` alias | `chezmoi` command |
| `.gitignore` for opt-in | `.chezmoiignore` for opt-out |
| Shell conditionals | Go templates |
| git-crypt for secrets | Native password manager |

## Chezmoi with XDG: Best Practices

1. **Keep `~/.zshenv` minimal** - Just XDG exports and ZDOTDIR redirect
2. **Store everything in `~/.config`** - Use `dot_config/` in source
3. **Use `private_` prefix** for sensitive configs (ssh, gnupg)
4. **Template platform differences** - Don't maintain branches
5. **Use password manager integration** - Avoid storing secrets in repo
6. **Run scripts for hostile apps** - `run_` scripts for symlinks

## Further Reading

- [Chezmoi documentation](https://www.chezmoi.io/)
- [Chezmoi comparison table](https://www.chezmoi.io/comparison-table/)
- [Template functions](https://www.chezmoi.io/reference/templates/functions/)
