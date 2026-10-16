# Example System Diagrams in Synthesis Style

Real-world system architectures drawn using modular synthesis conventions.

## Diagram Conventions

```
┌─────────────┐
│   MODULE     │
│              │
│ ○ Input      │  ○ = Input (open circle)
│ ● Output     │  ● = Output (filled circle)
└─────────────┘

Audio/Data path:  ────────  (solid line)
CV/Control path:  ········  (dotted line)
Gate/Trigger:     ─ ─ ─ ─  (dashed line)
```

---

## Web Application Request Flow

A typical HTTP request modeled as a signal chain.

```
┌───────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐
│  CLIENT    │    │   GATEWAY    │    │   SERVICE    │    │ DATABASE │
│ (Osc)     │    │  (Filter)    │    │  (VCA)       │    │ (Delay)  │
│           │    │              │    │              │    │          │
│ ● Request─┼────┼→○ In        │    │              │    │          │
│           │    │  Rate Limit ·┼····┼·○ CV Gain    │    │          │
│           │    │ ● Out───────┼────┼→○ Signal In  │    │          │
│           │    │              │    │ ● Out───────┼────┼→○ Write  │
│ ○ Response┼────┼─● Response  │    │              │    │ ● Read──┼─┐
│           │    │              │    │ ○ Data In───┼────┼──────────┼─┘
└───────────┘    └──────────────┘    └──────────────┘    └──────────┘
                        ·
                        ·
                 ┌──────────────┐
                 │   CONFIG     │
                 │ (Sequencer)  │
                 │              │
                 │ ● Auth Rules·┘
                 │ ● Rate Cfg ·
                 └──────────────┘
```

**Module mapping**:
- **Client** = Oscillator (generates signal)
- **Gateway** = Filter (passes valid requests, blocks others)
- **Config** = Sequencer (controls behavior patterns over time)
- **Service** = VCA (processes signal, amplitude controlled by auth/config)
- **Database** = Delay (stores and retrieves signal over time)

---

## CI/CD Pipeline

Continuous integration as a series of processing stages with gates.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   GIT    │    │  BUILD   │    │   TEST   │    │  STAGE   │    │  DEPLOY  │
│ (Trigger)│    │(Waveshape)│   │  (Gate)  │    │ (Reverb) │    │ (Output) │
│          │    │          │    │          │    │          │    │          │
│ ● Push ──┼────┼→○ Source │    │          │    │          │    │          │
│          │    │ ● Artifact┼───┼→○ Input  │    │          │    │          │
│          │    │          │    │ Threshold·┼····│·○ Enable │    │          │
│          │    │          │    │ ● Pass───┼────┼→○ Image  │    │          │
│          │    │          │    │          │    │ ● Env────┼────┼→○ Target │
│          │    │          │    │          │    │          │    │ ● Live   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                      ·                               │
                                      ·                               │
                                ┌──────────┐                   ┌──────────┐
                                │ COVERAGE │                   │ MONITOR  │
                                │  (Comp)  │                   │ (Meter)  │
                                │          │                   │          │
                                │ ● Thresh·┘                   │ ○ Signal─┘
                                └──────────┘                   │ ● Alert──→ [Slack]
                                                               └──────────┘
```

**Signal flow**: Code push triggers the chain. The test gate only opens (passes signal) when coverage meets threshold. Staging acts as reverb -- the same deployment echoed in a safe environment before reaching the output stage. Monitoring meters the live output and triggers alerts.

---

## Event-Driven Microservices

Multiple oscillators feeding a shared bus with independent processing.

```
┌──────────┐    ┌──────────────────────────────────────────┐
│  USER    │    │              EVENT BUS (Mixer)            │
│ (VCO 1)  │    │                                          │
│ ● Events─┼────┼→○ Ch 1                                   │
└──────────┘    │                            ● Out─┬──────┐│
                │                                  │      ││
┌──────────┐    │                                  │      ││
│  PAYMENT │    │                                  │      ││
│ (VCO 2)  │    │                                  │      ││
│ ● Events─┼────┼→○ Ch 2                           │      ││
└──────────┘    │                                  │      ││
                │                                  │      ││
┌──────────┐    │                                  │      ││
│ INVENTORY│    │                                  │      ││
│ (VCO 3)  │    │                                  │      ││
│ ● Events─┼────┼→○ Ch 3                           │      ││
└──────────┘    └──────────────────────────────────┼──────┼┘
                                                   │      │
                  ┌────────────────────────────────┘      │
                  │                                       │
                  ▼                                       ▼
           ┌──────────┐                            ┌──────────┐
           │ ANALYTICS│                            │  NOTIFY  │
           │(Bandpass) │                            │ (Envelope)│
           │          │                            │          │
           │ ○ In     │                            │ ○ In     │
           │ Filter:  │                            │ A: Batch │
           │  purchase│                            │ D: Format│
           │  events  │                            │ S: Queue │
           │ ● Report │                            │ R: Send  │
           └──────────┘                            └──────────┘
```

**Module mapping**:
- **Services** = VCOs, each generating their own event streams
- **Event Bus** = Mixer, combining all signals into a shared channel
- **Analytics** = Bandpass filter, extracting only purchase events from the full stream
- **Notification** = Envelope generator (Attack: batch incoming, Decay: format messages, Sustain: queue for delivery, Release: send and clean up)

---

## Machine Learning Pipeline

Data processing as a modular rack.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ RAW DATA │    │  CLEAN   │    │ FEATURES │    │  MODEL   │
│ (Noise)  │    │  (HPF)   │    │(Waveshape)│   │  (VCF)   │
│          │    │          │    │          │    │          │
│ ● Out────┼────┼→○ In     │    │          │    │          │
│          │    │ Remove:  │    │          │    │          │
│          │    │  nulls   │    │          │    │ Learning ·┼···┐
│          │    │  outliers│    │          │    │  Rate    │   ·
│          │    │ ● Clean──┼────┼→○ In     │    │          │   ·
│          │    │          │    │ ● Vectors┼────┼→○ In     │   ·
│          │    │          │    │          │    │ ● Predict│   ·
└──────────┘    └──────────┘    └──────────┘    └──────────┘   ·
                                                      │        ·
                                                      │        ·
                                                      ▼        ·
                                                ┌──────────┐   ·
                                                │ EVALUATE │   ·
                                                │(Comparator)  ·
                                                │          │   ·
                                                │ ○ Predict│   ·
                                                │ ○ Actual │   ·
                                                │          │   ·
                                                │ ● Error··┼···┘
                                                │  (CV feedback)
                                                └──────────┘
```

**Key insight**: The feedback loop from Evaluate back to Model (via CV/control path) is the training loop. Error signal modulates the model's parameters, exactly like an envelope follower controlling a filter's cutoff. Too much feedback (high learning rate) = oscillation. Too little = the system barely responds.

---

## Reading These Diagrams

### Signal Type Guide

| Line Style | Meaning | System Equivalent |
|------------|---------|-------------------|
| `────────` Solid | Audio / primary data | HTTP requests, database queries, event payloads |
| `········` Dotted | CV / control signal | Config values, feature flags, thresholds |
| `─ ─ ─ ─` Dashed | Gate / trigger | Webhooks, cron triggers, CI pipeline triggers |

### Module Type Quick Reference

| Synthesis Module | System Role | Look For |
|-----------------|-------------|----------|
| Oscillator (VCO) | Signal source | Generates data or events |
| Filter (VCF) | Selective processor | Passes some data, blocks rest |
| Amplifier (VCA) | Controlled throughput | Scales or gates data flow |
| Envelope (ADSR) | Lifecycle manager | Init, process, sustain, cleanup |
| Sequencer | Orchestrator | Steps through states in order |
| Mixer | Aggregator | Combines multiple inputs |
| Delay | Storage/buffer | Holds data for later retrieval |
| Gate | Binary pass/block | Tests pass, health checks, auth |
| Comparator | Threshold detector | Monitoring, alerting, validation |

### Design Process

1. Identify signal sources (what generates data?)
2. Trace the signal path (where does data flow?)
3. Mark control connections (what influences behavior?)
4. Identify feedback loops (where does output affect input?)
5. Look for missing attenuation (where could the system overload?)
