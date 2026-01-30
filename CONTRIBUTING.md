# Contributing

Thanks for contributing to this skills repository. Each skill is a self-contained folder with a `SKILL.md` entrypoint. Follow the steps below to keep the collections consistent across Claude Code, Codex, and Gemini CLI.

## Add or Update a Skill
1. Create a new folder at the repo root using kebab-case (e.g., `my-new-skill/`).
2. Add `SKILL.md` with YAML frontmatter:
   - `name:` must match the folder name.
   - `description:` short, specific, and task-focused.
3. Put helper scripts in `scripts/` and any supporting material in `references/` or `assets/`.

## Refresh Collections
Run after adding/removing skills:

```bash
python3 scripts/refresh_skill_collections.py
```
Use `--mode symlink` if you prefer symlinks instead of copies.

This regenerates:
- `collections/example-skills.txt`
- `collections/document-skills.txt`
- link directories under `skills/`, `.codex/skills`, `.claude/skills`, and `extensions/gemini/*/skills`
These generated files are committed to the repo. Include the updated outputs in your PRs.

## Validate
Ensure the frontmatter and naming rules are correct:

```bash
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_skills.py --collection document --unique
```

## Commit Guidance
- Use short, imperative subject lines (e.g., "Add prompt for X" or "Update README for Y").
- If a change affects a curated list or install flow, update `README.md`.
- Add third-party attributions to `THIRD_PARTY_NOTICES.md` when you introduce external assets or data.

## Gemini / Codex / Claude Code Notes
- Install only one collection at a time to avoid duplicate skill names (e.g., `docx`, `pdf` exist in both sets).
- Gemini CLI extensions live under `extensions/gemini/` and point to the generated `skills/` links.
- Codex and Claude Code load skills from `.codex/skills` and `.claude/skills` respectively.

## Release Checklist
1. Run refresh + validation:
   ```bash
   python3 scripts/refresh_skill_collections.py
   python3 scripts/validate_skills.py --collection example --unique
   python3 scripts/validate_skills.py --collection document --unique
   ```
2. Update `CHANGELOG.md` with the release summary.
3. Bump versions in:
   - `.claude-plugin/marketplace.json` (`metadata.version`)
   - `extensions/gemini/example-skills/gemini-extension.json`
   - `extensions/gemini/document-skills/gemini-extension.json`
4. Update `README.md` if install steps or collection membership changed.
5. Verify CI passes (`.github/workflows/validate-skills.yml`).
6. Tag and publish, then create a release (prefer `gh release create vX.Y.Z --generate-notes` or attach the changelog section as notes).
