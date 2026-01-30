# Coding Standards Instructions

## Markdown-First Approach

Skills are primarily instructional content, not code. The `SKILL.md` file is the primary artifact.

## Python Script Guidelines

When adding Python scripts to a skill's `scripts/` directory:

### Style

- Follow PEP 8 conventions
- Keep scripts focused and single-purpose
- Make scripts directly executable when appropriate
- Include docstrings for non-trivial functions

### Dependencies

- Document dependencies in comments or a requirements.txt
- Keep dependencies minimal
- Don't assume global package installation

### Example Structure

```python
#!/usr/bin/env python3
"""
Brief description of what this script does.

Usage:
    python3 script_name.py [arguments]
"""

import sys
import os

def main():
    """Main entry point."""
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

### Testing

- Include simple smoke tests when appropriate
- Document test commands in SKILL.md
- Example: `python3 scripts/my_script_test.py`

## Content Guidelines

### Examples in SKILL.md

- Keep examples concise and actionable
- Use ASCII art/content unless the domain requires otherwise
- Show concrete input/output when helpful
- Demonstrate edge cases when relevant

### Code Comments

- Don't over-comment obvious code
- Do comment non-obvious decisions or algorithms
- Explain "why" not "what" when code is clear

## File Organization

### Within a Skill Directory

```
my-skill/
  SKILL.md              # Required: instructions
  scripts/
    helper.py           # Executable helpers
    requirements.txt    # Python dependencies
  references/
    documentation.md    # Supporting docs
    examples/           # Example files
  assets/
    template.txt        # Templates
    config.json         # Configuration
```

### Naming Conventions

- **Directories**: lowercase, hyphen-separated
- **Python files**: lowercase, underscore-separated (snake_case)
- **Markdown files**: UPPERCASE or Title Case
- **Config/data**: lowercase with appropriate extension

## Security Practices

### Never Commit Secrets

❌ **Don't:**
```python
API_KEY = "sk-1234567890abcdef"  # allow-secret
DATABASE_URL = "postgres://user:pass@host/db"  # allow-secret
```

✅ **Do:**
```python
import os
API_KEY = os.environ.get("API_KEY")  # allow-secret
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### Handle Sensitive Data

- Read from environment variables
- Document required env vars in SKILL.md
- Provide clear error messages for missing credentials

## Documentation Standards

### SKILL.md Structure

Organize content logically:

1. **Overview**: What the skill does (1-2 sentences)
2. **Usage**: How agents should use it
3. **Instructions**: Step-by-step guidance
4. **Examples**: Concrete demonstrations
5. **Resources**: Scripts, references, assets
6. **Troubleshooting**: Common issues (if applicable)

### README.md Files

If adding a README to a skill subdirectory:

- Explain what the subdirectory contains
- Document script usage
- List dependencies
- Keep it brief

## Third-Party Content

When adding external assets, code, or data:

1. Verify licensing compatibility
2. Update `THIRD_PARTY_NOTICES.md`
3. Include attribution in the skill
4. Document source URLs

### THIRD_PARTY_NOTICES.md Format

```markdown
## Component Name
- Source: https://example.com/project
- License: MIT
- Copyright: (c) 2024 Author Name
- Used in: skill-name/path/to/file.ext
```
