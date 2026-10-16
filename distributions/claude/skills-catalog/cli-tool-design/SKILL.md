---
name: cli-tool-design
description: Design command-line interfaces with clear argument parsing, subcommands, help text, output formatting, and exit codes. Covers Click, Typer, argparse, and shell completion. Triggers on CLI tool development, argument parsing, or terminal UX design requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - cli
  - command-line
  - argparse
  - click
  - typer
  - terminal
governance_phases: [build]
organ_affinity: [organ-i, organ-vi, organ-vii, meta]
triggers: [user-asks-about-cli-design, project-has-cli-entry-point, context:building-cli-tool, file-type:*cli*]
complements: [python-packaging-patterns, configuration-management, error-handling-logging-patterns]
---

# CLI Tool Design

Build command-line tools that are discoverable, composable, and pleasant to use.

## Design Principles

### The UNIX Philosophy Applied

1. **Do one thing well** — Each command has a clear, singular purpose
2. **Compose through pipes** — Support stdin/stdout for chaining
3. **Fail loudly** — Non-zero exit codes and stderr for errors
4. **Be predictable** — Consistent flags, consistent output format

### Command Structure

```
program [global-options] command [command-options] [arguments]
```

Example:
```bash
organvm --verbose registry update --organ IV a-i--skills
```

## Framework Selection

| Framework | Language | Best For |
|-----------|----------|----------|
| **Typer** | Python | Modern CLIs with type hints, auto-completion |
| **Click** | Python | Complex CLIs, plugins, nested groups |
| **argparse** | Python | Zero-dependency, stdlib-only |
| **clap** | Rust | High-performance, compiled CLIs |
| **cobra** | Go | Go microservice CLIs |

## Building with Typer (Recommended for Python)

### Basic Command

```python
import typer

app = typer.Typer(help="ORGANVM system management CLI")

@app.command()
def status(
    organ: str = typer.Argument(help="Organ number (I-VII or META)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Show the status of an organ's repositories."""
    # Implementation here
```

### Subcommand Groups

```python
app = typer.Typer()
registry_app = typer.Typer(help="Registry operations")
app.add_typer(registry_app, name="registry")

@registry_app.command("update")
def registry_update(
    organ: str = typer.Argument(help="Target organ"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
):
    """Update registry entries for an organ."""
```

### Rich Output Integration

```python
from rich.console import Console
from rich.table import Table

console = Console(stderr=True)  # Status to stderr

def show_repos(repos: list[dict]):
    table = Table(title="Repositories")
    table.add_column("Name", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Tier")
    for repo in repos:
        table.add_row(repo["name"], repo["status"], repo["tier"])
    console.print(table)
```

## Argument Design

### Positional vs Optional

| Use Case | Type | Example |
|----------|------|---------|
| Required input | Positional | `program FILE` |
| Behavior modifier | Flag | `--verbose`, `--dry-run` |
| Configuration | Option | `--output FORMAT` |
| Multiple inputs | Variadic | `program FILE...` |

### Flag Conventions

```
-v, --verbose       Increase output verbosity
-q, --quiet         Suppress non-error output
-n, --dry-run       Show what would happen without doing it
-f, --force         Skip confirmation prompts
-o, --output FILE   Write output to FILE instead of stdout
    --json          Machine-readable JSON output
    --no-color      Disable colored output
```

### Boolean Flags with Negation

```python
@app.command()
def deploy(
    color: bool = typer.Option(True, "--color/--no-color"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive"),
):
```

## Output Design

### Human vs Machine Output

```python
import json
import sys

def output_results(results: list[dict], json_mode: bool = False):
    if json_mode:
        # Machine output to stdout
        json.dump(results, sys.stdout, indent=2)
    else:
        # Human output with formatting
        for r in results:
            console.print(f"[cyan]{r['name']}[/] — {r['status']}")
```

### Progress Indicators

```python
from rich.progress import track

for item in track(items, description="Processing..."):
    process(item)
```

### Stderr vs Stdout

- **stdout**: Data output (pipeable)
- **stderr**: Status messages, progress, errors

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Usage error (bad arguments) |
| 64-78 | BSD sysexits conventions |
| 130 | Interrupted (Ctrl+C) |

```python
import sys

def main():
    try:
        result = run_command()
        if not result.success:
            console.print(f"[red]Error:[/] {result.error}", file=sys.stderr)
            raise SystemExit(1)
    except KeyboardInterrupt:
        raise SystemExit(130)
```

## Configuration Loading

Priority order (highest to lowest):
1. Command-line arguments
2. Environment variables
3. Project-level config file (`.tool.yaml`)
4. User-level config (`~/.config/tool/config.yaml`)
5. System defaults

```python
def get_config(cli_value: str | None = None) -> str:
    return (
        cli_value
        or os.environ.get("TOOL_CONFIG")
        or load_project_config()
        or load_user_config()
        or DEFAULT_VALUE
    )
```

## Shell Completion

### Typer Auto-Completion

```bash
# Generate completion script
my-cli --install-completion

# Or manually
_MY_CLI_COMPLETE=bash_source my-cli > ~/.my-cli-complete.bash
source ~/.my-cli-complete.bash
```

### Custom Completions

```python
def complete_organ(incomplete: str) -> list[str]:
    organs = ["I", "II", "III", "IV", "V", "VI", "VII", "META"]
    return [o for o in organs if o.startswith(incomplete.upper())]

@app.command()
def status(organ: str = typer.Argument(autocompletion=complete_organ)):
    ...
```

## Testing CLIs

```python
from typer.testing import CliRunner

runner = CliRunner()

def test_status_command():
    result = runner.invoke(app, ["status", "IV"])
    assert result.exit_code == 0
    assert "a-i--skills" in result.stdout

def test_invalid_organ():
    result = runner.invoke(app, ["status", "INVALID"])
    assert result.exit_code == 2
```

## Anti-Patterns

- **Requiring interactive input in scripts** — Always support `--yes` / `--no-interactive` flags
- **Mixing data and status on stdout** — Use stderr for progress and status messages
- **Inconsistent flag naming** — Pick a convention and stick to it across all subcommands
- **No help text** — Every command, argument, and option needs a help string
- **Swallowing errors** — Always exit with appropriate non-zero codes on failure
