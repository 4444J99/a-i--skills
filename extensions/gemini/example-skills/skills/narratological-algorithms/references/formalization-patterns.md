# Formalization Patterns

Examples of converting narrative craft principles from prose to implementable algorithmic forms.

---

## Pattern 1: Conceptual Statement → Constraint Rule

**Source (prose):**
> "A scene must turn on a value change."

**Target (constraint):**
```
SCENE_VALIDITY_CONSTRAINT:
  ASSERT: scene.opening_value != scene.closing_value
  IF VIOLATED: scene is structurally invalid; DELETE or REVISE
```

**Source (prose):**
> "The collision should feel inevitable in retrospect, surprising in the moment."

**Target (constraint):**
```
COLLISION_CONSTRAINT:
  REQUIRES:
    - surprise_on_first_encounter == TRUE
    - logical_on_reflection == TRUE
  TEST: Can audience trace causal chain backward after reveal?
```

---

## Pattern 2: Process Description → Pseudocode Function

**Source (prose):**
> "Work backward from the collision point to plant the necessary setup elements."

**Target (pseudocode):**
```python
def retrofit_plot(collision_point):
    """Reverse-engineer setups from discovered collision"""
    required_elements = analyze_collision_requirements(collision_point)
    
    for element in required_elements:
        setup_scene = find_earliest_viable_placement(element)
        setup_scene.plant(element, visibility="low")
        
    validate_causal_chain(collision_point)
    return story_with_planted_setups
```

**Source (prose):**
> "Test each scene by asking whether it could be removed without damaging the whole."

**Target (pseudocode):**
```python
def necessity_test(scene, story):
    """Determine if scene is structurally necessary"""
    story_without = story.remove(scene)
    
    if story_without.is_coherent() and story_without.climax_works():
        return SCENE_IS_EXPENDABLE
    else:
        return SCENE_IS_NECESSARY
```

---

## Pattern 3: Best Practice → Validity Test

**Source (prose):**
> "Coincidence may be used to start complications but never to resolve them."

**Target (validity test):**
```
COINCIDENCE_VALIDITY_TEST:
  INPUT: coincidence_event, story_position
  
  IF story_position <= MIDPOINT:
    IF coincidence_event.creates_complication:
      RETURN: VALID
  
  IF story_position > MIDPOINT:
    IF coincidence_event.resolves_conflict:
      RETURN: INVALID (deus ex machina)
      
  IF story_position == CLIMAX:
    RETURN: ALWAYS_INVALID
```

**Source (prose):**
> "Characters should never learn or grow."

**Target (validity test):**
```
CHARACTER_STASIS_TEST:
  FOR character IN main_cast:
    episode_start_state = character.values_and_behaviors(t=0)
    episode_end_state = character.values_and_behaviors(t=end)
    
    IF episode_start_state != episode_end_state:
      RETURN: VIOLATION ("no hugging, no learning" breached)
      
  RETURN: VALID
```

---

## Pattern 4: Comparison → Decision Table

**Source (prose):**
> "Tragedy imitates persons better than average; comedy imitates persons worse than average, but 'worse' in comedy means the ludicrous—defect without pain."

**Target (decision table):**
| Genre | Character Type | Constraint |
|-------|---------------|------------|
| Tragedy | Better than average | Suffering must be undeserved; inspires pity |
| Comedy | Worse than average | Defect must be **ludicrous** only |
| Comedy | Worse than average | Defect must NOT cause pain/destruction |
| Drama | As they are | Realistic portraiture; mixed qualities |

**Source (prose):**
> "If the story is internal, the problem is external. If external, internal."

**Target (decision table):**
| Story Focus | Antagonism Source | Example |
|-------------|-------------------|---------|
| Internal journey (psychological) | External obstacles | Character seeking peace vs. chaotic world |
| External goal (achievement) | Internal obstacles | Character seeking prize vs. own fears |
| Balance | Both | Standard dramatic structure |

---

## Pattern 5: Taxonomy → Classification Tree

**Source (prose):**
> "Bridge elements can be shared locations, transferred objects, or mutual acquaintances."

**Target (classification tree):**
```
BRIDGE_ELEMENT_TYPES
├── SHARED_LOCATION
│     Restaurant, event venue, workplace
│     Multiple characters access independently
│
├── TRANSFERRED_OBJECT
│     Physical item passes between storylines
│     Must seem insignificant when introduced
│     Examples: golf ball, undergarment, gift
│
└── MUTUAL_ACQUAINTANCE
      Person known to characters in different plots
      Connection not initially apparent
      Reveals relationship at collision
```

**Source (prose):**
> "Arts differ by medium (what is used), object (what is imitated), and manner (how it is presented)."

**Target (classification tree):**
```
IMITATIVE_ARTS_TAXONOMY
├── BY MEDIUM
│     ├── Rhythm alone → Dance
│     ├── Harmony + Rhythm → Music
│     ├── Language alone → Poetry/Prose
│     └── Language + Harmony + Rhythm → Tragedy/Comedy
│
├── BY OBJECT
│     ├── Better than reality → Tragedy, Epic
│     ├── As they are → Realism
│     └── Worse than reality → Comedy, Parody
│
└── BY MANNER
      ├── Narrative (author voice) → Lyric
      ├── Narrative (assumed voice) → Epic
      └── Dramatic (direct action) → Tragedy/Comedy
```

---

## Pattern 6: Principle with Exception → Conditional Rule

**Source (prose):**
> "Show, don't tell—except when missing information would cause confusion."

**Target (conditional rule):**
```
EXPOSITION_RULE:
  DEFAULT: dramatize_information()  # Show through action
  
  EXCEPTION:
    IF audience_confusion_level > THRESHOLD:
      IF no_dramatic_vehicle_available:
        PERMIT: direct_exposition()
        CONSTRAINT: convert_to_ammunition_in_conflict()
        
  NEVER: expository_lump_outside_dramatic_context
```

**Source (prose):**
> "Use the probable impossible over the improbable possible."

**Target (conditional rule):**
```
PROBABILITY_RULE:
  PREFERENCE_ORDER:
    1. Probable AND Possible (ideal)
    2. Probable but Impossible (acceptable—audience accepts premise)
    3. Improbable but Possible (avoid—strains belief despite accuracy)
    4. Improbable AND Impossible (forbidden)
    
  RATIONALE: Emotional truth > Factual accuracy
```

---

## Pattern 7: Qualitative Spectrum → Enumerated Scale

**Source (prose):**
> "Values progress from positive to contrary to contradictory to negation of the negation."

**Target (enumerated scale):**
```
VALUE_PROGRESSION_SCALE:
  LEVEL 0: POSITIVE
           Example: Love, Justice, Truth
           
  LEVEL 1: CONTRARY (absence)
           Example: Indifference, Unfairness, Uncertainty
           
  LEVEL 2: CONTRADICTORY (opposite)
           Example: Hate, Injustice, Lie
           
  LEVEL 3: NEGATION OF NEGATION (extreme/ironic)
           Example: Self-hatred, Tyranny disguised as justice, 
                    Lie believed as truth
                    
  PROGRESSION_RULE: Story must touch Level 2 minimum;
                    Masterworks reach Level 3
```

---

## Pattern 8: Workflow → State Machine

**Source (prose):**
> "Write the step-outline until it pitches brilliantly, then the treatment, then the screenplay."

**Target (state machine):**
```
WRITING_STATE_MACHINE:

  [IDEA] 
      │
      ▼
  [STEP_OUTLINE] ←──────────────────┐
      │                              │
      │ pitch_test()                 │
      ▼                              │
  <Pitch Brilliant?> ───NO──────────┘
      │
      YES
      ▼
  [TREATMENT]
      │
      │ structure_locked()
      ▼
  <Structure Sound?> ───NO──→ [STEP_OUTLINE]
      │
      YES
      ▼
  [SCREENPLAY]
      │
      ▼
  [REVISION] (refinement only, not structural)
```

---

## Usage Notes

1. **Preserve original terminology** where it has specific meaning
2. **Add identifiers** (e.g., `LD-A0`) for cross-referencing
3. **Include source attribution** for direct quotes
4. **Mark inference** when formalizing implied principles
5. **Test formalization** by asking: "Could a system execute this?"
