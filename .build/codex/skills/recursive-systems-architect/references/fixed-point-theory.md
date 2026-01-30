# Fixed Point Theory

## What is a Fixed Point?

A fixed point of a function f is a value x where:
```
f(x) = x
```

The function maps the point to itself.

## Fixed Point in Recursive Systems

### Iteration to Fixed Point

```python
def find_fixed_point(f, initial, tolerance=1e-9, max_iter=1000):
    """
    Find x where f(x) = x by iteration
    """
    x = initial
    for i in range(max_iter):
        x_next = f(x)

        # Check convergence
        if abs(x_next - x) < tolerance:
            return x_next, i + 1  # Fixed point found

        x = x_next

    return x, max_iter  # May not have converged
```

### Examples

**Square Root via Fixed Point**
```python
# To find sqrt(a), solve x = (x + a/x) / 2
def sqrt_iteration(a):
    f = lambda x: (x + a/x) / 2
    result, iterations = find_fixed_point(f, a/2)
    return result

sqrt_iteration(2)  # ≈ 1.4142135623730951
```

**Self-Consistent Equations**
```python
# Economic equilibrium: price = f(demand(price))
def equilibrium_price():
    def price_function(p):
        demand = 100 - 2*p  # Demand decreases with price
        supply = 20 + 3*p   # Supply increases with price
        # New price adjusts toward equilibrium
        return (demand + supply) / 5

    return find_fixed_point(price_function, 50)
```

## Contraction Mapping Theorem

**Banach Fixed Point Theorem**:
If f is a contraction mapping (shrinks distances), then:
1. f has exactly one fixed point
2. Iteration from any start will converge to it

```python
def is_contraction(f, points, L=0.99):
    """
    Check if f is a contraction with factor < L
    |f(x) - f(y)| < L * |x - y| for all x, y
    """
    for x in points:
        for y in points:
            if x != y:
                ratio = abs(f(x) - f(y)) / abs(x - y)
                if ratio >= L:
                    return False, ratio
    return True, None
```

## Fixed Points in Type Systems

### Recursive Types

```haskell
-- List is a fixed point of: F(X) = 1 + A × X
-- List A = Fix (λX. 1 + A × X)

-- In practice:
data List a = Nil | Cons a (List a)
-- Nil corresponds to 1
-- Cons a (List a) corresponds to A × X
```

### Y Combinator

The Y combinator finds fixed points of functions:

```python
# Y = λf. (λx. f(x x)) (λx. f(x x))

def Y(f):
    """Y combinator - finds fixed point of f"""
    return (lambda x: f(lambda v: x(x)(v)))(
           lambda x: f(lambda v: x(x)(v)))

# Factorial without explicit recursion
factorial = Y(lambda f: lambda n: 1 if n == 0 else n * f(n - 1))
factorial(5)  # 120
```

## Fixed Points in Semantics

### Denotational Semantics

Programs can be understood as fixed points:

```python
# while condition do body
# is the least fixed point of:
# F(X) = if condition then body; X else skip

def while_semantics(condition, body):
    """
    Semantics of while loop as fixed point
    """
    def F(X):
        def loop(state):
            if condition(state):
                new_state = body(state)
                return X(new_state)
            else:
                return state
        return loop

    # Find least fixed point
    return lfp(F)
```

### Recursive Definitions

```python
# Factorial semantically:
# fact = F(fact) where F(f) = λn. if n=0 then 1 else n*f(n-1)
# fact is the fixed point of F
```

## Applications

### Self-Referential Systems

```python
class SelfStabilizingSystem:
    """
    System that evolves toward a fixed point state
    """

    def __init__(self, initial_state):
        self.state = initial_state

    def update_rule(self, state):
        """Override: how state evolves"""
        raise NotImplementedError

    def run_to_equilibrium(self, max_steps=1000, tolerance=1e-6):
        for step in range(max_steps):
            new_state = self.update_rule(self.state)

            if self._is_fixed_point(new_state, tolerance):
                return new_state, step

            self.state = new_state

        return self.state, max_steps

    def _is_fixed_point(self, new_state, tolerance):
        return self._distance(self.state, new_state) < tolerance
```

### Belief Propagation

```python
def belief_propagation_fixed_point(graph, max_iter=100):
    """
    Find fixed point of belief propagation messages
    """
    messages = initialize_messages(graph)

    for _ in range(max_iter):
        new_messages = {}
        for edge in graph.edges:
            new_messages[edge] = compute_message(graph, messages, edge)

        # Check for fixed point
        if messages_converged(messages, new_messages):
            return new_messages

        messages = new_messages

    return messages
```

### Game Theory Equilibria

Nash equilibrium is a fixed point of best-response dynamics:

```python
def find_nash_equilibrium(game, initial_strategies):
    """
    Find Nash equilibrium as fixed point of best responses
    """
    strategies = initial_strategies

    for _ in range(1000):
        new_strategies = {}
        for player in game.players:
            # Best response given others' strategies
            others = {p: s for p, s in strategies.items() if p != player}
            new_strategies[player] = best_response(game, player, others)

        if strategies == new_strategies:
            return strategies  # Fixed point = Nash equilibrium

        strategies = new_strategies

    return strategies
```

## Key Theorems

| Theorem | Statement | Application |
|---------|-----------|-------------|
| Banach | Contraction has unique fixed point | Iterative algorithms |
| Brouwer | Continuous f: D→D has fixed point | Existence proofs |
| Knaster-Tarski | Monotone f on lattice has fixed point | Program semantics |
| Kleene | ⊥, f(⊥), f(f(⊥)),... reaches lfp | Recursive definitions |
