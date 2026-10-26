# Domain Production Stack — {{DOMAIN_NAME}}

**Stratum:** 6 (Production stack)
**Domain:** {{DOMAIN_NAME}}
**Created:** {{DATE}}
**Authority:** {{USER}}

## Question

What does the work require to ship?

## Capture pipeline

How input gets acquired (cameras, mics, sensors, scraping, ingest).

| Stage | Tool / hardware | Configuration | Notes |
|---|---|---|---|
| _input source_ | _tool_ | _settings_ | _gotchas_ |

## Processing pipeline

How input transforms (editing, analysis, modeling, rendering).

| Stage | Tool / hardware | Configuration | Notes |
|---|---|---|---|
| _processing step 1_ | _tool_ | _settings_ | _gotchas_ |

## Distribution pipeline

How output reaches audience (platforms, formats, schedules).

| Channel | Format | Cadence | Notes |
|---|---|---|---|
| _channel_ | _format_ | _frequency_ | _gotchas_ |

## Surface map

Where the audience encounters the work (1st party / 2nd party / 3rd party).

| Tier | Surface | Owned? | Notes |
|---|---|---|---|
| 1st party | _our domain / our newsletter / our portfolio_ | yes | full control |
| 2nd party | _co-marketed channels_ | partial | shared control |
| 3rd party | _platforms (YouTube / Twitter / etc.)_ | no | platform risk |

## Tool inventory (versioned)

Specific software / hardware in use.

| Tool | Version | Function | Replacement risk |
|---|---|---|---|
| _tool 1_ | _v_ | _what it does_ | _what to swap to if it dies_ |

## Walk-through example

Walk a single artifact end-to-end as the example. A fresh contributor can ship a unit of work using only what's documented here.

**Artifact:** _name a representative output_

**Steps:**
1. _Capture step_
2. _Processing step_
3. _Distribution step_

**Outcome:** _what this produces, where it lands, how it's measured_

## Validation gate

A new contributor can ship a unit of work using only what's documented here.

## Cross-references

- Stratum 5 agent fleet — `domain-capture-engineer` consumes this stratum's capture pipeline as config

## Changelog

- {{DATE}} — initial fill
