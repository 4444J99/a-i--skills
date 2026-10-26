---
name: social-media-api-integration
description: Integrate with social media platform APIs for automated posting, scheduling, analytics retrieval, and content syndication. Covers OAuth flows, rate limiting, and multi-platform strategies. Triggers on social media API integration, automated posting, or platform API requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - social-media
  - api-integration
  - automation
  - oauth
  - content-syndication
governance_phases: [build]
organ_affinity: [organ-vii]
triggers: [user-asks-about-social-media-api, context:social-posting, context:content-syndication, context:social-automation]
complements: [oauth-flow-architect, content-distribution, essay-publishing-pipeline, webhook-integration-patterns]
---

# Social Media API Integration

Build reliable integrations with social platform APIs for automated content distribution.

## Platform API Overview

| Platform | API Style | Auth | Rate Limits | Key Constraint |
|----------|-----------|------|-------------|----------------|
| Bluesky | AT Protocol | App password / OAuth | 3000/5min | Decentralized, open protocol |
| Mastodon | REST | OAuth 2.0 | 300/5min per IP | Instance-specific endpoints |
| LinkedIn | REST | OAuth 2.0 | 100/day posts | Strict content policies |
| Dev.to | REST | API Key | 30/30s | Article-focused |
| Medium | REST | OAuth 2.0 + Bearer | 100/day | Import API only |
| RSS | Pull-based | None | N/A | Read-only syndication |

## Authentication Patterns

### OAuth 2.0 Flow (LinkedIn, Mastodon)

```python
from authlib.integrations.httpx_client import AsyncOAuth2Client

class SocialOAuth:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client = AsyncOAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )

    def get_auth_url(self, scope: str) -> str:
        url, state = self.client.create_authorization_url(
            "https://platform.example.com/oauth/authorize",
            scope=scope,
        )
        return url

    async def exchange_code(self, code: str) -> dict:
        token = await self.client.fetch_token(  # allow-secret
            "https://platform.example.com/oauth/token",
            code=code,
        )
        return token
```

### API Key Authentication (Dev.to, Bluesky)

```python
import httpx

class DevToClient:
    def __init__(self, api_key: str):  # allow-secret
        self.client = httpx.AsyncClient(
            base_url="https://dev.to/api",
            headers={"api-key": api_key, "Accept": "application/json"},
        )

    async def create_article(self, title: str, body: str, tags: list[str], published: bool = False):
        return await self.client.post("/articles", json={
            "article": {
                "title": title,
                "body_markdown": body,
                "tags": tags,
                "published": published,
            }
        })
```

## Multi-Platform Posting

### Content Adapter Pattern

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Post:
    title: str
    body: str
    url: str | None = None
    tags: list[str] | None = None
    image_url: str | None = None

class PlatformAdapter(ABC):
    @abstractmethod
    async def publish(self, post: Post) -> str:
        """Publish and return the post URL."""

    @abstractmethod
    def format_content(self, post: Post) -> dict:
        """Format post for platform constraints."""

class BlueskyAdapter(PlatformAdapter):
    async def publish(self, post: Post) -> str:
        content = self.format_content(post)
        # AT Protocol posting
        response = await self.client.post(
            "com.atproto.repo.createRecord",
            json=content,
        )
        return response["uri"]

    def format_content(self, post: Post) -> dict:
        text = post.body[:300]  # 300 char limit
        if post.url:
            text = f"{text}\n\n{post.url}"
        return {"collection": "app.bsky.feed.post", "record": {"text": text}}

class MastodonAdapter(PlatformAdapter):
    async def publish(self, post: Post) -> str:
        content = self.format_content(post)
        response = await self.client.post("/api/v1/statuses", json=content)
        return response.json()["url"]

    def format_content(self, post: Post) -> dict:
        text = post.body[:500]  # 500 char default
        if post.url:
            text = f"{text}\n\n{post.url}"
        return {"status": text, "visibility": "public"}
```

### Distribution Orchestrator

```python
class ContentDistributor:
    def __init__(self, adapters: dict[str, PlatformAdapter]):
        self.adapters = adapters

    async def distribute(self, post: Post, platforms: list[str] | None = None) -> dict[str, str]:
        targets = platforms or list(self.adapters.keys())
        results = {}
        for platform in targets:
            adapter = self.adapters[platform]
            try:
                url = await adapter.publish(post)
                results[platform] = url
            except Exception as e:
                results[platform] = f"ERROR: {e}"
        return results
```

## Rate Limiting

### Client-Side Rate Limiter

```python
import asyncio
import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: list[float] = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [t for t in self.requests if now - t < self.window]
            if len(self.requests) >= self.max_requests:
                wait_time = self.requests[0] + self.window - now
                await asyncio.sleep(wait_time)
            self.requests.append(time.time())
```

### Retry on Rate Limit

```python
async def api_call_with_retry(func, *args, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await func(*args)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 60))
                await asyncio.sleep(retry_after)
            else:
                raise
    raise Exception("Max retries exceeded")
```

## Scheduling

```python
from datetime import datetime, timedelta

class PostScheduler:
    def __init__(self, distributor: ContentDistributor):
        self.distributor = distributor
        self.queue: list[tuple[datetime, Post, list[str]]] = []

    def schedule(self, post: Post, platforms: list[str], publish_at: datetime):
        self.queue.append((publish_at, post, platforms))
        self.queue.sort(key=lambda x: x[0])

    async def run(self):
        while self.queue:
            publish_at, post, platforms = self.queue[0]
            now = datetime.now()
            if now >= publish_at:
                self.queue.pop(0)
                await self.distributor.distribute(post, platforms)
            else:
                await asyncio.sleep((publish_at - now).total_seconds())
```

## Analytics Retrieval

```python
@dataclass
class PostMetrics:
    views: int
    likes: int
    shares: int
    comments: int
    clicks: int

async def aggregate_metrics(post_urls: dict[str, str]) -> dict[str, PostMetrics]:
    metrics = {}
    for platform, url in post_urls.items():
        adapter = adapters[platform]
        metrics[platform] = await adapter.get_metrics(url)
    return metrics
```

## Anti-Patterns

- **Posting identical content everywhere** — Adapt format and tone per platform
- **Ignoring rate limits** — Always implement client-side rate limiting
- **Storing tokens in code** — Use environment variables or secret managers
- **No error handling on post failure** — Queue for retry, log failures
- **Synchronous multi-platform posting** — Use async/parallel posting with individual error handling
- **Hardcoded platform URLs** — Instance URLs vary (Mastodon), use configuration
