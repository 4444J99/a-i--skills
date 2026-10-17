# History Organization Patterns

Strategies for organizing SpecStory session history files.

## Directory Structures

### By Date (Default)

```
.specstory/history/
├── 2026/
│   ├── 01/
│   │   ├── 2026-01-15_10-30-22Z-refactor-auth.md
│   │   ├── 2026-01-15_14-22-01Z-fix-tests.md
│   │   └── 2026-01-22_19-20-56Z-add-feature.md
│   └── 02/
│       └── ...
└── 2025/
    ├── 12/
    │   └── ...
    └── 11/
        └── ...
```

**Pros:**
- Natural chronological browsing
- Easy to archive old months
- Works with standard file managers

**Cons:**
- Hard to find sessions by topic
- Active projects span multiple folders

### By Project/Feature

```
.specstory/history/
├── auth-system/
│   ├── 2026-01-15_refactor.md
│   ├── 2026-01-20_fix-bug.md
│   └── 2026-01-22_add-oauth.md
├── database/
│   ├── 2026-01-10_migration.md
│   └── 2026-01-18_optimize-queries.md
└── unsorted/
    └── ...
```

**Pros:**
- Topic-based browsing
- Related sessions together
- Good for documentation

**Cons:**
- Requires manual categorization
- Sessions may fit multiple categories

### Hybrid: Date + Topic Tags

```
.specstory/history/
├── 2026/
│   └── 01/
│       ├── 2026-01-15_10-30-22Z-refactor-auth.md
│       └── 2026-01-22_19-20-56Z-add-feature.md
└── .tags/
    ├── auth.txt          # Lists all auth-related sessions
    ├── database.txt      # Lists database sessions
    └── urgent.txt        # Priority sessions
```

**Pros:**
- Chronological storage
- Multiple categorizations possible
- Non-destructive tagging

---

## Filename Parsing

### Standard Format

```
2026-01-22_19-20-56Z-fix-authentication-bug.md
│         │        │  └── Session description (slugified)
│         │        └── Timezone indicator
│         └── Time (HH-MM-SS)
└── Date (YYYY-MM-DD)
```

### Parsing Regex

```python
FILENAME_PATTERN = r'''
    ^(?P<year>\d{4})-
    (?P<month>\d{2})-
    (?P<day>\d{2})_
    (?P<hour>\d{2})-
    (?P<minute>\d{2})-
    (?P<second>\d{2})Z-
    (?P<slug>.+)\.md$
'''
```

### Edge Cases

| Filename | Issue | Handling |
|----------|-------|----------|
| `notes.md` | No date | Skip or move to `unsorted/` |
| `2026-01-22.md` | No time | Use `00-00-00` |
| `2026-01-22_10-30.md` | Partial time | Use `10-30-00` |
| `session-notes-jan.md` | No parseable date | Use file mtime |

---

## File Operations

### Safe Move Pattern

```python
import shutil
from pathlib import Path

def safe_move(src, dest_dir):
    """Move file with collision handling."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = dest_dir / src.name

    # Handle collision
    if dest.exists():
        counter = 1
        while dest.exists():
            stem = src.stem
            dest = dest_dir / f"{stem}_{counter}{src.suffix}"
            counter += 1

    shutil.move(str(src), str(dest))
    return dest
```

### Dry Run Implementation

```python
def organize_dry_run(history_dir):
    """Preview organization without making changes."""
    moves = []

    for file in Path(history_dir).glob('*.md'):
        parsed = parse_filename(file.name)
        if parsed:
            dest = f"{parsed['year']}/{parsed['month']:02d}/"
            moves.append({
                'file': file.name,
                'from': str(file.parent),
                'to': dest
            })

    return moves
```

---

## Incremental Organization

### Track Organized Files

```python
MARKER_FILE = '.specstory/history/.organized'

def get_organized_files():
    """Return set of already-organized files."""
    marker = Path(MARKER_FILE)
    if marker.exists():
        return set(marker.read_text().splitlines())
    return set()

def mark_as_organized(files):
    """Record files that have been organized."""
    marker = Path(MARKER_FILE)
    existing = get_organized_files()
    existing.update(files)
    marker.write_text('\n'.join(sorted(existing)))
```

### Skip Already-Organized

```python
def find_files_to_organize(history_dir):
    """Find only files needing organization."""
    organized = get_organized_files()
    all_files = Path(history_dir).glob('*.md')

    # Only return files in root (not in subdirs) that aren't marked
    return [f for f in all_files
            if f.parent.name == 'history'
            and f.name not in organized]
```

---

## Archiving Old Sessions

### Archive Threshold

```python
from datetime import datetime, timedelta

def find_archivable_sessions(history_dir, days_old=90):
    """Find sessions older than threshold."""
    cutoff = datetime.now() - timedelta(days=days_old)
    archivable = []

    for file in Path(history_dir).rglob('*.md'):
        parsed = parse_filename(file.name)
        if parsed:
            session_date = datetime(
                int(parsed['year']),
                int(parsed['month']),
                int(parsed['day'])
            )
            if session_date < cutoff:
                archivable.append(file)

    return archivable
```

### Compression

```python
import tarfile
from pathlib import Path

def archive_month(history_dir, year, month):
    """Create compressed archive of a month's sessions."""
    month_dir = Path(history_dir) / str(year) / f"{month:02d}"
    if not month_dir.exists():
        return None

    archive_name = f"specstory-{year}-{month:02d}.tar.gz"
    archive_path = Path(history_dir) / 'archives' / archive_name

    archive_path.parent.mkdir(exist_ok=True)

    with tarfile.open(archive_path, 'w:gz') as tar:
        tar.add(month_dir, arcname=f"{year}/{month:02d}")

    return archive_path
```

---

## Summary Statistics

### After Organization

```python
def generate_summary(history_dir):
    """Generate organization summary."""
    stats = {
        'total_files': 0,
        'by_month': {},
        'oldest': None,
        'newest': None
    }

    for file in Path(history_dir).rglob('*.md'):
        stats['total_files'] += 1
        parsed = parse_filename(file.name)

        if parsed:
            key = f"{parsed['year']}/{parsed['month']:02d}"
            stats['by_month'][key] = stats['by_month'].get(key, 0) + 1

            date = f"{parsed['year']}-{parsed['month']}-{parsed['day']}"
            if stats['oldest'] is None or date < stats['oldest']:
                stats['oldest'] = date
            if stats['newest'] is None or date > stats['newest']:
                stats['newest'] = date

    return stats
```

### Report Template

```markdown
## Organization Summary

**Total Sessions:** {total_files}
**Date Range:** {oldest} to {newest}

### By Month
| Month | Sessions |
|-------|----------|
{by_month_rows}

### Actions Taken
- Files moved: {moved_count}
- Directories created: {dirs_created}
- Skipped (no date): {skipped_count}
```

---

## Maintenance Tasks

### Periodic Cleanup

| Task | Frequency | Command |
|------|-----------|---------|
| Organize new files | Weekly | `/specstory-organize` |
| Archive old months | Monthly | Custom archive script |
| Verify structure | Quarterly | Validation script |
| Remove empty dirs | As needed | `find . -type d -empty -delete` |

### Health Checks

```python
def check_history_health(history_dir):
    """Validate history directory structure."""
    issues = []

    # Check for files in wrong locations
    for file in Path(history_dir).glob('*.md'):
        parsed = parse_filename(file.name)
        if parsed:
            expected_dir = Path(history_dir) / parsed['year'] / f"{parsed['month']:02d}"
            if file.parent != expected_dir:
                issues.append(f"Misplaced: {file.name}")

    # Check for empty directories
    for dir in Path(history_dir).rglob('*'):
        if dir.is_dir() and not any(dir.iterdir()):
            issues.append(f"Empty directory: {dir}")

    return issues
```
