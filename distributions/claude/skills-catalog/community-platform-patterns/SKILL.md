---
name: community-platform-patterns
description: Build community platforms with user profiles, discussion forums, event management, and moderation tools. Covers real-time features, content moderation, and community engagement patterns. Triggers on community platform development, forum design, or social feature requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - community
  - forums
  - social-features
  - moderation
  - user-profiles
governance_phases: [build]
organ_affinity: [organ-vi]
triggers: [user-asks-about-community-platform, context:forum-design, context:community-features, context:discussion-platform]
complements: [realtime-websocket-patterns, backend-implementation-patterns, accessibility-patterns]
---

# Community Platform Patterns

Build engaging community platforms with sustainable moderation and meaningful interaction design.

## Core Data Model

```python
from datetime import datetime
from enum import Enum

class MemberRole(str, Enum):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"

class ContentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"      # Soft-removed by mod
    ARCHIVED = "archived"

# Core entities
class Member:
    id: str
    display_name: str
    bio: str
    joined_at: datetime
    role: MemberRole
    reputation: int = 0

class Discussion:
    id: str
    title: str
    body: str
    author_id: str
    category: str
    status: ContentStatus
    created_at: datetime
    reply_count: int = 0
    view_count: int = 0
    pinned: bool = False
    locked: bool = False

class Reply:
    id: str
    discussion_id: str
    author_id: str
    body: str
    parent_id: str | None = None  # Threaded replies
    status: ContentStatus
    created_at: datetime
    upvotes: int = 0
```

## Discussion Forum

### Thread Display Patterns

**Flat (chronological):** Best for announcements and linear conversations.

**Threaded (nested):** Best for technical discussions where tangents are valuable.

**Hybrid (flat with quoted replies):** Best for general discussion.

```python
async def get_discussion_with_replies(discussion_id: str, sort: str = "chronological"):
    discussion = await db.get_discussion(discussion_id)
    replies = await db.get_replies(discussion_id)

    if sort == "chronological":
        return sorted(replies, key=lambda r: r.created_at)
    elif sort == "threaded":
        return build_thread_tree(replies)
    elif sort == "popular":
        return sorted(replies, key=lambda r: r.upvotes, reverse=True)
```

### Categories and Tags

```python
CATEGORIES = {
    "reading-group": {"description": "Book discussions and study groups", "color": "#4A90D9"},
    "announcements": {"description": "Official updates", "color": "#E74C3C", "mod_only": True},
    "help": {"description": "Questions and support", "color": "#2ECC71"},
    "showcase": {"description": "Share your work", "color": "#F39C12"},
    "meta": {"description": "About the community itself", "color": "#9B59B6"},
}
```

## Reputation System

### Action-Based Scoring

| Action | Points | Rationale |
|--------|--------|-----------|
| Post discussion | +2 | Encourages contribution |
| Reply to discussion | +1 | Encourages engagement |
| Receive upvote | +5 | Community validation |
| Give upvote | +1 | Encourages voting |
| Marked as answer | +15 | High-value contribution |
| Post hidden by mod | -10 | Discourages violations |

### Privilege Tiers

```python
PRIVILEGE_TIERS = {
    0: ["read", "reply"],
    10: ["create_discussion", "upvote"],
    50: ["edit_own_posts", "flag_content"],
    100: ["create_events", "add_tags"],
    500: ["edit_wiki_posts"],
    1000: ["nominate_moderator"],
}

def get_privileges(reputation: int) -> list[str]:
    privileges = []
    for threshold, perms in PRIVILEGE_TIERS.items():
        if reputation >= threshold:
            privileges.extend(perms)
    return privileges
```

## Content Moderation

### Moderation Queue

```python
class ModerationAction(str, Enum):
    APPROVE = "approve"
    HIDE = "hide"
    WARN = "warn"
    BAN_TEMPORARY = "ban_temporary"
    BAN_PERMANENT = "ban_permanent"

async def flag_content(content_id: str, reason: str, reporter_id: str):
    flag = await db.create_flag(
        content_id=content_id,
        reason=reason,
        reporter_id=reporter_id,
    )
    # Auto-hide if threshold reached
    flag_count = await db.count_flags(content_id)
    if flag_count >= 3:
        await db.update_content_status(content_id, ContentStatus.HIDDEN)
        await notify_moderators(content_id, flag_count)
```

### Community Guidelines Enforcement

```python
GUIDELINES = {
    "be_respectful": "Treat others as you'd want to be treated",
    "stay_on_topic": "Keep discussions relevant to the community focus",
    "no_spam": "No promotional content without context",
    "cite_sources": "Back up claims with references when possible",
    "no_personal_attacks": "Criticize ideas, not people",
}

async def moderate(content_id: str, action: ModerationAction, reason: str, mod_id: str):
    await db.record_mod_action(content_id, action, reason, mod_id)
    if action == ModerationAction.HIDE:
        await db.update_content_status(content_id, ContentStatus.HIDDEN)
        await notify_author(content_id, reason)
    elif action == ModerationAction.WARN:
        await send_warning(content_id, reason)
```

## Event Management

```python
class Event:
    id: str
    title: str
    description: str
    organizer_id: str
    event_type: str  # "reading-group", "salon", "workshop", "office-hours"
    starts_at: datetime
    ends_at: datetime
    location: str  # URL for virtual, address for physical
    capacity: int | None
    rsvp_count: int = 0
    recurring: str | None = None  # "weekly", "biweekly", "monthly"

async def create_recurring_events(template: Event, count: int):
    events = []
    for i in range(count):
        event = template.copy()
        if template.recurring == "weekly":
            event.starts_at += timedelta(weeks=i)
            event.ends_at += timedelta(weeks=i)
        events.append(await db.create_event(event))
    return events
```

## Notification System

```python
class NotificationType(str, Enum):
    REPLY = "reply"
    MENTION = "mention"
    UPVOTE = "upvote"
    EVENT_REMINDER = "event_reminder"
    MOD_ACTION = "mod_action"

async def send_notification(user_id: str, notification_type: NotificationType, data: dict):
    prefs = await db.get_notification_preferences(user_id)
    if notification_type.value not in prefs.get("muted", []):
        await db.create_notification(user_id, notification_type, data)
        if prefs.get("email_enabled") and notification_type in prefs.get("email_types", []):
            await send_email_notification(user_id, notification_type, data)
```

## Anti-Patterns

- **No onboarding flow** — New members need guided first steps
- **Flat hierarchy only** — Categories/tags help people find relevant content
- **No moderation tools** — Build moderation from day one, not after the first incident
- **Gamification without purpose** — Points should encourage healthy behavior, not just activity
- **One-size-fits-all notifications** — Let members control what they receive
- **No archive strategy** — Old discussions should be searchable but not clutter active feeds
