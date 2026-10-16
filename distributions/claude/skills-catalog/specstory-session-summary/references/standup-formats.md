# Standup Summary Formats

Templates and patterns for presenting AI coding session summaries.

## Standard Standup Format

### Single Session

```markdown
### YYYY-MM-DD HH:MM - {Brief Title}
**Goal**: {1 sentence summarizing what user wanted}
**Outcome**: {emoji} {Brief result description}
**Files**: {comma-separated list, or "None"}
**Key insight**: {Notable decision or learning, if any}
```

### Multi-Task Session

```markdown
### YYYY-MM-DD HH:MM - {Overall Theme}
**Tasks**:
  1. {First task} - {outcome emoji}
  2. {Second task} - {outcome emoji}
**Files**: {comma-separated list}
**Key insight**: {Notable decision or learning}
```

---

## Outcome Status Icons

| Icon | Status | When to Use |
|------|--------|-------------|
| ✅ | Completed | Task finished successfully |
| 📚 | Research | Information gathering, no code changes |
| 🔧 | In Progress | Work started but session ended mid-task |
| ❌ | Abandoned | User changed direction or gave up |
| 🚧 | Blocked | Ended with unresolved error or blocker |

### Status Determination Logic

```
if final_message contains "done" or "complete" or commit:
    status = ✅ Completed
elif no Edit/Write calls found:
    status = 📚 Research
elif final_message contains "error" or "failed":
    status = 🚧 Blocked
elif session < 5 messages:
    status = ❌ Abandoned
else:
    status = 🔧 In Progress
```

---

## Session Title Extraction

### From User Intent

Derive title from the first user message:

| User Message | Derived Title |
|--------------|---------------|
| "Can you help me fix the authentication bug?" | Fix Authentication Bug |
| "I need to add a new endpoint for user settings" | Add User Settings Endpoint |
| "What's the best way to handle caching?" | Investigate Caching Strategy |
| "Update the README with installation instructions" | Update README Installation |

### Title Shortening Rules

1. Remove filler words: "Can you", "I need to", "Please"
2. Use imperative mood: "Fix X" not "Fixing X"
3. Keep under 50 characters
4. Be specific about the domain

---

## Summary Section Templates

### Patterns Section

```markdown
**Patterns**: {themes}, {repeated files}, {ongoing work}
```

Examples:
- "3 sessions focused on auth system; middleware.ts touched repeatedly"
- "Debugging theme across all sessions; no new features this week"
- "Mix of bug fixes and documentation updates"

### Unfinished Section

```markdown
**Unfinished**: {list of incomplete items}
```

Examples:
- "Database migration needs completion; test suite has 2 failing tests"
- "None detected"
- "API redesign started but not merged; waiting on review"

---

## Time Range Variations

### Last N Sessions

```markdown
## Session Summary (Last 5 Sessions)

### 2026-01-28 11:42 - ...
### 2026-01-28 10:15 - ...
### 2026-01-27 16:30 - ...
### 2026-01-27 09:00 - ...
### 2026-01-26 14:22 - ...

---
**Patterns**: ...
**Unfinished**: ...
```

### Today's Sessions

```markdown
## Today's Sessions (2026-01-28)

### 11:42 - Fix Authentication Bug
...

### 10:15 - Update Dependencies
...

---
**Today's Focus**: Authentication and maintenance
**Still Open**: Auth fix needs testing
```

### Date Range

```markdown
## Sessions: Jan 22-28, 2026

### Monday, Jan 22
- 09:15 - Morning standup prep (📚)
- 14:30 - Fix button alignment (✅)

### Tuesday, Jan 23
- 10:00 - Add logout feature (✅)

### Wednesday, Jan 24
- (No sessions)

...

---
**Week Summary**: 8 sessions, 6 completed, 1 research, 1 blocked
**Key Focus Areas**: UI components, authentication
```

---

## File Change Summary

### Extracting Modified Files

Look for these patterns in session history:

```
Edit( → Extract filename from tool call
Write( → Extract filename from tool call
Created file → Extract path from result
Modified file → Extract path from result
```

### Presenting Files

| Number of Files | Format |
|-----------------|--------|
| 0 | "None" or "Read-only session" |
| 1-3 | List all: `auth.ts, middleware.ts, config.json` |
| 4-6 | List all, shorter names: `auth, middleware, config` |
| 7+ | Summarize: `8 files in src/auth/` |

### Files to Highlight

- Files touched in multiple sessions (recurring work)
- Configuration files (settings changes)
- Test files (testing activity)
- README/docs (documentation updates)

---

## Key Insight Patterns

### What to Extract

| Look For | Example Insight |
|----------|-----------------|
| "decided to" / "chose" | "Chose JWT over sessions for stateless auth" |
| "instead of" | "Used Redis instead of in-memory cache for scaling" |
| Trade-off discussions | "Sacrificed bundle size for better DX" |
| Architecture decisions | "Moved to event-driven pattern for notifications" |
| Lessons learned | "Discovered race condition in concurrent updates" |

### When to Omit

- No clear decisions made
- Pure implementation without choices
- Routine maintenance

Use: `**Key insight**: None (routine implementation)`

---

## Example Outputs

### Daily Standup

```markdown
## Session Summary (Last 3 Sessions)

### 2026-01-28 11:42 - Investigate Chat CRDT Storage
**Goal**: Understand why chat index CRDT doesn't contain the thread
**Outcome**: 📚 Explained dual storage design for offline/online sync
**Files**: threads.json, crdt-debug/4X/, crdt-debug/aT/
**Key insight**: Two storage layers (CRDT + JSON) serve different sync scenarios

### 2026-01-28 10:15 - Address Code Review Comments
**Goal**: Fix clarity issues from code review
**Outcome**: ✅ Refactored normalizeChatIndexDoc function
**Files**: chat.go, automerge-bridge.js
**Key insight**: Replaced complex normalization with toPlainString helper

### 2026-01-27 14:30 - Automerge Architecture Deep Dive
**Goal**: Document how Automerge docs are constructed temporally
**Outcome**: 📚 Research complete, walkthrough provided
**Files**: automerge-bridge.js, document.go (read only)

---
**Patterns**: 3 sessions focused on CRDT/chat subsystem; automerge-bridge.js touched repeatedly
**Unfinished**: None detected
```

### Weekly Summary

```markdown
## Week of Jan 22-28, 2026

| Day | Sessions | Completed | Focus Area |
|-----|----------|-----------|------------|
| Mon | 2 | 2 | Auth system |
| Tue | 3 | 2 | Database |
| Wed | 1 | 1 | Testing |
| Thu | 2 | 1 | UI fixes |
| Fri | 2 | 2 | Documentation |

**Total**: 10 sessions, 8 completed, 2 research

**Key Accomplishments**:
- Auth system refactor completed
- Database migration finished
- All tests passing

**Carried Forward**:
- UI performance optimization (started Friday)
```

---

## Reading Strategy for Large Sessions

### Session Structure Analysis

```bash
# Count user messages to understand scope
grep -n "_\*\*User\*\*_" session.md | head -10
```

### Strategic Reading

| Section | What to Extract |
|---------|-----------------|
| First 500 lines | Initial request, approach taken |
| Last 300 lines | Final outcome, conclusion |
| Edit/Write calls | Files modified |
| User message markers | Number of distinct tasks |

### Multi-Request Sessions

When line numbers are far apart (e.g., 50, 800, 1500):

1. Read around each user message
2. Summarize 2-3 main tasks
3. Group minor tasks as "various small fixes"
