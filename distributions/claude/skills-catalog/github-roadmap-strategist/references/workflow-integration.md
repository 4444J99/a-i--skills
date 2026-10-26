# Workflow Integration: GitHub Roadmap Strategist

This document describes how `github-roadmap-strategist` integrates with other GitHub skills in the ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `github-repository-standards` | **Upstream/Downstream** | Link roadmap to READMEs, track initiatives |
| `github-repo-curator` | **Complementary** | Organize repos by roadmap themes |
| `github-profile-architect` | **Complementary** | Display roadmap progress on profile |

## Prerequisites

Before invoking `github-roadmap-strategist`, ensure:

1. **GitHub Projects V2 access** - Organization or personal projects enabled
2. **Stakeholder alignment** - Who needs visibility into the roadmap
3. **Repository structure** - Know which repos will feed the project

## Handoff Patterns

### To: github-repository-standards

**Trigger:** Roadmap items need documentation in READMEs.

**What to hand off:**
- Roadmap project URL for embedding
- Badge endpoints for status display
- Milestone information for changelog

**Expected output from standards:**
- Roadmap section in README
- Status badges displaying project health
- Links to initiative issues

### From: github-repository-standards

**Trigger:** New repository needs project tracking.

**What to receive:**
- Repository with standards applied
- Initiative requirements
- Tracking granularity (epic vs. task)

**Actions to take:**
- Create initiative issue in roadmap project
- Apply field taxonomy (Status, Theme, Confidence)
- Configure automation (branch → In Progress)

### To: github-repo-curator

**Trigger:** Organize repos by roadmap themes.

**What to hand off:**
- List of repos per strategic theme
- Topic tag recommendations
- Visibility recommendations (public roadmap items)

**Expected output from curator:**
- Consistent topics across theme repos
- Related repos cross-linked
- Archive decisions for completed initiatives

### To: github-profile-architect

**Trigger:** Display roadmap progress on profile.

**What to hand off:**
- Public roadmap URL (if applicable)
- Current initiative highlights
- Badge configuration for profile

**Expected output from architect:**
- Roadmap badge in profile hero
- "Currently Working On" section populated
- Links to public roadmap

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Roadmap Operations                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. ROADMAP-STRATEGIST: Define field taxonomy              │
│           │                                                 │
│           ├──▶ Status workflow                             │
│           │                                                 │
│           ├──▶ Strategic themes                            │
│           │                                                 │
│           ▼                                                 │
│  2. ROADMAP-STRATEGIST: Configure views                    │
│           │                                                 │
│           ├──▶ Executive Timeline                          │
│           │                                                 │
│           ├──▶ Engineering Kanban                          │
│           │                                                 │
│           ▼                                                 │
│  3. REPOSITORY-STANDARDS: Link in READMEs                  │
│           │                                                 │
│           ▼                                                 │
│  4. REPO-CURATOR: Organize by themes                       │
│           │                                                 │
│           ▼                                                 │
│  5. PROFILE-ARCHITECT: Display on profile (optional)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing roadmap setup, verify:

- [ ] Field taxonomy configured (Status, Theme, Confidence, Date)
- [ ] Views created (Timeline, Kanban, Triage)
- [ ] Triage protocol documented
- [ ] Automation configured (branch triggers, stale sweeper)
- [ ] README badges link to roadmap
- [ ] Public/private visibility correct
- [ ] Shadow items configured (if public roadmap with private work)

## Common Scenarios

### New Product Roadmap

1. **Roadmap Strategist:** Configure project, fields, views
2. **Repository Standards:** Add roadmap badges to main repo README
3. **Repo Curator:** Tag repos with strategic themes

### Public Roadmap for Open Source

1. **Roadmap Strategist:** Set up shadow item pattern
2. **Roadmap Strategist:** Configure public project with sanitized items
3. **Repository Standards:** Add public roadmap link to README
4. **Profile Architect:** Showcase roadmap on org/personal profile

### Quarterly Planning

1. **Roadmap Strategist:** Review metrics (Say/Do ratio)
2. **Roadmap Strategist:** Groom backlog, set Q targets
3. **Repo Curator:** Archive completed initiative repos
4. **Repository Standards:** Update changelogs

## Metrics Integration

The roadmap strategist tracks key metrics that inform other skills:

| Metric | Definition | Impacts |
|--------|------------|---------|
| Say/Do Ratio | % items delivered on target | Repository changelog frequency |
| Triage Velocity | Time in Triage queue | Repo curator prioritization |
| Staleness Index | % items not updated in 30d | Standards audit triggers |
| WIP Load | Active items per engineer | Profile "Currently Working On" |

## Public Roadmap Patterns

### Shadow Item Pattern

When internal work is private but roadmap must be public:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PRIVATE REPO (work happens here)                         │
│         │                                                   │
│         │ GitHub Action triggers on label "public-roadmap" │
│         ▼                                                   │
│   PUBLIC REPO (roadmap displayed here)                     │
│         │                                                   │
│         │ Issue created/synced (no comments)               │
│         ▼                                                   │
│   PUBLIC PROJECT (viewers see this)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key rules:**
- Comments never sync (internal discussions stay private)
- Status updates sync automatically
- Public issues are locked to prevent external noise

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Roadmap = Backlog | Strategic items buried in noise | Separate Backlog from Roadmap views |
| No triage protocol | Items rot without review | Assign weekly triage captain |
| Silent slips | Trust erodes | Require date updates when items slip |
| Public private items | Permission errors visible | Use shadow item pattern |
| No theme alignment | Work without strategy | Require Strategic Theme field |

## GitHub Actions Templates

### In-Progress Trigger

```yaml
# .github/workflows/roadmap-in-progress.yml
name: Mark In Progress
on:
  create:
    branches:
      - 'feature/*'
      - 'fix/*'
jobs:
  update-status:
    runs-on: ubuntu-latest
    steps:
      - name: Update Project Item
        uses: actions/github-script@v7
        # ... project item status update logic
```

### Stale Sweeper

```yaml
# .github/workflows/roadmap-stale.yml
name: Stale Item Check
on:
  schedule:
    - cron: '0 8 * * 1' # Every Monday 8 AM
jobs:
  check-stale:
    runs-on: ubuntu-latest
    steps:
      - name: Find stale items
        # Items in "In Progress" with no update in 14 days
```

## Related Resources

- [GitHub Skills Ecosystem Map](../../../docs/guides/github-skills-ecosystem.md)
- [Field Taxonomy Reference](./field-taxonomy.md)
- [Governance Protocols Reference](./governance-protocols.md)
