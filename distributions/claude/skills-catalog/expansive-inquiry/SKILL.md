---
name: expansive-inquiry
description: "Multi-perspective collaborative inquiry. Decomposes a topic into six cognitive lenses (Scope, Logic, Mythos, Bridge, Meta, Pattern) that operate as a chorus rather than a single voice, then synthesizes meta-patterns no single lens could find alone. MANDATORY TRIGGERS: 'expansive inquiry', 'multi-perspective inquiry', 'explore this from every angle', 'six-lens analysis', 'run a chorus on this'. STRONG TRIGGERS: 'help me think through X deeply', 'mythopoetic AND logical analysis'. Do NOT trigger on simple Q&A or failure-focused inquiries — use premortem for those."
license: MIT
complexity: advanced
time_to_learn: 1hour
tags:
  - multi-perspective
  - cognitive-architecture
  - epistemic-pluralism
  - recursive-inquiry
  - collaborative-intelligence
  - distributed-cognition
  - prospective-synthesis
governance_phases: [shape, build]
governance_norm_group: quality-gate
governance_auto_activate: false
organ_affinity: [organ-i, organ-iv]
triggers: [user-asks-expansive-inquiry, user-asks-multi-perspective, user-asks-deep-exploration, context:open-ended-inquiry, context:dramaturgical-analysis]
complements: [recursive-systems-architect, knowledge-architecture, evaluation-to-growth, prompt-engineering-patterns, narratological-algorithms, research-synthesis-workflow]
---

# Expansive Inquiry

## What this is

Expansive Inquiry is a cognitive architecture for distributed intelligence. Most inquiry flattens a topic into a single voice. This skill orchestrates six — each with a distinct epistemic posture — and weaves their outputs into a synthesis that surfaces emergent meta-patterns no single lens could find alone.

The lineage:
- The original prototype was a React app (V4) that ran six specialized AI roles sequentially over a user-supplied topic and exported each stage as YAML-frontmatter Markdown.
- Two rounds of critique pushed it toward (a) a real cognitive architecture rather than a six-stage pipeline, (b) parallel execution of independent stages, (c) context summarization to avoid token bloat in later stages, (d) a synthesis layer that detects contradictions across lenses, and (e) an HTML visualization of the inquiry shape ("epistemic signature").
- This skill encodes the matured methodology. Claude IS the orchestrator. The six lenses are personality vectors Claude adopts in turn, not external services. No React app required.

## When to invoke

**Good targets:**
- Open-ended thematic questions ("What is the role of ritual in distributed teams?")
- Strategic decisions where the user wants epistemic pluralism, not narrowing
- Dramaturgical / artistic / philosophical analysis where logic alone would flatten the subject
- Research synthesis where multiple disciplinary lenses are warranted
- Anything the user describes with words like "deeply", "from every angle", "chorus", "mythopoetic"

**Bad targets:**
- Failure-focused analysis → use `premortem` instead
- Decision-by-vote among options → use the LLM Council instead
- Factual/closed questions ("What's the capital of Mongolia?") → just answer
- Code review or feature spec → too narrow for six-lens orchestration

If the user wants ONE answer, this skill is the wrong tool. If they want a SHAPE — the topology of the topic across cognitive registers — this is the right tool.

---

## The six lenses (epistemic personalities)

Each lens has: a role, a posture, a prompt template, and an output structure. They are NOT generic "perspectives" — they are specific cognitive postures with distinct anti-patterns to resist.

### 1. Scope AI (clarification)

**Role:** Distill the user's topic into a single precise actionable inquiry sentence.
**Posture:** Phenomenological reduction. What is essential? What is peripheral?
**Anti-pattern to resist:** Restating the topic verbatim. The Scope AI MUST narrow or sharpen.

**Prompt:**
```
You are the Scope AI. Your role is to take an inquiry and distill it into a single,
precise, actionable sentence that captures the core question.

TOPIC: "{topic}"

Tasks:
1. Restate the topic as a focused question or proposition.
2. Name what is essential (must explore) and what is peripheral (can defer).
3. Identify any hidden ambiguities the user may not have noticed.

Output as Markdown with three sections: ## Core Inquiry, ## Essential vs. Peripheral, ## Hidden Ambiguities.
```

### 2. Logic AI (rational branching)

**Role:** Build a rigorous logical tree of orthodox lines of inquiry.
**Posture:** Analytic philosophy. Why? How? What if?
**Anti-pattern to resist:** Listing five generic branches with no internal recursion.

**Prompt:**
```
You are the Logic AI. You build rigorous logical frameworks via systematic rational exploration.

TOPIC: "{topic}"
SCOPE: {scope_summary}

Tasks:
1. Propose 5 orthodox, rational lines of inquiry.
2. For each line, drill three levels deep using "why?", "how?", or "what if?" — each level
   building on the previous, not branching laterally.
3. Render as a hierarchical tree (Markdown nested lists).

Output as Markdown with sections: ## Five Lines, ## Recursive Tree, ## Strongest Branch.
```

### 3. Mythos AI (intuitive branching)

**Role:** Reveal hidden dimensions through metaphor, archetype, and narrative.
**Posture:** Mythopoetic. Stories and symbols that illuminate.
**Anti-pattern to resist:** Generic "this is like a hero's journey" mappings. Mythos AI must commit to specific archetypal claims.

**Prompt:**
```
You are the Mythos AI. You think in stories, metaphors, and archetypal patterns.

TOPIC: "{topic}"
SCOPE: {scope_summary}

Tasks:
1. Propose 5 metaphorical or mythopoetic framings of the topic. Be specific to the topic — no
   generic "hero's journey" or "Tower of Babel" unless the structural fit is genuinely tight.
2. For each framing, write a 2-3 sentence analogical story or symbolic reading.
3. Identify the archetypal pattern revealed (e.g., trickster, threshold, sacrifice, return).

Output as Markdown with sections: ## Five Framings, ## Stories, ## Archetypal Reading.
```

### 4. Bridge AI (lateral / cross-domain)

**Role:** Find unexpected connections between this topic and seemingly unrelated domains.
**Posture:** Transdisciplinary. Surface analogical structure across far-apart fields.
**Anti-pattern to resist:** Adjacent-domain analogies (e.g., bridging biology to medicine). Bridge AI must REACH.

**Prompt:**
```
You are the Bridge AI. You find unexpected connections between seemingly unrelated domains.

TOPIC: "{topic}"
SCOPE: {scope_summary}
PRIOR LENSES: Logic produced {logic_summary}; Mythos produced {mythos_summary}.

Tasks:
1. Identify 5 domains far from the topic's natural neighborhood (e.g., bridge a software topic
   to choreography, fungal networks, monetary policy, glassblowing, or ant foraging — not to
   adjacent software).
2. For each, draw a specific structural analogy that bridges the domain to the topic.
3. Propose a hybrid question that emerges only from each cross-domain connection.

Output as Markdown with sections: ## Five Bridges, ## Hybrid Questions, ## Most Productive Bridge.
```

### 5. Meta AI (recursive design)

**Role:** Design self-improving feedback loops over the inquiry itself.
**Posture:** Reflexive. The inquiry is a system; what would make it converge faster?
**Anti-pattern to resist:** Treating "meta" as just "summary." Meta AI must propose machinery.

**Prompt:**
```
You are the Meta AI. You design self-improving recursive systems and think about thinking itself.

TOPIC: "{topic}"
PRIOR LENSES: Scope, Logic, Mythos, Bridge — full transcripts above.

Tasks:
1. Analyze the prior stages as a system. What did each lens contribute that the others missed?
2. Design a feedback loop that could refine the inquiry: which questions should be regenerated,
   which lines pruned, which stages re-run with revised input?
3. Propose 3 concrete ways the system could learn from this specific inquiry pattern.

Output as Markdown with sections: ## System Diagnosis, ## Feedback Loop, ## Three Adaptations.
```

### 6. Pattern AI (emergent meta-pattern recognition)

**Role:** Detect motifs and meta-patterns that span across all prior lenses.
**Posture:** Hyperscanning. What recurs? What is the topology?
**Anti-pattern to resist:** Restating themes from one lens as if they were emergent. Pattern AI must find what is visible ONLY in cross-lens overlay.

**Prompt:**
```
You are the Pattern AI. You recognize emergent structures and meta-patterns across complex,
multi-perspective information.

TOPIC: "{topic}"
PRIOR LENSES: Scope, Logic, Mythos, Bridge, Meta — full transcripts above.

Tasks:
1. Scan all five prior outputs for repeating motifs, structures, or themes that appear in MORE
   THAN ONE lens — those are the emergent patterns.
2. Propose 3 meta-patterns and explain how each manifests in at least 3 different lenses.
3. Speculate on the broader significance: what does the cross-lens overlay reveal about the
   topic that no single lens could?

Output as Markdown with sections: ## Cross-Lens Motifs, ## Three Meta-Patterns, ## Topological Reading.
```

---

## Execution graph (parallel where independent, sequential where dependent)

The original V4 ran all six stages sequentially. This is wasteful. The dependency graph:

```
Scope ──┬──> Logic ────┐
        ├──> Mythos ───┤
        │              ├──> Meta ──> Pattern
        └──> Bridge ───┘
```

**Stage 1 — Scope (sequential).** Must complete first; downstream lenses key off the scoped inquiry.

**Stage 2 — Logic, Mythos, Bridge (parallel).** All three take Scope as input but are independent of each other. Spawn three sub-agents in parallel via the Agent tool with `subagent_type: general-purpose` and the prompts above.

**Stage 3 — Meta (sequential).** Depends on stages 1+2; reflexive over the prior outputs.

**Stage 4 — Pattern (sequential).** Depends on all five prior; cross-lens overlay only works on a complete corpus.

**Performance note:** parallelizing stage 2 cuts wall-clock time roughly in half versus pure sequential execution.

---

## Context window discipline

The V4 prototype passed `JSON.stringify(results)` to every later stage, blowing through token budgets. This skill summarizes prior outputs before passing them down.

**Summarization rule:** for any prompt context that includes prior lens output, pass:
- The 1-paragraph **executive summary** of each prior lens (≤ 100 words).
- The full output ONLY for the immediately preceding lens (Meta sees full Bridge; Pattern sees full Meta but compressed earlier lenses).

If the user's topic is already token-heavy (e.g., a 10K-word brief), produce a Scope-stage compression of that brief and use the compression downstream.

---

## Output artifacts

Every Expansive Inquiry session produces:

```
expansive-inquiry-{slug}/
├── 00-scope.md          # YAML frontmatter + Scope output
├── 01-logic.md          # YAML frontmatter + Logic output
├── 02-mythos.md         # YAML frontmatter + Mythos output
├── 03-bridge.md         # YAML frontmatter + Bridge output
├── 04-meta.md           # YAML frontmatter + Meta output
├── 05-pattern.md        # YAML frontmatter + Pattern output
├── 06-synthesis.md      # Cross-lens synthesis + epistemic signature
└── inquiry-report.html  # Visual report (optional, see below)
```

Where `{slug}` is the kebab-cased topic.

### Per-stage frontmatter template

```yaml
---
title: "{stage_name} — {topic}"
description: "{stage_description}"
topic: "{topic}"
stage: "{stage_name}"
ai_role: "{stage_role}"
stage_number: {n}
total_stages: 6
inquiry_type: expansive_collaborative
generated: "{iso_timestamp}"
tags:
  - expansive-inquiry
  - {stage_slug}
  - {topic_slug}
methodology: multi-lens-collaborative-inquiry
---
```

### The synthesis stage (06)

The synthesis is the product. Most users will read the synthesis and skim the lens outputs. It must include:

1. **Topological reading.** What is the SHAPE of the topic across the six lenses?
2. **Epistemic signature.** A short character vector: e.g., "logic-heavy + metaphorically thin + recursively deep + bridge-rich". This is what the V5 critique called the "epistemic signature."
3. **Productive contradictions.** Where do lenses disagree? Disagreement is signal — surface it, don't smooth it.
4. **Three meta-patterns.** Pulled directly from Pattern AI, sharpened.
5. **The next inquiry.** Every Expansive Inquiry should produce its own next question. Always.

### Optional: HTML visualization

If the user requests a visual or if the inquiry is being shared/presented, generate `inquiry-report.html`:
- Single self-contained HTML file with inline CSS + (optionally) Chart.js for the epistemic-signature radar chart
- Dark background (#0a0e1a), six-card grid (one per lens) with distinct accent colors per stage
- Top section: synthesis + epistemic signature radar
- Footer: timestamp + topic + methodology version

---

## Important notes

- **Don't flatten the chorus.** If you find yourself writing similar things in Logic and Mythos, one of them is wrong. The Logic AI must NOT moonlight as the Mythos AI.
- **Resist generic outputs.** A generic Mythos reading ("this is like a hero's journey") fails the skill. Each lens must commit to topic-specific claims.
- **Spawn stage-2 lenses in parallel.** Single-message Agent calls with three tool uses. Sequential spawning wastes time and contaminates outputs.
- **Compress before recursing.** Never pass full prior outputs to all downstream lenses. Use the summarization rule above.
- **Surface contradictions in the synthesis.** Disagreement between Logic and Mythos is the most generative output of the entire inquiry. Do not smooth it.
- **Every inquiry produces a next inquiry.** No Expansive Inquiry terminates as "done" — it terminates as "and now this further question opens." Always conclude with the next question.
- **This is not the premortem.** The premortem assumes failure and reverse-engineers cause. Expansive Inquiry assumes nothing and explores the topology. If the user wants to know how their plan could fail, hand off to `premortem`.
- **This is not the LLM Council.** The Council polls multiple agents for opinion on a single decision. Expansive Inquiry decomposes a topic into six cognitive postures and synthesizes the cross-lens overlay. Different mechanism, different output.
