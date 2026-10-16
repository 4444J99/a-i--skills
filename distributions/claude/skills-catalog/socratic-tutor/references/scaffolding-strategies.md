# Scaffolding Strategies

Techniques for guiding learners to understanding without giving answers.

---

## The Scaffolding Spectrum

```
MORE SUPPORT ←──────────────────────────────────→ LESS SUPPORT

Direct          Hints &      Guiding       Open
Instruction  →  Cues      →  Questions  →  Inquiry

"Here's how"    "Look at"    "What if"     "How would you"
```

**Goal**: Start with minimal support. Add scaffolding only when needed. Remove it as learner progresses.

---

## Core Principles

### 1. Zone of Proximal Development

Scaffold within the zone between:
- What they can do alone (too easy)
- What they cannot do even with help (too hard)

**Signs you're in the zone:**
- Productive struggle (effortful but not frustrated)
- Partial success with guidance
- "Aha" moments after hints

### 2. Gradual Release of Responsibility

```
I do it     →     We do it     →     You do it
(Model)          (Guided)            (Independent)
```

Don't skip to "you do it" before they're ready. Don't linger on "I do it" longer than necessary.

### 3. Fade the Scaffold

Remove support incrementally:
- Start: "The issue is in the loop condition."
- Later: "The issue is in this function."
- Later: "What section would you check first?"
- Finally: "Walk me through your debugging process."

---

## Scaffolding Techniques

### Decomposition

Break complex problems into manageable pieces.

| Instead of | Try |
|------------|-----|
| "Implement a sorting algorithm" | "First, how would you find the smallest element? Now, what do you do with it?" |
| "Write an essay about X" | "What's your main claim? What's one piece of evidence?" |
| "Debug this code" | "What's the first thing that happens when you run it?" |

**Template:**
> "Let's break this down. What's the first small step?"

### Analogies & Prior Knowledge

Connect new concepts to familiar ones.

| New Concept | Familiar Analogy |
|-------------|------------------|
| Recursion | Russian nesting dolls, mirrors facing mirrors |
| Variables | Labeled boxes, name tags |
| APIs | Restaurant menus (you don't need to know how the kitchen works) |
| Inheritance | Family traits passed down |

**Template:**
> "This is like [familiar concept]. How might that help you think about this?"

### Worked Examples

Demonstrate with a parallel problem, then have them apply it.

**Process:**
1. Solve a similar (simpler) problem while thinking aloud
2. Highlight the transferable strategy
3. Present their problem
4. Ask: "How might you apply what we just did?"

**Caution:** Don't solve THEIR problem. Solve an adjacent one.

### Constraint Reduction

Remove complexity temporarily to focus on core concept.

| Full Problem | Reduced Version |
|--------------|-----------------|
| Handle all input types | "Assume input is always valid for now" |
| Build complete app | "Let's just get one feature working" |
| Debug entire codebase | "Let's isolate this one function" |

**Template:**
> "Let's simplify. If we ignore [complexity], what would you do?"

### Think-Aloud Protocol

Have learners verbalize their reasoning.

**Why it works:**
- Surfaces hidden confusion
- Slows down impulsive answers
- Creates teaching moments
- Builds metacognition

**Prompts:**
- "Walk me through your thinking."
- "Say out loud what you're considering."
- "What options are you weighing?"

### Visualization & Representation

Make abstract concepts concrete.

| Abstract | Concrete |
|----------|----------|
| Program flow | Draw a flowchart |
| Data structures | Sketch boxes and arrows |
| Arguments | Map claims and evidence |
| Processes | Create timeline |

**Template:**
> "Can you draw/diagram what's happening here?"

---

## Strategic Hints

### Hint Levels (Progressive Disclosure)

**Level 1: Metacognitive**
Focus on process, not content.
- "What strategies have worked for you before?"
- "What resources might help?"
- "Where would you start?"

**Level 2: Directional**
Point to a region without revealing answer.
- "The issue is somewhere in this section."
- "Think about how [concept] works."
- "What do you know about [related topic]?"

**Level 3: Specific**
Narrow to a particular element.
- "Look at line 15."
- "Check the return value."
- "Consider the edge case where X is zero."

**Level 4: Leading**
Almost give it away (use sparingly).
- "What if the loop never terminates?"
- "The problem is with how you're initializing X."
- "You're very close—it's a one-character fix."

### Hint Timing

**Give hints when:**
- 2-3 genuine attempts without progress
- Frustration is mounting
- The block is syntactic/trivial, not conceptual
- Time constraints require it

**Withhold hints when:**
- They haven't truly tried yet
- Struggle is productive
- They're learning more from the process
- A breakthrough seems imminent

---

## Handling Common Situations

### "Just tell me the answer"

**Resist.** Instead:
- "What have you tried so far?"
- "What's blocking you right now?"
- "Let's figure it out together. Start by telling me what you know."

If they persist:
> "I could tell you, but you won't learn as much. Let's try one more approach together."

### Repeated wrong answers

Don't just say "wrong." Instead:
1. Ask them to trace their reasoning
2. Find where the logic breaks down
3. Ask a question that reveals the gap

> "Let's test that. If X is true, what should we see when we try Y?"

### Complete silence / "I have no idea"

Break the paralysis:
- "What's the first thing you notice?"
- "What do you know for sure, even if it seems obvious?"
- "If you had to guess, what would you try?"
- "What part makes the least sense?"

### Surface-level answer

Push deeper:
- "Why does that work?"
- "What if I changed this?"
- "Can you think of an exception?"
- "Explain it to me like I've never seen this before."

### Correct answer, wrong reasoning

Don't let it slide:
- "Right answer. Walk me through how you got there."
- "Interesting. What if the input were different—would your approach still work?"
- "You got it, but I'm curious about your process. Why did you choose that method?"

---

## Fading Scaffolds

### Signs learner is ready for less support
- Solving similar problems faster
- Asking better questions themselves
- Self-correcting errors
- Explaining reasoning clearly
- Applying concepts to new contexts

### How to fade
1. Remove the most supportive scaffold first
2. Increase wait time before offering hints
3. Ask them to predict what hint you might give
4. Have them scaffold a peer

### Example progression
```
Week 1: "Look at the loop condition on line 12."
Week 2: "The bug is in the loop. What would you check?"
Week 3: "Walk me through your debugging process."
Week 4: "What do you think? Where would you start?"
```

---

## Scaffolding Checklist

Before giving support, ask yourself:

- [ ] Have they genuinely attempted the problem?
- [ ] Is the struggle productive or frustrating?
- [ ] Am I scaffolding, or just doing it for them?
- [ ] Is this the minimum support needed?
- [ ] Can I phrase this as a question instead of a statement?
- [ ] Will this scaffold help them solve similar problems later?
- [ ] Am I building independence, not dependence?

---

## Quick Reference: Scaffolds by Situation

| Situation | Scaffold |
|-----------|----------|
| Overwhelmed by complexity | Decomposition |
| Unfamiliar concept | Analogy to prior knowledge |
| Can't start | Worked example (parallel problem) |
| Multiple things wrong | Constraint reduction |
| Hidden confusion | Think-aloud protocol |
| Abstract concept | Visualization |
| Almost there | Directional hint |
| Trivial syntax block | Specific hint (then return to questions) |
