# Game Balancing Formulas

Mathematical formulas and curves for game economy and progression design.

## Progression Curves

### Linear Growth

Best for: Early tutorials, simple increments.

```
Value = Base + (Level * Increment)

Example: Health = 100 + (Level * 10)
Level 1: 110 HP
Level 5: 150 HP
Level 10: 200 HP
```

### Exponential Growth

Best for: RPG leveling, upgrade costs that feel increasingly significant.

```
Value = Base * (Multiplier ^ Level)

Example: XP Required = 100 * (1.5 ^ Level)
Level 1: 150 XP
Level 5: 759 XP
Level 10: 5,767 XP
```

### Polynomial Growth

Best for: Smooth mid-game progression, balanced difficulty curves.

```
Value = Base * (Level ^ Exponent)

Example: Cost = 10 * (Level ^ 2)
Level 1: 10 gold
Level 5: 250 gold
Level 10: 1,000 gold
```

### Logarithmic Growth

Best for: Diminishing returns, soft caps on stats.

```
Value = Base * log(Level + 1)

Example: Damage Bonus = 10 * log(Level + 1)
Level 1: 3.01
Level 5: 7.78
Level 10: 10.41
```

### S-Curve (Logistic)

Best for: Skill rating systems, bounded progression.

```
Value = Max / (1 + e^(-k * (Level - midpoint)))

Parameters:
- Max: Upper bound
- k: Steepness
- midpoint: Inflection point
```

## Economy Balancing

### Source/Sink Balance

Total sources must equal or slightly exceed sinks to prevent deflation.

| Source (Income) | Sink (Spending) |
|-----------------|-----------------|
| Quest rewards | Equipment repair |
| Enemy drops | Consumables |
| Crafting sales | Upgrades |
| Daily login | Fast travel |
| Achievement bonuses | Cosmetics |

### Time-to-Earn Ratio

```
Earnings Per Hour = (Reward * Success Rate) / Time Per Attempt

Target: 1-2 hours of gameplay for meaningful upgrade
```

### Currency Conversion

For premium currency:

```
Premium Value = (Free Earnings * Hours Saved) / Exchange Rate

Example:
- Free earning rate: 100 gold/hour
- Premium pack: 1000 gold
- Should represent: 8-12 hours of gameplay value
```

## Combat Balancing

### Damage Per Second (DPS)

```
DPS = (Base Damage * Attack Speed) * (1 + Crit Rate * Crit Multiplier)

Example:
Base Damage: 50
Attack Speed: 2/sec
Crit Rate: 10%
Crit Multiplier: 1.5x

DPS = (50 * 2) * (1 + 0.1 * 0.5) = 105
```

### Time to Kill (TTK)

```
TTK = Enemy HP / (DPS - Enemy Regen)

Target TTK by enemy type:
- Minion: 1-3 seconds
- Standard: 5-10 seconds
- Elite: 30-60 seconds
- Boss: 2-5 minutes
```

### Effective Health

```
Effective HP = HP / (1 - Damage Reduction)

Example:
HP: 1000
Armor providing 20% reduction

Effective HP = 1000 / 0.8 = 1250
```

### Power Budget

Assign point values to different stats to ensure balance:

| Stat | Point Value |
|------|-------------|
| +1% Crit | 1 point |
| +10 Damage | 2 points |
| +50 HP | 2 points |
| +5% Attack Speed | 1.5 points |

All items at same tier should have equal total points.

## Difficulty Scaling

### Player Count Scaling

```
Enemy HP = Base HP * (1 + (Players - 1) * Scale Factor)

Scale Factor recommendations:
- Casual: 0.5 per player
- Standard: 0.75 per player
- Hardcore: 1.0 per player
```

### Adaptive Difficulty

Track rolling performance:

```
Difficulty Modifier = Moving Average of (Deaths / Encounters)

If Modifier > 0.3: Reduce difficulty 10%
If Modifier < 0.1: Increase difficulty 10%
```

## Randomization

### Weighted Random

```python
def weighted_random(items, weights):
    total = sum(weights)
    roll = random() * total
    cumulative = 0
    for item, weight in zip(items, weights):
        cumulative += weight
        if roll <= cumulative:
            return item
```

### Loot Tables

| Rarity | Drop Weight | Approximate % |
|--------|-------------|---------------|
| Common | 100 | 60% |
| Uncommon | 50 | 30% |
| Rare | 15 | 9% |
| Epic | 1.5 | 0.9% |
| Legendary | 0.15 | 0.1% |

### Pity System

Guarantee rare drops after drought:

```
Effective Drop Rate = Base Rate * (1 + Attempts Since Last / Pity Threshold)

Or hard pity:
If Attempts >= Pity Threshold: Guarantee drop
```

## Quick Reference Tables

### XP Scaling by Level

| Level | Light RPG | Standard RPG | Hardcore RPG |
|-------|-----------|--------------|--------------|
| 1-10 | 100-500 | 100-1000 | 100-5000 |
| 11-25 | 500-2000 | 1000-10000 | 5000-50000 |
| 26-50 | 2000-5000 | 10000-50000 | 50000-500000 |

### Session Length Targets

| Game Type | Session Target | Checkpoint Frequency |
|-----------|----------------|----------------------|
| Mobile casual | 2-5 minutes | Every action |
| Mobile mid-core | 10-20 minutes | Every 2-3 minutes |
| PC casual | 30-60 minutes | Every 5-10 minutes |
| PC core | 1-3 hours | Every 15-30 minutes |

### Reward Frequency

| Reward Type | Frequency |
|-------------|-----------|
| Micro (gold, XP) | Every encounter |
| Small (consumables) | Every 2-5 minutes |
| Medium (equipment) | Every 10-30 minutes |
| Large (levels, unlocks) | Every 30-90 minutes |
| Major (achievements) | Every 2-4 hours |
