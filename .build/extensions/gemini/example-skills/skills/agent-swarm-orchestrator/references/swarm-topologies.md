# Swarm Topologies

## Topology Comparison

| Topology | Coordination | Fault Tolerance | Scalability | Best For |
|----------|--------------|-----------------|-------------|----------|
| Hierarchical | Centralized | Low | High | Clear decomposition |
| Peer-to-Peer | Distributed | High | Medium | Collaboration |
| Blackboard | Shared state | Medium | Medium | Complex problems |
| Pipeline | Sequential | Low | High | Workflow stages |
| Star | Central hub | Low | High | Task distribution |

## Hierarchical Topology

```
                    ┌──────────────┐
                    │ Orchestrator │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐
    │Supervisor │    │Supervisor │    │Supervisor │
    │    A      │    │    B      │    │    C      │
    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
          │                │                │
    ┌─────┼─────┐    ┌─────┼─────┐    ┌─────┼─────┐
    │     │     │    │     │     │    │     │     │
   ┌┴┐   ┌┴┐   ┌┴┐  ┌┴┐   ┌┴┐   ┌┴┐  ┌┴┐   ┌┴┐   ┌┴┐
   │W│   │W│   │W│  │W│   │W│   │W│  │W│   │W│   │W│
   └─┘   └─┘   └─┘  └─┘   └─┘   └─┘  └─┘   └─┘   └─┘
```

### Implementation

```python
class HierarchicalSwarm:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.supervisors = []
        self.workers = defaultdict(list)

    def add_team(self, supervisor, workers):
        self.supervisors.append(supervisor)
        self.workers[supervisor.id] = workers

    async def execute(self, task):
        # Orchestrator decomposes task
        subtasks = await self.orchestrator.decompose(task)

        # Assign to supervisors
        assignments = self.orchestrator.assign_to_supervisors(
            subtasks, self.supervisors
        )

        # Each supervisor manages their workers
        results = []
        for supervisor_id, tasks in assignments.items():
            supervisor = self.get_supervisor(supervisor_id)
            team_results = await supervisor.execute_with_team(
                tasks, self.workers[supervisor_id]
            )
            results.extend(team_results)

        # Orchestrator aggregates
        return await self.orchestrator.aggregate(results)
```

## Peer-to-Peer Topology

```
        ┌───┐───────────────┌───┐
        │ A │               │ B │
        └───┘               └───┘
          │ \             / │
          │   \         /   │
          │     \     /     │
          │       \ /       │
        ┌───┐     ╳       ┌───┐
        │ C │   /   \     │ D │
        └───┘ /       \   └───┘
            /           \
        ┌───┐           ┌───┐
        │ E │───────────│ F │
        └───┘           └───┘
```

### Implementation

```python
class P2PSwarm:
    def __init__(self):
        self.agents = {}
        self.connections = defaultdict(set)

    def add_agent(self, agent):
        self.agents[agent.id] = agent

    def connect(self, agent_a_id, agent_b_id):
        self.connections[agent_a_id].add(agent_b_id)
        self.connections[agent_b_id].add(agent_a_id)

    async def gossip(self, sender_id, message):
        """Propagate message through network"""
        visited = {sender_id}
        queue = [sender_id]

        while queue:
            current = queue.pop(0)
            for neighbor_id in self.connections[current]:
                if neighbor_id not in visited:
                    await self.agents[neighbor_id].receive(message)
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)

    async def consensus(self, proposal):
        """Reach agreement across peers"""
        votes = {}
        for agent_id, agent in self.agents.items():
            votes[agent_id] = await agent.vote(proposal)

        approve_count = sum(1 for v in votes.values() if v)
        return approve_count > len(self.agents) / 2
```

## Blackboard Topology

```
┌─────────────────────────────────────────────────────┐
│                     Blackboard                       │
│  ┌─────────────┐ ┌─────────────┐ ┌───────────────┐ │
│  │ Problem     │ │ Partial     │ │ Solutions     │ │
│  │ State       │ │ Results     │ │               │ │
│  └─────────────┘ └─────────────┘ └───────────────┘ │
└───────────────────────┬─────────────────────────────┘
                        │
    ┌───────────────────┼───────────────────┐
    │         Read/Write│                   │
    ▼                   ▼                   ▼
┌───────┐          ┌───────┐          ┌───────┐
│Agent A│          │Agent B│          │Agent C│
│Expert │          │Expert │          │Expert │
└───────┘          └───────┘          └───────┘
```

### Implementation

```python
class Blackboard:
    def __init__(self):
        self.state = {}
        self.lock = asyncio.Lock()

    async def read(self, key):
        async with self.lock:
            return self.state.get(key)

    async def write(self, key, value):
        async with self.lock:
            self.state[key] = value

    async def append(self, key, value):
        async with self.lock:
            if key not in self.state:
                self.state[key] = []
            self.state[key].append(value)


class BlackboardSwarm:
    def __init__(self):
        self.blackboard = Blackboard()
        self.agents = []

    async def run(self, initial_problem):
        await self.blackboard.write('problem', initial_problem)
        await self.blackboard.write('status', 'active')

        while await self.blackboard.read('status') == 'active':
            for agent in self.agents:
                if agent.can_contribute(self.blackboard):
                    contribution = await agent.contribute(self.blackboard)
                    await self.blackboard.append('contributions', contribution)

            # Check if solution found
            if await self.is_solved():
                await self.blackboard.write('status', 'solved')

        return await self.blackboard.read('solution')
```

## Pipeline Topology

```
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│ Input  │───►│Stage 1 │───►│Stage 2 │───►│Stage 3 │───► Output
│        │    │        │    │        │    │        │
└────────┘    └────────┘    └────────┘    └────────┘
                  │              │              │
                  ▼              ▼              ▼
              Parallel       Parallel       Parallel
              Workers        Workers        Workers
```

### Implementation

```python
class PipelineSwarm:
    def __init__(self):
        self.stages = []
        self.stage_workers = defaultdict(list)

    def add_stage(self, stage_id, workers):
        self.stages.append(stage_id)
        self.stage_workers[stage_id] = workers

    async def process(self, input_data):
        current = input_data

        for stage_id in self.stages:
            workers = self.stage_workers[stage_id]

            # Distribute work across stage workers
            if isinstance(current, list):
                # Parallel processing
                chunks = self._chunk(current, len(workers))
                results = await asyncio.gather(*[
                    worker.process(chunk)
                    for worker, chunk in zip(workers, chunks)
                ])
                current = self._flatten(results)
            else:
                # Single item
                current = await workers[0].process(current)

        return current
```

## Star Topology

```
              ┌─────────┐
              │ Central │
              │   Hub   │
              └────┬────┘
                   │
    ┌──────────────┼──────────────┐
    │      │       │       │      │
    ▼      ▼       ▼       ▼      ▼
  ┌───┐  ┌───┐   ┌───┐   ┌───┐  ┌───┐
  │ A │  │ B │   │ C │   │ D │  │ E │
  └───┘  └───┘   └───┘   └───┘  └───┘
```

### Implementation

```python
class StarSwarm:
    def __init__(self, hub):
        self.hub = hub
        self.peripherals = []

    def add_peripheral(self, agent):
        self.peripherals.append(agent)

    async def broadcast(self, message):
        """Hub sends to all peripherals"""
        await asyncio.gather(*[
            p.receive(message) for p in self.peripherals
        ])

    async def collect(self):
        """Hub collects from all peripherals"""
        return await asyncio.gather(*[
            p.report() for p in self.peripherals
        ])

    async def route(self, from_id, to_id, message):
        """All communication goes through hub"""
        await self.hub.route(from_id, to_id, message)
```

## Choosing a Topology

### Decision Guide

```
Start
  │
  ├── Clear task hierarchy? ──► Hierarchical
  │         │
  │         No
  │         │
  ├── Need fault tolerance? ──► Peer-to-Peer
  │         │
  │         No
  │         │
  ├── Shared state needed? ──► Blackboard
  │         │
  │         No
  │         │
  ├── Sequential stages? ──► Pipeline
  │         │
  │         No
  │         │
  └── Simple coordination? ──► Star
```

### Hybrid Approaches

Combine topologies for complex requirements:

```python
class HybridSwarm:
    """Hierarchical teams with P2P coordination between teams"""

    def __init__(self):
        self.teams = {}  # Each team is hierarchical
        self.team_connections = defaultdict(set)  # P2P between teams

    def add_team(self, team_id, supervisor, workers):
        self.teams[team_id] = {
            'supervisor': supervisor,
            'workers': workers
        }

    def connect_teams(self, team_a, team_b):
        self.team_connections[team_a].add(team_b)
        self.team_connections[team_b].add(team_a)
```
