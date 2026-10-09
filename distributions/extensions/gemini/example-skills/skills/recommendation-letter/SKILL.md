---
name: recommendation-letter
description: Draft, revise, or polish an evidence-based letter of recommendation for a scholarship, employment, or graduate study. Produce useful editable Markdown from facts supplied by the recommender, with optional PDF output when requested and a renderer is available. Use when asked for a recommendation, reference letter, or revision of an existing letter; establish the relationship, use concrete evidence, and preserve honest limits without inventing facts.
license: MIT
side_effects: [creates-files]
governance_phases: [shape, build]
organ_affinity: [organ-vi]
triggers: [user-asks-to-write-recommendation-letter, user-asks-for-reference-letter, user-asks-to-polish-a-recommendation]
---

# Recommendation Letter

Turn the facts a recommender actually holds into a credible, editable reference. Complete
the core workflow with text authoring; PDF rendering is optional and requires an available
document or PDF tool.

**Authority:** draft and prepare the letter for the recommender's review. Do not sign it,
claim it has been reviewed, or send it without explicit user authorization for that action.

**Data handling:** keep subject details and filled letters out of skill files, examples,
source repositories, commits, and public workspaces. Return the draft directly or save it
to the user's requested private location outside the source checkout, following the host
environment's artifact rules. Check the actual destination; a folder named
`recommendations/` does not establish that it is ignored by Git or private.

## Step 1 — Establish the facts and purpose

Reuse facts already supplied in the request, attachments, or existing draft. Collect only
what remains missing:

- **Relationship:** who the recommender is to the subject, in what capacity, and for how
  long when known. This establishes how the writer knows what they assert.
- **Identities:** the recommender's name and relevant role; the subject's name and preferred
  form of address. Use supplied pronouns or write around them when unknown.
- **Audience and purpose:** recipient or committee; scholarship, role, or program; relevant
  requirements and any requested length or format.
- **Evidence:** at least one concrete action, observed moment, or result the recommender can
  support. Distinguish firsthand observation from information supplied by someone else.
- **Contact:** the follow-up details the recommender wants included.

Ask a concise question for missing substantive facts. Do not invent relationships, dates,
achievements, credentials, motives, or anecdotes. If the user wants a draft before all facts
are available, use clearly marked placeholders and list the unresolved items separately.
Do not present that draft as complete or ready to send.

## Step 2 — Draft useful editable Markdown

Read [the recommendation rubric](references/recommendation-rubric.md). Build a letter with:

1. The requested date, recipient, salutation, and subject line, where supplied or appropriate.
2. An opening that states the relationship and the purpose of the recommendation.
3. Two or three focused paragraphs connecting concrete evidence to the relevant opportunity.
4. An endorsement whose strength matches the recommender's actual judgment, followed by an
   offer of follow-up, the recommender's name, and the supplied contact details.

Aim for one page unless the user or recipient requires otherwise. Preserve the recommender's
voice and the meaningful specifics. Remove repetitive adjectives and habitual hedging while
retaining material uncertainty and limits of observation. Do not turn limited knowledge into
certainty or insert an unconditional endorsement the recommender has not supported.

Treat an unexplained gap as unknown. Reframe a limitation constructively only when the
recommender's evidence supports that interpretation; do not invent deliberateness or intent.

## Step 3 — Review the draft against its sources

Check each factual claim against the supplied material. Verify names, the relationship,
recipient, opportunity, evidence, and contact details. Identify unresolved placeholders and
any claims that need the recommender's confirmation. Check the letter against the rubric.

Provide the complete editable Markdown even when no document renderer is available. Saving
a file is complete only after the destination contains the intended text; return its link
using the host environment's supported format.

## Step 4 — Render a PDF when requested

Use an available document or PDF tool and follow its instructions. Preserve the editable
Markdown alongside the rendered version. Do not assume a specific repository, Python
module, template package, or renderer is installed.

After rendering, open or render the actual PDF and inspect every page for missing text,
clipping, awkward page breaks, contact details, and unresolved placeholders. Verify the
requested page count before describing the result as a one-page letter. If rendering fails
or no renderer is available, provide the Markdown and state that the PDF was not produced.

## Step 5 — Hand off for human review

Show the letter and briefly flag the precise relationship wording or other facts that need
attention. State which artifacts were produced and whether any information remains missing.
The recommender reviews and signs; sending requires the user's explicit authorization.

## Reference

- [Recommendation rubric](references/recommendation-rubric.md) — the seven-rule drafting and
  review checklist, including evidence, honest scope, follow-up, and presentation.
