---
name: realtime-websocket-patterns
description: Implement real-time features with WebSockets, Server-Sent Events, and long polling. Covers connection management, room-based messaging, presence tracking, and scaling strategies. Triggers on WebSocket implementation, real-time communication, or live update feature requests.
license: MIT
complexity: advanced
time_to_learn: 30min
tags:
  - websocket
  - real-time
  - sse
  - live-updates
  - pub-sub
governance_phases: [build]
organ_affinity: [organ-ii, organ-iii]
triggers: [user-asks-about-websockets, context:real-time, context:live-updates, context:websocket, context:sse]
complements: [redis-patterns, backend-implementation-patterns, community-platform-patterns]
---

# Real-time WebSocket Patterns

Build reliable real-time features with WebSockets, SSE, and proper connection management.

## Protocol Selection

| Technology | Direction | Use Case | Complexity |
|-----------|-----------|----------|------------|
| **WebSocket** | Bidirectional | Chat, collaboration, gaming | High |
| **SSE** | Server → Client | Notifications, dashboards, feeds | Low |
| **Long Polling** | Request/Response | Fallback, simple updates | Low |
| **WebTransport** | Bidirectional | Low-latency, unreliable OK | Very High |

### Decision Matrix

```
Need bidirectional? ──yes──→ WebSocket
        │no
        ▼
Need low latency? ──yes──→ SSE
        │no
        ▼
Simple updates? ──yes──→ Long Polling
```

## WebSocket Server (FastAPI)

### Basic Setup

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dataclasses import dataclass, field

app = FastAPI()

@dataclass
class ConnectionManager:
    connections: dict[str, set[WebSocket]] = field(default_factory=dict)

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        self.connections.setdefault(room, set()).add(websocket)

    async def disconnect(self, websocket: WebSocket, room: str):
        self.connections.get(room, set()).discard(websocket)

    async def broadcast(self, room: str, message: dict):
        for ws in list(self.connections.get(room, set())):
            try:
                await ws.send_json(message)
            except Exception:
                self.connections[room].discard(ws)

manager = ConnectionManager()

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(room, {
                "type": "message",
                "room": room,
                "data": data,
            })
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room)
        await manager.broadcast(room, {
            "type": "user_left",
            "room": room,
        })
```

### Authentication

```python
from fastapi import Query, status

@app.websocket("/ws/{room}")
async def websocket_endpoint(
    websocket: WebSocket,
    room: str,
    token: str = Query(...),  # allow-secret
):
    user = await verify_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, room, user_id=user.id)
    # ...
```

## Message Protocol

### Structured Message Format

```python
from enum import Enum
from pydantic import BaseModel

class MessageType(str, Enum):
    TEXT = "text"
    PRESENCE = "presence"
    TYPING = "typing"
    SYSTEM = "system"
    ERROR = "error"
    ACK = "ack"

class WsMessage(BaseModel):
    type: MessageType
    id: str | None = None  # For acknowledgment
    room: str | None = None
    data: dict = {}
    timestamp: float

# Client sends
{"type": "text", "id": "msg_123", "room": "general", "data": {"content": "Hello"}}

# Server acknowledges
{"type": "ack", "id": "msg_123", "data": {"status": "delivered"}}

# Server broadcasts
{"type": "text", "room": "general", "data": {"content": "Hello", "author": "user_42"}, "timestamp": 1711000000}
```

## Presence Tracking

```python
import asyncio
from collections import defaultdict

class PresenceTracker:
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.presence: dict[str, dict[str, float]] = defaultdict(dict)  # room → {user_id: last_seen}

    async def heartbeat(self, room: str, user_id: str):
        self.presence[room][user_id] = asyncio.get_event_loop().time()

    async def get_online(self, room: str) -> list[str]:
        now = asyncio.get_event_loop().time()
        return [
            uid for uid, last_seen in self.presence.get(room, {}).items()
            if now - last_seen < self.timeout
        ]

    async def cleanup_loop(self):
        while True:
            now = asyncio.get_event_loop().time()
            for room in list(self.presence.keys()):
                expired = [
                    uid for uid, ts in self.presence[room].items()
                    if now - ts > self.timeout
                ]
                for uid in expired:
                    del self.presence[room][uid]
            await asyncio.sleep(self.timeout / 2)
```

## Server-Sent Events (SSE)

```python
from sse_starlette.sse import EventSourceResponse

@app.get("/events/{room}")
async def event_stream(room: str):
    async def generate():
        queue = asyncio.Queue()
        event_bus.subscribe(room, queue)
        try:
            while True:
                event = await queue.get()
                yield {
                    "event": event["type"],
                    "data": json.dumps(event["data"]),
                    "id": event.get("id"),
                }
        finally:
            event_bus.unsubscribe(room, queue)

    return EventSourceResponse(generate())
```

### Client-Side SSE

```javascript
const events = new EventSource('/events/general');

events.addEventListener('message', (e) => {
    const data = JSON.parse(e.data);
    handleMessage(data);
});

events.addEventListener('presence', (e) => {
    const data = JSON.parse(e.data);
    updateOnlineUsers(data);
});

events.onerror = () => {
    // Auto-reconnects with Last-Event-ID header
    console.log('Connection lost, reconnecting...');
};
```

## Scaling with Redis Pub/Sub

```python
import redis.asyncio as redis

class RedisPubSubBridge:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.local_manager = ConnectionManager()

    async def publish(self, room: str, message: dict):
        await self.redis.publish(f"ws:{room}", json.dumps(message))

    async def subscribe_loop(self, room: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(f"ws:{room}")
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await self.local_manager.broadcast(room, data)
```

## Reconnection & Reliability

### Client-Side Reconnection

```javascript
class ReconnectingWebSocket {
    constructor(url, options = {}) {
        this.url = url;
        this.maxRetries = options.maxRetries || 10;
        this.baseDelay = options.baseDelay || 1000;
        this.retries = 0;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);
        this.ws.onopen = () => { this.retries = 0; };
        this.ws.onclose = () => { this.reconnect(); };
        this.ws.onmessage = (e) => { this.onmessage?.(e); };
    }

    reconnect() {
        if (this.retries >= this.maxRetries) return;
        const delay = Math.min(this.baseDelay * Math.pow(2, this.retries), 30000);
        setTimeout(() => { this.retries++; this.connect(); }, delay);
    }
}
```

### Message Ordering

```python
class OrderedMessageBuffer:
    def __init__(self):
        self.last_seq = 0
        self.buffer: dict[int, dict] = {}

    def process(self, message: dict) -> list[dict]:
        seq = message.get("seq", 0)
        self.buffer[seq] = message
        ordered = []
        while self.last_seq + 1 in self.buffer:
            self.last_seq += 1
            ordered.append(self.buffer.pop(self.last_seq))
        return ordered
```

## Anti-Patterns

- **No heartbeat/ping** — Stale connections consume resources; ping every 30s
- **Unbounded connections** — Set per-room and per-user limits
- **No authentication** — Authenticate on connection, not per-message
- **Synchronous broadcast** — Failed sends to one client block all others
- **No reconnection strategy** — Clients will disconnect; handle it gracefully
- **WebSocket for everything** — Use SSE when only server-to-client is needed
