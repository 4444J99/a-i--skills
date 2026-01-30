# Perpetual Futures Mechanics

## How Perpetuals Work

Unlike traditional futures with expiration dates, perpetual futures never expire. They track the underlying asset price through a funding mechanism.

### Funding Rate

```
Funding Rate = (Mark Price - Index Price) / Index Price × Funding Interval

If Funding > 0: Longs pay Shorts
If Funding < 0: Shorts pay Longs
```

**Funding Payment:**
```
Payment = Position Size × Funding Rate

Example:
- Position: 10 BTC long
- Funding Rate: 0.01% (positive)
- Payment: 10 × 0.0001 = 0.001 BTC (you pay)
```

### Mark Price vs Index Price

**Index Price**: Spot price aggregated from multiple exchanges

```python
def calculate_index_price(exchange_prices, weights):
    """Weighted average of spot prices"""
    return sum(p * w for p, w in zip(exchange_prices, weights))
```

**Mark Price**: Fair value used for liquidation

```python
def calculate_mark_price(index_price, basis):
    """
    Mark price typically uses moving average of basis
    to prevent manipulation
    """
    return index_price * (1 + basis)
```

## Leverage and Margin

### Initial Margin

```python
def calculate_initial_margin(position_value, leverage):
    """
    Margin required to open position

    position_value: notional value
    leverage: desired leverage
    """
    return position_value / leverage

# Example:
# Open 1 BTC position at $50,000 with 10x leverage
# Initial margin = $50,000 / 10 = $5,000
```

### Maintenance Margin

```python
def calculate_maintenance_margin(position_value, mmr=0.005):
    """
    Minimum margin to keep position open
    mmr: maintenance margin rate (e.g., 0.5%)
    """
    return position_value * mmr
```

### Margin Ratio

```python
def calculate_margin_ratio(equity, position_value):
    """
    Current margin ratio
    Liquidation typically occurs around maintenance margin
    """
    return equity / position_value
```

## Liquidation

### Liquidation Price

```python
def long_liquidation_price(entry_price, leverage, mmr=0.005):
    """
    Price at which long position is liquidated

    Formula: Entry × (1 - 1/Leverage + MMR)
    """
    return entry_price * (1 - (1 / leverage) + mmr)

def short_liquidation_price(entry_price, leverage, mmr=0.005):
    """
    Price at which short position is liquidated

    Formula: Entry × (1 + 1/Leverage - MMR)
    """
    return entry_price * (1 + (1 / leverage) - mmr)

# Example:
# Long entry at $50,000, 10x leverage, 0.5% MMR
# Liq price = $50,000 × (1 - 0.1 + 0.005) = $45,250
```

### Bankruptcy Price

```python
def bankruptcy_price(entry_price, leverage, side='long'):
    """
    Price at which margin = 0
    Exchange loses money if price goes beyond this
    """
    if side == 'long':
        return entry_price * (1 - 1/leverage)
    else:
        return entry_price * (1 + 1/leverage)
```

### Insurance Fund

When liquidation occurs above bankruptcy price, difference goes to insurance fund.
When liquidation occurs below bankruptcy price, insurance fund covers loss.

```python
def liquidation_surplus_or_loss(entry_price, liquidation_price, bankruptcy_price, position_size, side):
    if side == 'long':
        surplus = (liquidation_price - bankruptcy_price) * position_size
    else:
        surplus = (bankruptcy_price - liquidation_price) * position_size

    return surplus  # Positive = fund gains, Negative = fund pays
```

## Position Accounting

### Unrealized PnL

```python
def unrealized_pnl(entry_price, current_price, size, side):
    if side == 'long':
        return (current_price - entry_price) * size
    else:  # short
        return (entry_price - current_price) * size
```

### Realized PnL (with funding)

```python
def realized_pnl(entry_price, exit_price, size, side, funding_paid, fees):
    if side == 'long':
        trading_pnl = (exit_price - entry_price) * size
    else:
        trading_pnl = (entry_price - exit_price) * size

    return trading_pnl - funding_paid - fees
```

### ROE (Return on Equity)

```python
def roe(pnl, margin):
    """Return on equity (margin used)"""
    return pnl / margin * 100  # Percentage
```

## Order Types

### Limit Order

```python
class LimitOrder:
    """Order at specific price or better"""
    def __init__(self, side, size, price, post_only=False):
        self.side = side
        self.size = size
        self.price = price
        self.post_only = post_only  # Only maker, cancel if would take

    def would_fill(self, market_price):
        if self.side == 'buy':
            return market_price <= self.price
        else:
            return market_price >= self.price
```

### Stop Loss / Take Profit

```python
class StopOrder:
    """Triggered when price reaches trigger level"""
    def __init__(self, side, size, trigger_price, order_type='market', limit_price=None):
        self.side = side
        self.size = size
        self.trigger_price = trigger_price
        self.order_type = order_type
        self.limit_price = limit_price
        self.triggered = False

    def check_trigger(self, mark_price):
        if self.side == 'buy':  # Stop loss for short, or buy stop
            return mark_price >= self.trigger_price
        else:  # Stop loss for long, or sell stop
            return mark_price <= self.trigger_price
```

### Reduce-Only Order

```python
class ReduceOnlyOrder:
    """Can only reduce position, not increase"""
    def __init__(self, side, size, price):
        self.side = side
        self.size = size
        self.price = price
        self.reduce_only = True

    def effective_size(self, current_position):
        """Limit size to not flip position"""
        if current_position == 0:
            return 0
        if (current_position > 0 and self.side == 'sell') or \
           (current_position < 0 and self.side == 'buy'):
            return min(self.size, abs(current_position))
        return 0
```

## Fee Structure

```python
class FeeStructure:
    def __init__(self, maker_rate=-0.0002, taker_rate=0.0005):
        """
        Maker: Add liquidity (limit orders that rest)
        Taker: Remove liquidity (market orders, crossing limit orders)

        Negative maker fee = rebate
        """
        self.maker_rate = maker_rate
        self.taker_rate = taker_rate

    def calculate_fee(self, notional_value, is_maker):
        rate = self.maker_rate if is_maker else self.taker_rate
        return notional_value * rate
```

## Funding Rate Calculation Details

### Premium Index

```python
def calculate_premium_index(mark_price, index_price):
    """Premium of perp over spot"""
    return (mark_price - index_price) / index_price
```

### Interest Rate Component

```python
def calculate_funding_rate(premium_index, interest_rate=0.0001):
    """
    Full funding rate formula

    interest_rate: typically ~0.01% per funding period
    """
    # Clamp premium to prevent extreme funding
    clamped_premium = max(-0.05, min(0.05, premium_index))

    # Funding = Premium + Interest
    return clamped_premium + interest_rate
```

### 8-Hour Funding

Most exchanges use 8-hour funding intervals:

```python
def annualized_funding(funding_rate):
    """Convert single funding rate to annual"""
    return funding_rate * 3 * 365  # 3 times per day × 365 days
```
