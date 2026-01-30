# Gemini CLI Extensions

This directory contains Gemini CLI extensions that expose the skills in this repo.

Install locally:

```bash
# Example skills
gemini extensions install ./extensions/gemini/example-skills

# Document skills
gemini extensions install ./extensions/gemini/document-skills
```

Regenerate links after adding/removing skills:

```bash
python3 scripts/refresh_skill_collections.py
```
Use `--mode symlink` if you prefer symlinks instead of copies.
