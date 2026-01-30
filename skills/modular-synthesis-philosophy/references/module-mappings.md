# Extended Module-to-System Mappings

## Sound Sources → Data Origins

### Oscillators

| Module Type | Waveform Character | System Equivalent | Use Case |
|-------------|-------------------|-------------------|----------|
| Analog VCO | Warm, drifting | Legacy system, human input | Organic variability desired |
| Digital VCO | Precise, stable | Database, structured API | Reliability required |
| Wavetable | Morphing, complex | ML model output | Evolving/contextual data |
| FM Oscillator | Harmonically rich | Derived/calculated data | Complex relationships |
| Additive | Built from partials | Aggregated sources | Composite signals |

### Noise & Random

| Module Type | Character | System Equivalent | Use Case |
|-------------|-----------|-------------------|----------|
| White noise | All frequencies equal | Pure random, entropy | Cryptographic seeds |
| Pink noise | 1/f distribution | Natural variation | Realistic simulation |
| Sample & Hold | Stepped random | Periodic sampling | Polling, snapshots |
| Turing Machine | Looping probability | Markov chains | Generative with memory |

---

## Processing → Transformation

### Filters

| Filter Type | Frequency Response | System Equivalent | Use Case |
|-------------|-------------------|-------------------|----------|
| Lowpass (LP) | Passes lows, cuts highs | Smoothing, averaging | Reduce noise/variance |
| Highpass (HP) | Passes highs, cuts lows | Change detection | Find deltas only |
| Bandpass (BP) | Passes middle range | Selective extraction | Specific queries |
| Notch | Cuts specific frequency | Exclusion filter | Remove specific patterns |
| Comb | Periodic peaks/valleys | Periodic pattern match | Rhythm/cycle detection |
| Allpass | Phase shift only | Delay, ordering | Timing adjustment |

### Waveshapers & Distortion

| Module Type | Effect | System Equivalent | Use Case |
|-------------|--------|-------------------|----------|
| Soft clip | Gentle saturation | Soft limits, graceful degradation | Overflow handling |
| Hard clip | Harsh limiting | Hard validation, truncation | Strict boundaries |
| Foldback | Wraps excess | Modulo operations | Cyclic data |
| Bitcrusher | Resolution reduction | Quantization, compression | Lossy optimization |
| Rectifier | Absolute value | Magnitude extraction | Direction-agnostic measure |

---

## Modulation → Control & Automation

### Envelopes (ADSR)

| Stage | Synthesis Function | System Equivalent |
|-------|-------------------|-------------------|
| Attack | Rise to peak | Initialization, ramp-up, warm cache |
| Decay | Fall to sustain | Stabilization, find steady state |
| Sustain | Held level | Active operation, steady state |
| Release | Return to zero | Cleanup, graceful shutdown, GC |

**Extended envelope types:**
- **AR (Attack-Release)**: Simple on/off → Request/response cycles
- **AD (Attack-Decay)**: Trigger and fade → One-shot processes
- **AHDSR**: Added Hold stage → Processing time before decay

### Sequencers

| Sequencer Type | Behavior | System Equivalent |
|----------------|----------|-------------------|
| Step sequencer | Fixed pattern, repeating | Cron jobs, batch schedules |
| Euclidean | Mathematically distributed | Load balancing, distributed triggers |
| Probabilistic | Chance-based triggers | A/B testing, canary deployments |
| Generative | Rule-based evolution | ML-driven scheduling |

### Clocks & Timing

| Module Type | Function | System Equivalent |
|-------------|----------|-------------------|
| Master clock | Central timing source | System clock, coordinator |
| Clock divider | Subdivide time | Batch windowing, sampling rate |
| Clock multiplier | Increase rate | Upsampling, interpolation |
| Swing/Shuffle | Humanize timing | Jitter, anti-pattern detection |
| Reset | Return to beginning | State reset, epoch boundary |

---

## Utilities → Infrastructure

### Mixing & Routing

| Module Type | Function | System Equivalent |
|-------------|----------|-------------------|
| Mixer | Combine signals | Data aggregation, merge |
| Crossfader | Blend between sources | A/B transition, blue-green deploy |
| Matrix mixer | Any-to-any routing | Service mesh, full connectivity |
| Sequential switch | Rotate through inputs | Round-robin, load balancer |
| Mute/Solo | Selective silence | Feature flags, kill switches |

### Signal Conditioning

| Module Type | Function | System Equivalent |
|-------------|----------|-------------------|
| VCA | Control amplitude | Throttle, gain control |
| Attenuator | Reduce level | Scale down, rate limit |
| Offset | Add constant | Bias, baseline shift |
| Slew limiter | Smooth changes | Rate limiting, gradual rollout |
| Precision adder | Exact combination | Lossless merge, sum |
| Comparator | Threshold detection | Conditional triggers |

### Utilities

| Module Type | Function | System Equivalent |
|-------------|----------|-------------------|
| Multiple | Copy signal | Fan-out, broadcast |
| Unity mixer | Sum without gain | Lossless aggregation |
| Half-wave rectifier | Positive only | Filter negative values |
| Logic (AND/OR/XOR) | Boolean on gates | Conditional logic |
| Min/Max | Select extreme | Best/worst case selection |

---

## Effects → Enhancement

### Time-Based

| Effect Type | Function | System Equivalent |
|-------------|----------|-------------------|
| Delay | Time offset copy | Message queue, buffer |
| Reverb | Many delays + feedback | Distributed echo, eventual consistency |
| Chorus | Modulated delays | Redundancy with variation |
| Phaser | Phase-shifted copies | Interference patterns |
| Granular | Micro-segment manipulation | Micro-batching, windowing |

### Dynamics

| Effect Type | Function | System Equivalent |
|-------------|----------|-------------------|
| Compressor | Reduce dynamic range | Normalize, auto-scale |
| Limiter | Hard ceiling | Rate limit, quota enforcement |
| Expander | Increase dynamic range | Amplify differences |
| Gate | Silence below threshold | Noise floor, minimum threshold |
| Ducker | Attenuate when triggered | Priority preemption |

---

## Patch Philosophy Mappings

### "Happy Accidents" → Emergence

When unexpected patches create interesting results:
- Document the unexpected behavior
- Analyze why it works
- Determine if it's reproducible
- Consider if it reveals a new pattern

### "Less is More" → Simplicity

A complex patch isn't always better:
- Each module adds latency/complexity
- Find the minimum viable signal path
- Remove modules that don't add value

### "Normalled Connections" → Defaults

Many modules have internal routings that work without patching:
- Design systems with sensible defaults
- Allow but don't require configuration
- "It just works" out of the box

### "Breaking Normalls" → Override

Patching overrides the default:
- Explicit configuration beats convention
- User intent overrides system defaults
- But defaults should be good enough for most cases
