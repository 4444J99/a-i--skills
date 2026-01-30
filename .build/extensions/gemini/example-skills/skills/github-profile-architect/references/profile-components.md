# GitHub Profile Components

Ready-to-use components for GitHub Profile READMEs.

---

## Hero Section Components

### Dynamic Typing Header

```html
<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=600&lines=Hi+%F0%9F%91%8B%2C+I'm+Your+Name;Full-Stack+Developer;Open+Source+Enthusiast;Building+Cool+Things" alt="Typing SVG" />
  </a>
</p>
```

**Parameters:**
- `font`: Fira Code, JetBrains Mono, Roboto Mono
- `weight`: 400-700
- `size`: Font size in pixels
- `duration`: Time per line (ms)
- `pause`: Pause between lines (ms)
- `color`: Hex color (no #)

### Profile View Counter

```markdown
![Profile Views](https://komarev.com/ghpvc/?username=YOUR_USERNAME&color=blue&style=flat-square)
```

**Style Options:** `flat`, `flat-square`, `plastic`, `for-the-badge`

### Social Badges Row

```html
<p align="center">
  <a href="https://linkedin.com/in/YOUR_USERNAME">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://twitter.com/YOUR_USERNAME">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" />
  </a>
  <a href="mailto:your@email.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  <a href="https://yourwebsite.com">
    <img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=About.me&logoColor=white" />
  </a>
</p>
```

---

## Bio Section Templates

### Junior Developer

```markdown
## About Me

- Currently learning **[Technology Stack]**
- Working on **[Project Name]** - [Brief Description]
- Looking for **[Internship/Entry-level Role]** opportunities
- Ask me about **[Topic you're enthusiastic about]**
- Fun fact: **[Something memorable]**
```

### Senior Developer

```markdown
## About Me

Building [type of systems] at **[Company]**. Previously: [Notable companies/projects].

- Architecting **[Current focus area]**
- Mentoring engineers on **[Specialty]**
- Writing about **[Topics]** at [Blog URL]

15+ years shipping production code. Open to consulting.
```

### DevRel/Educator

```markdown
## Hey, I'm [Name]

Developer Advocate at **[Company]**. I help developers [do something specific].

- Creating content about **[Topics]**
- Speaking at **[Conference types]**
- Maintaining **[Popular project]**

Let's connect: [Social links]
```

---

## Tech Stack Section

### Categorized Badges

```markdown
## Tech Stack

### Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

### Backend
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

### Infrastructure
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
```

### Compact Icon Grid

```html
<p align="left">
  <img src="https://skillicons.dev/icons?i=python,typescript,go,rust,react,nextjs,nodejs,postgres,redis,docker,kubernetes,aws" />
</p>
```

**Use skillicons.dev** for cleaner icon grids.

---

## Stats Components

### GitHub Stats Card

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=dark&hide_border=true&count_private=true)
```

**Key Parameters:**
- `theme`: dark, radical, merko, gruvbox, tokyonight, onedark, cobalt, synthwave, highcontrast, dracula
- `hide_border`: true/false
- `count_private`: true (requires self-deployment for accuracy)
- `show_icons`: true/false
- `hide`: stars,commits,prs,issues,contribs (comma-separated)

### Top Languages Card

```markdown
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USERNAME&layout=compact&theme=dark&hide_border=true)
```

**Layout Options:** `compact`, `donut`, `donut-vertical`, `pie`

### Streak Stats

```markdown
![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=YOUR_USERNAME&theme=dark&hide_border=true)
```

### Two-Column Stats Layout

```html
<p align="center">
  <img width="49%" src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=dark&hide_border=true" />
  <img width="49%" src="https://github-readme-streak-stats.herokuapp.com/?user=YOUR_USERNAME&theme=dark&hide_border=true" />
</p>
```

---

## Activity Components

### WakaTime Coding Stats

```markdown
![WakaTime Stats](https://github-readme-stats.vercel.app/api/wakatime?username=YOUR_WAKATIME_USERNAME&theme=dark&hide_border=true)
```

**Requires:** WakaTime account linked to your IDE.

### Recent Blog Posts (GitHub Action)

**README Section:**
```markdown
## Latest Blog Posts
<!-- BLOG-POST-LIST:START -->
<!-- BLOG-POST-LIST:END -->
```

**Workflow file** (`.github/workflows/blog-post-workflow.yml`):
```yaml
name: Latest blog post workflow
on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:

jobs:
  update-readme-with-blog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gautamkrishnar/blog-post-workflow@v1
        with:
          feed_list: "https://yourblog.com/feed,https://dev.to/feed/username"
          max_post_count: 5
```

### Contribution Graph

```markdown
![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=YOUR_USERNAME&theme=github-dark&hide_border=true)
```

---

## Layout Patterns

### Collapsible Sections

```html
<details>
<summary><b>Past Projects</b></summary>
<br>

| Project | Description | Tech |
|---------|-------------|------|
| Project A | Description | React, Node |
| Project B | Description | Python, AWS |

</details>
```

### Dark Mode Adaptive Images

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner-light.png">
  <img alt="Banner" src="./assets/banner-light.png">
</picture>
```

### Two-Column Bio + Stats

```html
<table border="0">
  <tr>
    <td width="50%">
      <h3>About Me</h3>
      <p>Your bio text here...</p>
    </td>
    <td width="50%">
      <img src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=dark" />
    </td>
  </tr>
</table>
```

---

## Badge Color Reference

### Brand Colors (from Simple Icons)

| Technology | Hex Code |
|------------|----------|
| JavaScript | F7DF1E |
| TypeScript | 3178C6 |
| Python | 3776AB |
| React | 61DAFB |
| Node.js | 339933 |
| Go | 00ADD8 |
| Rust | 000000 |
| AWS | 232F3E |
| Docker | 2496ED |
| PostgreSQL | 4169E1 |

**Find more:** https://simpleicons.org

### Badge Format

```
https://img.shields.io/badge/[LABEL]-[HEX_COLOR]?style=[STYLE]&logo=[LOGO]&logoColor=[LOGO_COLOR]
```

---

## Quick Reference URLs

| Resource | URL |
|----------|-----|
| Shields.io | https://shields.io |
| Simple Icons | https://simpleicons.org |
| Skill Icons | https://skillicons.dev |
| GitHub Stats | https://github.com/anuraghazra/github-readme-stats |
| Streak Stats | https://github.com/DenverCoder1/github-readme-streak-stats |
| Activity Graph | https://github.com/Ashutosh00710/github-readme-activity-graph |
| Typing SVG | https://github.com/DenverCoder1/readme-typing-svg |
| Blog Post Workflow | https://github.com/gautamkrishnar/blog-post-workflow |
