# Reader Testing Prompts

Prompts for testing document effectiveness with a fresh reader perspective.

---

## Core Testing Questions

### Discovery Questions
Questions a reader might ask when looking for this document:

```
- How do I [accomplish the document's main goal]?
- What is [the system/feature/process] this document describes?
- Why did we decide to [main decision in document]?
- What are the requirements for [project/feature]?
- When should I use [approach/system/process]?
```

### Comprehension Questions
Questions to verify the document conveys its content clearly:

```
- What problem does this solve?
- Who is the target audience?
- What are the key decisions made?
- What are the main constraints?
- What are the success criteria?
- What happens if [edge case]?
```

### Actionability Questions
Questions to verify the reader knows what to do next:

```
- What do I need to do first?
- Who do I contact for questions?
- Where can I find more details about [topic]?
- What are the next steps?
- How do I get started?
```

---

## Document-Specific Testing Prompts

### For Technical Specs

**Ask Reader Claude:**
```
Based on this spec, answer:
1. What system is being built?
2. What are the main components?
3. What are the dependencies?
4. What would a developer need to implement this?
5. What are the key technical decisions?
```

**Check for:**
- Can reader identify the system boundaries?
- Are APIs and interfaces clear?
- Are edge cases documented?
- Is the implementation path clear?

### For Decision Documents

**Ask Reader Claude:**
```
Based on this document, answer:
1. What decision was made?
2. What options were considered?
3. Why was the chosen option selected?
4. What are the tradeoffs?
5. Would you make the same decision based on this info?
```

**Check for:**
- Is the rationale convincing?
- Are alternatives fairly presented?
- Are tradeoffs acknowledged?
- Is the decision reversible, and is that clear?

### For PRDs

**Ask Reader Claude:**
```
Based on this PRD, answer:
1. What problem is being solved?
2. Who are the users?
3. What does success look like?
4. What's in scope vs out of scope?
5. What would you build based on this?
```

**Check for:**
- Is the problem statement clear?
- Are user stories testable?
- Are requirements prioritized?
- Is scope clearly bounded?

### For RFCs

**Ask Reader Claude:**
```
Based on this RFC, answer:
1. What is being proposed?
2. Why is this needed?
3. Who is affected?
4. What concerns would you raise?
5. Would you approve this proposal?
```

**Check for:**
- Is the motivation compelling?
- Is the impact clear?
- Are migration concerns addressed?
- Is the ask clear?

---

## Gap Detection Prompts

### Ambiguity Check
```
Read this document and identify:
1. Any terms that are used but not defined
2. Any statements that could be interpreted multiple ways
3. Any sections that assume knowledge the reader might not have
4. Any pronouns with unclear referents
```

### Assumption Check
```
What prior knowledge does this document assume the reader has?
List specific:
1. Technical concepts
2. Organizational context
3. Historical decisions
4. Domain knowledge
```

### Consistency Check
```
Review this document for internal consistency:
1. Do all sections align with the stated goals?
2. Are there any contradictions between sections?
3. Do examples match the described approach?
4. Are metrics/numbers consistent throughout?
```

### Completeness Check
```
What questions remain unanswered after reading this document?
Consider:
1. Edge cases not covered
2. Stakeholders not mentioned
3. Timeline gaps
4. Missing dependencies
```

---

## Testing Protocol

### Step 1: Generate Reader Questions
Before testing, predict what questions readers will ask:

```
Given this document about [topic], what would:
- A new team member ask?
- A senior engineer ask?
- A product manager ask?
- A stakeholder ask?
```

### Step 2: Test with Fresh Context
Provide ONLY the document to Reader Claude (no conversation context):

```
You are reading this document for the first time.
[PASTE DOCUMENT]

Answer these questions:
[INSERT RELEVANT QUESTIONS FROM ABOVE]

For each answer, note:
- Confidence level (High/Medium/Low)
- What was unclear or ambiguous
```

### Step 3: Identify Gaps
Compare Reader Claude's answers to expected answers:

| Question | Expected Answer | Reader Answer | Gap? |
|----------|-----------------|---------------|------|
| [Q1]     | [Expected]      | [Actual]      | [Y/N] |

### Step 4: Prioritize Fixes
Rank gaps by severity:

| Gap | Type | Impact | Fix Priority |
|-----|------|--------|--------------|
| [Gap 1] | Ambiguity/Missing/Contradiction | High/Med/Low | P0/P1/P2 |

---

## Common Failure Patterns

### The Curse of Knowledge
**Symptom**: Reader Claude asks for definitions of terms the author considers obvious.
**Fix**: Add a terminology section or define terms inline.

### The Missing Context
**Symptom**: Reader Claude can't explain *why* decisions were made.
**Fix**: Add background section or inline rationale.

### The Buried Lede
**Symptom**: Reader Claude buries the main point in their summary.
**Fix**: Move key information to the beginning.

### The Scope Creep
**Symptom**: Reader Claude thinks the document covers more than it does.
**Fix**: Add explicit "Out of Scope" section.

### The Dangling Reference
**Symptom**: Reader Claude asks about things mentioned but not explained.
**Fix**: Either explain inline or link to relevant documents.

---

## Quick Testing Checklist

Before considering a document "done":

- [ ] Fresh Reader Claude can summarize the main point in one sentence
- [ ] Reader Claude correctly identifies the target audience
- [ ] Reader Claude can answer "What should I do next?"
- [ ] Reader Claude doesn't identify any undefined terms
- [ ] Reader Claude finds no internal contradictions
- [ ] Reader Claude's questions are about details, not fundamentals
