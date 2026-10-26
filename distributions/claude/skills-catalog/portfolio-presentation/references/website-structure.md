# Portfolio Website Structure

## Information Architecture

```
/
├── Home (Hero + Featured Work)
├── Work/Projects
│   ├── Project 1 (Case Study)
│   ├── Project 2 (Case Study)
│   └── ...
├── About
├── Resume/CV (optional)
├── Contact
└── Blog (optional)
```

## Page Templates

### Home Page

```
┌─────────────────────────────────────┐
│           HERO SECTION              │
│  [Name]                             │
│  [Positioning Statement]            │
│  [CTA: View Work]                   │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│        FEATURED PROJECTS            │
│  ┌─────┐ ┌─────┐ ┌─────┐           │
│  │ P1  │ │ P2  │ │ P3  │           │
│  └─────┘ └─────┘ └─────┘           │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│          BRIEF ABOUT                │
│  [2-3 sentences + photo]            │
│  [Link to full About]               │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│            CONTACT                  │
│  [Email] [LinkedIn] [GitHub]        │
└─────────────────────────────────────┘
```

### Project Page

```
┌─────────────────────────────────────┐
│           PROJECT HERO              │
│  [Title]                            │
│  [Role | Year | Client]             │
│  [Hero Image]                       │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│           OVERVIEW                  │
│  [Challenge]                        │
│  [Solution]                         │
│  [Impact]                           │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│           PROCESS                   │
│  [Section with images]              │
│  [Section with images]              │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│           RESULTS                   │
│  [Metrics]                          │
│  [Testimonial]                      │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         NEXT PROJECT →              │
└─────────────────────────────────────┘
```

### About Page

```
┌─────────────────────────────────────┐
│         ABOUT HEADER                │
│  [Photo] [Intro paragraph]          │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         BACKGROUND                  │
│  [Professional story]               │
│  [Values/Approach]                  │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         SKILLS/TOOLS                │
│  [Grouped by category]              │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         EXPERIENCE                  │
│  [Timeline or list]                 │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         PERSONAL                    │
│  [Interests, personality]           │
└─────────────────────────────────────┘
```

## Technical Recommendations

### Performance
- Optimize images (WebP, lazy loading)
- Minimize JS/CSS
- Use CDN for assets
- Target <3s load time

### SEO Basics
- Unique titles per page
- Meta descriptions
- Alt text on images
- Semantic HTML
- robots.txt and sitemap

### Analytics
- Page views
- Time on page
- Project click-through
- Contact form submissions

## Platform Options

| Platform | Best For | Trade-offs |
|----------|----------|------------|
| Custom (Next.js, etc) | Full control | Maintenance burden |
| Webflow | Design flexibility | Learning curve |
| Squarespace | Quick setup | Limited customization |
| Cargo | Creative fields | Specific aesthetic |
| ReadyMag | Visual storytelling | Cost |
| GitHub Pages | Developers | Technical setup |
