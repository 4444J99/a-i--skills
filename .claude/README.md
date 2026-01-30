# Claude Code Skills

Claude Code can load skills from `.claude/skills` (top-level) or `.claude/skills-document` (document set).

Regenerate links after adding/removing skills:

```bash
python3 scripts/refresh_skill_collections.py
```

Use `--mode symlink` if you prefer symlinks instead of copies.
