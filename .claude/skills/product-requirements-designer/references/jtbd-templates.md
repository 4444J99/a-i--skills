# Jobs-to-Be-Done Templates

## Core Job Statement

### Format
```
When [situation/context],
I want to [motivation/goal],
so I can [expected outcome].
```

### Detailed Job Statement
```
[VERB] + [OBJECT] + [CLARIFIER]

Example: "Minimize the time it takes to identify the root cause of a system failure"
         [VERB]     [OBJECT]              [CLARIFIER]
```

### Job Statement Quality Checklist
- [ ] Solution-agnostic (no product/feature references)
- [ ] Stable over time (won't change with technology)
- [ ] Has clear beginning and end
- [ ] Measurable (can evaluate success)
- [ ] Written from user's perspective

---

## Job Map

### Template

```
┌─────────────────────────────────────────────────────────────────┐
│                        CORE JOB                                  │
│  [Main job statement]                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   DEFINE      │    │   EXECUTE     │    │   CONCLUDE    │
│   (Before)    │    │   (During)    │    │   (After)     │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Job Map Stages (Universal)

| Stage | Definition | Key Question |
|-------|------------|--------------|
| 1. Define | Determine goals and plan approach | What do I need to accomplish? |
| 2. Locate | Gather required inputs and resources | What do I need to get started? |
| 3. Prepare | Set up environment and inputs | How do I get ready? |
| 4. Confirm | Verify readiness to proceed | Am I ready to proceed? |
| 5. Execute | Perform the core job | How do I do it? |
| 6. Monitor | Track progress and results | Is it working? |
| 7. Modify | Make adjustments as needed | What needs to change? |
| 8. Conclude | Finish and clean up | How do I wrap up? |

### Detailed Job Map Template

| Stage | Job Steps | Pain Points | Opportunities |
|-------|-----------|-------------|---------------|
| **Define** | | | |
| | [Step 1.1] | [Pain] | [Opportunity] |
| | [Step 1.2] | [Pain] | [Opportunity] |
| **Locate** | | | |
| | [Step 2.1] | [Pain] | [Opportunity] |
| **Prepare** | | | |
| | [Step 3.1] | [Pain] | [Opportunity] |
| **Confirm** | | | |
| | [Step 4.1] | [Pain] | [Opportunity] |
| **Execute** | | | |
| | [Step 5.1] | [Pain] | [Opportunity] |
| | [Step 5.2] | [Pain] | [Opportunity] |
| **Monitor** | | | |
| | [Step 6.1] | [Pain] | [Opportunity] |
| **Modify** | | | |
| | [Step 7.1] | [Pain] | [Opportunity] |
| **Conclude** | | | |
| | [Step 8.1] | [Pain] | [Opportunity] |

---

## Forces Diagram

### Four Forces Model

```
        ┌─────────────────────────────────────────┐
        │         PUSH OF SITUATION               │
        │   (Problems with current solution)      │
        │   • [Pain point 1]                      │
        │   • [Pain point 2]                      │
        └─────────────────────────────────────────┘
                          │
                          ▼  DEMAND
        ┌─────────────────────────────────────────┐
        │                                         │
        │              SWITCH                     │
        │         (to new solution)               │
        │                                         │
        └─────────────────────────────────────────┘
                          ▲  DEMAND
                          │
        ┌─────────────────────────────────────────┐
        │         PULL OF NEW SOLUTION            │
        │   (Attraction to new approach)          │
        │   • [Benefit 1]                         │
        │   • [Benefit 2]                         │
        └─────────────────────────────────────────┘


        ┌─────────────────────────────────────────┐
        │         ANXIETY OF NEW SOLUTION         │
        │   (Concerns about switching)            │
        │   • [Fear 1]                            │
        │   • [Fear 2]                            │
        └─────────────────────────────────────────┘
                          │
                          ▼  RESISTANCE
        ┌─────────────────────────────────────────┐
        │                                         │
        │             NO SWITCH                   │
        │       (stay with current)               │
        │                                         │
        └─────────────────────────────────────────┘
                          ▲  RESISTANCE
                          │
        ┌─────────────────────────────────────────┐
        │         HABIT OF PRESENT                │
        │   (Comfort with current solution)       │
        │   • [Habit 1]                           │
        │   • [Habit 2]                           │
        └─────────────────────────────────────────┘
```

### Forces Analysis Template

| Force | Description | Strength (1-5) | Evidence |
|-------|-------------|----------------|----------|
| **Push** (away from current) | | | |
| [Push factor 1] | [Description] | [1-5] | [Quote/data] |
| [Push factor 2] | [Description] | [1-5] | [Quote/data] |
| **Pull** (toward new) | | | |
| [Pull factor 1] | [Description] | [1-5] | [Quote/data] |
| [Pull factor 2] | [Description] | [1-5] | [Quote/data] |
| **Anxiety** (about new) | | | |
| [Anxiety 1] | [Description] | [1-5] | [Quote/data] |
| [Anxiety 2] | [Description] | [1-5] | [Quote/data] |
| **Habit** (of current) | | | |
| [Habit 1] | [Description] | [1-5] | [Quote/data] |
| [Habit 2] | [Description] | [1-5] | [Quote/data] |

**Net Force Calculation**:
- Demand (Push + Pull): [Score]
- Resistance (Anxiety + Habit): [Score]
- **Net**: [Demand - Resistance]

---

## Outcome Statements

### Format
```
[DIRECTION] + [METRIC] + [OBJECT] + [CLARIFIER]

Directions: Minimize, Maximize, Optimize
```

### Examples
```
Minimize the time it takes to [action]
Maximize the accuracy of [outcome]
Minimize the likelihood of [negative outcome]
Maximize the number of [positive outcomes]
```

### Outcome Statement Template

| ID | Outcome Statement | Importance | Satisfaction | Opportunity |
|----|-------------------|------------|--------------|-------------|
| O-001 | Minimize the time to [X] | [1-10] | [1-10] | [I + (I-S)] |
| O-002 | Maximize the [Y] | [1-10] | [1-10] | [I + (I-S)] |
| O-003 | Minimize the likelihood of [Z] | [1-10] | [1-10] | [I + (I-S)] |

**Opportunity Score** = Importance + (Importance - Satisfaction)
- >15: Underserved (high opportunity)
- 10-15: Appropriately served
- <10: Overserved (low opportunity)

---

## JTBD Interview Guide

### Timeline Questions
1. "Walk me through the last time you [did the job]..."
2. "What triggered you to look for a solution?"
3. "What else did you try before this?"
4. "What made you finally decide to [switch/act]?"

### Push/Pull Questions
5. "What wasn't working with your previous approach?"
6. "What got you excited about the new approach?"

### Anxiety/Habit Questions
7. "What concerns did you have about trying something new?"
8. "What made it hard to move away from what you were doing?"

### Outcome Questions
9. "How do you know when you've done this well?"
10. "What would make this perfect?"

---

## Solution Mapping

### Job-to-Solution Matrix

| Job Step | Current Solution | Pain Points | Proposed Solution | Improvement |
|----------|------------------|-------------|-------------------|-------------|
| [Step] | [What they do now] | [Problems] | [Our solution] | [How better] |

### Solution-to-Job Fit

| Solution Feature | Job Step Addressed | Outcome Improved | Fit Score |
|------------------|-------------------|------------------|-----------|
| [Feature] | [Which step] | [Which outcome] | [1-5] |
