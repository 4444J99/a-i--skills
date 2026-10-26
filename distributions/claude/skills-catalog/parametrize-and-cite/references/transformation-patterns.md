# Transformation Patterns by Artifact Type

Detailed worked examples of how the parametrize-and-cite pipeline applies to common artifact types. Read the section matching the input you have in front of you.

## Pitch deck / one-pager

**Before:**

> Acme Corp is the #1 logistics platform in North America, processing $4.2B in shipments annually for over 12,000 enterprise customers including Walmart, Target, and FedEx. Founded in 2014 by Jane Smith, we operate out of Austin, TX and have raised $340M across four rounds led by Sequoia.

**After (transformed):**

> `{{ IDENTITY_COMPANY_NAME }}` is the `{{ STAT_MARKET_RANK }}` logistics platform in `{{ CATEGORY_REGION }}`, processing `{{ STAT_ANNUAL_VOLUME_USD }}` in shipments annually for over `{{ STAT_CUSTOMER_COUNT }}` enterprise customers including `{{ IDENTITY_REFERENCE_CUSTOMERS }}` [^1][^2]. Founded in `{{ DATE_FOUNDING_YEAR }}` by `{{ IDENTITY_FOUNDER_NAME }}`, we operate out of `{{ IDENTITY_HQ_CITY }}` and have raised `{{ STAT_TOTAL_FUNDING_USD }}` across `{{ STAT_FUNDING_ROUNDS }}` rounds led by `{{ IDENTITY_LEAD_INVESTOR }}` [^3][^4].

**Paired `.env.example`:**

```
IDENTITY_COMPANY_NAME="Acme Corp"
STAT_MARKET_RANK="#1"
CATEGORY_REGION="North America"
STAT_ANNUAL_VOLUME_USD="$4.2B"
STAT_CUSTOMER_COUNT="12,000"
IDENTITY_REFERENCE_CUSTOMERS="Walmart, Target, and FedEx"
DATE_FOUNDING_YEAR="2014"
IDENTITY_FOUNDER_NAME="Jane Smith"
IDENTITY_HQ_CITY="Austin, TX"
STAT_TOTAL_FUNDING_USD="$340M"
STAT_FUNDING_ROUNDS="four"
IDENTITY_LEAD_INVESTOR="Sequoia"
```

**Citation log entries:**

```
[^1] Market rank: claim requires independent verification. Sources required:
     - industry analyst report (e.g., Gartner, Forrester) — primary
     - trade press confirmation (e.g., Supply Chain Dive) — independent
[^2] Customer count + reference customers: requires
     - company-published case study OR press release — primary
     - customer-side confirmation (customer's own communications) — independent
[^3] Funding total + rounds: requires
     - SEC Form D filings OR Crunchbase entry — primary
     - VC firm portfolio page OR press release from lead investor — independent
[^4] Founder + founding year: requires
     - state business registration (e.g., TX SOS) — primary
     - LinkedIn founder profile OR press archive — independent
```

The transformation surfaces something important: a paragraph that *felt* like it was full of facts is actually full of unsourced claims. Parametrizing forces enumeration; enumeration forces citation.

## README / project documentation

**Before:**

> ## Performance
>
> AcmeRouter handles 50,000 requests per second on a single 4-core node, with p99 latency under 12ms. In production at Acme, we route 4.2 billion requests per day across our global edge network.

**After:**

> ## Performance
>
> `{{ IDENTITY_PRODUCT_NAME }}` handles `{{ STAT_BENCHMARK_RPS }}` requests per second on a single `{{ STAT_BENCHMARK_HARDWARE }}`, with p99 latency under `{{ STAT_BENCHMARK_LATENCY_MS }}`ms [^1][^2]. In production at `{{ IDENTITY_REFERENCE_DEPLOYMENT }}`, we route `{{ STAT_PRODUCTION_DAILY_REQUESTS }}` requests per day across our global edge network [^3][^4].

**`.env.example`:**

```
IDENTITY_PRODUCT_NAME="AcmeRouter"
STAT_BENCHMARK_RPS="50,000"
STAT_BENCHMARK_HARDWARE="4-core node"
STAT_BENCHMARK_LATENCY_MS="12"
IDENTITY_REFERENCE_DEPLOYMENT="Acme"
STAT_PRODUCTION_DAILY_REQUESTS="4.2 billion"
```

**Citation requirements:**

```
[^1][^2] Benchmark figures: requires
  - reproducible benchmark script in repo (primary)
  - independent benchmark run (e.g., TechEmpower, third-party blog) (independent)
[^3][^4] Production scale: requires
  - company engineering blog post with date (primary)
  - independent observability data (e.g., Cloudflare Radar, public status page) (independent)
```

## Configuration file / deployment manifest

Configs already lean toward parametrization, but often retain hard-coded values for "convenience." The mandate eliminates the convenience exception.

**Before (`docker-compose.yml`):**

```yaml
services:
  api:
    image: registry.acme.com/api:v3.2.1
    environment:
      - DATABASE_URL=postgres://acme:secret@db.acme.internal:5432/production
      - LOG_LEVEL=info
      - MAX_CONNECTIONS=200
    ports:
      - "8080:8080"
```

**After:**

```yaml
services:
  api:
    image: ${IDENTITY_REGISTRY_HOST}/${IDENTITY_IMAGE_NAME}:${VERSION_IMAGE_TAG}
    environment:
      - DATABASE_URL=${LINK_DATABASE_URL}
      - LOG_LEVEL=${CATEGORY_LOG_LEVEL}
      - MAX_CONNECTIONS=${THRESHOLD_MAX_CONNECTIONS}
    ports:
      - "${THRESHOLD_API_PORT}:${THRESHOLD_API_PORT}"
```

**`.env.example`:**

```
IDENTITY_REGISTRY_HOST="registry.acme.com"
IDENTITY_IMAGE_NAME="api"
VERSION_IMAGE_TAG="v3.2.1"
LINK_DATABASE_URL="postgres://USER:PASSWORD@HOST:PORT/DB"   # use real values in .env, never commit
CATEGORY_LOG_LEVEL="info"                                    # trace|debug|info|warn|error
THRESHOLD_MAX_CONNECTIONS="200"                              # tune per environment
THRESHOLD_API_PORT="8080"
```

Note: `DATABASE_URL` contained a secret (`secret` password). The example file shows the *shape* with placeholders, not the actual credential.

## Research report / market analysis

These artifacts are assertion-dense. The citation mandate dominates here.

**Before:**

> The global market for X is projected to reach $50B by 2030, growing at a 12% CAGR. Three players dominate: Acme (32% share), Beta Corp (24%), and Gamma Inc (18%). Enterprise adoption accelerated in 2024 following the EU's new compliance directive.

**After:**

> The global market for `{{ IDENTITY_MARKET_CATEGORY }}` is projected to reach `{{ STAT_MARKET_PROJECTED_SIZE_USD }}` by `{{ DATE_PROJECTION_HORIZON }}`, growing at a `{{ STAT_PROJECTED_CAGR_PCT }}` CAGR [^1][^2]. Three players dominate: `{{ IDENTITY_LEADER_1 }}` (`{{ STAT_LEADER_1_SHARE_PCT }}` share), `{{ IDENTITY_LEADER_2 }}` (`{{ STAT_LEADER_2_SHARE_PCT }}`), and `{{ IDENTITY_LEADER_3 }}` (`{{ STAT_LEADER_3_SHARE_PCT }}`) [^3][^4]. Enterprise adoption accelerated in `{{ DATE_ADOPTION_INFLECTION_YEAR }}` following `{{ IDENTITY_REGULATORY_CATALYST }}` [^5][^6].

**Citation requirements (with independence judgment):**

```
[^1][^2] Market size projection — at least two analyst firms with non-overlapping
         methodology. Two reports from the same firm don't count.
         Acceptable: Gartner + IDC. Not acceptable: Gartner core + Gartner deep-dive.
[^3][^4] Market share figures — primary methodology source + secondary confirmation.
         Companies' own self-reported share is one source; third-party measurement
         (e.g., Statista based on shipment data) is independent.
[^5][^6] Regulatory catalyst — text of the regulation itself (official journal) +
         independent legal analysis (law firm publication or academic paper).
         A press release from a vendor about the regulation is not independent.
```

## Data table

Tables present a special case: per-row assertions stack up quickly. Add citation columns.

**Before:**

| Provider | Market share | Founded |
|---|---|---|
| Acme | 32% | 2014 |
| Beta Corp | 24% | 2011 |
| Gamma Inc | 18% | 2018 |

**After:**

| Provider | Market share | Founded | Share source 1 | Share source 2 | Founded source 1 | Founded source 2 |
|---|---|---|---|---|---|---|
| `{{ IDENTITY_LEADER_1 }}` | `{{ STAT_LEADER_1_SHARE_PCT }}` | `{{ DATE_LEADER_1_FOUNDED }}` | [^1a] | [^1b] | [^1c] | [^1d] |
| `{{ IDENTITY_LEADER_2 }}` | `{{ STAT_LEADER_2_SHARE_PCT }}` | `{{ DATE_LEADER_2_FOUNDED }}` | [^2a] | [^2b] | [^2c] | [^2d] |
| `{{ IDENTITY_LEADER_3 }}` | `{{ STAT_LEADER_3_SHARE_PCT }}` | `{{ DATE_LEADER_3_FOUNDED }}` | [^3a] | [^3b] | [^3c] | [^3d] |

If twelve footnotes for three rows feels heavy, that's the point: the original table made twelve assertions, and shipping unsourced was hiding the cost. The parametrized version makes the citation budget visible.

## What to do when an artifact resists transformation

Some artifacts collapse when parametrized. A poem about Acme's founding story is *about* Acme; replacing the name with `{{ IDENTITY_COMPANY_NAME }}` destroys the artifact.

When this happens, do not force the transformation. Instead:

1. Surface the issue to the user: "This artifact is essentially particular — parametrizing would erase its purpose."
2. Offer alternatives: "Would you like me to (a) extract the *structure* into a separate template that could be re-instantiated for other companies, while leaving this artifact as-is, or (b) split the artifact into a particular keepsake and a reusable template?"
3. Wait for direction.

The mandate is for reusable artifacts. Particulars-as-art are not the target.
