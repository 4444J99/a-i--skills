# Choosing a License

How to select the right open source license for your project.

---

## Why Licensing Matters

- Code without a license is **not** open source; it defaults to "all rights reserved"
- A license tells others what they can and cannot do with your code
- Choosing wrong can limit adoption or expose you to liability
- Many companies have policies about which licenses they can use

---

## Common Licenses at a Glance

| License | Type | Requires Attribution | Copyleft | Patent Grant | Commercial Use |
|---------|------|---------------------|----------|--------------|----------------|
| MIT | Permissive | Yes | No | No | Yes |
| Apache 2.0 | Permissive | Yes | No | Yes | Yes |
| BSD 2-Clause | Permissive | Yes | No | No | Yes |
| GPL 3.0 | Strong copyleft | Yes | Yes (all) | Yes | Yes |
| LGPL 3.0 | Weak copyleft | Yes | Yes (library only) | Yes | Yes |
| MPL 2.0 | File-level copyleft | Yes | Yes (per file) | Yes | Yes |
| ISC | Permissive | Yes | No | No | Yes |
| Unlicense | Public domain | No | No | No | Yes |
| CC0 | Public domain | No | No | No | Yes |

---

## Decision Flowchart

```
Do you want maximum adoption with minimal restrictions?
├── Yes → MIT or Apache 2.0
│         ├── Need patent protection? → Apache 2.0
│         └── Want simplicity? → MIT
│
├── Want to ensure derivatives stay open source?
│   ├── Entire project must stay open? → GPL 3.0
│   ├── Only your library files? → LGPL 3.0
│   └── Only modified files? → MPL 2.0
│
└── Want to dedicate to public domain?
    └── Unlicense or CC0
```

---

## Detailed License Profiles

### MIT License

The most popular open source license. Short, simple, and permissive.

**Allows**: Commercial use, modification, distribution, private use
**Requires**: License and copyright notice included in copies
**Does not require**: Sharing source of derivatives

When to use: Libraries, tools, and projects where you want maximum adoption. Most npm packages, many GitHub projects.

### Apache 2.0

Like MIT but with an explicit patent grant and contributor license agreement.

**Allows**: Everything MIT allows
**Requires**: License notice, state changes, patent grant
**Includes**: Protection against patent trolling from contributors

When to use: Projects where patent protection matters (enterprise tools, APIs, anything touching patented technology). Required by some corporate contribution policies.

### GPL 3.0

Strong copyleft: any distributed derivative must also be GPL.

**Allows**: Commercial use, modification, distribution
**Requires**: Source code of derivatives must be available under GPL
**Prevents**: Tivoization (hardware restrictions on modified software)

When to use: Projects where you want to ensure all derivatives remain free/open. Linux kernel (GPL 2.0), many GNU tools.

### MPL 2.0

File-level copyleft: modified files must stay open, but you can combine with proprietary code.

**Allows**: Mixing with proprietary code in the same project
**Requires**: Modified MPL files stay under MPL
**Pragmatic**: Middle ground between permissive and copyleft

When to use: Libraries that you want to keep open but allow proprietary integration. Firefox uses MPL.

---

## Special Situations

### No License (All Rights Reserved)

If you publish code on GitHub without a license file, others technically cannot legally copy, modify, or distribute it. GitHub's Terms of Service allow viewing and forking, but not much else. Always add a license.

### Dual Licensing

Some projects offer two licenses:
- **Open source license** for community use (e.g., AGPL)
- **Commercial license** for companies that cannot comply with copyleft

Examples: MySQL (GPL + commercial), MongoDB (SSPL + commercial).

### Creative Commons for Non-Code

CC licenses are designed for content, not software:
- `CC BY 4.0` for documentation, tutorials, datasets
- `CC0` for public domain dedication
- Do **not** use CC licenses for source code (they lack patent clauses and are ambiguous about software)

### AGPL 3.0 (Network Copyleft)

Like GPL but also covers network use. If you run modified AGPL software as a web service, you must provide source to users. Relevant for SaaS products built on open source.

---

## Adding a License to Your Repository

1. Create a `LICENSE` file in the project root
2. Copy the full license text (use [choosealicense.com](https://choosealicense.com) for templates)
3. Fill in the year and copyright holder name
4. Reference the license in your README
5. Optionally add SPDX identifier to `package.json` or equivalent:
   ```json
   { "license": "MIT" }
   ```

### License Header (Optional)

Some licenses recommend adding a header to each source file:

```
// SPDX-License-Identifier: MIT
// Copyright (c) 2024 Your Name
```

SPDX identifiers are machine-readable and increasingly expected in enterprise contexts.

---

## Corporate Considerations

| Company Policy | Typically Allows | Typically Restricts |
|----------------|-----------------|---------------------|
| Very conservative | MIT, BSD, Apache 2.0 | GPL, AGPL, LGPL |
| Moderate | MIT, BSD, Apache, LGPL, MPL | GPL, AGPL |
| Open source friendly | Most licenses | AGPL (SaaS concern) |

If your project targets enterprise adoption, permissive licenses (MIT, Apache 2.0) minimize friction. GPL-family licenses are often flagged by corporate legal review.

---

## Quick Reference

- **Just want it out there**: MIT
- **Enterprise-grade permissive**: Apache 2.0
- **Keep derivatives open**: GPL 3.0
- **Open library, proprietary app OK**: LGPL 3.0 or MPL 2.0
- **SaaS must share**: AGPL 3.0
- **Public domain**: Unlicense or CC0
- **Documentation/content**: CC BY 4.0
