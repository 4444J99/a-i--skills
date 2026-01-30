# Workflow Integration: GitHub Repo Curator

This document describes how `github-repo-curator` integrates with other GitHub skills in the ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `github-profile-architect` | **Upstream/Downstream** | Before (get pinning criteria) or after (update profile) |
| `github-repository-standards` | **Downstream** | Apply standards to curated repos |
| `github-roadmap-strategist` | **Complementary** | Organize repos related to roadmap initiatives |

## Prerequisites

Before invoking `github-repo-curator`, ensure:

1. **Full repo access** - Can view all public and private repos
2. **Purpose clarity** - Know if this is for job search, OSS presence, or portfolio
3. **Target audience** - Recruiters, collaborators, or community

## Handoff Patterns

### From: github-profile-architect

**Trigger:** Profile strategy defined, need repos to pin.

**What to receive:**
- Persona type (Junior/Senior/DevRel)
- Portfolio strategy template (Hub, Complex, Visual, OSS)
- Technology focus areas to highlight

**Actions to take:**
- Audit all repositories against persona criteria
- Select 6 best-fit repos for pinning
- Recommend visibility changes for others

### To: github-repository-standards

**Trigger:** Repos selected for showcase need polish.

**What to hand off:**
- List of repos needing README updates
- Priority order (most visible first)
- Any special requirements (badges, diagrams)

**Expected output from standards:**
- Minimal root applied to each repo
- World-class README for each
- Consistent badge dashboard

### To: github-profile-architect

**Trigger:** Curation complete, profile needs update.

**What to hand off:**
- Final 6 pinned repo selections
- Social preview images created/updated
- Topics applied to each repo

**Expected actions:**
- Update profile README pinned repos section
- Refresh stats cards if needed
- Add any new showcase badges

### From/To: github-roadmap-strategist

**Trigger:** Organizing repos by project or initiative.

**Integration points:**
- Group repos by roadmap themes
- Apply consistent topics across related repos
- Archive repos for completed initiatives

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                   Repository Curation                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. PROFILE-ARCHITECT: Get persona & pinning criteria      │
│           │                                                 │
│           ▼                                                 │
│  2. REPO-CURATOR: Audit all repositories                   │
│           │                                                 │
│           ├──▶ Categorize: Keep / Archive / Delete         │
│           │                                                 │
│           ├──▶ Select 6 pins                               │
│           │                                                 │
│           ▼                                                 │
│  3. REPOSITORY-STANDARDS: Polish selected repos            │
│           │                                                 │
│           ▼                                                 │
│  4. REPO-CURATOR: Apply topics, set visibility             │
│           │                                                 │
│           ▼                                                 │
│  5. PROFILE-ARCHITECT: Update profile with selections      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing a curation session, verify:

- [ ] All repos audited (none overlooked)
- [ ] Visibility decisions made (public/private/archive/delete)
- [ ] 6 pinned repos selected with clear rationale
- [ ] Each selected repo ready for standards application
- [ ] Topics/tags strategy consistent across repos
- [ ] Social preview images set for pinned repos
- [ ] Profile architect notified of final selections

## Common Scenarios

### Portfolio Cleanup

1. **Repo Curator:** Audit, categorize, archive old projects
2. **Repository Standards:** Update READMEs for keepers
3. **Profile Architect:** Refresh pinned repos

### Job Search Preparation

1. **Profile Architect:** Define target role requirements
2. **Repo Curator:** Select repos demonstrating required skills
3. **Repository Standards:** Ensure professional presentation
4. **Profile Architect:** Hero section targets role

### Open Source Presence

1. **Repo Curator:** Identify contribution opportunities
2. **Repository Standards:** Ensure contribution repos are exemplary
3. **Roadmap Strategist:** Track contribution goals
4. **Profile Architect:** Showcase OSS activity

## Curation Decision Matrix

| Repo Type | Visibility | Pin Candidate? | Action |
|-----------|------------|----------------|--------|
| Best technical work | Public | Yes | Polish with standards |
| Active project | Public | Yes | Keep updated |
| Tutorial/learning | Public | Maybe | If demonstrates growth |
| Client work | Private | No | Keep for reference |
| Abandoned project | Archive | No | Archive or delete |
| Fork (unmodified) | Private/Delete | No | Delete unless needed |
| Experimental | Private | No | Keep if valuable |

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Random pinning | Incoherent portfolio story | Use persona-driven criteria |
| Unpolished showcases | Weak first impression | Apply standards before pinning |
| Too many public repos | Signal dilution | Archive/privatize liberally |
| Missing topics | Poor discoverability | Apply consistent tag strategy |
| Stale pins | Looks unmaintained | Review quarterly |

## Related Resources

- [GitHub Skills Ecosystem Map](../../../docs/guides/github-skills-ecosystem.md)
- [README Template Reference](./readme-template.md)
