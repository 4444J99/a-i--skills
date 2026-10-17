---
name: essay-publishing-pipeline
description: Publish essays and long-form content through a structured pipeline from draft to distribution. Covers markdown-to-HTML conversion, metadata management, cross-posting strategies, and RSS/Atom feed generation. Triggers on essay publishing, content pipeline, or blog deployment requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - publishing
  - essays
  - content-pipeline
  - markdown
  - rss
governance_phases: [build, prove]
organ_affinity: [organ-v]
triggers: [user-asks-about-publishing, context:essay-publishing, context:blog-deployment, context:content-pipeline]
complements: [creative-writing-craft, content-distribution, technical-analytical-writing]
---

# Essay Publishing Pipeline

Move written content from draft through editing, formatting, and multi-platform distribution.

## Pipeline Architecture

```
Draft → Edit → Format → Metadata → Build → Publish → Distribute
  ↑                                                      │
  └──────────── Feedback Loop ───────────────────────────┘
```

### Stage Definitions

| Stage | Input | Output | Tools |
|-------|-------|--------|-------|
| Draft | Ideas, notes | Raw markdown | Editor, voice notes |
| Edit | Raw markdown | Polished markdown | Linter, peer review |
| Format | Polished markdown | Structured content | Frontmatter, templates |
| Metadata | Structured content | Enriched content | Tags, categories, SEO |
| Build | Enriched content | HTML/PDF output | SSG, Pandoc |
| Publish | Built output | Live content | Deploy, CMS API |
| Distribute | Published URL | Cross-posts | RSS, social, newsletter |

## Content Structure

### Markdown with Frontmatter

```markdown
---
title: "On the Architecture of Automated Systems"
subtitle: "Why eight organs beat one monolith"
author: "Author Name"
date: 2026-03-20
updated: 2026-03-20
status: published
tags: [architecture, automation, organvm]
category: systems-thinking
series: "Orchestration Essays"
series_order: 3
abstract: >
  A 2000-word exploration of why modular organ-based
  architecture outperforms monolithic automation.
canonical_url: "https://example.com/essays/architecture-of-automated-systems"
---

# On the Architecture of Automated Systems

Opening paragraph that hooks the reader...
```

### Essay Taxonomy

| Field | Purpose | Example |
|-------|---------|---------|
| `status` | Workflow state | draft, review, published, archived |
| `tags` | Topic classification | [architecture, automation] |
| `category` | Primary category | systems-thinking |
| `series` | Multi-part grouping | "Orchestration Essays" |
| `canonical_url` | SEO canonical | Primary publication URL |
| `abstract` | Summary for feeds/cards | 1-2 sentence summary |

## Markdown Processing

### Conversion Pipeline

```bash
# Markdown → HTML with Pandoc
pandoc essay.md \
  --from markdown+yaml_metadata_block \
  --to html5 \
  --template template.html \
  --highlight-style tango \
  --toc \
  --toc-depth=2 \
  --output essay.html

# Markdown → PDF
pandoc essay.md \
  --pdf-engine=weasyprint \
  --css style.css \
  --output essay.pdf
```

### Static Site Generator Integration

```python
# Build script for essay collection
from pathlib import Path
import yaml
import markdown

def build_essays(source_dir: str, output_dir: str):
    essays = []
    for md_file in sorted(Path(source_dir).glob("*.md")):
        text = md_file.read_text()
        frontmatter, content = text.split("---\n", 2)[1:]
        meta = yaml.safe_load(frontmatter)
        if meta.get("status") != "published":
            continue
        html = markdown.markdown(content, extensions=["fenced_code", "tables", "toc"])
        essays.append({"meta": meta, "html": html, "slug": md_file.stem})

    for essay in essays:
        output = Path(output_dir) / f"{essay['slug']}/index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_template(essay))

    build_index(essays, output_dir)
    build_rss_feed(essays, output_dir)
```

## RSS/Atom Feed Generation

```python
from datetime import datetime
import xml.etree.ElementTree as ET

def build_rss_feed(essays: list[dict], output_dir: str):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Essay Collection"
    ET.SubElement(channel, "link").text = "https://example.com/essays"
    ET.SubElement(channel, "description").text = "Long-form writing on systems and culture"

    for essay in essays[:20]:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = essay["meta"]["title"]
        ET.SubElement(item, "link").text = f"https://example.com/essays/{essay['slug']}"
        ET.SubElement(item, "description").text = essay["meta"].get("abstract", "")
        ET.SubElement(item, "pubDate").text = essay["meta"]["date"].strftime(
            "%a, %d %b %Y 00:00:00 GMT"
        )

    tree = ET.ElementTree(rss)
    tree.write(f"{output_dir}/feed.xml", xml_declaration=True, encoding="utf-8")
```

## Cross-Posting Strategy

### POSSE (Publish on Own Site, Syndicate Elsewhere)

```
Own site (canonical) → Medium → Dev.to → LinkedIn → Newsletter
                    ↗          ↗
            RSS feed triggers automation
```

### Cross-Post Formatting

| Platform | Format | Limits | Notes |
|----------|--------|--------|-------|
| Own site | Full HTML | None | Canonical URL |
| Medium | Markdown import | None | Set canonical URL |
| Dev.to | Markdown + frontmatter | None | Use API for automation |
| LinkedIn | Plain text + link | 3000 chars | Excerpt + link to full |
| Newsletter | HTML email | Images inline | Adapt layout for email |

### Automated Cross-Posting

```python
async def cross_post(essay: dict):
    canonical = essay["meta"]["canonical_url"]

    # Dev.to
    await devto_api.create_article(
        title=essay["meta"]["title"],
        body_markdown=essay["content"],
        canonical_url=canonical,
        tags=essay["meta"]["tags"][:4],
        published=True,
    )

    # Newsletter
    await newsletter_api.create_campaign(
        subject=essay["meta"]["title"],
        html=render_email_template(essay),
    )
```

## Quality Gates

### Pre-Publish Checklist

- [ ] Spell check and grammar review
- [ ] Links verified (no 404s)
- [ ] Images optimized and alt-text present
- [ ] Frontmatter complete (title, date, tags, abstract)
- [ ] Canonical URL set
- [ ] Open Graph / social card metadata present
- [ ] RSS feed validates
- [ ] Mobile rendering verified

### SEO Metadata

```html
<meta property="og:title" content="Essay Title">
<meta property="og:description" content="Abstract text">
<meta property="og:type" content="article">
<meta property="og:url" content="https://example.com/essays/slug">
<meta name="twitter:card" content="summary_large_image">
```

## Anti-Patterns

- **Publishing without canonical URL** — Leads to duplicate content SEO penalties
- **Manual cross-posting** — Automate with APIs and RSS triggers
- **No RSS feed** — Essential for syndication and discoverability
- **Draft content leaking** — Always check `status` field before building
- **No versioning** — Track `updated` date for revised essays
- **Platform-first publishing** — Always publish on own domain first (POSSE)
