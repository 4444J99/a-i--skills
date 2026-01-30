# Yak Shave Analysis Patterns

Strategies for identifying and interpreting yak shaving in coding sessions.

## What is Yak Shaving?

### Definition

Yak shaving occurs when solving a problem requires solving an unrelated prerequisite, which requires another unrelated prerequisite, and so on, until you are metaphorically shaving a yak.

### Classic Example

```
Goal: Deploy my app
├── But CI is failing
│   ├── Need to update Node version
│   │   ├── Need to update nvm
│   │   │   ├── Need to fix shell config
│   │   │   │   └── Need to understand zsh vs bash
```

By the time you're researching shell differences, you have forgotten about deploying your app.

---

## Indicators of Yak Shaving

### Strong Indicators

| Signal | Example |
|--------|---------|
| Domain jumps | "Fixing CSS" → "Updating webpack config" |
| Prerequisite chains | "But first I need to..." repeated |
| Unrelated tool use | Reading build files when fixing UI bug |
| Session length explosion | 5-minute task takes 2 hours |
| New file creation | Asked to fix one file, created 10 |

### Weak Indicators

| Signal | May Be | But Could Also Be |
|--------|--------|-------------------|
| Many file edits | Yak shave | Legitimate refactor |
| Long session | Lost focus | Complex task |
| Multiple domains | Wandering | Full-stack feature |
| Web searches | Going down rabbit holes | Necessary research |

---

## Session Analysis Framework

### Phase 1: Initial Intent

Extract and categorize the original request:

```
User Message: "Can you fix the button alignment on the login page?"

Category: UI/CSS
Expected Scope: Single file, small change
Complexity: Quick (< 10 minutes)
Expected Files: login.css, Login.tsx
```

### Phase 2: Track Domain Transitions

Monitor which areas of the codebase are touched:

```
Timeline:
09:00 - [UI] Opened Login.tsx
09:02 - [UI] Opened login.css
09:05 - [CONFIG] Opened tailwind.config.js   ← First domain shift
09:08 - [BUILD] Opened postcss.config.js     ← Second domain shift
09:12 - [DEPS] Reading package.json          ← Third domain shift
09:15 - [BUILD] Running npm commands         ← Escalation
```

### Phase 3: Measure Drift

Calculate how far the session wandered:

```
Original Domain: UI
Domains Visited: UI → CONFIG → BUILD → DEPS
Domain Shift Count: 3
Return to Original: No
Goal Completed: No
```

---

## Pattern Library

### Pattern 1: The Prerequisite Cascade

**Signature**: Chain of "but first" moments

```
Session Flow:
1. "Fix button" → Found outdated CSS framework
2. "Update CSS framework" → Requires build tool update
3. "Update build tool" → Breaks tests
4. "Fix tests" → Need new test runner
5. Session ends → Button still misaligned
```

**Score**: 75-90 (High yak shave)

### Pattern 2: The Environment Spiral

**Signature**: Local dev issues derail actual work

```
Session Flow:
1. "Add new feature" → Can not run locally
2. "Fix local env" → Node version wrong
3. "Update Node" → nvm issues
4. "Fix nvm" → Shell config problems
5. Eventually works → But it is late
```

**Score**: 60-80 (Significant yak shave)

### Pattern 3: The Refactor Trap

**Signature**: "While I'm here" mentality

```
Session Flow:
1. "Fix typo in auth.ts"
2. "While here, improve the function"
3. "Actually, refactor the whole module"
4. "Should update related tests too"
5. 2 hours later, still refactoring
```

**Score**: 40-60 (Moderate yak shave)

### Pattern 4: The Research Rabbit Hole

**Signature**: Learning replaces doing

```
Session Flow:
1. "Implement caching"
2. Read about Redis vs Memcached
3. Research distributed caching
4. Deep dive into CAP theorem
5. Session ends with extensive notes, no code
```

**Score**: 30-50 (Research, may be valuable)

### Pattern 5: The Debug Cascade

**Signature**: One bug reveals many

```
Session Flow:
1. "Fix auth bug"
2. Find race condition
3. Race condition reveals timing issue
4. Timing issue shows architecture flaw
5. Stuck on fundamental redesign
```

**Score**: Variable (May be necessary discovery)

---

## Healthy vs Unhealthy Yak Shaving

### Healthy (Low Score Deserved)

| Situation | Why It's OK |
|-----------|-------------|
| Discovering blocking issue | Must fix to proceed |
| Finding security vulnerability | Should address immediately |
| Uncovering tech debt | Awareness is valuable |
| Necessary refactor | Old code prevented progress |

### Unhealthy (High Score Deserved)

| Situation | Why It's Bad |
|-----------|--------------|
| Perfectionism on tangent | Original goal forgotten |
| Premature optimization | Not needed yet |
| Gold-plating | Over-engineering |
| Avoidance behavior | Doing easier tangent work |

---

## Time-Based Analysis

### Session Duration vs Complexity

| Task Type | Expected Duration | Yak Shave Threshold |
|-----------|-------------------|---------------------|
| Typo fix | 5 min | > 15 min |
| Small bug | 15-30 min | > 1 hour |
| Feature | 1-2 hours | > 4 hours |
| Refactor | 2-4 hours | > 8 hours |

### Late-Night Penalty

Sessions after 10 PM or before 6 AM get a yak shave multiplier:

```python
def apply_time_penalty(score, session_hour):
    """Late night sessions are more prone to yak shaving."""
    if session_hour >= 22 or session_hour < 6:
        return min(100, score * 1.2)  # 20% penalty
    return score
```

---

## Reporting Templates

### Individual Session Report

```
## Yak Shave Analysis: "fix button alignment"

**Date**: 2026-01-25, 11:42 PM
**Duration**: 2h 15m
**Score**: 87/100 (Epic Rabbit Hole)

### Journey Map
```
button fix (UI)
  ↓ found outdated PostCSS
tailwind config (CONFIG)
  ↓ plugin compatibility issue
postcss update (BUILD)
  ↓ broke purge settings
webpack config (BUILD)
  ↓ needed Node 18
nvm update (SYSTEM)
  ↓ ... still fixing button?
```

### What Happened
Started with CSS alignment, ended configuring build system.
The button is still misaligned.

### Key Diversion Point
09:05 - Opened tailwind.config.js instead of trying CSS override.

### Recommendation
When facing config issues for small fixes, try inline styles first.
```

### Aggregate Report

```
## Weekly Yak Shave Report (Jan 22-28, 2026)

**Sessions Analyzed**: 12
**Average Score**: 47/100

### Distribution
| Range | Count | Sessions |
|-------|-------|----------|
| 0-20  | 3 | typo-fix, update-readme, quick-query |
| 21-40 | 4 | add-feature, fix-test, ... |
| 41-60 | 2 | refactor-auth, update-deps |
| 61-80 | 2 | debug-perf, add-caching |
| 81-100| 1 | fix-button (the infamous one) |

### Patterns Identified
- **UI tasks** have highest yak shave rate (avg 58)
- **Late night** sessions score 23% higher
- **"Quick fix"** requests are most likely to derail

### Recommendations
1. Time-box CSS fixes to 15 minutes
2. Avoid "just one more thing" after 10 PM
3. When stuck, ask for help before diving into configs
```

---

## Self-Awareness Prompts

Questions to ask during a session:

1. **"What was I originally trying to do?"**
   - If you cannot remember, you are yak shaving

2. **"Will this help me complete my original task?"**
   - "No, but it'll be cleaner" = yak shave

3. **"Is this the simplest solution?"**
   - If not, consider stopping

4. **"How long ago was my last commit?"**
   - Over an hour with no commits = possible yak shave

5. **"Can I timebox this and come back?"**
   - If yes, do it
