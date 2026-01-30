# PKM Methodologies Reference

A practical guide to the three core Personal Knowledge Management systems.

---

## Zettelkasten

The "slip box" method developed by sociologist Niklas Luhmann.

### Core Principles

1. **Atomicity**: One idea per note
2. **Connectivity**: Notes link to other notes
3. **Emergence**: Understanding grows through connections
4. **Bottom-up**: Structure emerges from notes, not imposed

### Note Types

| Type | Purpose | Characteristics |
|------|---------|-----------------|
| Fleeting | Capture quick thoughts | Temporary, processed daily |
| Literature | Summarize sources | References external material |
| Permanent | Atomic ideas | Self-contained, linked |
| Hub/Index | Navigation | Links to related notes |

### Workflow

```
1. Capture → Fleeting notes (quick capture)
2. Process → Literature notes (from sources)
3. Distill → Permanent notes (atomic ideas)
4. Connect → Link to existing notes
5. Review → Follow connections, discover patterns
```

### Linking Practices

- **Direct links**: "This relates to [[note]]"
- **Explanatory links**: "This contradicts [[note]] because..."
- **Structural links**: Index notes that collect related topics
- **Folgezettel**: Sequential numbering for note sequences

### When to Use Zettelkasten

Best for:
- Long-term knowledge building
- Research and writing projects
- Developing original ideas
- Finding unexpected connections

---

## PARA

Tiago Forte's organizational framework for digital information.

### The Four Categories

```
P - Projects  → Active efforts with deadlines
A - Areas     → Ongoing responsibilities
R - Resources → Topics of interest
A - Archives  → Inactive items
```

### Detailed Definitions

#### Projects
- Has a deadline
- Has a clear outcome
- Requires multiple tasks

**Examples**: Launch website, write report, plan event

#### Areas
- Ongoing responsibility
- No end date
- Standards to maintain

**Examples**: Health, finances, career development, relationships

#### Resources
- Topic of ongoing interest
- Reference material
- No immediate action required

**Examples**: Design inspiration, industry news, hobby research

#### Archives
- Completed projects
- Inactive areas
- Outdated resources

**Purpose**: Out of sight, but searchable when needed

### Decision Flowchart

```
Is it actionable?
├── YES: Does it have a deadline?
│   ├── YES → PROJECT
│   └── NO: Is it an ongoing responsibility?
│       ├── YES → AREA
│       └── NO → RESOURCE
└── NO: Might I need this later?
    ├── YES → ARCHIVE
    └── NO → DELETE
```

### PARA Organization Tips

| Guideline | Explanation |
|-----------|-------------|
| Keep projects visible | They drive immediate work |
| Limit active projects | 10-15 maximum |
| Review areas monthly | Check standards are maintained |
| Prune resources quarterly | Remove what you don't reference |
| Archive liberally | Better to archive than delete |

### When to Use PARA

Best for:
- Action-oriented work
- Managing information across tools
- Reducing decision fatigue
- Maintaining productivity focus

---

## LYT (Linking Your Thinking)

Nick Milo's framework for navigating linked notes.

### Core Concepts

#### Home Note
The single entry point to your knowledge base.

```markdown
# Home

## Active Focus
- [[Current Project]]
- [[Weekly Review]]

## Maps of Content
- [[MOC - Writing]]
- [[MOC - Technology]]
- [[MOC - Personal Development]]

## Utilities
- [[Inbox]]
- [[Templates]]
```

#### Maps of Content (MOCs)
Index notes that curate and link to related notes.

```markdown
# MOC - Writing

## Process
- [[Drafting Techniques]]
- [[Revision Workflow]]
- [[Publishing Checklist]]

## Craft
- [[Show Don't Tell]]
- [[Dialogue Best Practices]]
- [[Pacing and Rhythm]]

## Projects
- [[Book Project - Title]]
- [[Blog Post Ideas]]
```

### Fluid Frameworks

LYT emphasizes flexible, evolving structure:

```
Phase 1: COLLECT
→ Notes accumulate in inbox

Phase 2: COLLIDE
→ Notes start linking to each other
→ Clusters form organically

Phase 3: COALESCE
→ Create MOC when cluster grows too large
→ MOC provides navigation structure

Phase 4: COMPLETE
→ MOCs link to Home note
→ Navigation becomes fluid
```

### Idea Compass

Directional linking for context:

```
        North (upstream)
        ↑
West ←  IDEA  → East
(similar)     (opposite)
        ↓
        South (downstream)
```

| Direction | Question | Link Type |
|-----------|----------|-----------|
| North | What does this come from? | Source, predecessor |
| South | What does this lead to? | Outcome, successor |
| East | What is opposite? | Contrast, alternative |
| West | What is similar? | Related, parallel |

### When to Use LYT

Best for:
- Large, growing note collections
- Finding patterns across domains
- Balancing structure and flexibility
- Creative and research work

---

## Combining Methodologies

These methods aren't mutually exclusive.

### Common Combinations

| Combination | How It Works |
|-------------|--------------|
| PARA + Zettelkasten | PARA for projects, Zettelkasten for Resources |
| LYT + Zettelkasten | MOCs as hub notes, atomic permanent notes |
| All three | PARA structure, Zettelkasten notes, LYT navigation |

### Recommended Hybrid Approach

```
STRUCTURE (PARA)
├── Projects/     → Active work
├── Areas/        → Ongoing responsibilities
├── Resources/    → Topics of interest
│   └── (Zettelkasten permanent notes live here)
│   └── (MOCs provide navigation)
└── Archives/     → Inactive items

NAVIGATION (LYT)
├── Home note     → Entry point
└── MOCs          → Topic indices

NOTES (Zettelkasten)
├── Fleeting      → Inbox, processed daily
├── Literature    → Source summaries
└── Permanent     → Atomic, linked ideas
```

---

## Quick Reference

### Choosing a Starting Point

| Your Goal | Start With |
|-----------|------------|
| Get organized quickly | PARA |
| Build long-term knowledge | Zettelkasten |
| Navigate large collections | LYT |
| Manage action + knowledge | PARA + Zettelkasten |

### Daily Workflow

```
Morning: Check Projects (PARA)
Working: Create notes (Zettelkasten)
Evening: Process inbox, link notes (All methods)
Weekly: Review MOCs, update structure (LYT)
```

### Red Flags

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Can't find notes | Poor linking | Add more connections |
| Too many folders | Over-organizing | Flatten, use links instead |
| Inbox overflow | Not processing | Schedule daily review |
| Notes feel disconnected | No structure | Create MOCs or indices |
| Structure feels rigid | Over-planning | Let patterns emerge |
