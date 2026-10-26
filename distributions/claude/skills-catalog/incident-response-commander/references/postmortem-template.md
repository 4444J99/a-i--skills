# Post-Mortem Template

Blameless analysis framework for learning from incidents.

## Post-Mortem Document Template

```markdown
# Post-Mortem: [Brief Incident Title]

**Incident ID:** INC-[YYYY-MM-DD]-[###]
**Date:** [Incident date]
**Authors:** [Names]
**Status:** [Draft/In Review/Final]
**Meeting Date:** [Post-mortem meeting date]

---

## Executive Summary

[2-3 sentences summarizing what happened, the impact, and the key
takeaway. Write this for someone with 30 seconds to read.]

---

## Impact

### User Impact
- **Duration:** [X hours Y minutes]
- **Users affected:** [Number or percentage]
- **User-facing symptoms:** [What users experienced]

### Business Impact
- **Revenue impact:** [Quantified if applicable]
- **SLA impact:** [Breach details if applicable]
- **Reputation:** [Customer complaints, social media, etc.]

### Technical Impact
- **Services affected:** [List of services]
- **Data impact:** [Any data loss or corruption]
- **Infrastructure:** [Any lasting infrastructure impact]

---

## Timeline

_All times in UTC_

| Time | Event |
|------|-------|
| HH:MM | [First indication of problem] |
| HH:MM | [Alert fired / User report received] |
| HH:MM | [Incident declared] |
| HH:MM | [First responder action] |
| HH:MM | [Key investigation step] |
| HH:MM | [Root cause identified] |
| HH:MM | [Mitigation deployed] |
| HH:MM | [Service restored] |
| HH:MM | [Incident closed] |

### Detection Gap
- **Time from start to detection:** [X minutes]
- **Detection method:** [Alert/User report/Internal discovery]
- **Could we have detected sooner?** [Analysis]

---

## Root Cause Analysis

### The Five Whys

1. **Why did [immediate cause] happen?**
   [Answer]

2. **Why did [answer 1] happen?**
   [Answer]

3. **Why did [answer 2] happen?**
   [Answer]

4. **Why did [answer 3] happen?**
   [Answer]

5. **Why did [answer 4] happen?**
   [Answer → Root cause]

### Contributing Factors

| Factor | Category | Contribution |
|--------|----------|--------------|
| [Factor 1] | Process/Technical/Human | [How it contributed] |
| [Factor 2] | Process/Technical/Human | [How it contributed] |
| [Factor 3] | Process/Technical/Human | [How it contributed] |

### What Went Wrong

- [Specific failure point 1]
- [Specific failure point 2]
- [Specific failure point 3]

### What Went Right

- [What worked well in the response]
- [What prevented the incident from being worse]
- [Effective tooling/process that helped]

---

## Lessons Learned

### Detection
- **Lesson:** [What we learned about detecting this type of issue]
- **Gap:** [What monitoring/alerting was missing]

### Response
- **Lesson:** [What we learned about incident response]
- **Gap:** [What processes or tools were missing]

### Prevention
- **Lesson:** [What we learned about preventing this type of issue]
- **Gap:** [What safeguards were missing]

---

## Action Items

### Immediate (This Sprint)

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| 1 | [Action description] | [Name] | [Date] | [Open/In Progress/Done] |
| 2 | [Action description] | [Name] | [Date] | [Open/In Progress/Done] |

### Short-term (This Quarter)

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| 3 | [Action description] | [Name] | [Date] | [Open/In Progress/Done] |
| 4 | [Action description] | [Name] | [Date] | [Open/In Progress/Done] |

### Long-term (Backlog)

| ID | Action | Owner | Priority | Status |
|----|--------|-------|----------|--------|
| 5 | [Action description] | [Name] | [P1/P2/P3] | [Backlog] |
| 6 | [Action description] | [Name] | [P1/P2/P3] | [Backlog] |

---

## Appendix

### Supporting Data
- [Link to dashboards]
- [Link to logs]
- [Link to war room transcript]

### Related Incidents
- [INC-XXXX] - [Brief description and relationship]

### External References
- [Link to relevant documentation]
- [Link to vendor incident report if applicable]
```

---

## Five Whys Facilitation Guide

### Running an Effective Five Whys Session

**Before the meeting:**
1. Gather timeline and facts
2. Identify participants (responders + domain experts)
3. Share context with attendees
4. Set ground rules: blameless, curious, constructive

**During the meeting:**

```
Facilitator script:

"We're here to learn, not to blame. Our goal is to
understand what happened so we can prevent it from
happening again.

Let's start with what happened: [state the incident].

Now, why did [the incident] happen?"

[Document the answer]

"Okay, and why did [answer 1] happen?"

[Continue until you reach systemic causes]

"Are there any other contributing factors we haven't
discussed?"
```

**Stopping criteria:**
- You've reached a systemic or organizational cause
- The answers start becoming circular
- You've identified actionable improvements
- Usually 5-7 levels deep is sufficient

### Example Five Whys

```
Incident: Production database ran out of disk space

1. Why did the database run out of disk space?
   → A batch job created millions of temporary records.

2. Why did the batch job create millions of temporary records?
   → It processed a 10x larger dataset than usual.

3. Why was the dataset 10x larger?
   → A customer uploaded a year's worth of historical data.

4. Why wasn't this anticipated?
   → No upload size limits were enforced.

5. Why weren't upload limits enforced?
   → Requirements assumed "typical" usage patterns
     without defining or enforcing boundaries.

Root cause: Missing input validation and capacity planning
for edge-case data volumes.
```

---

## Blameless Culture Guidelines

### Principles

```
1. ASSUME POSITIVE INTENT
   People made the best decisions they could with the
   information they had at the time.

2. FOCUS ON SYSTEMS, NOT INDIVIDUALS
   "Why did the system allow this?" not "Why did
   [person] do this?"

3. TREAT ERRORS AS LEARNING OPPORTUNITIES
   Every incident is a chance to improve.

4. SHARE OPENLY
   Post-mortems are shared widely so everyone learns.

5. FOLLOW THROUGH ON ACTIONS
   Action items must be completed to close the loop.
```

### Language to Use

| Instead of | Say |
|------------|-----|
| "John caused the outage" | "The deployment triggered the outage" |
| "Why didn't anyone notice?" | "What monitoring would have caught this?" |
| "This was careless" | "What safeguards could prevent this?" |
| "They should have known" | "What would have made this more obvious?" |
| "Human error" | "The system allowed an unsafe action" |

### Common Anti-Patterns

```
ANTI-PATTERN: Stop at human error
BAD: "Why did the outage happen?" → "Bob deployed bad code"
BETTER: Continue asking why Bob was able to deploy bad code
        without automated checks catching it.

ANTI-PATTERN: Single root cause
BAD: Identifying one thing as THE cause
BETTER: Most incidents have multiple contributing factors.
        Explore them all.

ANTI-PATTERN: Blame disguised as process
BAD: "We need to train people to be more careful"
BETTER: "We need automated safeguards so that human
        mistakes don't reach production"

ANTI-PATTERN: Action items without owners
BAD: "We should add monitoring"
BETTER: "[Name] will add disk space alerting by [date]"
```

---

## Action Item Categories

### Detection Improvements

```
Examples:
- Add alert for [specific metric]
- Lower threshold on existing [alert]
- Add dashboard for [visibility gap]
- Instrument [code path] with logging
- Add synthetic monitoring for [flow]
```

### Response Improvements

```
Examples:
- Document runbook for [scenario]
- Add rollback automation for [service]
- Create playbook for [incident type]
- Improve on-call escalation path
- Add capacity to failover region
```

### Prevention Improvements

```
Examples:
- Add input validation for [data]
- Implement rate limiting on [endpoint]
- Add automated testing for [scenario]
- Implement canary deployments
- Add circuit breaker to [dependency]
```

### Process Improvements

```
Examples:
- Update change management process
- Revise code review checklist
- Improve deployment pipeline
- Update on-call documentation
- Improve communication templates
```

---

## Post-Mortem Meeting Agenda

```
INCIDENT POST-MORTEM MEETING
Duration: 60-90 minutes

1. OPENING (5 min)
   - Welcome and ground rules
   - Blameless reminder
   - Meeting objectives

2. TIMELINE REVIEW (15 min)
   - Walk through the incident chronologically
   - Clarify any gaps or questions
   - Note key decision points

3. ROOT CAUSE ANALYSIS (20 min)
   - Five Whys exercise
   - Identify contributing factors
   - Discuss what went wrong AND right

4. LESSONS LEARNED (10 min)
   - What did we learn?
   - What surprised us?
   - What would we do differently?

5. ACTION ITEMS (15 min)
   - Brainstorm improvements
   - Prioritize actions
   - Assign owners and due dates

6. CLOSING (5 min)
   - Summarize key takeaways
   - Confirm document owner
   - Schedule follow-up if needed

OUTPUTS:
- Completed post-mortem document
- Prioritized action items with owners
- Shared learning with broader team
```

---

## Post-Mortem Quality Checklist

```
Before publishing, verify:

Timeline:
□ All key events documented
□ Times are accurate and in UTC
□ Detection gap calculated

Root Cause:
□ Five Whys completed to systemic cause
□ Multiple contributing factors identified
□ No blame or named individuals in causes

Impact:
□ User impact quantified
□ Business impact assessed
□ Duration accurately calculated

Action Items:
□ Each action is specific and measurable
□ Each action has an owner
□ Each action has a due date
□ Actions address root causes, not symptoms
□ Mix of immediate and systemic fixes

Writing:
□ Executive summary is concise
□ Language is blameless
□ Technical details are accurate
□ Actionable insights are clear

Process:
□ Reviewed by incident participants
□ Shared with relevant teams
□ Action items tracked in project system
□ Follow-up meeting scheduled if needed
```
