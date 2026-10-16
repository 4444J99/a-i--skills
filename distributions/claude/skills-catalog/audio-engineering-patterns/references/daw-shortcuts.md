# DAW Workflow Tips

Efficient workflows and techniques across major DAWs.

## Universal Workflow Principles

### Session Setup Checklist

Before recording or mixing, establish:

1. **Sample rate**: 44.1 kHz (music) or 48 kHz (video/broadcast)
2. **Bit depth**: 24-bit for recording, 32-bit float for mixing
3. **Buffer size**: 64-128 samples for recording (low latency), 512-1024 for mixing (CPU headroom)
4. **Template**: Load your standard bus structure, sends, and default plugins
5. **Naming**: Label every track before you start

### Session Organization

| Color Code | Track Type | Purpose |
|------------|------------|---------|
| Red/Orange | Drums | Percussion group |
| Yellow | Bass | Low-end elements |
| Green | Guitars/Keys | Harmonic instruments |
| Blue | Vocals | Lead and backing |
| Purple | Synths/Pads | Electronic elements |
| Grey | FX Returns | Reverb, delay sends |

### Folder/Bus Structure

```
Master
├── Drums (bus)
│   ├── Kick
│   ├── Snare
│   ├── Hats
│   └── Overheads
├── Bass (bus)
├── Music (bus)
│   ├── Guitar L
│   ├── Guitar R
│   └── Keys
├── Vocals (bus)
│   ├── Lead
│   └── BVox (bus)
├── FX (bus)
└── Sends
    ├── Reverb Short
    ├── Reverb Long
    └── Delay
```

---

## Keyboard Shortcuts (Cross-DAW)

### Essential Operations

| Action | Logic Pro | Ableton Live | Pro Tools | Reaper |
|--------|-----------|--------------|-----------|--------|
| Play/Stop | Space | Space | Space | Space |
| Record | R | F9 | F12 / Num 3 | R |
| Undo | Cmd+Z | Cmd+Z | Cmd+Z | Cmd+Z |
| Split/Cut | Cmd+T | Cmd+E | Cmd+E / B | S |
| Duplicate | Cmd+D | Cmd+D | Cmd+D | Cmd+D |
| Zoom In | Cmd+Right | Cmd++ | Cmd+] | + |
| Zoom Out | Cmd+Left | Cmd+- | Cmd+[ | - |
| Save | Cmd+S | Cmd+S | Cmd+S | Cmd+S |

### Navigation

| Action | Logic Pro | Ableton Live | Pro Tools | Reaper |
|--------|-----------|--------------|-----------|--------|
| Go to start | Return | Home | Return | Home |
| Loop toggle | C | Cmd+L | Shift+Cmd+L | R |
| Zoom to fit | Z | Cmd+Shift+F | Opt+A | Ctrl+Shift+Z |
| Scroll to cursor | Shift+F | Cmd+Shift+F | — | Ctrl+Shift+C |

### Editing

| Action | Logic Pro | Ableton Live | Pro Tools | Reaper |
|--------|-----------|--------------|-----------|--------|
| Select all | Cmd+A | Cmd+A | Cmd+A | Cmd+A |
| Crossfade | X | — | Cmd+F | X |
| Nudge left | , | — | , | — |
| Nudge right | . | — | . | — |
| Quantize | Q | Cmd+U | Cmd+0 | — |

---

## Workflow Techniques

### Gain Staging in the DAW

1. Set every fader to unity (0 dB) at session start
2. Use clip gain / input trim to hit -18 to -12 dBFS per track
3. Process with plugins at this level
4. Adjust faders only for mix balance
5. Check mix bus level last — aim for -6 dBFS peak before mastering

### Reference Track Workflow

1. Import a commercial reference track to a dedicated track
2. Route it directly to outputs (bypass mix bus processing)
3. Level-match to your mix using a LUFS meter
4. A/B frequently during mixing — compare tone, balance, width
5. Do not try to match loudness; match frequency balance and spatial depth

### Bounce/Export Checklist

| Setting | For Mixing | For Mastering | For Stems |
|---------|-----------|---------------|-----------|
| Format | WAV | WAV | WAV |
| Bit Depth | 32-bit float | 24-bit | 32-bit float |
| Sample Rate | Session rate | Session rate | Session rate |
| Dithering | No | Yes (if going to 16-bit) | No |
| Normalization | Off | Off | Off |
| Tail | Include 2-5s reverb tail | Include tail | Include tail |

---

## Mixing Speed Tips

### Quick Rough Mix

1. **Faders only** — balance everything in 5 minutes, no plugins
2. **Pan positions** — place everything in the stereo field
3. **One reverb send** — a single room reverb on everything
4. Listen to the rough mix for a day before touching plugins

### A/B Everything

- Bypass plugins frequently — is it actually better?
- Compare in mono — does it still work?
- Compare at low volume — does the balance hold?
- Compare on headphones and speakers

### Commit and Move On

- Print effects to audio when a sound is locked in
- Freeze tracks to save CPU
- Set a time limit per track (15-20 minutes max)
- If you cannot decide between two options in 30 seconds, it does not matter — pick one

---

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Crackling/pops | Buffer too low | Increase buffer size |
| Latency when recording | Buffer too high | Lower buffer, use direct monitoring |
| Plugin not loading | Compatibility issue | Check plugin format (AU/VST/AAX), rescan |
| Phase issues | Mic bleed or duplicate tracks | Check polarity, zoom in on waveforms |
| Mix sounds different exported | Dithering, normalization, or sample rate conversion | Match export settings to session; disable normalization |
| CPU overload | Too many plugins | Freeze tracks, use offline bounce, increase buffer |
| Mud in the low end | Stacking bass frequencies | High-pass everything that does not need lows |

---

## Template Strategy

Build session templates for your common workflows:

### Recording Template
- Pre-labeled tracks with input assignments
- Headphone mix sends configured
- Click track with count-in enabled
- Low buffer size preset

### Mixing Template
- Bus structure with color coding
- Default sends (short reverb, long reverb, delay)
- Reference track routed to output
- Metering on mix bus (LUFS, spectrum, phase)

### Mastering Template
- Linear phase EQ, multiband comp, limiter pre-loaded
- Metering chain (LUFS, true peak, spectrum, stereo correlation)
- Reference track import slot
- Dithering on output (POW-r or MBIT+)

Save templates in your DAW's default template location. Revisit and update them every few months as your workflow evolves.
