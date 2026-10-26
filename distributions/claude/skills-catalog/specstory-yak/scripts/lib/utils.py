"""Utility functions for specstory yak shave analyzer."""

import subprocess
from pathlib import Path
from typing import Optional


def find_specstory_path() -> Optional[Path]:
    """Auto-detect .specstory/history path by searching up from cwd."""
    current = Path.cwd()
    for _ in range(10):  # Max 10 levels up
        specstory = current / ".specstory" / "history"
        if specstory.exists():
            return specstory
        if current.parent == current:
            break
        current = current.parent
    return None


def get_git_author(filepath: Path) -> str:
    """Get the git author who committed this file using git blame."""
    try:
        # Get the author of the first line (file creator)
        result = subprocess.run(
            ["git", "blame", "-p", "-L", "1,1", str(filepath)],
            capture_output=True,
            text=True,
            cwd=filepath.parent,
            timeout=5
        )
        if result.returncode == 0:
            # Parse porcelain output for author
            for line in result.stdout.split("\n"):
                if line.startswith("author "):
                    return line[7:].strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    return "unknown"


def detect_platform() -> str:
    """Detect the user's platform for installation instructions."""
    import platform
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "linux":
        # Check for WSL
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    return "wsl"
        except:
            pass
        return "linux"
    return "unknown"


def get_install_instructions() -> str:
    """Return platform-specific installation instructions for SpecStory."""
    platform = detect_platform()

    instructions = """
No .specstory/history directory found.

SpecStory automatically saves your AI coding conversations to .specstory/history/
You need to install SpecStory to start capturing sessions.

"""

    if platform == "macos":
        instructions += """FOR CLAUDE CODE (macOS - Homebrew):
    brew tap specstoryai/tap
    brew update
    brew install specstory
    specstory run claude        # Run Claude Code with auto-save
    specstory sync claude       # Sync existing sessions

"""
    elif platform in ("linux", "wsl"):
        instructions += """FOR CLAUDE CODE (Linux/WSL):
    # Download from: https://github.com/specstoryai/getspecstory/releases
    tar -xzf SpecStoryCLI_Linux_x86_64.tar.gz
    sudo mv specstory /usr/local/bin/
    sudo chmod +x /usr/local/bin/specstory
    specstory run claude        # Run Claude Code with auto-save
    specstory sync claude       # Sync existing sessions

"""
    else:
        instructions += """FOR CLAUDE CODE:
    # macOS: brew tap specstoryai/tap && brew install specstory
    # Linux: Download from https://github.com/specstoryai/getspecstory/releases
    specstory run claude        # Run Claude Code with auto-save
    specstory sync claude       # Sync existing sessions

"""

    instructions += """FOR CURSOR / VS CODE:
    1. Open Cursor or VS Code
    2. Press Ctrl/Cmd+Shift+X (Extensions)
    3. Search "SpecStory" and click Install
    4. Start chatting - sessions auto-save to .specstory/history/

MORE INFO: https://docs.specstory.com/docs/quickstart

TIP: Use --path to analyze a specific .specstory/history location:
    python analyze.py --path /path/to/.specstory/history
"""
    return instructions
