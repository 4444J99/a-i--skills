# SpecStory Project Stats

A Claude Code skill that fetches project statistics for the current project from SpecStory's cloud platform.

## Overview

This skill automatically determines your project ID and fetches statistics from the SpecStory API. The project ID is calculated using a deterministic algorithm that ensures consistency across different environments.

## Project ID Calculation

The skill determines the project ID using the following priority:

1. **`.specstory/.project.json`**: If this file exists, it uses:
   - `git_id` field (preferred)
   - `workspace_id` field (fallback)

2. **Git Repository**: If no project JSON exists, it extracts the repository name from `.git/config` (remote "origin")

3. **Folder Name**: If no git repository is found, it uses the current folder name

The identifier is then hashed using SHA256, truncated to 16 characters, and formatted as `xxxx-xxxx-xxxx-xxxx`.

## Usage

### As a Claude Code Skill

Simply invoke the skill:
```
/specstory-project-stats
```

### Direct Script Execution

You can also run the script directly:
```bash
node skills/specstory-project-stats/scripts/get-stats.js
```

### Custom API Endpoint

To use a different SpecStory API endpoint (e.g., production):
```bash
SPECSTORY_API_URL=https://cloud.specstory.com node skills/specstory-project-stats/scripts/get-stats.js
```

By default, the script uses `https://cloud.specstory.com`, for local development you can override it with `SPECSTORY_API_URL=http://localhost:5173`.

## API Endpoint

The skill calls:
```
{baseUrl}/api/v1/projects/{projectId}/stats
```

Where:
- `baseUrl` defaults to `https://cloud.specstory.com` (configurable via `SPECSTORY_API_URL`, use `http://localhost:5173` for local development)
- `projectId` is calculated as described above

## Requirements

- Node.js (uses built-in modules: `fs`, `path`, `crypto`, `https`)
- No external dependencies required

## Files

- `scripts/get-stats.js`: Main script that calculates project ID and fetches stats
- `SKILL.md`: Claude Code skill instructions
- `README.md`: This documentation file

## Example Output

```
Project ID: a1b2-c3d4-e5f6-7890
Fetching stats from: https://cloud.specstory.com/api/v1/projects/a1b2-c3d4-e5f6-7890/stats

Stats:
{
  "project": "example/repo",
  "total_commits": 1234,
  "contributors": 56,
  ...
}
```

## Error Handling

The script will exit with an error if:
- The API endpoint is unreachable
- The API returns a non-200 status code
- The response cannot be parsed as JSON

Error messages will include helpful context for debugging.
