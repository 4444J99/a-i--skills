# Project Metrics Guide

Interpreting and presenting SpecStory project statistics.

## Core Metrics

### Session Count

| Metric | Definition | Use |
|--------|------------|-----|
| **Total Sessions** | All-time count of AI coding sessions | Overall project activity |
| **Last 30 Days** | Sessions in rolling 30-day window | Recent activity level |
| **Last 7 Days** | Sessions in rolling 7-day window | Current momentum |

**Interpretation:**

```
High total + low recent = Project mature or dormant
Low total + high recent = New or ramping up
Steady week-over-week = Consistent development
```

### Contributor Count

| Metric | Definition | Use |
|--------|------------|-----|
| **Total Contributors** | Unique users who created sessions | Team size indicator |
| **Active (30 days)** | Contributors with recent sessions | Engaged team size |

**Interpretation:**

```
Total >> Active = High turnover or sporadic use
Total ≈ Active = Consistent team engagement
Single contributor = Solo project
```

### Activity Metrics

| Metric | Definition | Use |
|--------|------------|-----|
| **First Session** | Date of earliest recorded session | Project age |
| **Last Session** | Most recent session date | Current status |
| **Avg Sessions/Week** | Mean weekly session count | Velocity indicator |

---

## Derived Metrics

### Session Velocity

```
Weekly Velocity = sessions_last_7_days / 7
Monthly Velocity = sessions_last_30_days / 30

Trend = weekly_velocity / monthly_velocity
  > 1.0 = Accelerating
  ≈ 1.0 = Steady
  < 1.0 = Decelerating
```

### Contributor Engagement

```
Engagement Rate = active_30_days / total_contributors

High (> 0.8) = Strong team engagement
Medium (0.4-0.8) = Normal engagement
Low (< 0.4) = May indicate issues
```

### Sessions per Contributor

```
Avg Sessions per Contributor = total_sessions / total_contributors

High (> 30) = Power users or small team
Medium (10-30) = Balanced usage
Low (< 10) = Light usage or large team
```

---

## Presentation Templates

### Summary Card

```
┌─────────────────────────────────────────┐
│  specstoryai/agent-skills               │
├─────────────────────────────────────────┤
│  Sessions: 156 total                    │
│            47 last 30 days              │
│            12 last 7 days               │
│                                         │
│  Contributors: 5 total (3 active)       │
│                                         │
│  Activity: Oct 2025 - Jan 2026          │
│           ~8 sessions/week              │
└─────────────────────────────────────────┘
```

### Trend Indicator

```
Current week:  12 sessions  ████████████
Previous week:  8 sessions  ████████
Trend: ↑ 50% increase
```

### Natural Language Summary

**Template:**

> This project has captured **{total_sessions} sessions** since **{first_session}**.
> With **{active_contributors}** active contributors in the last 30 days,
> the team averages about **{avg_sessions_per_week} sessions per week**.
> {trend_commentary}

**Example:**

> This project has captured **156 sessions** since **October 2025**.
> With **3** active contributors in the last 30 days,
> the team averages about **8 sessions per week**.
> Activity has been steady, with consistent weekly contributions.

---

## Benchmarks

### Session Activity Levels

| Level | Sessions/Week | Interpretation |
|-------|---------------|----------------|
| **Very High** | > 20 | Heavy AI-assisted development |
| **High** | 10-20 | Active daily use |
| **Moderate** | 5-10 | Regular use |
| **Low** | 1-5 | Occasional use |
| **Minimal** | < 1 | Infrequent use |

### Team Size Indicators

| Contributors | Project Type |
|--------------|--------------|
| 1 | Solo developer |
| 2-5 | Small team |
| 6-15 | Medium team |
| 15+ | Large organization |

### Project Maturity

| Age | Interpretation |
|-----|----------------|
| < 1 month | New project |
| 1-6 months | Active development |
| 6-12 months | Established project |
| > 12 months | Mature project |

---

## Comparison Metrics

### Week-over-Week

```javascript
function weekOverWeekChange(stats) {
  const current = stats.sessions.last_7_days;
  const previousWeek = stats.sessions.last_30_days / 4; // Approximate

  const change = ((current - previousWeek) / previousWeek) * 100;

  return {
    current,
    previous: previousWeek,
    changePercent: change.toFixed(1),
    trend: change > 5 ? 'up' : change < -5 ? 'down' : 'stable'
  };
}
```

### Month-over-Month

```javascript
function monthOverMonthChange(stats, previousMonthStats) {
  const current = stats.sessions.last_30_days;
  const previous = previousMonthStats?.sessions.last_30_days || 0;

  if (previous === 0) return { trend: 'new', changePercent: 'N/A' };

  const change = ((current - previous) / previous) * 100;

  return {
    current,
    previous,
    changePercent: change.toFixed(1),
    trend: change > 10 ? 'up' : change < -10 ? 'down' : 'stable'
  };
}
```

---

## Visualization Suggestions

### Activity Timeline

```
Jan 2026  ████████████████████████ (47)
Dec 2025  ██████████████████████ (44)
Nov 2025  ██████████████████ (36)
Oct 2025  ██████████████ (29)
```

### Contributor Distribution

```
alice@example.com   ████████████████ (62 sessions)
bob@example.com     ████████████ (48 sessions)
charlie@example.com ████████ (32 sessions)
others              ████ (14 sessions)
```

### Weekly Trend

```
W1  W2  W3  W4  (last month)
██  ███ ██  ████
8   12  10  17
       Trend: ↑
```

---

## Error State Presentations

### Project Not Found

```
┌─────────────────────────────────────────┐
│  Project Not Found                      │
├─────────────────────────────────────────┤
│  This project hasn't been synced to     │
│  SpecStory Cloud yet.                   │
│                                         │
│  To get started:                        │
│  1. Install SpecStory                   │
│  2. Run `specstory sync`                │
│  3. Try this command again              │
└─────────────────────────────────────────┘
```

### No Recent Activity

```
┌─────────────────────────────────────────┐
│  specstoryai/old-project                │
├─────────────────────────────────────────┤
│  Sessions: 42 total                     │
│            0 last 30 days               │
│                                         │
│  Last active: August 2025               │
│  Status: Dormant                        │
└─────────────────────────────────────────┘
```

### Network Error

```
┌─────────────────────────────────────────┐
│  Unable to Fetch Stats                  │
├─────────────────────────────────────────┤
│  Could not connect to SpecStory Cloud.  │
│                                         │
│  • Check your internet connection       │
│  • API may be temporarily unavailable   │
│  • Try again in a few minutes           │
└─────────────────────────────────────────┘
```

---

## Privacy Considerations

### What's Shared

| Data | Included | Notes |
|------|----------|-------|
| Session count | Yes | Aggregate only |
| Session titles | Yes | May contain project info |
| Contributor emails | No | Count only |
| Session content | No | Never shared via stats |

### Public vs Private

- **Public projects**: Stats visible without auth
- **Private projects**: Require API authentication

### Data Retention

- Stats computed from synced sessions
- Historical data retained indefinitely
- Deletion requests via support
