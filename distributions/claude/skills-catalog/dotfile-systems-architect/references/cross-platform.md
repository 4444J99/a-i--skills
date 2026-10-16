# Cross-Platform Compatibility

A robust dotfiles setup often needs to span multiple operating systems. This introduces path inconsistencies that require careful handling.

## The Challenge

Each platform has different conventions:

| Platform | Config Location | User Data | Notes |
|----------|-----------------|-----------|-------|
| Linux | `~/.config` (XDG) | `~/.local/share` | Most XDG-compliant |
| macOS | `~/Library/...` | `~/Library/...` | GUI apps ignore XDG |
| Windows | `%APPDATA%` | `%LOCALAPPDATA%` | Different path separators |
| WSL | `~/.config` | `~/.local/share` | Linux inside Windows |

## macOS ~/Library Challenge

macOS GUI applications enforce the `~/Library` structure. While CLI tools are increasingly XDG-compliant, system apps are not.

### Protected Directories

These directories are relied upon by macOS and cannot be removed:
- `~/Desktop`
- `~/Documents`
- `~/Downloads`
- `~/Library`
- `~/Movies`
- `~/Music`
- `~/Pictures`
- `~/Public`

**Pragmatic approach:** Accept these as the "base system" and focus on keeping everything else minimal.

### Symlink Strategy for GUI Apps

Use your XDG repo as the source of truth, symlink to macOS locations:

```bash
#!/usr/bin/env bash
# setup-macos.sh

if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "This script is for macOS only"
    exit 1
fi

# VS Code
ln -sf "$XDG_CONFIG_HOME/vscode/settings.json" \
       "$HOME/Library/Application Support/Code/User/settings.json"

# Claude Desktop
mkdir -p "$HOME/Library/Application Support/Claude"
ln -sf "$XDG_CONFIG_HOME/claude/claude_desktop_config.json" \
       "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Karabiner Elements
ln -sf "$XDG_CONFIG_HOME/karabiner" \
       "$HOME/.config/karabiner"

# Rectangle (window manager)
mkdir -p "$HOME/Library/Application Support/Rectangle"
ln -sf "$XDG_CONFIG_HOME/rectangle/RectangleConfig.json" \
       "$HOME/Library/Application Support/Rectangle/RectangleConfig.json"
```

### Hiding macOS Directories

You can hide directories from Finder (not delete them):

```bash
chflags hidden ~/Desktop
chflags hidden ~/Public
```

**Warning:** This may confuse you when looking for files. Use sparingly.

---

## Linux: The XDG Native

Linux (especially GNOME/KDE environments) has the best XDG support.

### Relocating Desktop/Downloads

Use `~/.config/user-dirs.dirs`:

```bash
# ~/.config/user-dirs.dirs
XDG_DESKTOP_DIR="$HOME/.local/share/Desktop"
XDG_DOWNLOAD_DIR="$HOME/tmp/downloads"
XDG_DOCUMENTS_DIR="$HOME/docs"
XDG_MUSIC_DIR="$HOME/media/music"
XDG_PICTURES_DIR="$HOME/media/pictures"
XDG_VIDEOS_DIR="$HOME/media/videos"
```

Apply changes:

```bash
xdg-user-dirs-update
```

---

## Windows and WSL

### WSL (Windows Subsystem for Linux)

WSL is essentially a Linux instance. Manage it as an independent Linux node:

- Use standard XDG paths
- Keep configs separate from Windows
- Can access Windows filesystem at `/mnt/c/` but don't mix configs

### Native Windows

PowerShell and Windows Terminal use `%APPDATA%`:

```
%APPDATA%\
├── Code\           # VS Code
├── npm\            # npm global
└── ...

%LOCALAPPDATA%\
├── nvim\           # Neovim
└── ...
```

### Cross-Platform with Single Repo

If managing both Windows and Unix from one repo, **Chezmoi is strongly recommended** over the Bare Repo method.

Chezmoi handles:
- Line-ending conversion (CRLF vs LF)
- Path separators (`\` vs `/`)
- Platform-specific templating

---

## Chezmoi: When It's the Better Choice

For heterogeneous environments (macOS + Linux + Windows), Chezmoi offers native templating:

### Template Example

```
# ~/.local/share/chezmoi/dot_gitconfig.tmpl

[user]
    name = {{ .name }}
    email = {{ .email }}

[core]
{{- if eq .chezmoi.os "darwin" }}
    editor = /usr/local/bin/nvim
{{- else if eq .chezmoi.os "linux" }}
    editor = /usr/bin/nvim
{{- else if eq .chezmoi.os "windows" }}
    editor = "C:\\Program Files\\Neovim\\bin\\nvim.exe"
{{- end }}
```

### Platform-Specific Files

```
~/.local/share/chezmoi/
├── .chezmoiignore
├── dot_zshrc                    # All platforms
├── dot_zshrc.tmpl               # Templated version
├── private_dot_ssh/
│   └── config.tmpl
├── .chezmoiignore_darwin        # macOS-specific ignores
└── .chezmoiignore_linux         # Linux-specific ignores
```

---

## Conditional Logic in Shell

If sticking with Bare Repo, use shell conditionals:

```bash
# ~/.config/zsh/.zshrc

# OS Detection
case "$(uname -s)" in
    Darwin)
        export BROWSER="open"
        alias ls="ls -G"
        # Homebrew paths
        eval "$(/opt/homebrew/bin/brew shellenv)"
        ;;
    Linux)
        export BROWSER="xdg-open"
        alias ls="ls --color=auto"
        ;;
esac

# Machine-specific
if [[ -f "$ZDOTDIR/.zshrc.local" ]]; then
    source "$ZDOTDIR/.zshrc.local"
fi
```

### Platform-Specific Symlinks

```bash
#!/usr/bin/env bash
# setup.sh - Cross-platform setup

set -euo pipefail

XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"

case "$(uname -s)" in
    Darwin)
        # macOS-specific symlinks
        ln -sf "$XDG_CONFIG_HOME/vscode/settings.json" \
               "$HOME/Library/Application Support/Code/User/settings.json"
        ;;
    Linux)
        # Linux: VS Code respects XDG
        mkdir -p "$XDG_CONFIG_HOME/Code/User"
        ln -sf "$XDG_CONFIG_HOME/vscode/settings.json" \
               "$XDG_CONFIG_HOME/Code/User/settings.json"
        ;;
esac
```

---

## Git Branching for Platforms

Alternative to templating: use branches.

```bash
# Main branch: common configs
config checkout main

# Platform branches
config checkout -b macos
# Make macOS-specific changes
config commit -m "macOS specific configs"

config checkout -b linux
# Make Linux-specific changes
config commit -m "Linux specific configs"

# On a new machine
config checkout macos  # or linux
```

**Cons:** Harder to sync common changes across branches.

---

## Recommended Approach by Scenario

| Scenario | Recommended Approach |
|----------|---------------------|
| Single platform (macOS only) | Bare Git Repo |
| macOS + Linux (similar) | Bare Git Repo + shell conditionals |
| macOS + Linux + Windows | Chezmoi |
| Team/enterprise fleet | Chezmoi or Ansible |
| Maximum simplicity | GNU Stow + platform scripts |

---

## Common Path Mappings

| Application | macOS | Linux |
|-------------|-------|-------|
| VS Code Settings | `~/Library/Application Support/Code/User/` | `~/.config/Code/User/` |
| Claude Desktop | `~/Library/Application Support/Claude/` | `~/.config/claude/` |
| Karabiner | `~/.config/karabiner/` | N/A |
| Rectangle | `~/Library/Application Support/Rectangle/` | N/A |
| Firefox | `~/Library/Application Support/Firefox/` | `~/.mozilla/firefox/` |
| Chrome | `~/Library/Application Support/Google/Chrome/` | `~/.config/google-chrome/` |

---

## Testing Cross-Platform Configs

Before deploying to a new platform:

1. **Use a VM or container** to test
2. **Check for hardcoded paths** in your configs
3. **Verify symlinks work** (Windows has different symlink semantics)
4. **Test shell scripts** with `shellcheck`

```bash
# Find hardcoded home paths
grep -r "/Users/" ~/.config
grep -r "/home/" ~/.config

# Check for platform assumptions
grep -r "Darwin\|Linux" ~/.config
```
