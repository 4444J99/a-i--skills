# Emergent Behavior Patterns

## Stigmergy

Indirect coordination through environment modification.

### Digital Pheromone System

```python
import time

class PheromoneMap:
    """Digital pheromone trails for indirect coordination"""

    def __init__(self, decay_rate=0.1, evaporation_interval=1.0):
        self.trails = {}  # location -> {type: strength}
        self.decay_rate = decay_rate
        self.evaporation_interval = evaporation_interval
        self.last_evaporation = time.time()

    def deposit(self, location, pheromone_type, strength=1.0):
        """Agent deposits pheromone at location"""
        if location not in self.trails:
            self.trails[location] = {}
        current = self.trails[location].get(pheromone_type, 0)
        self.trails[location][pheromone_type] = min(1.0, current + strength)

    def sense(self, location, pheromone_type=None):
        """Sense pheromone strength at location"""
        self._maybe_evaporate()
        if location not in self.trails:
            return {} if pheromone_type is None else 0

        if pheromone_type:
            return self.trails[location].get(pheromone_type, 0)
        return dict(self.trails[location])

    def sense_gradient(self, location, pheromone_type, neighbors_fn):
        """Find direction of strongest pheromone"""
        neighbors = neighbors_fn(location)
        strengths = {n: self.sense(n, pheromone_type) for n in neighbors}
        if not strengths:
            return None
        return max(strengths, key=strengths.get)

    def _maybe_evaporate(self):
        now = time.time()
        if now - self.last_evaporation >= self.evaporation_interval:
            self._evaporate()
            self.last_evaporation = now

    def _evaporate(self):
        """Reduce all pheromone strengths"""
        for location in list(self.trails.keys()):
            for p_type in list(self.trails[location].keys()):
                self.trails[location][p_type] *= (1 - self.decay_rate)
                if self.trails[location][p_type] < 0.01:
                    del self.trails[location][p_type]
            if not self.trails[location]:
                del self.trails[location]
```

### Stigmergic Agent

```python
class StigmergicAgent:
    """Agent that coordinates via pheromones"""

    def __init__(self, agent_id, pheromone_map):
        self.id = agent_id
        self.pheromones = pheromone_map
        self.location = None

    async def forage(self, target_type):
        """Follow pheromone trail to target"""
        while True:
            # Sense environment
            gradient = self.pheromones.sense_gradient(
                self.location,
                target_type,
                self.get_neighbors
            )

            if gradient:
                # Move toward strongest signal
                await self.move_to(gradient)
            else:
                # Random exploration
                await self.random_move()

            # Check if found target
            if await self.at_target(target_type):
                return self.location

    async def return_with_trail(self, start, end, trail_type):
        """Return while leaving pheromone trail"""
        path = self.find_path(end, start)
        for location in path:
            await self.move_to(location)
            self.pheromones.deposit(location, trail_type)
```

## Swarm Intelligence

### Ant Colony Optimization

```python
class AntColonyOptimizer:
    """Solve optimization problems with virtual ants"""

    def __init__(self, graph, num_ants=10, alpha=1.0, beta=2.0, rho=0.1):
        self.graph = graph
        self.num_ants = num_ants
        self.alpha = alpha  # Pheromone importance
        self.beta = beta    # Heuristic importance
        self.rho = rho      # Evaporation rate
        self.pheromones = {e: 1.0 for e in graph.edges}

    def solve(self, start, end, iterations=100):
        best_path = None
        best_cost = float('inf')

        for _ in range(iterations):
            paths = self._construct_solutions(start, end)
            self._update_pheromones(paths)

            for path, cost in paths:
                if cost < best_cost:
                    best_path = path
                    best_cost = cost

        return best_path, best_cost

    def _construct_solutions(self, start, end):
        """Each ant constructs a solution"""
        solutions = []
        for _ in range(self.num_ants):
            path = self._ant_walk(start, end)
            cost = self._path_cost(path)
            solutions.append((path, cost))
        return solutions

    def _ant_walk(self, start, end):
        """Single ant builds path"""
        path = [start]
        current = start
        visited = {start}

        while current != end:
            neighbors = self.graph.neighbors(current)
            unvisited = [n for n in neighbors if n not in visited]

            if not unvisited:
                break  # Dead end

            # Probabilistic selection
            probs = self._transition_probs(current, unvisited)
            next_node = self._weighted_choice(unvisited, probs)

            path.append(next_node)
            visited.add(next_node)
            current = next_node

        return path

    def _transition_probs(self, current, candidates):
        """Calculate transition probabilities"""
        probs = []
        for candidate in candidates:
            edge = (current, candidate)
            pheromone = self.pheromones.get(edge, 0.1) ** self.alpha
            heuristic = (1 / self.graph.edge_cost(edge)) ** self.beta
            probs.append(pheromone * heuristic)

        total = sum(probs)
        return [p / total for p in probs]

    def _update_pheromones(self, solutions):
        """Evaporate and deposit pheromones"""
        # Evaporation
        for edge in self.pheromones:
            self.pheromones[edge] *= (1 - self.rho)

        # Deposit based on solution quality
        for path, cost in solutions:
            deposit = 1 / cost
            for i in range(len(path) - 1):
                edge = (path[i], path[i+1])
                self.pheromones[edge] = self.pheromones.get(edge, 0) + deposit
```

### Particle Swarm Optimization

```python
import numpy as np

class ParticleSwarmOptimizer:
    """Optimize via particle swarm"""

    def __init__(self, objective_fn, dimensions, bounds, num_particles=30):
        self.objective = objective_fn
        self.dims = dimensions
        self.bounds = bounds
        self.num_particles = num_particles

        # Initialize particles
        self.positions = np.random.uniform(
            bounds[0], bounds[1], (num_particles, dimensions)
        )
        self.velocities = np.random.uniform(
            -1, 1, (num_particles, dimensions)
        )
        self.personal_best_positions = self.positions.copy()
        self.personal_best_scores = np.array([
            self.objective(p) for p in self.positions
        ])
        self.global_best_idx = self.personal_best_scores.argmin()
        self.global_best_position = self.positions[self.global_best_idx].copy()

    def optimize(self, iterations=100, w=0.7, c1=1.5, c2=1.5):
        """
        w: inertia weight
        c1: cognitive weight (personal best)
        c2: social weight (global best)
        """
        for _ in range(iterations):
            for i in range(self.num_particles):
                # Update velocity
                r1, r2 = np.random.random(2)
                cognitive = c1 * r1 * (self.personal_best_positions[i] - self.positions[i])
                social = c2 * r2 * (self.global_best_position - self.positions[i])
                self.velocities[i] = w * self.velocities[i] + cognitive + social

                # Update position
                self.positions[i] += self.velocities[i]
                self.positions[i] = np.clip(
                    self.positions[i], self.bounds[0], self.bounds[1]
                )

                # Update personal best
                score = self.objective(self.positions[i])
                if score < self.personal_best_scores[i]:
                    self.personal_best_scores[i] = score
                    self.personal_best_positions[i] = self.positions[i].copy()

                    # Update global best
                    if score < self.personal_best_scores[self.global_best_idx]:
                        self.global_best_idx = i
                        self.global_best_position = self.positions[i].copy()

        return self.global_best_position, self.objective(self.global_best_position)
```

## Self-Organization

### Flocking (Boids)

```python
import numpy as np

class Boid:
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

class FlockingSystem:
    """Reynolds flocking rules"""

    def __init__(self, boids, separation_dist=2.0, alignment_dist=5.0, cohesion_dist=10.0):
        self.boids = boids
        self.sep_dist = separation_dist
        self.align_dist = alignment_dist
        self.cohesion_dist = cohesion_dist

    def update(self, dt=0.1):
        for boid in self.boids:
            separation = self._separation(boid)
            alignment = self._alignment(boid)
            cohesion = self._cohesion(boid)

            # Combine forces
            acceleration = separation + alignment + cohesion

            # Update velocity and position
            boid.velocity += acceleration * dt
            boid.velocity = self._limit_speed(boid.velocity, max_speed=5.0)
            boid.position += boid.velocity * dt

    def _separation(self, boid):
        """Steer away from nearby boids"""
        steer = np.zeros(2)
        count = 0
        for other in self.boids:
            if other is boid:
                continue
            dist = np.linalg.norm(other.position - boid.position)
            if dist < self.sep_dist:
                diff = boid.position - other.position
                diff /= dist  # Weight by distance
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        return steer

    def _alignment(self, boid):
        """Align with average heading of neighbors"""
        avg_velocity = np.zeros(2)
        count = 0
        for other in self.boids:
            if other is boid:
                continue
            dist = np.linalg.norm(other.position - boid.position)
            if dist < self.align_dist:
                avg_velocity += other.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            return (avg_velocity - boid.velocity) * 0.05
        return np.zeros(2)

    def _cohesion(self, boid):
        """Steer toward center of neighbors"""
        center = np.zeros(2)
        count = 0
        for other in self.boids:
            if other is boid:
                continue
            dist = np.linalg.norm(other.position - boid.position)
            if dist < self.cohesion_dist:
                center += other.position
                count += 1
        if count > 0:
            center /= count
            return (center - boid.position) * 0.01
        return np.zeros(2)

    def _limit_speed(self, velocity, max_speed):
        speed = np.linalg.norm(velocity)
        if speed > max_speed:
            return velocity * (max_speed / speed)
        return velocity
```

## Emergent Task Allocation

```python
class ResponseThresholdModel:
    """Task allocation through threshold response"""

    def __init__(self, agents, task_types):
        self.agents = agents
        self.task_types = task_types
        # Each agent has threshold for each task type
        self.thresholds = {
            agent.id: {task: np.random.uniform(0, 1) for task in task_types}
            for agent in agents
        }
        # Stimulus levels for tasks
        self.stimuli = {task: 0.0 for task in task_types}

    def update_stimuli(self, task_demands):
        """Update task urgency based on demand"""
        for task, demand in task_demands.items():
            self.stimuli[task] = min(1.0, self.stimuli[task] + demand * 0.1)
            # Decay if no demand
            if demand == 0:
                self.stimuli[task] *= 0.95

    def decide_task(self, agent):
        """Agent probabilistically chooses task"""
        probs = {}
        for task in self.task_types:
            s = self.stimuli[task]
            theta = self.thresholds[agent.id][task]
            # Probability increases with stimulus, decreases with threshold
            probs[task] = s**2 / (s**2 + theta**2) if theta > 0 else 1.0

        # Normalize
        total = sum(probs.values())
        if total > 0:
            probs = {k: v/total for k, v in probs.items()}

        # Select task
        return np.random.choice(list(probs.keys()), p=list(probs.values()))

    def adapt_thresholds(self, agent, task, success):
        """Agents adapt thresholds based on experience"""
        if success:
            # Lower threshold for successful tasks
            self.thresholds[agent.id][task] *= 0.95
        else:
            # Raise threshold for failed tasks
            self.thresholds[agent.id][task] = min(1.0, self.thresholds[agent.id][task] * 1.05)
```
