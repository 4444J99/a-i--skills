# Yak Shave Scoring Methodology

Technical guide to calculating yak shave scores for AI coding sessions.

## Score Components

### Overview

| Component | Weight | Description |
|-----------|--------|-------------|
| Domain Shifts | 40% | File reference domain changes |
| Goal Completion | 25% | Original intent fulfillment |
| Session Length Ratio | 20% | Effort vs. ask complexity |
| Tool Type Cascade | 15% | Escalation pattern |

**Total Score Range**: 0-100

---

## Domain Shift Analysis (40%)

### What is a Domain?

A domain represents a conceptual area of the codebase:

| Domain | Example Paths | Indicators |
|--------|---------------|------------|
| **ui** | `src/components/`, `styles/` | CSS, JSX, HTML |
| **api** | `src/api/`, `routes/` | Endpoints, handlers |
| **database** | `migrations/`, `models/` | SQL, ORM, schemas |
| **auth** | `src/auth/`, `middleware/` | Auth, tokens, sessions |
| **config** | `config/`, `.env*` | Settings, env vars |
| **build** | `webpack.config.js`, `Dockerfile` | Build tooling |
| **ci** | `.github/`, `.circleci/` | Pipelines |
| **test** | `tests/`, `__tests__/` | Test files |
| **docs** | `README.md`, `docs/` | Documentation |

### Counting Domain Shifts

```python
def count_domain_shifts(file_references):
    """Count transitions between domains."""
    domains = [classify_domain(f) for f in file_references]
    domains = [d for d in domains if d]  # Remove None

    shifts = 0
    for i in range(1, len(domains)):
        if domains[i] != domains[i-1]:
            shifts += 1

    return shifts
```

### Domain Score Calculation

```python
def domain_shift_score(shifts):
    """Convert shift count to 0-100 score."""
    if shifts == 0:
        return 0
    elif shifts == 1:
        return 15
    elif shifts == 2:
        return 35
    elif shifts == 3:
        return 55
    elif shifts == 4:
        return 75
    else:
        return min(100, 75 + (shifts - 4) * 5)
```

---

## Goal Completion Analysis (25%)

### Detecting Original Goal

Extract from first user message:

```python
def extract_original_goal(first_message):
    """Identify the stated objective."""
    # Look for imperative verbs
    goal_patterns = [
        r'^(fix|add|update|refactor|implement|create|debug|optimize|remove)',
        r'(can you|please|help me)\s+(fix|add|update|refactor|implement)',
        r'(need to|want to|should)\s+(fix|add|update|refactor|implement)',
    ]

    for pattern in goal_patterns:
        match = re.search(pattern, first_message, re.IGNORECASE)
        if match:
            return match.group(0)

    return first_message[:100]  # Fallback to first 100 chars
```

### Completion Detection

```python
def detect_goal_completion(content, original_goal):
    """Check if original goal was achieved."""
    last_portion = content[-2000:]

    # Strong completion signals
    completion_signals = [
        'done', 'complete', 'finished', 'working',
        'fixed', 'added', 'updated', 'implemented',
        'committed', 'merged', 'deployed'
    ]

    goal_verbs = extract_verbs(original_goal)

    # Check for matching completion
    for verb in goal_verbs:
        past_tense = get_past_tense(verb)
        if past_tense in last_portion.lower():
            return True

    # Generic completion check
    signal_count = sum(1 for s in completion_signals
                       if s in last_portion.lower())

    return signal_count >= 2
```

### Goal Completion Score

```python
def goal_completion_score(completed, original_domain, final_domain):
    """Score based on goal completion and domain alignment."""
    if completed and original_domain == final_domain:
        return 0  # Perfect - did what was asked
    elif completed and original_domain != final_domain:
        return 40  # Completed but wandered
    elif not completed and original_domain == final_domain:
        return 60  # Didn't finish but stayed focused
    else:
        return 100  # Neither completed nor stayed on track
```

---

## Session Length Ratio (20%)

### Complexity Estimation

```python
def estimate_task_complexity(first_message):
    """Estimate expected session length from request."""

    quick_indicators = ['typo', 'simple', 'quick', 'small', 'minor', 'just']
    medium_indicators = ['add', 'update', 'fix', 'change']
    complex_indicators = ['refactor', 'implement', 'design', 'architecture',
                          'migrate', 'rewrite', 'investigate']

    message_lower = first_message.lower()

    if any(ind in message_lower for ind in quick_indicators):
        return 'quick'  # Expected: < 10 messages
    elif any(ind in message_lower for ind in complex_indicators):
        return 'complex'  # Expected: 20+ messages
    else:
        return 'medium'  # Expected: 10-20 messages
```

### Length Score

```python
def session_length_score(message_count, complexity):
    """Score based on session length vs expected."""

    thresholds = {
        'quick': {'expected': 5, 'max_reasonable': 15},
        'medium': {'expected': 15, 'max_reasonable': 30},
        'complex': {'expected': 25, 'max_reasonable': 50}
    }

    expected = thresholds[complexity]['expected']
    max_reasonable = thresholds[complexity]['max_reasonable']

    if message_count <= expected:
        return 0
    elif message_count <= max_reasonable:
        # Linear scale from 0 to 50
        ratio = (message_count - expected) / (max_reasonable - expected)
        return int(ratio * 50)
    else:
        # Beyond reasonable, scale 50-100
        overage = message_count - max_reasonable
        return min(100, 50 + overage * 2)
```

---

## Tool Type Cascade (15%)

### Escalation Pattern

Tools naturally escalate during yak shaving:

```
Read → Search → Edit → Create → Deploy
  0      20       40      60       80
```

### Detecting Escalation

```python
TOOL_ESCALATION = {
    'Read': 0,
    'Grep': 10,
    'Glob': 10,
    'WebFetch': 20,
    'Edit': 30,
    'Write': 40,
    'Bash': 50,  # Could be anything
}

def tool_cascade_score(tool_calls):
    """Score based on tool escalation pattern."""
    if not tool_calls:
        return 0

    max_tool_level = 0
    for call in tool_calls:
        level = TOOL_ESCALATION.get(call['name'], 25)
        max_tool_level = max(max_tool_level, level)

    # Check for specific escalation patterns
    has_read = any(t['name'] == 'Read' for t in tool_calls)
    has_edit = any(t['name'] == 'Edit' for t in tool_calls)
    has_write = any(t['name'] == 'Write' for t in tool_calls)
    has_bash = any(t['name'] == 'Bash' for t in tool_calls)

    # Escalation from read-only to file creation is a red flag
    if has_read and has_write and not has_edit:
        max_tool_level = max(max_tool_level, 60)

    # Heavy bash usage often indicates environment yak shaving
    bash_count = sum(1 for t in tool_calls if t['name'] == 'Bash')
    if bash_count > 10:
        max_tool_level = max(max_tool_level, 70)

    return max_tool_level
```

---

## Final Score Calculation

```python
def calculate_yak_shave_score(session):
    """Calculate overall yak shave score."""

    # Component scores (0-100 each)
    domain_score = domain_shift_score(session['domain_shifts'])
    completion_score = goal_completion_score(
        session['goal_completed'],
        session['original_domain'],
        session['final_domain']
    )
    length_score = session_length_score(
        session['message_count'],
        session['complexity']
    )
    tool_score = tool_cascade_score(session['tool_calls'])

    # Weighted average
    final_score = (
        domain_score * 0.40 +
        completion_score * 0.25 +
        length_score * 0.20 +
        tool_score * 0.15
    )

    return round(final_score)
```

---

## Score Interpretation

| Range | Label | Description |
|-------|-------|-------------|
| 0-20 | Laser Focused | Stayed on task, efficient |
| 21-40 | Minor Tangents | Brief detours, returned to goal |
| 41-60 | Moderate Drift | Noticeable wandering |
| 61-80 | Significant Yak Shaving | Lost original thread |
| 81-100 | Epic Rabbit Hole | Completely derailed |

### Score Breakdown Report

```
Session: "fix button alignment"
Overall Score: 87/100 (Epic Rabbit Hole)

Components:
  Domain Shifts:    95/100 (40%) → ui → build → docker → k8s
  Goal Completion:  80/100 (25%) → Original goal not completed
  Session Length:   70/100 (20%) → 45 messages for "quick fix"
  Tool Cascade:     90/100 (15%) → Escalated to deployment tools

Verdict: Started with CSS, ended configuring Kubernetes.
```

---

## Pattern Detection

### Common Yak Shave Patterns

```python
YAK_SHAVE_PATTERNS = {
    'environment_spiral': {
        'trigger': ['version', 'install', 'dependency'],
        'domains': ['config', 'build', 'ci'],
        'description': 'Environment setup rabbit hole'
    },
    'debugging_cascade': {
        'trigger': ['error', 'bug', 'fix'],
        'domains': ['*', 'test', 'config'],
        'description': 'Bug led to unrelated investigation'
    },
    'scope_creep': {
        'trigger': ['while we\'re at it', 'might as well', 'also'],
        'domains': ['any', 'many'],
        'description': 'Task expanded beyond original scope'
    },
    'perfectionism': {
        'trigger': ['refactor', 'clean up', 'improve'],
        'domains': ['same', 'same', 'same'],
        'description': 'Excessive polish on tangential code'
    }
}
```

### Detecting Trigger Phrases

```python
def detect_yak_shave_triggers(content):
    """Find phrases that indicate yak shaving."""
    triggers = []

    trigger_phrases = [
        'but first',
        'before I can',
        'need to',
        'have to',
        'wait, I need',
        'actually',
        'turns out',
        'hmm',
        'oh, that\'s because'
    ]

    for phrase in trigger_phrases:
        if phrase in content.lower():
            triggers.append(phrase)

    return triggers
```
