# Workflow Integration: GitHub Repository Standards

This document describes how `github-repository-standards` integrates with other GitHub skills in the ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `github-repo-curator` | **Upstream** | After curator selects repos for showcase |
| `github-profile-architect` | **Upstream** | When profile pins need polished READMEs |
| `github-roadmap-strategist` | **Downstream** | Link README to roadmap, add tracking badges |

## Prerequisites

Before invoking `github-repository-standards`, ensure:

1. **Repository selected** - Know which repo(s) to standardize
2. **Purpose defined** - Library, CLI, app, or documentation project
3. **Audience known** - Contributors, users, or both

## Handoff Patterns

### From: github-repo-curator

**Trigger:** Repos selected for portfolio need professional READMEs.

**What to receive:**
- List of repos to standardize (priority order)
- Portfolio context (why these were selected)
- Any persona-specific requirements

**Actions to take:**
- Apply minimal root structure
- Create world-class README for each
- Ensure badge consistency across all

### From: github-profile-architect

**Trigger:** Pinned repos need quality assurance.

**What to receive:**
- List of 6 pinned repos
- Profile persona (affects README tone)
- Badge style preferences

**Actions to take:**
- Audit each repo's root structure
- Update READMEs to match profile quality
- Ensure dark mode compatibility

### To: github-roadmap-strategist

**Trigger:** Repo needs ongoing tracking or public roadmap link.

**What to hand off:**
- README badge endpoints needed
- Roadmap section location in README
- Initiative tracking requirements

**Expected output from roadmap:**
- Badge configuration for project status
- Link to public roadmap (if applicable)
- Tracking issue templates

### To: github-repo-curator

**Trigger:** Standards applied, repo ready for positioning.

**What to hand off:**
- Confirmation of standards applied
- Suggested topics based on tech stack
- Social preview image recommendations

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                 Repository Standardization                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. REPO-CURATOR: Select repos for standardization         │
│           │                                                 │
│           ▼                                                 │
│  2. REPOSITORY-STANDARDS: Audit root structure             │
│           │                                                 │
│           ├──▶ Apply .config/ strategy                     │
│           │                                                 │
│           ├──▶ Move files to .github/                      │
│           │                                                 │
│           ▼                                                 │
│  3. REPOSITORY-STANDARDS: Engineer README                  │
│           │                                                 │
│           ├──▶ Hero section with badges                    │
│           │                                                 │
│           ├──▶ Mermaid diagrams                            │
│           │                                                 │
│           ▼                                                 │
│  4. ROADMAP-STRATEGIST: Add tracking (optional)            │
│           │                                                 │
│           ▼                                                 │
│  5. REPO-CURATOR: Position in portfolio                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing standardization, verify:

- [ ] Root contains only architectural pillars
- [ ] Configs moved to `.config/` with glue code
- [ ] Community files in `.github/`
- [ ] README has hero, TOC, usage, badges
- [ ] All images have alt text (accessibility)
- [ ] Dark mode images use `<picture>` tags
- [ ] Mermaid diagrams render correctly
- [ ] Badge dashboard is functional (links work)
- [ ] LICENSE in root (required for detection)

## Common Scenarios

### New Repository Setup

1. **Repository Standards:** Scaffold directories, create README
2. **Repo Curator:** Set visibility, apply topics
3. **Roadmap Strategist:** Create tracking issue (if tracked)

### Existing Repository Polish

1. **Repository Standards:** Audit root, relocate configs
2. **Repository Standards:** Rewrite README with standards
3. **Repo Curator:** Update visibility if needed

### Open Source Launch

1. **Repository Standards:** Full minimal root + README
2. **Repository Standards:** Community health files
3. **Repo Curator:** License selection, topics
4. **Roadmap Strategist:** Public roadmap setup

## Standards Application Matrix

| File/Directory | Current Location | Target Location | Glue Required |
|----------------|------------------|-----------------|---------------|
| `.eslintrc.*` | root | `.config/eslint.config.js` | `--config` flag |
| `.prettierrc` | root | `.config/.prettierrc.json` | `--config` flag |
| `CONTRIBUTING.md` | root | `.github/CONTRIBUTING.md` | None (GitHub detects) |
| `CODEOWNERS` | root | `.github/CODEOWNERS` | None |
| `tsconfig.json` | root | **Keep in root** | N/A (project manifest) |
| `.editorconfig` | root | **Keep in root** | N/A (no override support) |
| `LICENSE` | root | **Keep in root** | N/A (detection requirement) |

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Moving tsconfig | Breaks compilation context | Keep project manifests in root |
| Moving LICENSE | Breaks GitHub detection | Always keep LICENSE in root |
| No glue code | Moved configs don't work | Provide package.json + VS Code settings |
| Badge-only hero | No substance | Include pitch and value proposition |
| Static diagrams | Documentation rot | Use Mermaid (diagrams as code) |

## README Quick Reference

### Hero Section Order

1. Logo (transparent, dark-mode compatible)
2. One-line pitch
3. Badge dashboard (Status, Metadata, Social)
4. Table of Contents

### Badge Categories

| Category | Purpose | Example |
|----------|---------|---------|
| Status | Build, tests, coverage | `build passing` |
| Metadata | Version, license, size | `MIT` |
| Social | Stars, forks, downloads | `1.2k stars` |
| Activity | Last commit, release | `v2.0.0` |

## Related Resources

- [GitHub Skills Ecosystem Map](../../../docs/guides/github-skills-ecosystem.md)
- [Root Hygiene Checklist](./root-hygiene-checklist.md)
- [README Anatomy Reference](./readme-anatomy.md)
