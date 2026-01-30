# Choice Architecture for Interactive Theatre

## Meaningful Choice Design

### The MICE Framework

| Element | Description | Design Question |
|---------|-------------|-----------------|
| **M**ilieu | Setting/environment | Does choice change where story goes? |
| **I**dea | Theme/meaning | Does choice reveal different perspectives? |
| **C**haracter | Relationships | Does choice affect who characters become? |
| **E**vent | Plot outcomes | Does choice change what happens? |

### Choice Impact Matrix

```
              Low Stakes          High Stakes
           ┌─────────────────┬─────────────────┐
           │                 │                 │
Reversible │  Exploration    │   Pivotal       │
           │  choices        │   decisions     │
           │  (flavor)       │   (key moments) │
           │                 │                 │
           ├─────────────────┼─────────────────┤
           │                 │                 │
Permanent  │  Commitment     │   Defining      │
           │  choices        │   choices       │
           │  (investment)   │   (character)   │
           │                 │                 │
           └─────────────────┴─────────────────┘
```

## Choice Presentation Patterns

### Binary Choice

```
       ┌─────────────────┐
       │   SITUATION     │
       └────────┬────────┘
                │
       ┌────────┴────────┐
       ▼                 ▼
   ┌───────┐         ┌───────┐
   │   A   │         │   B   │
   │(clear │         │(clear │
   │stakes)│         │stakes)│
   └───────┘         └───────┘

Best for: Moral dilemmas, time pressure
Example: Save the child OR chase the villain
```

### Multiple Choice

```
              ┌───────────┐
              │ SITUATION │
              └─────┬─────┘
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    ┌───────┐   ┌───────┐   ┌───────┐
    │   A   │   │   B   │   │   C   │
    │       │   │       │   │       │
    └───────┘   └───────┘   └───────┘

Best for: Character expression, exploration
Example: Approach the stranger with humor/caution/aggression
```

### Hidden Choice

Choices embedded in natural actions:
- Where you stand = who you side with
- What you pick up = what you value
- Who you follow = whose story you see

### Delayed Choice

```
Make choice at T1 ────────────► Consequence at T2
   │                                   │
   └── Player may forget ──────────────┘
       Creates surprise/callback
```

## Avoiding Choice Paralysis

### Limit Options
- 2-4 options maximum
- More options = more anxiety
- Use tiered choices if complexity needed

### Provide Context
- Clear stakes ("One person dies either way")
- Character motivation hints
- Time cues ("You have seconds to decide")

### Create Urgency Appropriately
- Real time pressure for dramatic moments
- Breathing room for character choices
- Never rush world-changing decisions

### Signal Importance
```
Small Choice:          Casual presentation
                       No dramatic shift

Medium Choice:         Pause, lighting change
                       Character reaction

Major Choice:          Full stop, direct address
                       Clear stakes stated
```

## Consequence Design

### Immediate Feedback

```python
class ImmediateFeedback:
    """Show choice mattered right away"""

    def on_choice(self, choice):
        # Change something visible
        self.environment.shift_mood(choice.mood)

        # Character reacts
        self.npc.react_to_choice(choice)

        # Other audience sees impact
        self.broadcast_change(choice.visual_cue)
```

### Delayed Consequences

```python
class DelayedConsequence:
    """Callback to earlier choice"""

    def __init__(self):
        self.choice_memory = {}

    def record_choice(self, choice_id, option):
        self.choice_memory[choice_id] = option

    def trigger_consequence(self, choice_id):
        if choice_id in self.choice_memory:
            option = self.choice_memory[choice_id]
            # Reference the earlier choice
            self.remind_audience(choice_id, option)
            # Deliver consequence
            self.execute_consequence(option)
```

### Branching vs Folding

```
BRANCHING (expensive):
     ┌─ B1 ─ C1 ─ D1
A ───┼─ B2 ─ C2 ─ D2
     └─ B3 ─ C3 ─ D3

FOLDING (practical):
     ┌─ B1 ─┐
A ───┼─ B2 ─┼───── C ─┬─ D1
     └─ B3 ─┘         └─ D2

Memory: B1/B2/B3 affects HOW C plays
        but all reach same story beat
```

## Collective Choice Mechanics

### Voting Systems

| Method | Pros | Cons |
|--------|------|------|
| Majority | Democratic | Minority ignored |
| Plurality | Fast | May not represent will |
| Consensus | Everyone heard | Slow, may deadlock |
| Random delegate | Personal agency | Single person decides |
| Area voting | Physical/intuitive | Space constraints |

### Physical Voting

```
STAND HERE        or        STAND HERE
for Option A                for Option B
    ▼                           ▼
┌────────────┐           ┌────────────┐
│   ●  ●     │           │     ●      │
│ ●   ●  ●   │           │   ●   ●    │
│    ●  ●    │           │  ●    ●  ● │
└────────────┘           └────────────┘
    7 votes                   6 votes
```

### Sound Voting

```
"Cheer for the option you want!"

Option A: [CHEERING]
          └── measure volume ───► 72 dB

Option B: [CHEERING]
          └── measure volume ───► 68 dB

Winner: Option A
```

## Edge Cases

### No One Chooses

```python
def handle_no_choice(timeout_seconds=30):
    """What happens when audience doesn't choose"""
    options = [
        # Default: most narratively interesting
        "default_path",
        # Random: embrace chaos
        "random_choice",
        # Character decides: NPC takes action
        "npc_decides",
        # Performer decides: in-the-moment call
        "performer_call"
    ]
    return config.no_choice_policy
```

### Split Exactly Even

```python
def handle_tie():
    """What happens when votes are tied"""
    options = [
        # Coin flip: fair but arbitrary
        "random",
        # Both happen: parallel universe moment
        "both_paths",
        # Compromise: middle ground
        "synthesis",
        # Character breaks tie: dramatic moment
        "npc_tiebreaker"
    ]
```

### Disruptive Choices

When audience member tries to derail:
1. **Yes, and**: Incorporate if possible
2. **Redirect**: "Interesting, but..."
3. **Ignore**: Performer focuses elsewhere
4. **Acknowledge**: "That's not an option here"
