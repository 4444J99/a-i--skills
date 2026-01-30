# SpecStory Cloud API Reference

API endpoints and data structures for fetching project statistics.

## Base URL

```
Production: https://cloud.specstory.com
Development: http://localhost:5173
```

Override with environment variable:
```bash
SPECSTORY_API_URL=https://your-instance.com
```

---

## Endpoints

### Get Project Stats

```
GET /api/v1/projects/{project_id}/stats
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | string | Project identifier (e.g., `owner/repo`) |

**Response:**

```json
{
  "project_id": "specstoryai/agent-skills",
  "sessions": {
    "total": 156,
    "last_30_days": 47,
    "last_7_days": 12
  },
  "contributors": {
    "total": 5,
    "active_last_30_days": 3
  },
  "activity": {
    "first_session": "2025-10-15",
    "last_session": "2026-01-28",
    "avg_sessions_per_week": 8.2
  }
}
```

### Get Project Info

```
GET /api/v1/projects/{project_id}
```

**Response:**

```json
{
  "project_id": "specstoryai/agent-skills",
  "name": "Agent Skills",
  "visibility": "public",
  "created_at": "2025-10-15T10:30:00Z",
  "last_sync": "2026-01-28T14:22:00Z"
}
```

### List Project Sessions

```
GET /api/v1/projects/{project_id}/sessions
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | 20 | Max results per page |
| `offset` | int | 0 | Pagination offset |
| `from` | string | - | Start date (YYYY-MM-DD) |
| `to` | string | - | End date (YYYY-MM-DD) |

**Response:**

```json
{
  "sessions": [
    {
      "id": "abc123",
      "title": "Fix authentication bug",
      "started_at": "2026-01-28T14:22:00Z",
      "duration_minutes": 45,
      "contributor": "user@example.com"
    }
  ],
  "total": 156,
  "has_more": true
}
```

---

## Project ID Resolution

### Resolution Order

1. `.specstory/.project.json` - Explicit project configuration
2. Git remote URL - Derived from `origin` remote
3. Directory name - Fallback to folder name

### Project JSON Format

```json
{
  "git_id": "github.com/owner/repo",
  "workspace_id": "ws_abc123",
  "sync_enabled": true
}
```

### Git Remote Parsing

```javascript
function parseGitRemote(remoteUrl) {
  // SSH format: git@github.com:owner/repo.git
  // HTTPS format: https://github.com/owner/repo.git

  const patterns = [
    /git@([^:]+):([^\/]+)\/(.+?)(?:\.git)?$/,
    /https?:\/\/([^\/]+)\/([^\/]+)\/(.+?)(?:\.git)?$/
  ];

  for (const pattern of patterns) {
    const match = remoteUrl.match(pattern);
    if (match) {
      return `${match[1]}/${match[2]}/${match[3]}`;
    }
  }
  return null;
}
```

---

## Error Responses

### 404 Not Found

```json
{
  "error": "project_not_found",
  "message": "Project 'owner/repo' does not exist or has no synced sessions",
  "suggestion": "Run 'specstory sync' to push your local sessions"
}
```

### 401 Unauthorized

```json
{
  "error": "unauthorized",
  "message": "Authentication required for private project statistics"
}
```

### 429 Rate Limited

```json
{
  "error": "rate_limited",
  "message": "Too many requests. Please wait before retrying.",
  "retry_after": 60
}
```

### 500 Server Error

```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred",
  "request_id": "req_abc123"
}
```

---

## Response Data Types

### Session Statistics

| Field | Type | Description |
|-------|------|-------------|
| `total` | int | All-time session count |
| `last_30_days` | int | Sessions in past 30 days |
| `last_7_days` | int | Sessions in past week |

### Contributor Statistics

| Field | Type | Description |
|-------|------|-------------|
| `total` | int | Unique contributors ever |
| `active_last_30_days` | int | Active in past 30 days |

### Activity Statistics

| Field | Type | Description |
|-------|------|-------------|
| `first_session` | string | Date of first session (YYYY-MM-DD) |
| `last_session` | string | Date of most recent session |
| `avg_sessions_per_week` | float | Average weekly session count |

---

## Request Examples

### cURL

```bash
# Get project stats
curl https://cloud.specstory.com/api/v1/projects/specstoryai/agent-skills/stats

# With custom endpoint
curl ${SPECSTORY_API_URL}/api/v1/projects/owner/repo/stats
```

### JavaScript (fetch)

```javascript
async function getProjectStats(projectId) {
  const baseUrl = process.env.SPECSTORY_API_URL || 'https://cloud.specstory.com';
  const response = await fetch(`${baseUrl}/api/v1/projects/${projectId}/stats`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }

  return response.json();
}
```

### Node.js Script

```javascript
const https = require('https');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function getStats() {
  // 1. Resolve project ID
  let projectId = resolveProjectId();

  // 2. Fetch stats
  const stats = await fetchStats(projectId);

  // 3. Output
  console.log(JSON.stringify(stats, null, 2));
}

function resolveProjectId() {
  // Try .project.json first
  const projectJsonPath = '.specstory/.project.json';
  if (fs.existsSync(projectJsonPath)) {
    const config = JSON.parse(fs.readFileSync(projectJsonPath, 'utf8'));
    if (config.git_id) return config.git_id;
    if (config.workspace_id) return config.workspace_id;
  }

  // Try git remote
  try {
    const remote = execSync('git remote get-url origin', { encoding: 'utf8' }).trim();
    const parsed = parseGitRemote(remote);
    if (parsed) return parsed;
  } catch (e) {
    // No git remote
  }

  // Fallback to directory name
  return path.basename(process.cwd());
}
```

---

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/stats` | 60 requests | per minute |
| `/sessions` | 30 requests | per minute |
| `/projects` | 100 requests | per minute |

### Handling Rate Limits

```javascript
async function fetchWithRetry(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url);

    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After') || 60;
      await sleep(retryAfter * 1000);
      continue;
    }

    return response;
  }
  throw new Error('Max retries exceeded');
}
```

---

## Webhooks (Coming Soon)

Subscribe to project events:

```json
{
  "event": "session.created",
  "project_id": "owner/repo",
  "session": {
    "id": "abc123",
    "title": "New feature",
    "started_at": "2026-01-28T14:22:00Z"
  }
}
```

Available events:
- `session.created` - New session synced
- `session.updated` - Session content updated
- `project.stats_updated` - Statistics refreshed
