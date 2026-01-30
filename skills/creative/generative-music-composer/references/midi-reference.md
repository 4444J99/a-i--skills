# MIDI Reference

## MIDI File Creation

### Using midiutil

```python
from midiutil import MIDIFile

def create_midi(notes, filename, tempo=120):
    """
    notes: list of (pitch, start_time, duration, velocity)
    """
    midi = MIDIFile(1)  # One track
    track = 0
    channel = 0
    time = 0  # Start at beginning

    midi.addTempo(track, time, tempo)

    for pitch, start, duration, velocity in notes:
        midi.addNote(track, channel, pitch, start, duration, velocity)

    with open(filename, 'wb') as f:
        midi.writeFile(f)
```

### Using mido

```python
import mido

def create_midi_mido(notes, filename, tempo=500000):  # microseconds per beat
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Sort by start time
    events = []
    for pitch, start, duration, velocity in notes:
        events.append((start, 'note_on', pitch, velocity))
        events.append((start + duration, 'note_off', pitch, 0))

    events.sort(key=lambda x: x[0])

    # Convert to delta times
    last_time = 0
    for time, msg_type, pitch, velocity in events:
        delta = int((time - last_time) * mid.ticks_per_beat)
        track.append(mido.Message(msg_type, note=pitch,
                                  velocity=velocity, time=delta))
        last_time = time

    mid.save(filename)
```

## MIDI Messages

### Note Messages

```python
# Note On (start note)
msg = mido.Message('note_on', note=60, velocity=100, time=0)

# Note Off (end note)
msg = mido.Message('note_off', note=60, velocity=0, time=480)

# Velocity: 0-127 (0 = note off equivalent)
```

### Control Change

```python
# Sustain pedal
msg = mido.Message('control_change', control=64, value=127)  # Pedal down
msg = mido.Message('control_change', control=64, value=0)    # Pedal up

# Volume
msg = mido.Message('control_change', control=7, value=100)

# Pan
msg = mido.Message('control_change', control=10, value=64)  # Center

# Modulation
msg = mido.Message('control_change', control=1, value=64)
```

### Program Change (Instrument)

```python
# Change instrument
msg = mido.Message('program_change', program=0)  # Piano

# Common instruments (General MIDI):
# 0: Acoustic Grand Piano
# 24: Acoustic Guitar
# 33: Electric Bass
# 40: Violin
# 56: Trumpet
# 73: Flute
```

## Reading MIDI

```python
def read_midi(filename):
    """Extract notes from MIDI file"""
    mid = mido.MidiFile(filename)
    notes = []

    for track in mid.tracks:
        current_time = 0
        active_notes = {}  # pitch -> (start_time, velocity)

        for msg in track:
            current_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                active_notes[msg.note] = (current_time, msg.velocity)

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active_notes:
                    start, velocity = active_notes.pop(msg.note)
                    duration = current_time - start
                    notes.append({
                        'pitch': msg.note,
                        'start': start,
                        'duration': duration,
                        'velocity': velocity
                    })

    return notes
```

## Time Conversion

```python
def ticks_to_seconds(ticks, ticks_per_beat, tempo):
    """Convert MIDI ticks to seconds"""
    # tempo is in microseconds per beat
    seconds_per_tick = (tempo / 1e6) / ticks_per_beat
    return ticks * seconds_per_tick

def seconds_to_ticks(seconds, ticks_per_beat, tempo):
    """Convert seconds to MIDI ticks"""
    seconds_per_tick = (tempo / 1e6) / ticks_per_beat
    return int(seconds / seconds_per_tick)

def bpm_to_tempo(bpm):
    """Convert BPM to MIDI tempo (microseconds per beat)"""
    return int(60_000_000 / bpm)

def tempo_to_bpm(tempo):
    """Convert MIDI tempo to BPM"""
    return 60_000_000 / tempo
```

## Multi-Track

```python
def create_multitrack(tracks_data, filename, tempo=120):
    """
    tracks_data: list of (instrument, notes) tuples
    """
    mid = mido.MidiFile(type=1)  # Type 1 = multi-track

    # Tempo track
    tempo_track = mido.MidiTrack()
    mid.tracks.append(tempo_track)
    tempo_track.append(mido.MetaMessage('set_tempo',
                                         tempo=bpm_to_tempo(tempo)))

    for channel, (instrument, notes) in enumerate(tracks_data):
        track = mido.MidiTrack()
        mid.tracks.append(track)

        # Set instrument
        track.append(mido.Message('program_change',
                                  channel=channel,
                                  program=instrument,
                                  time=0))

        # Add notes
        events = []
        for n in notes:
            events.append((n['start'], 'note_on', n['pitch'], n['velocity']))
            events.append((n['start'] + n['duration'], 'note_off', n['pitch'], 0))

        events.sort(key=lambda x: x[0])

        last_time = 0
        for time, msg_type, pitch, velocity in events:
            delta = int(time - last_time)
            track.append(mido.Message(msg_type,
                                      channel=channel,
                                      note=pitch,
                                      velocity=velocity,
                                      time=delta))
            last_time = time

    mid.save(filename)
```

## Common Pitfalls

1. **Delta time vs absolute time**: MIDI uses delta (relative) times
2. **Note off**: Can be note_off message OR note_on with velocity=0
3. **Channel 10**: Reserved for drums in General MIDI
4. **Tempo**: Is per-track meta message, usually on track 0
5. **Ticks per beat**: Varies by file, check `mid.ticks_per_beat`
