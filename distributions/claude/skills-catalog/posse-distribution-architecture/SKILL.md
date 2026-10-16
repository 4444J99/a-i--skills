---
name: posse-distribution-architecture
description: Implement POSSE (Publish on Own Site, Syndicate Elsewhere) content distribution with canonical URLs, cross-platform syndication, backfeed collection, and resilient delivery. Covers multi-platform publishing automation and IndieWeb patterns. Triggers on POSSE implementation, content syndication architecture, or IndieWeb publishing requests.
license: MIT
complexity: advanced
time_to_learn: 30min
tags:
  - posse
  - syndication
  - indieweb
  - content-distribution
  - cross-platform
governance_phases: [build]
organ_affinity: [organ-vii]
triggers: [user-asks-about-posse, context:content-syndication, context:indieweb, context:cross-platform-publishing]
complements: [resilience-patterns, social-media-api-integration, essay-publishing-pipeline, content-distribution]
---

# POSSE Distribution Architecture

Publish on your own site first, then syndicate everywhere else — with resilience.

## POSSE Principle

```
Your Site (canonical) ──→ Platform A (syndicated copy)
         │               ├─→ Platform B (syndicated copy)
         │               ├─→ Platform C (syndicated copy)
         │               └─→ Newsletter (syndicated copy)
         │
         ←── Backfeed (likes, comments, reshares from platforms)
```

**Why POSSE over platform-first:**
- Own your canonical URL and content
- Platform changes don't destroy your archive
- Canonical URL gets SEO benefit
- Single source of truth for corrections

## Architecture

### Core Components

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class SyndicationStatus(str, Enum):
    PENDING = "pending"
    PUBLISHED = "published"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class CanonicalContent:
    id: str
    title: str
    body: str
    canonical_url: str
    published_at: datetime
    content_type: str  # "essay", "note", "photo", "event"
    tags: list[str] = field(default_factory=list)
    syndications: dict[str, SyndicationStatus] = field(default_factory=dict)

@dataclass
class SyndicationTarget:
    platform: str
    adapter: "PlatformAdapter"
    enabled: bool = True
    format_rules: dict = field(default_factory=dict)
```

### Distribution Pipeline

```python
class POSSEDistributor:
    def __init__(self, targets: list[SyndicationTarget]):
        self.targets = {t.platform: t for t in targets if t.enabled}

    async def distribute(self, content: CanonicalContent) -> dict[str, str]:
        results = {}
        for platform, target in self.targets.items():
            try:
                adapted = target.adapter.adapt(content)
                syndication_url = await target.adapter.publish(adapted)
                content.syndications[platform] = SyndicationStatus.PUBLISHED
                results[platform] = syndication_url
            except RateLimitError:
                content.syndications[platform] = SyndicationStatus.RETRYING
                await self.queue_retry(platform, content)
            except Exception as e:
                content.syndications[platform] = SyndicationStatus.FAILED
                results[platform] = f"FAILED: {e}"
        return results
```

### Content Adaptation

```python
from abc import ABC, abstractmethod

class PlatformAdapter(ABC):
    @abstractmethod
    def adapt(self, content: CanonicalContent) -> dict:
        """Transform content for platform constraints."""

    @abstractmethod
    async def publish(self, adapted: dict) -> str:
        """Publish and return syndication URL."""

class BlueskyAdapter(PlatformAdapter):
    MAX_LENGTH = 300

    def adapt(self, content: CanonicalContent) -> dict:
        if content.content_type == "essay":
            text = f"{content.title}\n\n{content.body[:200]}...\n\n{content.canonical_url}"
        else:
            text = content.body[:self.MAX_LENGTH - len(content.canonical_url) - 2]
            text = f"{text}\n\n{content.canonical_url}"
        return {"text": text[:self.MAX_LENGTH], "tags": content.tags[:8]}

class NewsletterAdapter(PlatformAdapter):
    def adapt(self, content: CanonicalContent) -> dict:
        return {
            "subject": content.title,
            "html": render_email_template(content),
            "canonical_url": content.canonical_url,
        }

class DevToAdapter(PlatformAdapter):
    def adapt(self, content: CanonicalContent) -> dict:
        return {
            "title": content.title,
            "body_markdown": content.body,
            "canonical_url": content.canonical_url,
            "tags": content.tags[:4],
            "published": True,
        }
```

## Resilient Delivery

### Retry Queue

```python
import asyncio
from collections import defaultdict

class RetryQueue:
    def __init__(self, max_retries: int = 3, base_delay: float = 60):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.queue: list[tuple[str, CanonicalContent, int]] = []

    async def add(self, platform: str, content: CanonicalContent, attempt: int = 0):
        self.queue.append((platform, content, attempt))

    async def process(self, distributor: POSSEDistributor):
        while self.queue:
            platform, content, attempt = self.queue.pop(0)
            if attempt >= self.max_retries:
                log.error("syndication_abandoned", platform=platform, content_id=content.id)
                continue

            delay = self.base_delay * (2 ** attempt)
            await asyncio.sleep(delay)

            target = distributor.targets.get(platform)
            if not target:
                continue

            try:
                adapted = target.adapter.adapt(content)
                url = await target.adapter.publish(adapted)
                content.syndications[platform] = SyndicationStatus.PUBLISHED
            except Exception:
                await self.add(platform, content, attempt + 1)
```

### Circuit Breaker per Platform

```python
class PlatformCircuitBreaker:
    def __init__(self):
        self.circuits: dict[str, CircuitBreaker] = {}

    def get(self, platform: str) -> CircuitBreaker:
        if platform not in self.circuits:
            self.circuits[platform] = CircuitBreaker(
                failure_threshold=3,
                recovery_timeout=300,  # 5 minutes
            )
        return self.circuits[platform]

    async def publish(self, platform: str, adapter: PlatformAdapter, content: dict) -> str:
        circuit = self.get(platform)
        return await circuit.call(adapter.publish, content)
```

## Backfeed Collection

```python
async def collect_backfeed(syndication_urls: dict[str, str]) -> list[dict]:
    backfeed = []
    for platform, url in syndication_urls.items():
        try:
            adapter = get_adapter(platform)
            metrics = await adapter.get_metrics(url)
            backfeed.append({
                "platform": platform,
                "url": url,
                "likes": metrics.get("likes", 0),
                "reposts": metrics.get("reposts", 0),
                "comments": metrics.get("comments", []),
            })
        except Exception:
            pass  # Backfeed is best-effort
    return backfeed
```

## Syndication Manifest

```yaml
# syndication-manifest.yaml
content:
  - id: essay-2026-03-20-architecture
    canonical_url: https://example.com/essays/architecture
    published_at: 2026-03-20T10:00:00Z
    syndications:
      bluesky:
        status: published
        url: https://bsky.app/profile/.../post/...
        published_at: 2026-03-20T10:01:00Z
      devto:
        status: published
        url: https://dev.to/author/article
        published_at: 2026-03-20T10:02:00Z
      newsletter:
        status: published
        campaign_id: "abc123"
        published_at: 2026-03-20T10:05:00Z
    backfeed:
      total_likes: 42
      total_reposts: 8
      total_comments: 3
      last_collected: 2026-03-20T22:00:00Z
```

## Anti-Patterns

- **Platform-first publishing** — Always publish on own site first; canonical URL is sacred
- **No canonical URL** — Every syndicated copy must link back to the original
- **Synchronous distribution** — Publish locally first, syndicate asynchronously
- **No retry logic** — Platforms have outages; queue and retry failed syndications
- **Identical content everywhere** — Adapt format and length per platform
- **Ignoring backfeed** — Engagement data from platforms enriches the canonical record
