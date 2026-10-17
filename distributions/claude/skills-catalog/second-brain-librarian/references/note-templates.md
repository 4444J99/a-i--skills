# Note Templates Reference

Ready-to-use templates for different note types in PKM systems.

---

## Fleeting Note Template

Quick capture for thoughts that need processing later.

```markdown
---
type: fleeting
captured: {{date}}
source: thought | conversation | reading | observation
status: inbox
---

# Quick Thought

[Write the thought exactly as it came to you]

## Context
- Where: [location/situation]
- Trigger: [what prompted this thought]

## Process Later
- [ ] Develop into permanent note?
- [ ] Connect to existing notes?
- [ ] Archive or discard?
```

### Minimal Fleeting Note

```markdown
{{date}} | {{time}}

[Thought]

#inbox
```

---

## Literature Note Template

Summaries and insights from books, articles, videos, podcasts.

```markdown
---
type: literature
title: "{{Source Title}}"
author: {{Author Name}}
source-type: book | article | video | podcast | paper
date-consumed: {{date}}
status: processing | complete
rating: 1-5
---

# {{Source Title}}

**Author**: {{Author}}
**Link/Citation**: [link or citation]

## Summary
[3-5 sentence summary of the main argument/content]

## Key Ideas

### Idea 1: [Title]
[Explanation in your own words]
- Page/timestamp:

### Idea 2: [Title]
[Explanation in your own words]
- Page/timestamp:

### Idea 3: [Title]
[Explanation in your own words]
- Page/timestamp:

## Quotes
> "Direct quote worth remembering"
> — p. XX

## My Reactions
- [Agreement, disagreement, questions, connections]

## Action Items
- [ ] Create permanent note about [concept]
- [ ] Connect to [[existing note]]
- [ ] Research further: [topic]

## Related
- [[Related Note 1]]
- [[Related Note 2]]
```

---

## Permanent Note Template

Atomic, self-contained ideas that stand on their own.

```markdown
---
type: permanent
created: {{date}}
modified: {{date}}
tags:
---

# [Single Concept Title]

[One clear statement of the idea - this should make sense without context]

## Explanation
[Expand on the idea in your own words. Use examples if helpful.
Keep it focused - one idea per note.]

## Evidence/Support
- [Why you believe this]
- [Source: [[Literature Note]] or experience]

## Connections
- **Supports**: [[Note that this supports]]
- **Contradicts**: [[Note that this challenges]]
- **Related**: [[Similar or adjacent concept]]
- **Leads to**: [[Logical next step or consequence]]

## Questions
- [Unresolved questions about this idea]

---
Source: [[Original Literature Note]]
```

### Minimal Permanent Note

```markdown
# [Concept]

[Single paragraph explaining the idea completely]

Links: [[Related]] | [[Connected]] | [[Opposite]]
```

---

## Map of Content (MOC) Template

Navigation hubs that organize related notes.

```markdown
---
type: moc
topic: {{Topic Name}}
created: {{date}}
modified: {{date}}
---

# {{Topic Name}}

[Brief description of what this topic covers and why it matters to you]

## Core Concepts
The foundational ideas in this domain:
- [[Fundamental Concept 1]]
- [[Fundamental Concept 2]]
- [[Fundamental Concept 3]]

## How Things Work
Process and mechanics:
- [[How X Works]]
- [[The Relationship Between X and Y]]

## Practical Applications
Using this knowledge:
- [[Technique 1]]
- [[Best Practice 2]]
- [[Common Mistake 3]]

## Open Questions
What I'm still exploring:
- [[Question about X]]
- [[Tension between Y and Z]]

## Resources
Sources and further reading:
- [[Literature Note - Book Title]]
- [[Literature Note - Article]]

## Related Maps
- [[Adjacent MOC 1]]
- [[Adjacent MOC 2]]

---
Parent: [[Home]] or [[Parent MOC]]
```

---

## Project Note Template

For PARA-style project management.

```markdown
---
type: project
status: active | on-hold | complete
deadline: {{date}}
area: [[Related Area]]
created: {{date}}
---

# Project: {{Project Name}}

## Outcome
[What does "done" look like? Be specific.]

## Why This Matters
[Connection to goals or areas of responsibility]

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Resources Needed
- [[Resource 1]]
- [[Resource 2]]

## Notes & Progress
### {{date}}
[Update on progress]

## Related
- Area: [[Related Area]]
- Projects: [[Related Project]]
- Resources: [[Relevant Resource]]
```

---

## Area Note Template

For ongoing responsibilities (PARA).

```markdown
---
type: area
status: active
review-frequency: weekly | monthly | quarterly
---

# Area: {{Area Name}}

## Description
[What is this area of responsibility?]

## Standards
What "good" looks like:
- [ ] [Standard 1]
- [ ] [Standard 2]
- [ ] [Standard 3]

## Current Focus
[What aspect needs attention right now?]

## Active Projects
- [[Project 1]]
- [[Project 2]]

## Key Resources
- [[Resource 1]]
- [[Resource 2]]

## Review Notes
### {{date}}
[Status, concerns, next focus]
```

---

## Daily Note Template

For daily capture and review.

```markdown
---
type: daily
date: {{date}}
---

# {{date}} {{day}}

## Today's Focus
1. [Most important task]
2. [Second priority]
3. [Third priority]

## Captured
### Thoughts
-

### Tasks (captured throughout day)
- [ ]

### Notes
- [[New note created today]]

## End of Day
### Completed
- [x]

### Moved to Tomorrow
- [ ]

### Reflections
[What worked, what didn't, what I learned]
```

---

## Weekly Review Template

```markdown
---
type: review
period: week
date: {{date}}
---

# Weekly Review: {{week}}

## Review Projects
| Project | Status | Next Action |
|---------|--------|-------------|
| [[Project 1]] | On track | Continue |
| [[Project 2]] | Blocked | Resolve X |

## Process Inbox
- [ ] Fleeting notes processed: ___ / ___
- [ ] Literature notes completed: ___ / ___
- [ ] Permanent notes created: ___

## Connections Made
- Linked [[Note A]] to [[Note B]]
- Created [[New MOC]]

## Areas Check
- [ ] Area 1: Standards met?
- [ ] Area 2: Standards met?

## Next Week's Focus
1.
2.
3.

## Insights This Week
[Key realizations, patterns noticed, ideas sparked]
```

---

## Quick Capture Formats

For when you need speed over structure.

### Voice Memo Transcription

```markdown
{{date}} | Voice Note

[Transcription or summary]

Process: #inbox
```

### Web Clip

```markdown
---
type: clip
url:
captured: {{date}}
---

# {{Page Title}}

[Key excerpt or summary]

Why saved: [reason]
```

### Meeting Note

```markdown
---
type: meeting
date: {{date}}
attendees:
---

# Meeting: {{Topic}}

## Discussed
-

## Decisions
-

## Actions
- [ ] @{{person}}: Task

## Follow-up
[[Related Project]]
```

---

## Template Usage Tips

| Situation | Template | Tip |
|-----------|----------|-----|
| Quick thought | Fleeting (minimal) | Capture fast, process later |
| Reading a book | Literature | Fill in as you read |
| Developing an idea | Permanent | Start with one clear sentence |
| Topic getting complex | MOC | Create when 5+ notes exist |
| Starting new work | Project | Define outcome first |
| Daily work | Daily | Review at day's end |

### Processing Priority

```
1. Daily notes      → Process same day
2. Fleeting notes   → Process within 24-48 hours
3. Literature notes → Complete within a week
4. MOCs             → Update when adding notes
5. Weekly review    → Every 7 days
```
