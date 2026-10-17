# AMM (Automated Market Maker) Formulas

## Constant Product (Uniswap V2)

### Core Formula

```
x × y = k (constant)

x: reserve of token A
y: reserve of token B
k: constant product
```

### Price

```python
def get_price(reserve_a, reserve_b):
    """Price of A in terms of B"""
    return reserve_b / reserve_a
```

### Swap Output

```python
def get_amount_out(amount_in, reserve_in, reserve_out, fee=0.003):
    """
    Calculate output amount for a swap

    fee: typically 0.3% (0.003)
    """
    amount_in_with_fee = amount_in * (1 - fee)
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in + amount_in_with_fee
    return numerator / denominator

# Example:
# Swap 1 ETH for USDC
# reserve_eth = 100 ETH
# reserve_usdc = 200,000 USDC
# amount_out = (0.997 × 200000) / (100 + 0.997) ≈ 1974 USDC
```

### Price Impact

```python
def calculate_price_impact(amount_in, reserve_in, reserve_out):
    """
    Price impact as percentage

    Larger trades = higher impact
    """
    spot_price = reserve_out / reserve_in
    amount_out = get_amount_out(amount_in, reserve_in, reserve_out)
    execution_price = amount_in / amount_out
    return (execution_price - spot_price) / spot_price
```

### Slippage

```python
def calculate_slippage(expected_out, actual_out):
    """Difference between expected and actual output"""
    return (expected_out - actual_out) / expected_out
```

## Liquidity Provision

### Adding Liquidity

```python
def calculate_liquidity_tokens(
    amount_a,
    amount_b,
    reserve_a,
    reserve_b,
    total_supply
):
    """
    LP tokens minted when adding liquidity

    Must add proportional amounts to maintain price
    """
    if total_supply == 0:
        # First deposit: sqrt(amount_a × amount_b)
        import math
        return math.sqrt(amount_a * amount_b)

    # Subsequent: proportional to existing supply
    lp_from_a = (amount_a / reserve_a) * total_supply
    lp_from_b = (amount_b / reserve_b) * total_supply
    return min(lp_from_a, lp_from_b)
```

### Removing Liquidity

```python
def calculate_withdrawal(lp_tokens, reserve_a, reserve_b, total_supply):
    """
    Amounts received when removing liquidity
    """
    share = lp_tokens / total_supply
    amount_a = reserve_a * share
    amount_b = reserve_b * share
    return amount_a, amount_b
```

### Impermanent Loss

```python
import math

def impermanent_loss(price_ratio):
    """
    Calculate IL given price change

    price_ratio: new_price / original_price

    Returns negative percentage (loss)
    """
    return 2 * math.sqrt(price_ratio) / (1 + price_ratio) - 1

# Examples:
# 1.25x price change: IL = -0.6%
# 1.50x price change: IL = -2.0%
# 2.00x price change: IL = -5.7%
# 3.00x price change: IL = -13.4%
# 5.00x price change: IL = -25.5%
```

## Concentrated Liquidity (Uniswap V3)

### Virtual Reserves

```python
import math

def virtual_reserves(liquidity, sqrt_price, sqrt_price_lower, sqrt_price_upper):
    """
    Calculate virtual reserves for concentrated position
    """
    # Token A reserves
    if sqrt_price <= sqrt_price_lower:
        # All in token A
        x = liquidity * (sqrt_price_upper - sqrt_price_lower) / (sqrt_price_lower * sqrt_price_upper)
        y = 0
    elif sqrt_price >= sqrt_price_upper:
        # All in token B
        x = 0
        y = liquidity * (sqrt_price_upper - sqrt_price_lower)
    else:
        # In range
        x = liquidity * (sqrt_price_upper - sqrt_price) / (sqrt_price * sqrt_price_upper)
        y = liquidity * (sqrt_price - sqrt_price_lower)

    return x, y
```

### Tick Math

```python
def price_to_tick(price, tick_spacing=1):
    """Convert price to tick"""
    tick = math.log(price) / math.log(1.0001)
    return int(tick // tick_spacing) * tick_spacing

def tick_to_price(tick):
    """Convert tick to price"""
    return 1.0001 ** tick

def tick_to_sqrt_price(tick):
    """Convert tick to sqrt price (Q64.96 format typically)"""
    return math.sqrt(1.0001 ** tick)
```

### Position Value

```python
def position_value(liquidity, current_tick, lower_tick, upper_tick, token_b_price):
    """
    Calculate current value of concentrated liquidity position
    """
    sqrt_price = tick_to_sqrt_price(current_tick)
    sqrt_lower = tick_to_sqrt_price(lower_tick)
    sqrt_upper = tick_to_sqrt_price(upper_tick)

    x, y = virtual_reserves(liquidity, sqrt_price, sqrt_lower, sqrt_upper)

    # Value in token B terms
    return x * token_b_price + y
```

### Liquidity for Amounts

```python
def liquidity_for_amounts(
    amount_a,
    amount_b,
    sqrt_price,
    sqrt_price_lower,
    sqrt_price_upper
):
    """
    Calculate liquidity from token amounts
    """
    if sqrt_price <= sqrt_price_lower:
        # Below range: use only token A
        liquidity = amount_a * sqrt_price_lower * sqrt_price_upper / (sqrt_price_upper - sqrt_price_lower)
    elif sqrt_price >= sqrt_price_upper:
        # Above range: use only token B
        liquidity = amount_b / (sqrt_price_upper - sqrt_price_lower)
    else:
        # In range: use both
        liquidity_a = amount_a * sqrt_price * sqrt_price_upper / (sqrt_price_upper - sqrt_price)
        liquidity_b = amount_b / (sqrt_price - sqrt_price_lower)
        liquidity = min(liquidity_a, liquidity_b)

    return liquidity
```

## Fee Calculations

### Uniswap V2 Fees

```python
def calculate_fees_earned(volume, fee_rate, lp_share):
    """
    Fees earned by LP

    volume: trading volume through pool
    fee_rate: 0.003 for 0.3%
    lp_share: your share of pool
    """
    total_fees = volume * fee_rate
    return total_fees * lp_share
```

### Uniswap V3 Fees

```python
def calculate_concentrated_fees(
    volume_in_range,
    fee_tier,
    position_liquidity,
    total_liquidity_in_range
):
    """
    Fees earned by concentrated position

    Only earns when price is in position's range
    """
    total_fees = volume_in_range * fee_tier
    position_share = position_liquidity / total_liquidity_in_range
    return total_fees * position_share
```

## APR/APY Calculations

```python
def calculate_lp_apr(daily_fees, position_value, days=365):
    """Annual Percentage Rate from fees"""
    daily_return = daily_fees / position_value
    return daily_return * days

def calculate_lp_apy(daily_fees, position_value, compounds_per_year=365):
    """Annual Percentage Yield with compounding"""
    daily_return = daily_fees / position_value
    return (1 + daily_return) ** compounds_per_year - 1

def calculate_net_apr(fee_apr, il_percent):
    """Net return accounting for impermanent loss"""
    return fee_apr + il_percent  # IL is negative
```

## Curve StableSwap

```python
def stableswap_invariant(reserves, A, n):
    """
    StableSwap invariant (simplified)

    A: amplification coefficient
    n: number of tokens
    D: invariant

    A × D^n × sum(x_i) + D = A × D^n × n^n × product(x_i) + D^(n+1) / (n^n × product(x_i))
    """
    # This is typically solved iteratively
    pass
```
