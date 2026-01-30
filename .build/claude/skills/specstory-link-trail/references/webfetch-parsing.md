# WebFetch Parsing Guide

Technical reference for extracting WebFetch tool calls from SpecStory history files.

## SpecStory History Format

### File Structure

SpecStory history files are markdown documents with tool calls embedded in XML-like blocks. User messages are marked with `_**User**_` and assistant responses include function calls and results.

### WebFetch Tool Call Pattern

```xml
<function_calls>
<invoke name="WebFetch">
<parameter name="url">https://example.com/page</parameter>
<parameter name="prompt">Extract relevant information</parameter>
</invoke>
</function_calls>
```

### WebFetch Result Pattern

```xml
<function_results>
<result>
<name>WebFetch</name>
<output>
[Content or error message]
</output>
</result>
</function_results>
```

---

## Parsing Strategies

### Regex-Based Extraction

```python
import re

# Extract WebFetch URLs
url_pattern = r'<invoke name="WebFetch">\s*<parameter name="url">([^<]+)</parameter>'
urls = re.findall(url_pattern, content)

# Extract with context (prompt)
full_pattern = r'''<invoke name="WebFetch">\s*
<parameter name="url">([^<]+)</parameter>\s*
<parameter name="prompt">([^<]+)</parameter>'''
matches = re.findall(full_pattern, content, re.MULTILINE)
```

### Line-by-Line Parsing

```python
def parse_webfetch(file_path):
    results = []
    current_url = None
    in_webfetch = False

    for line in open(file_path):
        if 'invoke name="WebFetch"' in line:
            in_webfetch = True
        elif in_webfetch and 'parameter name="url"' in line:
            match = re.search(r'>([^<]+)<', line)
            if match:
                current_url = match.group(1)
                results.append({'url': current_url, 'line': line_num})
        elif '</invoke>' in line:
            in_webfetch = False

    return results
```

---

## URL Extraction Patterns

### Standard WebFetch

```
Input: <parameter name="url">https://docs.python.org/3/</parameter>
Output: https://docs.python.org/3/
```

### URL with Query Parameters

```
Input: <parameter name="url">https://api.github.com/repos?page=2</parameter>
Output: https://api.github.com/repos?page=2
```

### Encoded URLs

```python
from urllib.parse import unquote

# Handle URL encoding
encoded_url = "https://example.com/path%20with%20spaces"
decoded_url = unquote(encoded_url)
# Result: https://example.com/path with spaces
```

---

## Result Status Detection

### Success Indicators

```python
def is_successful_fetch(result_text):
    failure_patterns = [
        'Error:',
        '403 Forbidden',
        '404 Not Found',
        'Connection refused',
        'Timeout',
        'SSL Error',
        'Could not fetch',
    ]
    return not any(p in result_text for p in failure_patterns)
```

### Status Code Extraction

```python
def extract_status_code(result_text):
    # Pattern: "HTTP 404" or "Status: 404" or "returned 404"
    patterns = [
        r'HTTP\s*(\d{3})',
        r'Status:\s*(\d{3})',
        r'returned\s*(\d{3})',
        r'(\d{3})\s*(Forbidden|Not Found|Error)',
    ]
    for pattern in patterns:
        match = re.search(pattern, result_text)
        if match:
            return int(match.group(1))
    return 200  # Assume success if no error found
```

---

## Session Context Extraction

### Session Title from Filename

```python
def parse_session_from_filename(filename):
    # Format: 2026-01-22_19-20-56Z-fix-authentication-bug.md
    pattern = r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})Z-(.+)\.md'
    match = re.match(pattern, filename)
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2).replace('-', ':'),
            'title': match.group(3).replace('-', ' ').title()
        }
    return None
```

### Session Title from Content

```python
def extract_session_title(content):
    # Look for first heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1)
    return None
```

---

## Deduplication

### URL Normalization

```python
from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)
    # Lowercase host
    normalized = parsed._replace(
        netloc=parsed.netloc.lower(),
        # Remove trailing slash from path
        path=parsed.path.rstrip('/') or '/'
    )
    return urlunparse(normalized)
```

### Counting Duplicates

```python
from collections import Counter

def count_url_fetches(urls):
    normalized = [normalize_url(u) for u in urls]
    return Counter(normalized)
```

---

## Output Formats

### JSON Output

```json
{
  "session": "fix-authentication-bug",
  "date": "2026-01-22",
  "urls": [
    {
      "url": "https://docs.github.com/en/rest",
      "status": 200,
      "fetch_count": 2,
      "first_line": 142
    },
    {
      "url": "https://internal.company.com/api",
      "status": 403,
      "fetch_count": 1,
      "first_line": 289
    }
  ],
  "summary": {
    "total_fetches": 3,
    "successful": 2,
    "failed": 1
  }
}
```

### Markdown Report

```markdown
## Session: Fix Authentication Bug (2026-01-22)

### Successful Fetches
- https://docs.github.com/en/rest (x2)

### Failed Fetches
- https://internal.company.com/api (403 Forbidden)

### Summary
- Total fetches: 3
- Success rate: 67%
```

---

## Edge Cases

### Multi-line Parameter Values

```python
# Some URLs may span multiple lines in malformed history
def extract_multiline_url(content, start_pos):
    # Find closing tag, handling newlines
    end_pos = content.find('</parameter>', start_pos)
    if end_pos > start_pos:
        url = content[start_pos:end_pos].strip()
        return url.replace('\n', '')
    return None
```

### Escaped Characters

```python
def unescape_url(url):
    replacements = [
        ('&amp;', '&'),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&quot;', '"'),
    ]
    for old, new in replacements:
        url = url.replace(old, new)
    return url
```

### Truncated History Files

```python
def validate_history_file(content):
    # Check for proper structure
    has_user = '_**User**_' in content
    has_function = '<function_calls>' in content or '<function_results>' in content
    is_complete = content.strip().endswith(('```', '---', '.', '?', '!'))

    return {
        'valid': has_user,
        'has_tool_calls': has_function,
        'appears_complete': is_complete
    }
```

---

## Performance Considerations

### Large File Handling

```python
def stream_parse_webfetch(file_path):
    """Memory-efficient parsing for large history files."""
    buffer = []
    in_function_call = False

    with open(file_path, 'r') as f:
        for line in f:
            if '<function_calls>' in line:
                in_function_call = True
                buffer = [line]
            elif in_function_call:
                buffer.append(line)
                if '</function_calls>' in line:
                    yield ''.join(buffer)
                    in_function_call = False
                    buffer = []
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def parse_all_sessions(history_dir):
    files = list(Path(history_dir).glob('*.md'))

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(parse_single_file, files))

    return results
```
