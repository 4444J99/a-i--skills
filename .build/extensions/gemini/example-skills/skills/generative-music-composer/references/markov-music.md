# Markov Chains for Music Generation

## Basic Markov Model

### First-Order (Single Note Context)

```python
from collections import defaultdict
import random

class FirstOrderMarkov:
    def __init__(self):
        self.transitions = defaultdict(list)

    def train(self, sequences):
        for seq in sequences:
            for i in range(len(seq) - 1):
                current = seq[i]
                next_note = seq[i + 1]
                self.transitions[current].append(next_note)

    def generate(self, start, length):
        result = [start]
        current = start
        for _ in range(length - 1):
            if current in self.transitions:
                current = random.choice(self.transitions[current])
            else:
                current = random.choice(list(self.transitions.keys()))
            result.append(current)
        return result
```

### Higher-Order (N-gram Context)

```python
class HigherOrderMarkov:
    def __init__(self, order=2):
        self.order = order
        self.transitions = defaultdict(list)

    def train(self, sequences):
        for seq in sequences:
            for i in range(len(seq) - self.order):
                state = tuple(seq[i:i + self.order])
                next_note = seq[i + self.order]
                self.transitions[state].append(next_note)

    def generate(self, seed, length):
        if len(seed) < self.order:
            raise ValueError(f"Seed must have at least {self.order} elements")

        result = list(seed[:self.order])
        for _ in range(length - self.order):
            state = tuple(result[-self.order:])
            if state in self.transitions:
                next_note = random.choice(self.transitions[state])
            else:
                # Fallback: use any known state
                state = random.choice(list(self.transitions.keys()))
                next_note = random.choice(self.transitions[state])
            result.append(next_note)
        return result
```

## Weighted Transitions

### With Probability Counts

```python
class WeightedMarkov:
    def __init__(self, order=2):
        self.order = order
        self.counts = defaultdict(lambda: defaultdict(int))

    def train(self, sequences):
        for seq in sequences:
            for i in range(len(seq) - self.order):
                state = tuple(seq[i:i + self.order])
                next_note = seq[i + self.order]
                self.counts[state][next_note] += 1

    def get_probabilities(self, state):
        if state not in self.counts:
            return {}
        total = sum(self.counts[state].values())
        return {note: count/total
                for note, count in self.counts[state].items()}

    def generate(self, seed, length, temperature=1.0):
        result = list(seed[:self.order])
        for _ in range(length - self.order):
            state = tuple(result[-self.order:])
            probs = self.get_probabilities(state)

            if not probs:
                # Fallback
                state = random.choice(list(self.counts.keys()))
                probs = self.get_probabilities(state)

            # Apply temperature
            adjusted = self._apply_temperature(probs, temperature)
            next_note = self._weighted_choice(adjusted)
            result.append(next_note)

        return result

    def _apply_temperature(self, probs, temp):
        """Temperature: <1 = more deterministic, >1 = more random"""
        if temp == 1.0:
            return probs
        adjusted = {k: v ** (1/temp) for k, v in probs.items()}
        total = sum(adjusted.values())
        return {k: v/total for k, v in adjusted.items()}

    def _weighted_choice(self, probs):
        r = random.random()
        cumulative = 0
        for note, prob in probs.items():
            cumulative += prob
            if r <= cumulative:
                return note
        return list(probs.keys())[-1]
```

## Multi-Dimensional Markov

### Parallel Chains for Pitch and Rhythm

```python
class MultiDimensionalMarkov:
    def __init__(self, order=2):
        self.pitch_chain = WeightedMarkov(order)
        self.rhythm_chain = WeightedMarkov(order)
        self.joint_chain = WeightedMarkov(order)

    def train(self, melodies):
        """melodies: list of [(pitch, duration), ...]"""
        pitches = [[note[0] for note in melody] for melody in melodies]
        rhythms = [[note[1] for note in melody] for melody in melodies]
        joints = [melody for melody in melodies]

        self.pitch_chain.train(pitches)
        self.rhythm_chain.train(rhythms)
        self.joint_chain.train(joints)

    def generate_independent(self, pitch_seed, rhythm_seed, length):
        """Generate pitch and rhythm independently"""
        pitches = self.pitch_chain.generate(pitch_seed, length)
        rhythms = self.rhythm_chain.generate(rhythm_seed, length)
        return list(zip(pitches, rhythms))

    def generate_joint(self, seed, length):
        """Generate pitch and rhythm together"""
        return self.joint_chain.generate(seed, length)
```

## Constrained Generation

### Within Scale

```python
def generate_in_scale(markov, seed, length, scale_notes):
    """Generate but only allow notes in scale"""
    result = list(seed)
    for _ in range(length - len(seed)):
        state = tuple(result[-markov.order:])
        probs = markov.get_probabilities(state)

        # Filter to scale notes
        filtered = {k: v for k, v in probs.items()
                   if k % 12 in scale_notes}

        if not filtered:
            # Force to nearest scale note
            nearest = min(scale_notes,
                         key=lambda s: min(abs(s - k % 12) for k in probs))
            next_note = nearest + (result[-1] // 12) * 12
        else:
            # Renormalize
            total = sum(filtered.values())
            filtered = {k: v/total for k, v in filtered.items()}
            next_note = weighted_choice(filtered)

        result.append(next_note)
    return result
```

### With Rhythm Constraints

```python
def generate_with_meter(markov, seed, beats_per_measure, total_beats):
    """Generate rhythm that fits meter"""
    result = []
    current_beat = 0

    while current_beat < total_beats:
        beat_in_measure = current_beat % beats_per_measure

        # Get candidates
        state = tuple(result[-markov.order:]) if len(result) >= markov.order else None
        probs = markov.get_probabilities(state) if state else {0.5: 1.0}

        # Filter durations that don't cross barline badly
        remaining_in_measure = beats_per_measure - beat_in_measure
        filtered = {dur: prob for dur, prob in probs.items()
                   if dur <= remaining_in_measure or dur >= beats_per_measure}

        if filtered:
            total = sum(filtered.values())
            filtered = {k: v/total for k, v in filtered.items()}
            duration = weighted_choice(filtered)
        else:
            duration = remaining_in_measure

        result.append(duration)
        current_beat += duration

    return result
```

## Training Data Preprocessing

```python
def preprocess_midi(midi_file):
    """Extract training sequences from MIDI"""
    import mido

    mid = mido.MidiFile(midi_file)
    sequences = []

    for track in mid.tracks:
        notes = []
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append(msg.note)
        if notes:
            sequences.append(notes)

    return sequences

def augment_sequences(sequences):
    """Data augmentation: transpose to all keys"""
    augmented = []
    for seq in sequences:
        for transpose in range(-6, 6):
            augmented.append([n + transpose for n in seq])
    return augmented
```
