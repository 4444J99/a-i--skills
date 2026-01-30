# Live Systems Technical Implementation

## Show Control Systems

### QLab (Industry Standard)

```
QLab Cue Structure:
├── Cue 1: House lights down
├── Cue 2: Sound: Ambient start
├── Cue 3: Video: Projection A
├── Cue 4: Group cue
│   ├── Sound: Music
│   ├── Light: State B
│   └── Video: Loop
└── Cue 5: MIDI: Trigger external
```

### OSC (Open Sound Control)

```python
from pythonosc import udp_client, dispatcher, osc_server

# Send OSC message
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
client.send_message("/cue/1/go", [])

# Receive OSC messages
def handle_cue(address, *args):
    cue_number = args[0]
    execute_cue(cue_number)

disp = dispatcher.Dispatcher()
disp.map("/cue/*/go", handle_cue)

server = osc_server.ThreadingOSCUDPServer(
    ("0.0.0.0", 9001), disp
)
server.serve_forever()
```

## Audience Tracking

### RFID/NFC System

```python
class AudienceTracker:
    """Track audience via RFID wristbands"""

    def __init__(self):
        self.readers = {}  # zone_id -> reader
        self.audience = {}  # wristband_id -> AudienceMember

    def register_reader(self, zone_id, reader):
        self.readers[zone_id] = reader
        reader.on_scan = lambda tag: self.on_scan(zone_id, tag)

    def on_scan(self, zone_id, tag_id):
        if tag_id in self.audience:
            member = self.audience[tag_id]
            old_zone = member.current_zone
            member.current_zone = zone_id
            member.zone_history.append((zone_id, time.time()))

            # Trigger zone-based events
            self.on_zone_change(member, old_zone, zone_id)

    def get_zone_population(self, zone_id):
        return [m for m in self.audience.values()
                if m.current_zone == zone_id]
```

### Bluetooth Beacon Tracking

```python
class BeaconTracker:
    """Track via BLE beacons"""

    def __init__(self):
        self.beacons = {}  # uuid -> location
        self.devices = {}  # mac -> last_seen_beacon

    def process_detection(self, device_mac, beacon_uuid, rssi):
        """Process beacon detection from device"""
        if rssi > -70:  # Close enough to count
            self.devices[device_mac] = {
                'beacon': beacon_uuid,
                'rssi': rssi,
                'time': time.time()
            }

    def get_device_location(self, device_mac):
        if device_mac in self.devices:
            beacon = self.devices[device_mac]['beacon']
            return self.beacons.get(beacon)
        return None
```

## Performer Communication

### IEM (In-Ear Monitor) System

```
Stage Manager → Audio Mixer → Wireless transmitters → Performer IEMs

Message Types:
- Go cues: "Scene 5, go"
- Standby: "Standing by for blackout"
- Emergency: "Hold position"
- Improvise: "Audience in zone 3, redirect"
```

### Wearable Haptic Cues

```python
class HapticCueSystem:
    """Send vibration patterns to performers"""

    PATTERNS = {
        'go': [100, 0],                    # Single buzz
        'standby': [50, 50, 50, 50],       # Quick double
        'hold': [200, 100, 200],           # Long-short-long
        'redirect': [50, 50, 50, 50, 50, 50],  # Triple
        'emergency': [500]                  # Long continuous
    }

    def send_cue(self, performer_id, cue_type):
        pattern = self.PATTERNS.get(cue_type, [100])
        self.transmit(performer_id, pattern)
```

### Visual Cue System

```python
class VisualCueSystem:
    """Hidden visual cues for performers"""

    def __init__(self):
        self.cue_lights = {}  # location -> LED controller

    def set_cue(self, location, color, pattern='solid'):
        """
        Colors:
        - Red: Hold/stop
        - Green: Go
        - Blue: Standby
        - Amber: Warning
        - White: Neutral

        Patterns:
        - solid: Constant
        - pulse: Slow fade
        - flash: Quick blink
        """
        self.cue_lights[location].set(color, pattern)
```

## Real-Time Decision Engine

```python
class ShowDecisionEngine:
    """Make real-time decisions based on audience state"""

    def __init__(self, show_state, rules):
        self.state = show_state
        self.rules = rules

    def evaluate(self):
        """Check rules and trigger actions"""
        for rule in self.rules:
            if rule.condition(self.state):
                return rule.action

        return None

    def update_state(self, event):
        """Process incoming events"""
        self.state.update(event)
        action = self.evaluate()
        if action:
            self.execute(action)


# Example rules
rules = [
    Rule(
        condition=lambda s: s.zone_population('main') < 5,
        action=Action('trigger_event', 'draw_to_main')
    ),
    Rule(
        condition=lambda s: s.time_in_scene > 600,  # 10 minutes
        action=Action('advance_scene')
    ),
    Rule(
        condition=lambda s: s.engagement_score < 0.3,
        action=Action('performer_interaction', 'increase')
    )
]
```

## Voting/Input Systems

### Mobile App Integration

```python
from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

votes = {}

@socketio.on('vote')
def handle_vote(data):
    session_id = request.sid
    choice = data['choice']
    votes[session_id] = choice

    # Broadcast vote count
    counts = count_votes()
    emit('vote_update', counts, broadcast=True)

@socketio.on('get_results')
def get_results():
    emit('results', count_votes())

def count_votes():
    from collections import Counter
    return dict(Counter(votes.values()))
```

### Physical Button System

```python
import RPi.GPIO as GPIO

class ButtonVotingSystem:
    """Physical buttons for voting"""

    def __init__(self, pins):
        self.pins = pins  # {option: pin_number}
        self.votes = {opt: 0 for opt in pins}

        GPIO.setmode(GPIO.BCM)
        for opt, pin in pins.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING,
                                 callback=lambda ch, o=opt: self.record_vote(o),
                                 bouncetime=300)

    def record_vote(self, option):
        self.votes[option] += 1
        self.on_vote_change(self.votes)

    def reset(self):
        self.votes = {opt: 0 for opt in self.pins}
```

## Safety Systems

```python
class EmergencyProtocol:
    """Emergency stop and safety systems"""

    def __init__(self, show_controller):
        self.controller = show_controller
        self.emergency_active = False

    def trigger_emergency(self, reason):
        self.emergency_active = True

        # Stop all cues
        self.controller.stop_all()

        # House lights up
        self.controller.house_lights(100)

        # Notify all staff
        self.notify_staff(f"EMERGENCY: {reason}")

        # Guide audience
        self.play_evacuation_announcement()

    def notify_staff(self, message):
        # Page all radios
        # Send to all wearables
        # Flash all cue lights red
        pass
```
