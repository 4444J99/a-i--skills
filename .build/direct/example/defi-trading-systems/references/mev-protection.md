# MEV Protection Strategies

## Understanding MEV

### What is MEV?

**Maximal Extractable Value**: Profit extracted by reordering, inserting, or censoring transactions.

### Common MEV Attacks

| Attack | Description | Target |
|--------|-------------|--------|
| Sandwich | Buy before, sell after victim | Large swaps |
| Frontrunning | Copy and execute before | Arbitrage txs |
| Backrunning | Execute immediately after | Price updates |
| Liquidation | Beat others to liquidate | Undercollateralized |
| JIT Liquidity | Add/remove around swaps | Large trades |

### Sandwich Attack Example

```
Block Order:
1. Attacker: Buy token (raises price)
2. Victim: Buy token (worse price)
3. Attacker: Sell token (profit)

Victim loss = Attacker profit (minus gas)
```

## Protection Strategies

### 1. Slippage Protection

```python
def calculate_safe_slippage(amount_in, expected_out, max_slippage_pct=0.5):
    """
    Set minimum output to protect against sandwich

    max_slippage_pct: Maximum acceptable slippage
    """
    min_amount_out = expected_out * (1 - max_slippage_pct / 100)
    return min_amount_out

# In Solidity:
# require(amountOut >= minAmountOut, "Slippage too high");
```

### 2. Private Mempool

Submit transactions directly to block builders:

```python
import requests

def submit_to_flashbots(signed_tx, target_block):
    """Submit to Flashbots private mempool"""
    bundle = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_sendBundle",
        "params": [{
            "txs": [signed_tx],
            "blockNumber": hex(target_block)
        }]
    }

    response = requests.post(
        "https://relay.flashbots.net",
        json=bundle,
        headers={"X-Flashbots-Signature": signature}
    )
    return response.json()
```

### 3. MEV Blocker

Use RPC endpoints that protect against MEV:

```python
MEV_PROTECTED_RPCS = {
    'flashbots_protect': 'https://rpc.flashbots.net',
    'mev_blocker': 'https://rpc.mevblocker.io',
    'bloxroute': 'https://mev-protection.bloxroute.com'
}

# Send transaction through protected RPC
w3 = Web3(Web3.HTTPProvider(MEV_PROTECTED_RPCS['flashbots_protect']))
tx_hash = w3.eth.send_raw_transaction(signed_tx)
```

### 4. Order Splitting

Break large orders into smaller chunks:

```python
def split_order(total_amount, max_chunk_size, min_time_between):
    """
    Split large order to reduce MEV exposure

    Smaller orders = less attractive to sandwichers
    """
    chunks = []
    remaining = total_amount

    while remaining > 0:
        chunk = min(remaining, max_chunk_size)
        chunks.append({
            'amount': chunk,
            'delay': len(chunks) * min_time_between
        })
        remaining -= chunk

    return chunks

# Example: $100k order
chunks = split_order(100000, 10000, 30)  # $10k chunks, 30s apart
```

### 5. TWAP (Time-Weighted Average Price)

```python
class TWAPExecutor:
    """Execute order over time to minimize impact"""

    def __init__(self, total_amount, duration_minutes, num_orders):
        self.total = total_amount
        self.order_size = total_amount / num_orders
        self.interval = (duration_minutes * 60) / num_orders
        self.executed = 0

    async def execute_next(self):
        if self.executed >= self.total:
            return None

        # Execute single chunk
        result = await execute_swap(self.order_size)
        self.executed += self.order_size

        return result

    def get_schedule(self):
        return [
            {'amount': self.order_size, 'time': i * self.interval}
            for i in range(int(self.total / self.order_size))
        ]
```

### 6. Commit-Reveal Scheme

```solidity
// Commit phase: submit hash of order
function commitOrder(bytes32 commitment) external {
    commitments[msg.sender] = Commitment({
        hash: commitment,
        timestamp: block.timestamp
    });
}

// Reveal phase: execute after delay
function revealOrder(
    uint256 amountIn,
    uint256 minAmountOut,
    bytes32 salt
) external {
    Commitment memory c = commitments[msg.sender];

    // Verify commitment
    require(
        keccak256(abi.encode(amountIn, minAmountOut, salt)) == c.hash,
        "Invalid reveal"
    );

    // Ensure delay passed
    require(
        block.timestamp >= c.timestamp + REVEAL_DELAY,
        "Too early"
    );

    // Execute order
    executeSwap(amountIn, minAmountOut);
}
```

### 7. DEX Aggregators

Use aggregators that split across venues:

```python
async def get_best_route(token_in, token_out, amount):
    """
    Query aggregators for best execution

    Aggregators split orders across DEXes to minimize impact
    """
    routes = await asyncio.gather(
        query_1inch(token_in, token_out, amount),
        query_paraswap(token_in, token_out, amount),
        query_cowswap(token_in, token_out, amount)
    )

    return max(routes, key=lambda r: r['expected_output'])
```

### 8. Batch Auctions (CoW Protocol)

```
Traditional:          Batch Auction:
Order 1 → Execute    Order 1 ─┐
Order 2 → Execute    Order 2 ─┼── Batch → Single price
Order 3 → Execute    Order 3 ─┘

Batch auctions match orders at uniform price
Eliminates sandwiching within batch
```

## Detection

### Detect Sandwich Attack

```python
def detect_sandwich(tx_hash, block):
    """Analyze if transaction was sandwiched"""
    # Get transaction position in block
    tx_index = get_tx_index(tx_hash, block)
    block_txs = get_block_transactions(block)

    # Look for buy before and sell after from same address
    potential_frontrun = block_txs[tx_index - 1] if tx_index > 0 else None
    potential_backrun = block_txs[tx_index + 1] if tx_index < len(block_txs) - 1 else None

    if potential_frontrun and potential_backrun:
        if (potential_frontrun['from'] == potential_backrun['from'] and
            is_opposite_trade(potential_frontrun, potential_backrun)):
            return {
                'sandwiched': True,
                'attacker': potential_frontrun['from'],
                'estimated_loss': calculate_sandwich_loss(
                    potential_frontrun, tx_hash, potential_backrun
                )
            }

    return {'sandwiched': False}
```

## Best Practices

1. **Always set slippage** - Never use 0% or very high slippage
2. **Use private mempools** - For large trades
3. **Split large orders** - Reduce single-trade exposure
4. **Check gas prices** - Unusual gas = possible attack
5. **Use limit orders** - When possible, avoid market orders
6. **Monitor executions** - Track actual vs expected prices
7. **Use MEV-aware DEXes** - CoW Protocol, Uniswap X
