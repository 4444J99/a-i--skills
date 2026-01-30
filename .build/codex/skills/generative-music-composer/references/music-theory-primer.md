# Music Theory for Generative Systems

## Pitch and Scales

### MIDI Note Numbers
```
C4 (Middle C) = 60
Each semitone = +1 or -1
Octave = 12 semitones

Common range: 21 (A0) to 108 (C8)
```

### Scale Patterns (intervals from root)

| Scale | Pattern | Notes in C |
|-------|---------|------------|
| Major | 0,2,4,5,7,9,11 | C,D,E,F,G,A,B |
| Minor (Natural) | 0,2,3,5,7,8,10 | C,D,Eb,F,G,Ab,Bb |
| Harmonic Minor | 0,2,3,5,7,8,11 | C,D,Eb,F,G,Ab,B |
| Pentatonic Major | 0,2,4,7,9 | C,D,E,G,A |
| Pentatonic Minor | 0,3,5,7,10 | C,Eb,F,G,Bb |
| Blues | 0,3,5,6,7,10 | C,Eb,F,Gb,G,Bb |

```python
def get_scale_notes(root, scale_pattern):
    """Get MIDI notes for a scale"""
    return [(root + interval) % 12 + (root // 12) * 12
            for interval in scale_pattern]
```

## Chord Construction

### Chord Formulas (intervals from root)

| Chord Type | Formula | Example (C) |
|------------|---------|-------------|
| Major | 0,4,7 | C,E,G |
| Minor | 0,3,7 | C,Eb,G |
| Diminished | 0,3,6 | C,Eb,Gb |
| Augmented | 0,4,8 | C,E,G# |
| Major 7 | 0,4,7,11 | C,E,G,B |
| Minor 7 | 0,3,7,10 | C,Eb,G,Bb |
| Dominant 7 | 0,4,7,10 | C,E,G,Bb |
| Diminished 7 | 0,3,6,9 | C,Eb,Gb,A |

```python
CHORD_FORMULAS = {
    'maj': [0, 4, 7],
    'min': [0, 3, 7],
    'dim': [0, 3, 6],
    'aug': [0, 4, 8],
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10],
    '7': [0, 4, 7, 10],
    'dim7': [0, 3, 6, 9]
}

def build_chord(root, chord_type):
    return [root + interval for interval in CHORD_FORMULAS[chord_type]]
```

### Chord Progressions (Roman Numerals)

| Numeral | In C Major | Quality |
|---------|------------|---------|
| I | C | Major |
| ii | Dm | Minor |
| iii | Em | Minor |
| IV | F | Major |
| V | G | Major |
| vi | Am | Minor |
| vii° | Bdim | Diminished |

**Common Progressions:**
- I - IV - V - I (50s)
- I - V - vi - IV (Pop)
- ii - V - I (Jazz)
- I - vi - IV - V (Doo-wop)

## Rhythm

### Note Values

| Name | Beats (4/4) | Duration |
|------|-------------|----------|
| Whole | 4 | ○ |
| Half | 2 | d |
| Quarter | 1 | ♩ |
| Eighth | 0.5 | ♪ |
| Sixteenth | 0.25 | ♬ |
| Triplet | 1/3 | |

### Time Signatures

| Signature | Feel | Beats per measure |
|-----------|------|-------------------|
| 4/4 | Common time | 4 quarter notes |
| 3/4 | Waltz | 3 quarter notes |
| 6/8 | Compound duple | 6 eighth notes (2 groups of 3) |
| 5/4 | Irregular | 5 quarter notes |
| 7/8 | Irregular | 7 eighth notes |

## Voice Leading Rules

**Avoid:**
- Parallel fifths (both voices move same direction by P5)
- Parallel octaves (both voices move same direction by P8)
- Voice crossing (lower voice goes above higher)
- Large leaps (>P5) without step resolution

**Prefer:**
- Contrary motion
- Common tones held between chords
- Stepwise motion
- Resolve tendency tones (7→1, 4→3)

## Cadences

| Type | Chords | Function |
|------|--------|----------|
| Authentic | V - I | Strong ending |
| Plagal | IV - I | "Amen" |
| Half | ? - V | Pause, not end |
| Deceptive | V - vi | Surprise |

## Intervals

| Semitones | Name | Quality |
|-----------|------|---------|
| 0 | Unison | Perfect |
| 1 | Minor 2nd | Dissonant |
| 2 | Major 2nd | Dissonant |
| 3 | Minor 3rd | Consonant |
| 4 | Major 3rd | Consonant |
| 5 | Perfect 4th | Perfect |
| 6 | Tritone | Dissonant |
| 7 | Perfect 5th | Perfect |
| 8 | Minor 6th | Consonant |
| 9 | Major 6th | Consonant |
| 10 | Minor 7th | Dissonant |
| 11 | Major 7th | Dissonant |
| 12 | Octave | Perfect |
