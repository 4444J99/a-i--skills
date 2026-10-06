# Claude Code Skills

Claude Code can load skills from `.claude/skills`; copy or link `distributions/claude/skills/` there.

Regenerate links after adding/removing skills:

```bash
python3 scripts/refresh_skill_collections.py
```

Use `--mode symlink` if you prefer symlinks instead of copies.
