# Workflow Integration: GitHub Profile Architect

This document describes how `github-profile-architect` integrates with other GitHub skills in the ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `github-repo-curator` | **Downstream** | After defining profile strategy, select repos to pin |
| `github-repository-standards` | **Downstream** | Ensure pinned repos meet quality standards |
| `github-roadmap-strategist` | **Complementary** | Display roadmap badges or progress on profile |

## Prerequisites

Before invoking `github-profile-architect`, ensure:

1. **Repository inventory exists** - Know which repos are available to pin
2. **Persona is defined** - Junior/Senior/DevRel determines strategy
3. **Contact channels ready** - Email, LinkedIn, portfolio URLs

## Handoff Patterns

### To: github-repo-curator

**Trigger:** After building the hero section, you need to select pinned repos.

**What to hand off:**
- Persona type (affects repo selection criteria)
- Portfolio strategy (Hub, Complex, Visual, OSS contribution)
- Desired skill signals (what technologies to showcase)

**Expected output from curator:**
- 6 pinned repository selections with rationale
- Visibility recommendations (archive/delete others)
- Topic tags for each selected repo

### To: github-repository-standards

**Trigger:** Each pinned repo needs a polished README.

**What to hand off:**
- List of 6 pinned repos
- Profile persona context
- Any specific badge requirements

**Expected output from standards:**
- Minimal root structure applied
- World-class README for each repo
- Consistent badge styling

### From: github-roadmap-strategist

**Trigger:** Display project progress on profile.

**What to receive:**
- Roadmap project URL for embedding
- Badge endpoints for current status
- Milestone dates for "Currently Working On"

**Integration points:**
- Add roadmap badge to profile hero section
- Update "Currently Working On" from active roadmap items
- Link to public roadmap in profile footer

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Profile Optimization                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. PROFILE-ARCHITECT: Define persona & hero               │
│           │                                                 │
│           ▼                                                 │
│  2. REPO-CURATOR: Select 6 pinned repos                    │
│           │                                                 │
│           ▼                                                 │
│  3. REPOSITORY-STANDARDS: Polish each pinned repo          │
│           │                                                 │
│           ▼                                                 │
│  4. PROFILE-ARCHITECT: Implement automation                │
│           │                                                 │
│           ▼                                                 │
│  5. ROADMAP-STRATEGIST: (optional) Link project tracking   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing a profile optimization, verify:

- [ ] Hero section follows persona strategy
- [ ] 6 pinned repos selected via curator criteria
- [ ] Each pinned repo has standards-compliant README
- [ ] Badge colors are cohesive (no "fruit salad")
- [ ] Dark mode compatibility verified (`<picture>` tags)
- [ ] Automation workflows configured (if applicable)
- [ ] Contact links functional
- [ ] Profile README renders correctly on GitHub

## Common Scenarios

### Junior Developer Profile

1. **Profile Architect:** Streak stats, learning roadmap, "Currently Learning"
2. **Repo Curator:** Breadth over depth, tutorial/bootcamp projects OK
3. **Repository Standards:** Ensure even simple repos have proper READMEs

### Senior Engineer Profile

1. **Profile Architect:** Minimal hero, architecture focus, private stats
2. **Repo Curator:** Quality over quantity, OSS contributions prioritized
3. **Repository Standards:** Emphasize technical depth, diagrams
4. **Roadmap Strategist:** Link to team/org roadmaps if public

### DevRel Profile

1. **Profile Architect:** Content feeds (blog/YouTube), sponsor button
2. **Repo Curator:** Community repos, talk repos, demo repos
3. **Repository Standards:** Heavy on examples, accessibility
4. **Roadmap Strategist:** Public community roadmaps

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Skipping curator | Random pins, poor showcase | Always audit repos before pinning |
| Unpolished pins | Profile links to messy repos | Apply standards to all pinned repos |
| Static profile | Looks abandoned over time | Implement automation (Actions) |
| Persona mismatch | Senior with junior styling | Respect persona-specific guidance |

## Related Resources

- [GitHub Skills Ecosystem Map](../../../docs/guides/github-skills-ecosystem.md)
- [Profile Components Reference](./profile-components.md)
- [Persona Strategies Reference](./persona-strategies.md)
