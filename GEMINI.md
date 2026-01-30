# Agent Skills Repository

## Project Overview

This repository hosts a collection of "skills" for AI agents (specifically Claude, Codex, and Gemini CLI). A skill is a self-contained directory containing a `SKILL.md` file with instructions, along with any necessary scripts, templates, or assets. These skills allow agents to perform specialized tasks ranging from creative writing and art generation to technical documentation and code analysis.

The repository includes:
*   **Example Skills:** A wide variety of general-purpose skills in the root directory.
*   **Document Skills:** A specialized set of skills for handling complex file formats (PDF, DOCX, PPTX, XLSX) located in `document-skills/`.
*   **Integration Support:** generated directories and configuration files to support loading these skills into Claude Code, Codex, and Gemini CLI.

## Directory Structure

*   `skills/`: Generated directory containing symlinks or copies of all active example skills.
*   `document-skills/`: Contains the source for document handling skills (`docx`, `pdf`, `pptx`, `xlsx`).
*   `collections/`: Text files listing the paths to all skills in each collection.
*   `scripts/`: Python scripts for repository maintenance (validation, refreshing lists, releasing).
*   `extensions/gemini/`: Gemini CLI extension configurations.
*   `.claude/`, `.codex/`: Generated configurations for their respective agents.
*   `SKILL.md`: The entry point for any skill. Every skill directory (e.g., `skill-creator/`) MUST have one.

## Usage

### 1. Installation

**For Gemini CLI:**
To install the example skills collection:
```bash
gemini extensions install ./extensions/gemini/example-skills
```
To install the document skills collection:
```bash
gemini extensions install ./extensions/gemini/document-skills
```

**For Claude Code:**
```bash
/plugin marketplace add anthropics/skills
/plugin install example-skills@anthropic-agent-skills
```

### 2. Creating a New Skill

1.  Create a new directory in the root (use kebab-case, e.g., `my-new-skill`).
2.  Create a `SKILL.md` file inside it.
3.  Add the required YAML frontmatter to `SKILL.md`:
    ```markdown
    ---
    name: my-new-skill
    description: A concise description of what the skill does.
    ---
    
    # My New Skill
    
    [Detailed instructions for the agent go here]
    ```
4.  (Optional) Add scripts to a `scripts/` subdirectory within your skill folder.

## Development & Maintenance

This project uses Python scripts for management. There is no central build step, but you must run maintenance scripts after adding or modifying skills.

### Key Commands

**Refresh Collections:**
Updates the generated link directories and collection lists. Run this after adding/removing a skill.
```bash
python3 scripts/refresh_skill_collections.py
```
*   Use `--mode symlink` to use symlinks instead of copying files (useful for local dev).

**Validate Skills:**
Checks that skills follow the required format (valid YAML frontmatter, naming conventions, etc.).
```bash
# Validate example skills
python3 scripts/validate_skills.py --collection example --unique

# Validate document skills
python3 scripts/validate_skills.py --collection document --unique
```

**Validate Generated Directories:**
Ensures that the generated directories are in sync with the source skills.
```bash
python3 scripts/validate_generated_dirs.py
```

## Conventions

*   **Naming:** Skill directories and their `name` in frontmatter must be lowercase kebab-case (e.g., `algorithmic-art`).
*   **Self-Contained:** Each skill should be self-contained. Dependencies should be minimal or clearly documented.
*   **Maintenance:** Generated directories (`skills/`, `.codex/`, etc.) are committed to the repo. Always run `refresh_skill_collections.py` before submitting a PR.
