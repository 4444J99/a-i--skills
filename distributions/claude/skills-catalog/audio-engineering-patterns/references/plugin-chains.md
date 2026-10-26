# Common Processing Chains

Standard plugin orders and signal chains for mixing and sound design.

## Fundamental Chain Order

Insert processing follows the signal flow principle: shape first, control second, enhance last.

```
High-Pass Filter → EQ (Subtractive) → Compression → EQ (Additive) → Saturation → Spatial FX
```

**Why this order matters**: Cutting problem frequencies before compression prevents the compressor from reacting to unwanted energy. Additive EQ after compression lets you boost without triggering gain reduction.

---

## Vocal Chain

### Standard Lead Vocal

```
1. Gain Trim (hit plugin sweet spots)
2. High-Pass Filter (80-120 Hz)
3. De-Esser (5-8 kHz, 4-6 dB reduction)
4. Subtractive EQ (cut 200-400 Hz mud, cut 800 Hz honk)
5. Compressor (3-4:1, medium attack, auto release, 4-8 dB GR)
6. Additive EQ (boost 3 kHz presence, shelf 10 kHz air)
7. Plate Reverb (send, 1.5-2.5s decay, pre-delay 40-60 ms)
8. Delay (send, 1/4 note tempo-synced, filtered)
```

### Backing Vocals

```
1. High-Pass Filter (150-200 Hz)
2. Subtractive EQ (narrow cut at competing lead vocal frequencies)
3. Compressor (4-6:1, fast attack to tame peaks)
4. De-Esser (more aggressive than lead)
5. Reverb (send, longer decay than lead for depth)
```

**Tip**: Keep backing vocals darker and further back than the lead. Cut 2-5 kHz to prevent competition.

---

## Drum Chains

### Kick Drum

```
1. High-Pass Filter (30-40 Hz, remove sub-rumble)
2. Subtractive EQ (cut 300-400 Hz boxiness)
3. Compressor (4:1, slow attack 10-30 ms to preserve transient, fast release)
4. Additive EQ (boost 60-80 Hz weight, boost 3-5 kHz click)
5. Saturation (subtle, adds harmonics for small speakers)
```

### Snare Drum

```
1. High-Pass Filter (80-100 Hz)
2. Subtractive EQ (cut 400-600 Hz cardboard)
3. Compressor (4:1, medium attack to shape transient)
4. Additive EQ (boost 200 Hz body, boost 5 kHz crack)
5. Parallel Compression (heavy compression blended in at low level)
```

### Drum Bus

```
1. Subtractive EQ (gentle cuts only)
2. Bus Compressor (2-4:1, slow attack 10-30 ms, auto release, 2-4 dB GR)
3. Saturation (tape emulation, subtle)
4. Clipper (catch transient peaks, 1-2 dB)
```

---

## Bass Chains

### Electric Bass (DI)

```
1. High-Pass Filter (30-40 Hz)
2. Subtractive EQ (cut 200-300 Hz mud)
3. Compressor (4:1, medium-fast attack, medium release, 6-10 dB GR)
4. Additive EQ (boost 80 Hz fundamental, boost 800-1200 Hz growl)
5. Saturation (tube or tape, adds upper harmonics)
```

### Synth Bass / 808

```
1. EQ (cut everything above 200 Hz for pure sub layer)
2. Compressor (gentle, 2:1, mostly for consistency)
3. Saturation (drive upper harmonics for speaker translation)
4. Limiter (catch peaks, maintain level)
```

**Technique**: Layer a clean sub (low-passed) with a driven mid-bass (high-passed at 150 Hz) for both weight and presence.

---

## Guitar Chains

### Clean Electric Guitar

```
1. High-Pass Filter (80-100 Hz)
2. Subtractive EQ (cut 300-500 Hz if muddy)
3. Compressor (2-3:1, slow attack, preserve dynamics)
4. Additive EQ (boost 2-3 kHz sparkle)
5. Chorus or Delay (send, subtle width)
```

### Distorted Electric Guitar

```
1. High-Pass Filter (80-100 Hz, critical to prevent low-end mush)
2. Low-Pass Filter (10-12 kHz, tame fizz)
3. Subtractive EQ (cut 800 Hz honk, cut 3-5 kHz if harsh)
4. Compression (often not needed—distortion is compression)
5. Room Reverb (send, short decay, blend into mix)
```

---

## Mix Bus Chain

### Standard Mix Bus

```
1. EQ (gentle broad moves only: +1 dB shelf at 10 kHz, -1 dB at 300 Hz)
2. Bus Compressor (2:1, slowest attack, auto release, 1-3 dB GR)
3. Tape Saturation (subtle warmth and glue)
4. Limiter (safety, -1 dB ceiling, rarely engaging)
```

### Mastering Chain

```
1. Linear Phase EQ (broad tonal shaping)
2. Multiband Compression (gentle, target problem bands only)
3. Stereo Enhancement (mid/side EQ, subtle width above 4 kHz)
4. Saturation (analog-style warmth)
5. Limiter (-1 dB true peak, target LUFS for platform)
```

---

## Parallel Processing Setups

### Parallel Compression (New York Style)

```
Dry Signal ─────────────────────────┐
                                    ├─→ [Mix Bus]
Aux Send → [Compressor 20:1] ──────┘
           (fast attack, fast release,
            heavy GR 10-20 dB)
```

Blend the crushed signal under the dry for energy without losing transients.

### Parallel Saturation

```
Dry Signal ──────────────────────────┐
                                     ├─→ [Mix Bus]
Aux Send → [HPF 200Hz] → [Drive] ───┘
```

Filter before saturation to keep low end clean; blend in distorted harmonics for presence.

---

## Common Chain Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| EQ boost before compression | Compressor overreacts to boosted frequencies | Cut first, boost after compression |
| Reverb on insert | Wet signal gets compressed/processed | Use sends for time-based effects |
| Too many plugins | Phase issues, latency, mud | Remove anything not making an audible improvement |
| Same compressor on everything | One-dimensional dynamics | Match compressor character to source |
| Saturation after limiting | Distorts peaks, undoes limiter's work | Saturate before limiting |
