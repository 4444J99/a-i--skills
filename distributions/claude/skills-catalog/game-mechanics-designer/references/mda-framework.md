# MDA Framework Reference

The Mechanics-Dynamics-Aesthetics framework for analyzing and designing games.

## Framework Overview

```
Designer's Perspective:
Mechanics -> Dynamics -> Aesthetics

Player's Perspective:
Aesthetics <- Dynamics <- Mechanics
```

**Mechanics**: The rules, systems, and components.
**Dynamics**: The emergent behavior when players interact with mechanics.
**Aesthetics**: The emotional experience the player has.

## The Eight Aesthetics

### 1. Sensation (Game as Sense-Pleasure)

Visual, auditory, and tactile delight.

| Element | Example |
|---------|---------|
| Visual | Particle effects, screen shake |
| Audio | Satisfying hit sounds, music |
| Haptic | Controller rumble, impact feedback |

**Games**: Journey, Tetris Effect, Beat Saber

### 2. Fantasy (Game as Make-Believe)

Immersion in a fictional world or role.

| Element | Example |
|---------|---------|
| Role | Being a hero, villain, god |
| World | Exploring alien planets, historical eras |
| Power | Abilities beyond real life |

**Games**: Skyrim, The Witcher, Mass Effect

### 3. Narrative (Game as Drama)

Unfolding story and character development.

| Element | Example |
|---------|---------|
| Plot | Branching storylines |
| Character | Relationship building, dialogue |
| Stakes | Meaningful choices with consequences |

**Games**: The Last of Us, Disco Elysium, Undertale

### 4. Challenge (Game as Obstacle Course)

Testing skills, problem-solving, mastery.

| Element | Example |
|---------|---------|
| Skill | Timing, precision, reaction |
| Strategy | Planning, optimization |
| Mastery | Learning curves, difficulty progression |

**Games**: Dark Souls, Celeste, Super Meat Boy

### 5. Fellowship (Game as Social Framework)

Cooperation, community, shared experiences.

| Element | Example |
|---------|---------|
| Cooperation | Team objectives, shared resources |
| Communication | Voice chat, ping systems |
| Community | Guilds, clans, social spaces |

**Games**: Monster Hunter, Destiny 2, Animal Crossing

### 6. Discovery (Game as Uncharted Territory)

Exploration, secrets, and uncovering the unknown.

| Element | Example |
|---------|---------|
| Exploration | Open worlds, hidden areas |
| Secrets | Easter eggs, lore fragments |
| Knowledge | Learning game systems, meta discovery |

**Games**: Outer Wilds, Breath of the Wild, Metroid

### 7. Expression (Game as Self-Discovery)

Creativity, customization, personal statement.

| Element | Example |
|---------|---------|
| Creation | Building, crafting, designing |
| Customization | Character appearance, loadouts |
| Style | Playstyle freedom, emergent solutions |

**Games**: Minecraft, The Sims, Dreams

### 8. Submission (Game as Pastime)

Relaxation, comfort, mindless engagement.

| Element | Example |
|---------|---------|
| Flow | Repetitive satisfying loops |
| Comfort | Low-stakes, familiar patterns |
| Zen | Meditative gameplay |

**Games**: Stardew Valley, Candy Crush, Euro Truck Simulator

## Mechanics Catalog

### Core Mechanics

| Mechanic | Description | Common Dynamics |
|----------|-------------|-----------------|
| Movement | Traversal through space | Exploration, evasion |
| Combat | Conflict resolution | Risk/reward, mastery |
| Resource | Acquire, manage, spend | Economy, strategy |
| Puzzle | Pattern/logic solving | Discovery, challenge |
| Collection | Gathering items/sets | Completion, expression |
| Progression | Advancement systems | Investment, power fantasy |

### Social Mechanics

| Mechanic | Description | Common Dynamics |
|----------|-------------|-----------------|
| Trading | Exchange between players | Economy, negotiation |
| Voting | Group decision making | Politics, alliances |
| Communication | Information sharing | Coordination, deception |
| Competition | Zero-sum contests | Rivalry, ranking |
| Cooperation | Shared goals | Teamwork, dependency |

### Meta Mechanics

| Mechanic | Description | Common Dynamics |
|----------|-------------|-----------------|
| Random | Chance-based outcomes | Gambling, surprise |
| Timing | Time-based constraints | Pressure, rhythm |
| Information | Hidden/revealed knowledge | Deduction, bluffing |
| Territory | Area control | Strategy, conflict |

## Dynamics Patterns

### Emergent Dynamics

| Dynamic | Enabling Mechanics | Player Behavior |
|---------|-------------------|-----------------|
| Camping | Position + Respawn | Waiting at advantageous spots |
| Rushing | Speed + Objectives | Aggressive early attacks |
| Turtling | Defense + Resources | Building up before engaging |
| Griefing | PvP + Low Penalty | Harassment of other players |
| Min-maxing | Stats + Builds | Optimizing for performance |

### Positive Loops

```
Investment -> Reward -> More Investment

Example: Kill enemy -> Get XP -> Level up -> Kill harder enemies
```

### Negative Loops

```
Success -> Increased Challenge

Example: Lead in racing -> Worse power-ups (rubber banding)
```

## Design Process

### 1. Start with Aesthetics

What emotion do you want players to feel?

```
Primary Aesthetic: Challenge
Secondary: Discovery
Tertiary: Sensation
```

### 2. Identify Dynamics

What behaviors will create those feelings?

```
Challenge -> Mastery through repetition
Discovery -> Uncovering hidden techniques
Sensation -> Satisfying feedback on success
```

### 3. Design Mechanics

What rules enable those behaviors?

```
Tight controls + Difficult timing = Mastery gameplay
Hidden shortcuts + Environmental clues = Discovery
Screen shake + Sound effects + Slow-mo = Sensation
```

### 4. Iterate

Playtest and adjust:

| Observation | Diagnosis | Solution |
|-------------|-----------|----------|
| Players frustrated | Challenge too high | Adjust difficulty curve |
| Players bored | Challenge too low | Add complexity |
| Players confused | Mechanics unclear | Better onboarding |
| Players leave early | Wrong aesthetic mix | Revisit core pillars |

## Player Types (Bartle Taxonomy)

| Type | Primary Aesthetic | Seeks |
|------|-------------------|-------|
| Achievers | Challenge | Goals, completion |
| Explorers | Discovery | Secrets, knowledge |
| Socializers | Fellowship | Interaction, community |
| Killers | Challenge + Expression | Dominance, competition |

### Balancing for Types

| Feature | Achievers | Explorers | Socializers | Killers |
|---------|-----------|-----------|-------------|---------|
| Leaderboards | High | Low | Medium | High |
| Hidden areas | Medium | High | Low | Low |
| Chat systems | Low | Medium | High | Medium |
| PvP arenas | Medium | Low | Low | High |

## Analysis Template

```markdown
## Game: [Title]

### Primary Aesthetics
1. [First aesthetic]
2. [Second aesthetic]
3. [Third aesthetic]

### Core Mechanics
- [Mechanic 1]: [Brief description]
- [Mechanic 2]: [Brief description]

### Key Dynamics
- [Dynamic 1]: Emerges from [mechanic interaction]
- [Dynamic 2]: Emerges from [mechanic interaction]

### What Works
- [Strength 1]
- [Strength 2]

### What Could Improve
- [Issue 1]: [Suggested mechanic change]
- [Issue 2]: [Suggested mechanic change]
```
