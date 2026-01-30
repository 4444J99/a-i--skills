# Development Workflow Instructions

## No Repo-Wide Build System

This repository does not have a centralized build, test, or lint system. Each skill is independent.

## Common Development Commands

### After Adding/Modifying Skills

**Always run the refresh script:**
```bash
python3 scripts/refresh_skill_collections.py
```

This regenerates:
- Link directories (skills/, .codex/skills, .claude/skills, etc.)
- Collection lists (collections/*.txt)
- Gemini extension bundles

**For local development (optional):**
```bash
python3 scripts/refresh_skill_collections.py --mode symlink
```
Creates symlinks instead of copies for faster iteration.

### Validation Before Committing

```bash
# Validate example skills
python3 scripts/validate_skills.py --collection example --unique

# Validate document skills
python3 scripts/validate_skills.py --collection document --unique

# Verify generated directories are in sync
python3 scripts/validate_generated_dirs.py
```

### Full Validation Pipeline

```bash
python3 scripts/refresh_skill_collections.py && \
python3 scripts/validate_skills.py --collection example --unique && \
python3 scripts/validate_skills.py --collection document --unique && \
python3 scripts/validate_generated_dirs.py
```

## Per-Skill Testing

Run skill-specific tests when they exist:

```bash
# Example: PDF skill tests
python3 document-skills/pdf/scripts/check_bounding_boxes_test.py

# Install skill-specific dependencies as needed
pip install -r mcp-builder/scripts/requirements.txt
pip install -r slack-gif-creator/requirements.txt
```

## Release Workflow

Use the release script for version management:

```bash
# Basic release
python3 scripts/release.py 1.2.0 \
  --change "Description of changes"

# Full release with git operations
python3 scripts/release.py 1.2.0 \
  --change "Major feature update" \
  --add "New feature description" \
  --add "Another feature" \
  --commit \
  --tag \
  --push \
  --release \
  --notes-from-changelog
```

The release script updates:
- `.claude-plugin/marketplace.json`
- `extensions/gemini/*/gemini-extension.json`
- `CHANGELOG.md`
- Git tags

## Creating a New Skill

1. **Create directory:**
   ```bash
   mkdir my-new-skill
   cd my-new-skill
   ```

2. **Create SKILL.md:**
   ```bash
   cat > SKILL.md << 'EOF'
   ---
   name: my-new-skill
   description: Brief description of what this skill does
   ---

   # My New Skill

   [Add instructions here]
   EOF
   ```

3. **Add optional resources:**
   ```bash
   mkdir -p scripts references assets
   ```

4. **Refresh and validate:**
   ```bash
   cd ..
   python3 scripts/refresh_skill_collections.py
   python3 scripts/validate_skills.py --collection example --unique
   ```

5. **Commit changes:**
   ```bash
   git add my-new-skill/
   git add collections/ skills/ .codex/ .claude/ extensions/
   git commit -m "Add my-new-skill"
   ```

## Modifying Existing Skills

1. Edit the skill's SKILL.md or resources
2. Run refresh script
3. Run validation
4. Commit both the skill changes AND generated directories

## Pull Request Checklist

- [ ] Skill SKILL.md has valid frontmatter
- [ ] Name matches directory name
- [ ] Refresh script executed
- [ ] Validation passes
- [ ] Generated directories included in PR
- [ ] README.md updated (if adding to curated lists)
- [ ] THIRD_PARTY_NOTICES.md updated (if adding external assets)
- [ ] Commit message follows convention

## Commit Message Style

Format: `<imperative verb> <subject> [(#PR-number)]`

Examples:
```
Add accessibility-patterns skill (#42)
Update pdf skill validation script
Fix typo in mcp-builder documentation
Clarify installation steps in README.md (#20)
```
