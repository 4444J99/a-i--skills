# Session Parsing Guide

Technical patterns for extracting information from SpecStory history files.

## History File Structure

### File Naming Convention

```
2026-01-22_19-20-56Z-fix-authentication-bug.md
│         │        │  └── Session slug (kebab-case)
│         │        └── UTC indicator
│         └── Time (HH-MM-SS)
└── Date (YYYY-MM-DD)
```

### Internal Structure

```markdown
# Session Title

_**User**_

[User message content]

---

_**Assistant**_

[Assistant response]

[Possible tool calls]

[Tool results]

---

_**User**_

[Next user message]

...
```

---

## Message Extraction

### User Messages

Pattern: `_**User**_` followed by content until next `---`

```python
def extract_user_messages(content):
    messages = []
    parts = content.split('_**User**_')

    for i, part in enumerate(parts[1:], 1):
        # Content ends at next delimiter
        end_markers = ['---', '_**Assistant**_', '<function_calls>']
        end_pos = len(part)

        for marker in end_markers:
            pos = part.find(marker)
            if pos != -1 and pos < end_pos:
                end_pos = pos

        message = part[:end_pos].strip()
        messages.append({
            'index': i,
            'content': message,
            'word_count': len(message.split())
        })

    return messages
```

### Assistant Messages

Pattern: `_**Assistant**_` followed by content until next user message or tool call

```python
def extract_assistant_messages(content):
    messages = []
    parts = content.split('_**Assistant**_')

    for part in parts[1:]:
        # Content ends at user message or function call
        end_pos = min(
            part.find('_**User**_') if '_**User**_' in part else len(part),
            part.find('<function_calls>') if '<function_calls>' in part else len(part)
        )

        message = part[:end_pos].strip()
        if message:
            messages.append(message)

    return messages
```

---

## Tool Call Extraction

### Identifying Tool Types

```python
TOOL_PATTERNS = {
    'read': r'<invoke name="Read">',
    'write': r'<invoke name="Write">',
    'edit': r'<invoke name="Edit">',
    'bash': r'<invoke name="Bash">',
    'glob': r'<invoke name="Glob">',
    'grep': r'<invoke name="Grep">',
    'webfetch': r'<invoke name="WebFetch">'
}

def categorize_tool_calls(content):
    counts = {}
    for tool, pattern in TOOL_PATTERNS.items():
        counts[tool] = len(re.findall(pattern, content))
    return counts
```

### Extracting File Paths

From Edit/Write calls:

```python
def extract_modified_files(content):
    files = set()

    # Edit calls
    edit_pattern = r'<invoke name="Edit">\s*<parameter name="file_path">([^<]+)</parameter>'
    files.update(re.findall(edit_pattern, content))

    # Write calls
    write_pattern = r'<invoke name="Write">\s*<parameter name="file_path">([^<]+)</parameter>'
    files.update(re.findall(write_pattern, content))

    return sorted(files)
```

### File Path Cleanup

```python
def shorten_path(path):
    """Convert full path to just filename."""
    parts = path.split('/')
    return parts[-1] if parts else path

def group_by_directory(paths):
    """Group files by parent directory."""
    from collections import defaultdict
    groups = defaultdict(list)

    for path in paths:
        parts = path.split('/')
        if len(parts) > 1:
            dir_name = parts[-2]
            groups[dir_name].append(parts[-1])
        else:
            groups['root'].append(path)

    return dict(groups)
```

---

## Session Intent Detection

### Goal Extraction

```python
def extract_goal(first_user_message):
    """Derive session goal from first user message."""

    # Remove common prefixes
    prefixes_to_remove = [
        r'^(Can you|Could you|Please|I need you to|I want to|Help me)\s+',
        r'^(I need to|I want to|Let\'s)\s+',
    ]

    goal = first_user_message

    for prefix in prefixes_to_remove:
        goal = re.sub(prefix, '', goal, flags=re.IGNORECASE)

    # Capitalize first letter
    if goal:
        goal = goal[0].upper() + goal[1:]

    # Truncate to first sentence or 100 chars
    end_markers = ['. ', '? ', '! ', '\n']
    end_pos = len(goal)
    for marker in end_markers:
        pos = goal.find(marker)
        if pos != -1 and pos < end_pos:
            end_pos = pos

    goal = goal[:min(end_pos, 100)]

    return goal.strip()
```

### Outcome Detection

```python
def detect_outcome(content):
    """Determine session outcome from content analysis."""

    last_500_chars = content[-500:]
    tool_counts = categorize_tool_calls(content)

    # Check for completion indicators
    completion_phrases = [
        'done', 'complete', 'finished', 'successfully',
        'merged', 'deployed', 'pushed', 'committed'
    ]

    if any(phrase in last_500_chars.lower() for phrase in completion_phrases):
        return ('✅', 'Completed')

    # Check if it was research only
    if tool_counts['edit'] == 0 and tool_counts['write'] == 0:
        return ('📚', 'Research only, no code changes')

    # Check for errors
    error_phrases = ['error', 'failed', 'cannot', 'unable', 'blocked']
    if any(phrase in last_500_chars.lower() for phrase in error_phrases):
        return ('🚧', 'Blocked by error')

    # Check session length
    user_messages = content.count('_**User**_')
    if user_messages < 3:
        return ('❌', 'Abandoned early')

    # Default to in progress
    return ('🔧', 'In progress')
```

---

## Key Insight Extraction

### Decision Detection

```python
DECISION_PATTERNS = [
    r'decided to\s+(.+?)(?:\.|$)',
    r'chose\s+(.+?)\s+(?:because|over|instead)',
    r'instead of\s+(.+?),?\s+(?:we|I)',
    r'trade-off:\s*(.+?)(?:\.|$)',
    r'the approach is to\s+(.+?)(?:\.|$)',
]

def extract_decisions(content):
    decisions = []
    for pattern in DECISION_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        decisions.extend(matches)
    return decisions[:3]  # Top 3 decisions
```

### Insight Formatting

```python
def format_insight(decisions, modified_files):
    if decisions:
        return decisions[0].strip()

    if len(modified_files) > 5:
        return f"Touched {len(modified_files)} files across the codebase"

    return None
```

---

## Multi-Task Session Handling

### Detecting Multiple Tasks

```python
def is_multi_task_session(content):
    """Detect if session has multiple distinct tasks."""
    user_positions = [m.start() for m in re.finditer(r'_\*\*User\*\*_', content)]

    if len(user_positions) < 2:
        return False

    # Check if user messages are far apart (different contexts)
    for i in range(1, len(user_positions)):
        gap = user_positions[i] - user_positions[i-1]
        if gap > 5000:  # More than 5000 chars between messages
            return True

    return False
```

### Task Grouping

```python
def group_tasks(content):
    """Group content into distinct task sections."""
    tasks = []
    user_pattern = r'_\*\*User\*\*_\s*\n\n(.+?)(?=_\*\*|$)'

    matches = list(re.finditer(user_pattern, content, re.DOTALL))

    for i, match in enumerate(matches):
        task_content = match.group(1)[:500]  # First 500 chars of each task

        # Find where this task ends
        if i < len(matches) - 1:
            task_end = matches[i + 1].start()
        else:
            task_end = len(content)

        task_section = content[match.start():task_end]

        tasks.append({
            'goal': extract_goal(task_content),
            'outcome': detect_outcome(task_section),
            'files': extract_modified_files(task_section)
        })

    return tasks
```

---

## Large File Handling

### Chunked Reading Strategy

```python
def analyze_large_session(file_path, limit=2000):
    """Analyze large session file efficiently."""

    with open(file_path, 'r') as f:
        content = f.read()

    total_lines = content.count('\n')

    if total_lines <= limit:
        return full_analysis(content)

    # Read strategically
    lines = content.split('\n')

    beginning = '\n'.join(lines[:500])    # First 500 lines
    end = '\n'.join(lines[-300:])          # Last 300 lines

    # Get structure
    user_message_lines = [
        i for i, line in enumerate(lines)
        if '_**User**_' in line
    ]

    # Read around each user message
    user_contexts = []
    for line_num in user_message_lines[:5]:  # First 5 user messages
        start = max(0, line_num - 5)
        end_line = min(len(lines), line_num + 50)
        user_contexts.append('\n'.join(lines[start:end_line]))

    return {
        'beginning': beginning,
        'end': end,
        'user_contexts': user_contexts,
        'total_lines': total_lines,
        'user_message_count': len(user_message_lines)
    }
```

### Memory-Efficient Grep

```python
def grep_in_file(file_path, pattern):
    """Search file without loading entirely into memory."""
    matches = []

    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if re.search(pattern, line):
                matches.append({
                    'line': line_num,
                    'content': line.strip()
                })

    return matches
```

---

## Session Metadata

### Extract Session Info

```python
def get_session_metadata(file_path):
    """Extract metadata from session file."""
    filename = os.path.basename(file_path)

    # Parse filename
    pattern = r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})Z-(.+)\.md'
    match = re.match(pattern, filename)

    if not match:
        return None

    year, month, day, hour, minute, second, slug = match.groups()

    return {
        'date': f'{year}-{month}-{day}',
        'time': f'{hour}:{minute}',
        'datetime': f'{year}-{month}-{day} {hour}:{minute}',
        'slug': slug,
        'title': slug.replace('-', ' ').title(),
        'file_path': file_path,
        'file_size': os.path.getsize(file_path)
    }
```
