---
name: data-backup-patterns
description: Implement reliable data backup and recovery strategies with automated scheduling, encryption, rotation policies, and disaster recovery testing. Covers database backups, file system snapshots, and cloud storage patterns. Triggers on backup strategy, disaster recovery, or data protection requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - backup
  - disaster-recovery
  - data-protection
  - automation
  - encryption
governance_phases: [build, prove]
governance_norm_group: security-baseline
organ_affinity: [all]
triggers: [user-asks-about-backup, context:disaster-recovery, context:data-protection, context:backup-strategy]
complements: [docker-containerization, configuration-management, deployment-cicd]
---

# Data Backup Patterns

Protect data with automated, tested, and recoverable backup strategies.

## Backup Strategy Framework

### The 3-2-1 Rule

- **3** copies of data (1 primary + 2 backups)
- **2** different storage media/types
- **1** offsite copy

### Backup Types

| Type | Speed | Storage | Recovery | When |
|------|-------|---------|----------|------|
| **Full** | Slow | Large | Fast | Weekly |
| **Incremental** | Fast | Small | Slow (needs chain) | Daily |
| **Differential** | Medium | Medium | Medium (needs last full) | Daily |
| **Snapshot** | Instant | Varies | Fast | Hourly |

## Database Backups

### PostgreSQL

```bash
#!/usr/bin/env bash
set -euo pipefail

DB_NAME="${DB_NAME:?}"
BACKUP_DIR="${BACKUP_DIR:-/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

# Full backup with compression
pg_dump "$DB_NAME" \
  --format=custom \
  --compress=9 \
  --file="${BACKUP_FILE}"

# Verify backup is valid
pg_restore --list "${BACKUP_FILE}" > /dev/null

echo "Backup created: ${BACKUP_FILE} ($(du -h "${BACKUP_FILE}" | cut -f1))"
```

### Point-in-Time Recovery (WAL Archiving)

```bash
# postgresql.conf
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'

# Restore to specific time
restore_command = 'cp /archive/wal/%f %p'
recovery_target_time = '2026-03-20 10:00:00'
```

### Redis

```bash
# Trigger RDB snapshot
redis-cli BGSAVE

# Or use AOF for point-in-time recovery
# redis.conf
appendonly yes
appendfsync everysec
```

## File System Backups

### Rsync-Based

```bash
#!/usr/bin/env bash
set -euo pipefail

SOURCE="/data"
DEST="/backups/daily"
LATEST="${DEST}/latest"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TARGET="${DEST}/${TIMESTAMP}"

# Incremental backup using hard links
rsync -av --delete \
  --link-dest="${LATEST}" \
  "${SOURCE}/" "${TARGET}/"

# Update latest symlink
ln -snf "${TARGET}" "${LATEST}"

echo "Backup complete: ${TARGET}"
```

### Exclusion Patterns

```
# .backup-exclude
.git/
node_modules/
.venv/
__pycache__/
*.pyc
.env.local
*.secret
tmp/
.build/
```

## Encryption

### GPG Encryption

```bash
# Encrypt backup
gpg --symmetric --cipher-algo AES256 \
  --output "${BACKUP_FILE}.gpg" \
  "${BACKUP_FILE}"

# Decrypt for restore
gpg --decrypt "${BACKUP_FILE}.gpg" > "${BACKUP_FILE}"
```

### Age Encryption (Modern Alternative)

```bash
# Generate key pair
age-keygen -o key.txt

# Encrypt
age -r age1xxxxxx -o backup.sql.age backup.sql

# Decrypt
age -d -i key.txt backup.sql.age > backup.sql
```

## Rotation Policies

```python
from pathlib import Path
from datetime import datetime, timedelta

class BackupRotator:
    def __init__(self, backup_dir: str, keep_daily: int = 7, keep_weekly: int = 4, keep_monthly: int = 12):
        self.backup_dir = Path(backup_dir)
        self.keep_daily = keep_daily
        self.keep_weekly = keep_weekly
        self.keep_monthly = keep_monthly

    def rotate(self):
        backups = sorted(self.backup_dir.glob("*.sql.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
        now = datetime.now()
        keep = set()

        # Keep recent daily
        for b in backups[:self.keep_daily]:
            keep.add(b)

        # Keep weekly (one per week)
        for week in range(self.keep_weekly):
            target = now - timedelta(weeks=week)
            closest = min(backups, key=lambda b: abs(datetime.fromtimestamp(b.stat().st_mtime) - target))
            keep.add(closest)

        # Keep monthly (one per month)
        for month in range(self.keep_monthly):
            target = now - timedelta(days=30 * month)
            closest = min(backups, key=lambda b: abs(datetime.fromtimestamp(b.stat().st_mtime) - target))
            keep.add(closest)

        # Remove the rest
        for backup in backups:
            if backup not in keep:
                backup.unlink()
```

## Cloud Storage

### S3-Compatible Upload

```bash
#!/usr/bin/env bash
set -euo pipefail

BUCKET="${BACKUP_BUCKET:?}"
PREFIX="backups/$(date +%Y/%m)"

# Upload with server-side encryption
aws s3 cp "${BACKUP_FILE}" \
  "s3://${BUCKET}/${PREFIX}/$(basename ${BACKUP_FILE})" \
  --storage-class STANDARD_IA \
  --sse AES256

# Set lifecycle policy for automatic archival
# (configure once in S3 lifecycle rules)
# 30 days → Glacier, 365 days → Deep Archive
```

## Automated Scheduling

### Cron/Launchd

```bash
# crontab
0 2 * * * /scripts/backup-daily.sh >> /var/log/backup.log 2>&1
0 3 * * 0 /scripts/backup-weekly.sh >> /var/log/backup.log 2>&1
```

```xml
<!-- ~/Library/LaunchAgents/com.backup.daily.plist -->
<plist version="1.0">
<dict>
    <key>Label</key><string>com.backup.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/scripts/backup-daily.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>2</integer>
        <key>Minute</key><integer>0</integer>
    </dict>
</dict>
</plist>
```

## Recovery Testing

### Automated Recovery Test

```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_FILE="${1:?Usage: test-restore.sh <backup-file>}"
TEST_DB="restore_test_$(date +%s)"

# Restore to test database
createdb "${TEST_DB}"
pg_restore --dbname="${TEST_DB}" "${BACKUP_FILE}"

# Verify data integrity
ROW_COUNT=$(psql -t -c "SELECT count(*) FROM repos" "${TEST_DB}")
if [[ "${ROW_COUNT}" -lt 50 ]]; then
    echo "FAIL: Expected 50+ repos, got ${ROW_COUNT}"
    dropdb "${TEST_DB}"
    exit 1
fi

echo "PASS: Restored ${ROW_COUNT} repos successfully"
dropdb "${TEST_DB}"
```

## Anti-Patterns

- **Untested backups** — A backup you haven't restored is not a backup
- **No encryption for sensitive data** — Always encrypt backups at rest
- **Single location** — Follow the 3-2-1 rule
- **No rotation** — Unbounded backup growth fills storage
- **Manual-only backups** — Automate everything; manual backups get forgotten
- **No monitoring** — Alert on backup failures immediately
