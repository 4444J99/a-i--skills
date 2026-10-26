# Citation Independence: Judgment Calls

The multi-citation mandate says "≥2 independent sources." This file disambiguates "independent." It exists because most citation failures are not absent citations — they're *sibling* citations dressed up as independent ones.

## The independence test

Two sources are independent when ALL of the following are true:

1. **Different parent organizations.** Not just different URLs — different editorial chains of command.
2. **Neither cites the other as its source.** A secondary that just reports the primary is not independent of the primary.
3. **Each has direct access to the evidence**, OR each cites a *different* primary.
4. **No shared financial or contractual interest in the claim being true.**

Fail any test → one effective source, not two.

## Common failure modes

### Same-org siblings

The company's homepage + the company's blog + the company's press release + the company's investor presentation are **one source** for any claim about the company. They share an editorial chain.

| Source A | Source B | Independent? |
|---|---|---|
| acme.com/about | acme.com/blog/post | No — same org |
| acme.com | Acme's LinkedIn page | No — same org publishing on a different platform |
| Acme's 10-K | Acme's Q3 earnings call | No — same org, same accounting |
| Acme's case study | Acme's customer testimonial page | No — same org curating customer voices |

### Echo chains

A press release issued by Acme + a news article that quotes Acme's press release without independent reporting = **one source**. The news outlet's masthead doesn't make the reporting independent if the reporting has no independent evidence.

The test: if Source A retracted, would Source B's claim still stand? If no → echo.

### Aggregator + member

An industry-association report (e.g., trade group statistics) + a member company's restatement of those numbers = **one source**. The member got the number from the association.

### Analyst firm internal cross-reference

A Gartner report citing a different Gartner report = **one source**. Two reports from the same firm, even on different topics, share methodology choices that may bias the same direction.

### Wikipedia chains

A Wikipedia article cites a source; another article on the same wiki re-cites that source = **one source**. Wikipedia is a *navigator* of citations, not a source itself.

### Co-published or sponsored

A whitepaper co-authored by Acme and a research firm = **one source for any claim favorable to Acme**, even if the research firm's name appears. Sponsorship creates editorial pressure that compromises independence.

### Translations and reprints

The same article in English and French = **one source**. The same article in two different magazines (syndication) = **one source**.

## When sources ARE independent

| Source A | Source B | Independent? |
|---|---|---|
| Acme press release | Reuters article with new quote from non-Acme source | Yes — Reuters added independent evidence |
| EU regulation official text | Law firm's independent analysis | Yes — analysis adds non-EU expertise |
| Census Bureau data | Academic paper using BLS data | Yes — different primary sources, different agencies |
| Gartner report | IDC report | Yes — different firms, different methodologies |
| Company's audited financials (10-K) | Independent investigative journalism citing source documents | Yes — journalism has its own evidence chain |

## When you cannot find two independent sources

Don't fake it. Choose explicitly:

### Option 1: Flag and ship

Mark the assertion with `[CITATION-REQUIRED: only 1 independent source]` and list it in the verification gap section. Useful when the claim is non-load-bearing.

### Option 2: Demote to conditional

Rewrite the assertion to acknowledge the gap:

- Before: "Method X is 40% faster than method Y."
- After: "Per [the one source], method X is 40% faster than method Y; this figure has not been independently reproduced."

### Option 3: Demote to attribution

Reframe as "what someone said" rather than "what is true":

- Before: "Acme acquired Beta for $200M."
- After: "Acme announced the acquisition of Beta for $200M [^source]." (Now the assertion is that Acme announced, not that the figure is correct.)

### Option 4: Remove

If the claim cannot be cited and isn't reframeable, cut it. An artifact that omits a load-bearing unsourced claim is more credible than an artifact that asserts it.

## Special cases

### Mathematical or definitional claims

"A right triangle has one 90-degree angle" needs no citation — it's a definition. Apply this carefully: "Python is the most popular programming language" is not a definition, it's a contested empirical claim.

### Self-evident from the artifact

"Section 3 contains the API reference." Verify by reading section 3. No external citation needed.

### Direct quotations

A direct quote from a named person needs the source of the quote (single citation sufficient), but the *underlying truth* of what the person said still needs independent verification if the quote is being used as evidence.

- Quote-as-record: "Smith said, 'We will hit $1B revenue' [^press conference transcript]." — one citation is fine; you're citing that Smith said it.
- Quote-as-truth: "Acme will hit $1B revenue per CEO Smith [^press conference transcript][^Acme financial guidance]." — needs the second citation because you're using the quote to claim future revenue.

### Internal-only artifacts

Within an organization, "Acme's internal Q3 figures show…" with citation to the internal dashboard is acceptable for internal-only artifacts. The mandate still applies — internal dashboard + internal report = one source. Cross-check against another internal system (e.g., billing + CRM) for two independent internal sources.

## Quick reference

| If you have… | Treat as |
|---|---|
| 1 source | Flag the assertion |
| 2+ from same parent org | 1 source — find more |
| Press release + news that quotes it | 1 source — find original reporting |
| Wikipedia + the source Wikipedia cites | 1 source (the original) |
| Sponsored research + sponsor | 1 source |
| Two competing analyst firms | 2 sources ✓ |
| Government data + academic paper using different data | 2 sources ✓ |
| Primary text + independent analysis | 2 sources ✓ |

When in doubt, ask: "If source A were retracted, would source B's claim still stand on its own evidence?" If yes, independent. If no, echo.
