---
name: parametrize-and-cite
description: Transform any data, document, deck, README, manifest, config, or report by (1) extracting every piece of dynamic information — names, links, statistics, costs, identifiers, dates, thresholds — into configurable variables instead of hard-coding, and (2) enforcing that every factual assertion carries at least two independent citations. Triggers on "remove branding," "make this reusable," "transmute this," "parametrize," "no hard-coded values," "configurable," "needs citations," "verify these claims," or any request to convert a one-off artifact into a parameterized template.
license: MIT
metadata:
  category: data-transformation
governance_phases: [build, prove]
governance_norm_group: quality-gate
governance_auto_activate: true
organ_affinity: [all]
triggers: [request:debrand, request:parametrize, request:anonymize, request:make-reusable, content:contains-hard-coded-values, content:contains-unsourced-claims]
complements: [coding-standards-enforcer, configuration-management, github-repository-standards, voice-enforcement]
---

# Parametrize and Cite

Two universal mandates apply to any data or compilation thereof:

1. **All dynamic information is a configurable environment variable.** Names, links, statistics, costs, identifiers, dates, thresholds, contact details — never hard-coded. The structure is reusable; the particulars are injected.
2. **All assertions require multiple citations.** Every factual claim carries at least two independent sources. Single-source claims are flagged, not shipped.

These are not stylistic preferences. They are substrate disciplines that determine whether an artifact survives time (parametrization protects against drift; multi-citation protects against epistemic collapse).

## When this skill fires

Apply this skill whenever the input is a "compiled artifact" — anything that bundles structure with particulars:

- pitch decks, one-pagers, sales sheets, README files
- competitive analyses, market reports, research summaries
- configuration files, manifests, deployment templates
- onboarding docs, runbooks, SOPs, playbooks
- any document that mixes "the pattern" with "this specific instance"
- any document that makes claims (numbers, attributions, characterizations)

If the artifact has a brand-shaped surface AND reusable bones, this skill fires. If it makes assertions, this skill fires.

## The transformation pipeline

Run the artifact through five phases in order. Don't skip phases — each one catches a different class of issue.

### Phase 1: Audit

Read the artifact end-to-end before transforming anything. Build two inventories:

- **Dynamic-information inventory**: every concrete particular (see the taxonomy below).
- **Assertion inventory**: every factual claim, with its current citation count.

Note: an "assertion" is anything stated as fact that the reader is expected to believe. Opinions and recommendations are not assertions. Numbers, attributions, comparisons, and historical claims are.

### Phase 2: Identify dynamics

Categorize each particular by what makes it dynamic. Use this taxonomy:

| Category | Examples | Env var prefix |
|---|---|---|
| Identity | company name, person name, project name, brand | `IDENTITY_*` |
| Locator | URL, repo path, email, phone, address | `LINK_*` / `CONTACT_*` |
| Quantitative | revenue, count, percentage, ratio, score | `STAT_*` |
| Monetary | price, cost, budget, fee, salary | `COST_*` |
| Temporal | date, deadline, duration, period | `DATE_*` / `DURATION_*` |
| Threshold | limit, quota, target, SLA | `THRESHOLD_*` |
| Credential | API key, token, account ID | `SECRET_*` (never default) |
| Categorical | tier, plan, region, jurisdiction | `CATEGORY_*` |

Anything that *could* differ between instances of this artifact's reuse is dynamic, even if it feels permanent today. "Our company name" is dynamic — the artifact might be reused by an acquirer, a fork, a parallel project, or a customer-facing variant.

### Phase 3: Parametrize

Replace each dynamic particular with an env-var reference. Choose a template syntax that matches the artifact's medium:

- **Markdown / prose docs**: `{{ IDENTITY_COMPANY_NAME }}` (Mustache-style) or `${IDENTITY_COMPANY_NAME}` (shell-style)
- **YAML / JSON configs**: `${IDENTITY_COMPANY_NAME}` (envsubst-style) or platform-native (`!Ref`, `${{ vars.X }}`, etc.)
- **Code files**: language-idiomatic (`os.environ["IDENTITY_COMPANY_NAME"]`, `process.env.IDENTITY_COMPANY_NAME`)

Generate a paired `.env.example` (or platform-equivalent: `config.example.yaml`, `terraform.tfvars.example`, etc.) with every variable, a one-line comment describing what it controls, and a sample value drawn from the original artifact.

```
# Identity
IDENTITY_COMPANY_NAME="Example Corp"        # Replaces brand references in headers, footers
IDENTITY_PRODUCT_NAME="ExampleProduct"      # Used in feature descriptions

# Stats — quarterly report figures
STAT_Q4_REVENUE_USD=4200000                 # Q4 top-line revenue
STAT_Q4_GROWTH_PCT=23                       # YoY growth percentage

# Costs — pricing tier defaults
COST_TIER_STARTER_USD_MONTH=49              # Starter plan monthly price
```

**Never inline secrets even as examples.** For `SECRET_*` variables, the example file shows the variable name and a placeholder (`SECRET_API_KEY=changeme-in-production`), never a real key.

### Phase 4: Cite

For every assertion in the inventory, attach at least two independent citations. Define independence carefully:

- **Two sources from the same parent org are not independent.** A company's own homepage + its own blog = one source.
- **A primary source + a secondary that reports on the primary is not two independent sources.** That's one source plus its echo.
- **Two independent sources** = two organizations with no editorial or financial relationship, each having direct access to the underlying evidence (or each citing a distinct primary).

Citation format depends on the medium:

- **Prose docs**: inline footnotes `[^1]` + bibliography section
- **Slides / decks**: source line at bottom of slide, full sources in appendix
- **Data tables**: per-row source column + per-column source notes
- **Code comments**: `# Source: <url> (accessed YYYY-MM-DD); cross-checked: <url>`

Where you cannot find two independent citations, do one of the following — explicitly, never silently:

1. **Flag with `[CITATION-REQUIRED]`** in the output and list in a "Verification gap" section.
2. **Demote the assertion to a conditional**: "If [source] is correct, then…"
3. **Remove the assertion** if it's load-bearing but unsupportable.

Never invent or fabricate sources. Never paper over with weasel phrases ("studies have shown," "it is widely known").

### Phase 5: Emit

Produce four artifacts as a set:

1. **The transformed artifact** — original content with dynamics parametrized and assertions cited.
2. **`.env.example`** (or platform equivalent) — every variable with comment and sample value.
3. **`CITATIONS.md`** — full bibliography organized by section, with accessed-dates and brief notes on independence.
4. **`TRANSFORMATION_LOG.md`** — what was changed, what was flagged, what was removed, with rationale.

The four-artifact emission is non-negotiable. Shipping the transformed artifact without the `.env.example` strands the user; without `CITATIONS.md` the citations are unverifiable; without the log the user can't audit what you changed.

## What counts as dynamic — edge cases

Some particulars feel permanent but are dynamic on reuse. Treat each as a variable:

- **"The current year"** — `DATE_PUBLICATION_YEAR`, not literal `2026`
- **"Our team size"** — `STAT_TEAM_HEADCOUNT`, even if it changes annually
- **License names** — `IDENTITY_LICENSE_TYPE`, in case the template is reused under different terms
- **Tone-of-voice phrases unique to a brand** — these are dynamic; the structure of the sentence is reusable
- **Compliance thresholds tied to a jurisdiction** — `THRESHOLD_GDPR_RETENTION_DAYS`, in case the template moves to another regime

If you're unsure whether something is dynamic, parametrize it. The cost of an extra env var is near-zero. The cost of a hard-coded value that needed to vary is reissuing the whole artifact.

## What counts as an assertion — edge cases

These are assertions and require citation:

- "X is the largest provider in Y market"
- "23% of users churn within 30 days"
- "This complies with regulation Z"
- "Method A is faster than method B"
- "The acquisition closed on date D for price P"

These are NOT assertions (no citation needed):

- "We recommend X because…" (recommendation)
- "Consider whether Y applies to your context" (advice)
- "This document describes our approach to Z" (descriptive)
- "Section 3 covers configuration" (structural)

If a sentence both recommends AND asserts, split it: "Adopt approach X (recommendation). Approach X has been measured at 40% lower latency [^1][^2] (assertion)."

## Output verification checklist

Before declaring the transformation complete, verify:

- [ ] Every concrete particular from the original is either parametrized or explicitly retained with rationale
- [ ] `.env.example` has one line per variable, with comment and sample
- [ ] No secret has a real value in the example file
- [ ] Every assertion has ≥2 independent citations OR is flagged / demoted / removed
- [ ] Bibliography lists every cited source with URL and accessed-date
- [ ] Transformation log enumerates every change
- [ ] Re-reading the transformed artifact with only the env-var names in place still makes structural sense (sentences don't collapse into nonsense when the particulars are abstracted)

The last check matters: if the artifact becomes incoherent when the particulars are removed, the artifact was *about* the particulars and parametrization is the wrong move — surface this to the user rather than ship a degraded version.

## Reference

For detailed pattern examples by artifact type (decks, READMEs, configs, reports), see `references/transformation-patterns.md`.

For citation-independence judgment calls (when is a source "the same parent org"? when does a secondary count as independent?), see `references/citation-independence.md`.
