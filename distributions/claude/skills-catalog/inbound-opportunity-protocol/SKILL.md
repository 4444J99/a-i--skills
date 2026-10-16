---
license: MIT
name: inbound-opportunity-protocol
description: End-to-end protocol for when outbound open-source contributions generate inbound relationship opportunities. Covers contact verification, company research, architectural comparison, conversation preparation with multi-register talking points (technical/humanities/ELI5), response drafting, and honest boundary mapping. Triggers on inbound emails from contribution targets, cold outreach from people who found your PRs, or any signal that an open-source contribution attracted strategic attention.
---
license: MIT

# Inbound Opportunity Protocol

When outbound contributions attract inbound attention — an email, a follow, a DM, a meeting request — this protocol governs the response. The contribution engine's campaign phases (UNBLOCK → ENGAGE → CULTIVATE → HARVEST → INJECT) produce these moments. This skill handles HARVEST.

## When to Use

- An external person emails after seeing a PR or GitHub activity
- A company reaches out based on open-source contributions
- A contributor on your repos proposes collaboration
- Any signal that code output has converted to human contact

## The Protocol

### Phase 1: Verify (Before Responding)

Establish who contacted you and why. Never reply before completing verification.

**1.1 Identity verification:**
- Search GitHub for the person and their org (`gh api search/users`, `gh search repos owner:<org>`)
- Check their GitHub profile: repos, followers, contribution history, company affiliation
- Search the web: company website, LinkedIn, Twitter/X, Crunchbase
- Cross-reference with existing outreach/campaign data if the contact traces to a tracked relationship

**1.2 Company research (if applicable):**
- Fetch and analyze their public website, docs, and product pages
- Identify: team size, funding stage, tech stack, product architecture
- Check for job openings (research, don't mention)
- Assess: is this a potential employer, partner, collaborator, or user?

**1.3 Signal assessment:**
- What triggered the contact? (specific PR, GitHub profile, repo discovery)
- How fast did they respond? (same-day = they're monitoring the contributor space)
- What do they want? (knowledge exchange, hiring, partnership, product feedback)
- Strategic value: rate across 4 axes:
  - **Skill acquisition** — what can we learn from them?
  - **Reputation leverage** — does association increase visibility?
  - **Relationship depth** — could this become a lasting professional connection?
  - **Direct improvement** — does their work improve our stack?

### Phase 2: Architecture Comparison

Before responding, understand how their system compares to yours. This determines conversation strategy.

**2.1 Map their architecture:**
- Read their docs, API references, and any public code
- Identify their core primitives (what are their equivalents of your key abstractions?)
- Note what they've built vs what they're building vs what they're struggling with

**2.2 Find the intersection:**
- Where do architectures overlap? (shared problems, similar solutions)
- Where do they diverge? (different trade-offs, complementary approaches)
- What do you have that they don't? (your distinctive contribution to the conversation)
- What do they have that you don't? (what you can learn)

**2.3 Identify the hook:**
- Find one architectural position where your approach differs from the mainstream
- Frame it as a refinement, not a contradiction — "I'd push your thesis further" not "you're wrong"
- The hook must be genuine and grounded in implementation, not theoretical posturing

### Phase 3: Prepare Talking Points

Build a conversation prep document with three registers. Same architecture, three voices.

**3.1 Technical register:**
For each major architectural component:
- **30-second explanation** — conversational, no jargon, how to explain it to a peer
- **Design trade-off** — what was the alternative, why this was chosen
- **Honest limitation** — what doesn't work yet or where the design breaks
- **Connection to their question** — how this relates to what they asked about

**3.2 Humanities register:**
Translate each component into its intellectual lineage:
- Biological precedent (ecology, ethology, neuroscience)
- Philosophical framing (phenomenology, systems theory, process philosophy)
- Cultural/literary reference (art, literature, social theory)
- The humanities register demonstrates depth of understanding — knowing WHY it works at a conceptual level, not just how

**3.3 ELI5 register:**
Translate each component into a simple analogy:
- Everyday metaphor (kitchen, school, office, nature)
- No technical terms whatsoever
- The ELI5 register is the escape hatch — when reaching for jargon that can't be backed up, drop to ELI5. It sounds confident, not evasive.

**3.4 Boundary mapping:**
Explicitly list:
- **Three things NOT to claim** — areas where depth is thin or implementation is incomplete
- **Three questions to ask them** — questions that reveal their architecture without directly asking "show me your code"
- **Landmines to avoid** — company-specific sensitivities, naming confusions, things not to dismiss

### Phase 4: Draft Response

The response follows strict constraints:

**4.1 Length discipline:**
- Match or beat their brevity. If they wrote 5 sentences, write 4.
- Never explain full architecture in the first message.
- The response is a hook, not a presentation.

**4.2 Structure:**
1. Acknowledge what brought them to you (shows understanding of the connection)
2. Engage with their thesis — refine it, don't just agree ("resonates, but I'd push it further")
3. Offer the hook — one distinctive architectural position
4. Accept the meeting/chat
5. Sign off

**4.3 What NOT to include:**
- Don't link to repos (let them discover the iceberg)
- Don't mention job interest
- Don't list credentials or projects
- Don't oversell — a peer being consulted, not an applicant pitching

### Phase 5: Pre-Conversation Preparation

After sending the response and before the actual conversation:

**5.1 Code fluency pass:**
Read key source files — not to memorize, but to have *opinions* about design trade-offs. Know the constants, thresholds, and architectural reasons.

**5.2 Conversation strategy:**
- Lead with the distinctive claim (the hook from the response)
- Ask questions that reveal their architecture before exposing yours
- Cite external validation (contributor threads, community engagement) not just own work
- If asked about production scale: be honest. "Architecturally designed and unit-tested, not validated at scale."

**5.3 Power position awareness:**
If they reached out first, the responder is the expert being consulted. Maintain that framing:
- Don't volunteer weaknesses unprompted
- Don't ask about job openings
- Let employment/partnership surface naturally from demonstrated competence
- The conversation IS the audition without either side calling it that

### Phase 6: Post-Conversation

**6.1 Log the interaction:**
- Add/update entry in outreach.yaml with event and relationship score adjustment
- Update campaign.yaml if this advances a campaign phase
- Add to tracked_conversations.yaml if ongoing

**6.2 Backflow extraction:**
- What architectural patterns were learned from their system?
- What questions did they ask that reveal gaps in own thinking?
- Deposit learnings into backflow.yaml with organ targets

**6.3 Follow-up:**
- If action items were discussed, execute within 48 hours
- If they suggested looking at something specific, research and respond
- If the conversation was purely exploratory, brief follow-up within 24 hours

## Artifacts

The protocol produces three artifacts, stored in `contrib_engine/artifacts/`:

1. `<company>-briefing.md` — company profile, architecture, team, competitive positioning
2. `<company>-conversation-prep.md` — technical talking points, trade-offs, boundaries, questions
3. `<company>-conversation-filters.md` — humanities and ELI5 translations of the same architecture

## Key Principles

- **Research before responding.** Never reply to an inbound contact without completing Phase 1.
- **Shorter than theirs.** The response is a hook, not a pitch deck.
- **Three registers, one architecture.** Technical for depth, humanities for breadth, ELI5 for escape.
- **Honest boundaries.** Know what NOT to claim before the conversation starts.
- **The conversation is the demonstration.** Competence surfaces through substance, not credentials.
