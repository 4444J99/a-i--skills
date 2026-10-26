# Coordination Protocols

## Consensus Algorithms

### Simple Majority Voting

```python
class MajorityVoting:
    def __init__(self, agents, threshold=0.5):
        self.agents = agents
        self.threshold = threshold

    async def vote(self, proposal):
        votes = {}
        for agent in self.agents:
            votes[agent.id] = await agent.vote(proposal)

        approve_count = sum(1 for v in votes.values() if v)
        total = len(votes)

        return {
            'passed': approve_count / total > self.threshold,
            'approve': approve_count,
            'reject': total - approve_count,
            'votes': votes
        }
```

### Weighted Voting

```python
class WeightedVoting:
    def __init__(self, agents, weights):
        self.agents = agents
        self.weights = weights  # agent_id -> weight

    async def vote(self, proposal):
        weighted_approve = 0
        total_weight = sum(self.weights.values())

        for agent in self.agents:
            vote = await agent.vote(proposal)
            if vote:
                weighted_approve += self.weights[agent.id]

        return {
            'passed': weighted_approve > total_weight / 2,
            'weighted_approve': weighted_approve,
            'total_weight': total_weight
        }
```

### Borda Count (Ranked Choice)

```python
class BordaCount:
    """Ranked choice voting for multiple options"""

    def __init__(self, agents):
        self.agents = agents

    async def vote(self, options):
        scores = {opt: 0 for opt in options}
        n = len(options)

        for agent in self.agents:
            rankings = await agent.rank(options)
            for rank, option in enumerate(rankings):
                scores[option] += (n - rank)  # Higher rank = more points

        winner = max(scores, key=scores.get)
        return {
            'winner': winner,
            'scores': scores
        }
```

### Paxos-Inspired Consensus

```python
class PaxosConsensus:
    """Simplified Paxos for agent consensus"""

    def __init__(self, agents):
        self.agents = agents
        self.proposal_number = 0

    async def propose(self, value):
        self.proposal_number += 1
        n = self.proposal_number

        # Phase 1: Prepare
        prepare_responses = []
        for agent in self.agents:
            response = await agent.prepare(n)
            prepare_responses.append(response)

        # Check majority promised
        promises = [r for r in prepare_responses if r['promised']]
        if len(promises) < len(self.agents) // 2 + 1:
            return {'accepted': False, 'reason': 'No majority promise'}

        # Use highest accepted value or proposed value
        highest = max(promises, key=lambda r: r.get('accepted_n', 0))
        final_value = highest.get('accepted_value', value)

        # Phase 2: Accept
        accept_responses = []
        for agent in self.agents:
            response = await agent.accept(n, final_value)
            accept_responses.append(response)

        # Check majority accepted
        accepted = [r for r in accept_responses if r['accepted']]
        if len(accepted) < len(self.agents) // 2 + 1:
            return {'accepted': False, 'reason': 'No majority accept'}

        return {'accepted': True, 'value': final_value}
```

## Task Allocation Protocols

### Contract Net Protocol

```python
class ContractNetProtocol:
    """
    1. Manager announces task
    2. Contractors bid
    3. Manager awards to best bidder
    4. Contractor executes
    """

    def __init__(self, manager, contractors):
        self.manager = manager
        self.contractors = contractors

    async def allocate_task(self, task):
        # Announce
        announcement = self.manager.create_announcement(task)

        # Collect bids
        bids = []
        for contractor in self.contractors:
            if contractor.can_handle(task):
                bid = await contractor.submit_bid(announcement)
                bids.append(bid)

        if not bids:
            return {'allocated': False, 'reason': 'No bids'}

        # Award to best bid
        best_bid = self.manager.evaluate_bids(bids)
        winner = best_bid['contractor']

        # Confirm award
        await winner.award_contract(task)

        return {
            'allocated': True,
            'contractor': winner.id,
            'bid': best_bid
        }
```

### Auction-Based Allocation

```python
class TaskAuction:
    """Auction tasks to agents"""

    def __init__(self, agents):
        self.agents = agents

    async def first_price_auction(self, task):
        """Winner pays their bid"""
        bids = {}
        for agent in self.agents:
            bid = await agent.bid(task)
            bids[agent.id] = bid

        winner_id = min(bids, key=bids.get)  # Lowest cost bid
        return {
            'winner': winner_id,
            'price': bids[winner_id]
        }

    async def second_price_auction(self, task):
        """Winner pays second-highest bid"""
        bids = {}
        for agent in self.agents:
            bid = await agent.bid(task)
            bids[agent.id] = bid

        sorted_bids = sorted(bids.items(), key=lambda x: x[1])
        winner_id = sorted_bids[0][0]
        price = sorted_bids[1][1] if len(sorted_bids) > 1 else sorted_bids[0][1]

        return {
            'winner': winner_id,
            'price': price
        }
```

### Market-Based Allocation

```python
class TaskMarket:
    """Market where agents buy/sell task rights"""

    def __init__(self):
        self.task_prices = {}
        self.agent_budgets = {}
        self.allocations = {}

    def set_budget(self, agent_id, budget):
        self.agent_budgets[agent_id] = budget

    async def allocate(self, tasks, agents):
        """Market clearing allocation"""
        remaining_tasks = list(tasks)
        allocations = {agent.id: [] for agent in agents}

        while remaining_tasks:
            # Collect demand at current prices
            demands = {}
            for agent in agents:
                affordable = [
                    t for t in remaining_tasks
                    if self.task_prices.get(t.id, 0) <= self.agent_budgets[agent.id]
                ]
                if affordable:
                    preferred = await agent.rank_tasks(affordable)
                    demands[agent.id] = preferred[0] if preferred else None

            # Allocate non-contested tasks
            task_demand = defaultdict(list)
            for agent_id, task in demands.items():
                if task:
                    task_demand[task.id].append(agent_id)

            for task_id, demanding_agents in task_demand.items():
                if len(demanding_agents) == 1:
                    # Allocate
                    agent_id = demanding_agents[0]
                    allocations[agent_id].append(task_id)
                    remaining_tasks = [t for t in remaining_tasks if t.id != task_id]
                else:
                    # Increase price
                    self.task_prices[task_id] = self.task_prices.get(task_id, 0) + 1

            # Prevent infinite loop
            if not any(demands.values()):
                break

        return allocations
```

## Communication Protocols

### Request-Response

```python
class RequestResponse:
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.pending = {}

    async def request(self, sender, receiver, message):
        request_id = generate_id()
        future = asyncio.Future()
        self.pending[request_id] = future

        await receiver.receive({
            'type': 'request',
            'id': request_id,
            'from': sender.id,
            'content': message
        })

        try:
            response = await asyncio.wait_for(future, self.timeout)
            return response
        except asyncio.TimeoutError:
            del self.pending[request_id]
            raise

    async def respond(self, request_id, response):
        if request_id in self.pending:
            self.pending[request_id].set_result(response)
            del self.pending[request_id]
```

### Publish-Subscribe

```python
class PubSub:
    def __init__(self):
        self.subscribers = defaultdict(set)

    def subscribe(self, agent, topic):
        self.subscribers[topic].add(agent)

    def unsubscribe(self, agent, topic):
        self.subscribers[topic].discard(agent)

    async def publish(self, topic, message):
        for agent in self.subscribers[topic]:
            await agent.receive({
                'type': 'publication',
                'topic': topic,
                'content': message
            })
```

### Gossip Protocol

```python
class GossipProtocol:
    """Epidemic information spread"""

    def __init__(self, agents, fanout=3):
        self.agents = agents
        self.fanout = fanout  # Number of peers to gossip to
        self.seen = defaultdict(set)  # message_id -> agents who've seen

    async def gossip(self, sender, message):
        message_id = message.get('id', generate_id())
        self.seen[message_id].add(sender.id)

        # Select random peers (excluding those who've seen)
        candidates = [a for a in self.agents
                      if a.id not in self.seen[message_id]]
        targets = random.sample(candidates, min(self.fanout, len(candidates)))

        for target in targets:
            self.seen[message_id].add(target.id)
            await target.receive({
                'type': 'gossip',
                'id': message_id,
                'content': message
            })
            # Recipient will continue gossiping
```

## Synchronization

### Barrier Synchronization

```python
class Barrier:
    """Wait for all agents to reach a point"""

    def __init__(self, agent_count):
        self.count = agent_count
        self.arrived = 0
        self.event = asyncio.Event()
        self.lock = asyncio.Lock()

    async def wait(self, agent_id):
        async with self.lock:
            self.arrived += 1
            if self.arrived >= self.count:
                self.event.set()

        await self.event.wait()
```

### Leader Election

```python
class LeaderElection:
    """Elect a leader among agents"""

    async def bully_election(self, agents):
        """Bully algorithm: highest ID wins"""
        # Sort by ID (or priority)
        candidates = sorted(agents, key=lambda a: a.priority, reverse=True)

        for candidate in candidates:
            if await candidate.is_alive():
                # Announce leadership
                for agent in agents:
                    await agent.notify_leader(candidate.id)
                return candidate.id

        return None
```
