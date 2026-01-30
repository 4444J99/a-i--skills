# Evaluation-to-Growth Inline Revision Template

Use this format when user selects **Inline Revisions** output.

---

## Format Conventions

Inline revisions embed feedback directly within or alongside the original content using visual markers.

### Marker System

```
[ORIGINAL TEXT]                           ← Unchanged, passes all checks
~~[REMOVED TEXT]~~                        ← Suggested deletion (strikethrough)
**[ADDED TEXT]**                          ← Suggested addition (bold)
[ORIGINAL]→[REVISED]                      ← Suggested replacement
[TEXT]{COMMENT: explanation}              ← Comment without change
[TEXT]{CRITIQUE: finding}                 ← Critique finding
[TEXT]{LOGIC: issue}                      ← Logic check finding
[TEXT]{LOGOS: note}                       ← Logos review note
[TEXT]{PATHOS: note}                      ← Pathos review note
[TEXT]{ETHOS: note}                       ← Ethos review note
[TEXT]{BLIND SPOT: risk}                  ← Blind spot identified
[TEXT]{SHATTER POINT: vulnerability}      ← Shatter point identified
[TEXT]{BLOOM: insight}                    ← Emergent insight
```

### Severity Indicators

```
{🔴 CRITICAL: ...}    ← Must address before publishing
{🟡 IMPORTANT: ...}   ← Should address for quality
{🟢 SUGGESTION: ...}  ← Optional improvement
{💡 INSIGHT: ...}     ← Growth opportunity
```

---

## Example: Inline Revision Output

### Original Content with Inline Feedback

---

> **The Impact of Remote Work on Productivity**
> 
> Remote work has **completely**→**significantly** transformed how businesses operate.{🟡 LOGOS: "completely" is absolute claim without evidence}
> 
> ~~Many~~ **Most** studies show that employees working from home are more productive than their office counterparts.{🔴 LOGIC: Claim needs citation. Which studies? Add source.}
> 
> The benefits are clear: no commute, flexible schedules, and better work-life balance.{CRITIQUE: Strength—clear enumeration of benefits}
> 
> **However, remote work also presents challenges including isolation, communication barriers, and difficulty separating work from personal life.**{🟢 SUGGESTION: Added for balance—original lacked counterpoint}
> 
> Companies that embrace remote work{ETHOS: Consider adding "according to [source]" to strengthen authority} will thrive in the modern economy, while those that resist will fall behind.{🟡 SHATTER POINT: Binary framing invites criticism. Consider nuancing.}
> 
> ~~In conclusion,~~ Remote work is the future.{PATHOS: "In conclusion" is weak; direct statement is stronger}{🔴 BLIND SPOT: Assumes all industries/roles can go remote—address exceptions}
> 
> {💡 BLOOM: Consider expanding into specific industry analysis—different sectors have different remote work viability}

---

## Summary Block

After inline revisions, include a summary block:

```
---
## Inline Revision Summary

### Changes by Type
- Deletions: 2
- Additions: 1
- Replacements: 1
- Comments: 8

### By Severity
- 🔴 Critical: 2 (must address)
- 🟡 Important: 2 (should address)
- 🟢 Suggestions: 1 (optional)
- 💡 Insights: 1 (growth opportunity)

### By Phase
- Critique: 1
- Logic: 1
- Logos: 1
- Pathos: 1
- Ethos: 1
- Blind Spots: 1
- Shatter Points: 1
- Bloom: 1

### Priority Actions
1. [🔴] Add citation for productivity claim
2. [🔴] Address industry exceptions to remote work
3. [🟡] Nuance the "thrive vs fall behind" framing
4. [🟡] Replace "completely" with qualified language
---
```

---

## Clean Version Block

Optionally provide a clean revised version with all changes applied:

```
---
## Revised Version (Clean)

**The Impact of Remote Work on Productivity**

Remote work has significantly transformed how businesses operate.

According to a 2023 Stanford study, most research shows that employees working from home are more productive than their office counterparts.

The benefits are clear: no commute, flexible schedules, and better work-life balance. However, remote work also presents challenges including isolation, communication barriers, and difficulty separating work from personal life.

Companies that strategically embrace remote work—adapting policies to their specific industry needs—position themselves well for the modern economy. The transition requires thoughtful implementation rather than wholesale adoption or rejection.

Remote work is reshaping the future of work, though its application varies significantly across industries and roles.

---
```

---

## Interactive Mode: Step-by-Step Inline

In interactive mode, present inline feedback one phase at a time:

### Step 1: Critique Pass
Show only `{CRITIQUE: ...}` markers

### Step 2: Logic Pass  
Add `{LOGIC: ...}` markers

### Step 3: Logos Pass
Add `{LOGOS: ...}` markers

### Step 4: Pathos Pass
Add `{PATHOS: ...}` markers

### Step 5: Ethos Pass
Add `{ETHOS: ...}` markers

### Step 6: Risk Pass
Add `{BLIND SPOT: ...}` and `{SHATTER POINT: ...}` markers

### Step 7: Growth Pass
Add `{BLOOM: ...}` markers and suggested additions

### Step 8: Final Review
Present complete inline version with all markers, summary, and clean revision

---

## Comparison View (Optional)

For longer content, offer side-by-side comparison:

```
| Original | Revised | Notes |
|----------|---------|-------|
| Remote work has completely transformed... | Remote work has significantly transformed... | Qualified absolute claim |
| Many studies show... | According to a 2023 Stanford study, most research shows... | Added citation, adjusted language |
| [no counterpoint] | However, remote work also presents challenges... | Added balance |
```

---

*Inline revision format from Evaluation-to-Growth framework*
