# Metacognitive System Patterns

## Metacognition Architecture

### Three-Level Model

```
┌─────────────────────────────────────────────────────────┐
│                  METALEVEL (Level 2)                     │
│  • Monitor cognitive processes                          │
│  • Evaluate performance                                 │
│  • Select/modify strategies                             │
└─────────────────────────────────────────────────────────┘
                         ↕ Monitor & Control
┌─────────────────────────────────────────────────────────┐
│                  OBJECT LEVEL (Level 1)                  │
│  • Execute cognitive operations                         │
│  • Process information                                  │
│  • Generate outputs                                     │
└─────────────────────────────────────────────────────────┘
                         ↕ Perception & Action
┌─────────────────────────────────────────────────────────┐
│                  ENVIRONMENT (Level 0)                   │
│  • External world                                       │
│  • Input/output interface                               │
└─────────────────────────────────────────────────────────┘
```

### Implementation Pattern

```python
class MetacognitiveAgent:
    """
    Agent with metacognitive capabilities
    """

    def __init__(self):
        # Object level
        self.knowledge = {}
        self.strategies = {}
        self.current_strategy = None

        # Meta level
        self.performance_history = []
        self.strategy_evaluations = {}
        self.confidence_model = {}

    def process(self, task):
        """Main processing with metacognitive oversight"""

        # Meta: Select strategy
        strategy = self._meta_select_strategy(task)

        # Object: Execute strategy
        result = self._execute_strategy(strategy, task)

        # Meta: Monitor result
        self._meta_monitor(strategy, task, result)

        # Meta: Decide if result is acceptable
        if not self._meta_evaluate(result):
            # Meta: Adjust and retry
            return self._meta_adjust_and_retry(task, result)

        return result

    def _meta_select_strategy(self, task):
        """Metalevel: Choose appropriate strategy"""
        task_type = self._classify_task(task)

        # Check past performance for similar tasks
        best_strategy = None
        best_score = -1

        for strategy, evaluations in self.strategy_evaluations.items():
            if task_type in evaluations:
                score = evaluations[task_type]['success_rate']
                if score > best_score:
                    best_score = score
                    best_strategy = strategy

        return best_strategy or self._default_strategy()

    def _meta_monitor(self, strategy, task, result):
        """Metalevel: Track performance"""
        self.performance_history.append({
            'strategy': strategy,
            'task_type': self._classify_task(task),
            'success': self._evaluate_success(result),
            'confidence': self._estimate_confidence(result),
            'resources_used': self._measure_resources()
        })

    def _meta_evaluate(self, result):
        """Metalevel: Evaluate if result meets criteria"""
        confidence = self._estimate_confidence(result)
        threshold = self.confidence_model.get('acceptance_threshold', 0.8)
        return confidence >= threshold

    def _meta_adjust_and_retry(self, task, previous_result):
        """Metalevel: Modify approach and try again"""
        # Analyze failure
        failure_analysis = self._analyze_failure(previous_result)

        # Adjust strategy based on analysis
        if failure_analysis['type'] == 'insufficient_knowledge':
            self._acquire_knowledge(task)
        elif failure_analysis['type'] == 'wrong_strategy':
            self.current_strategy = self._alternative_strategy()
        elif failure_analysis['type'] == 'insufficient_effort':
            self._increase_resources()

        # Retry with adjustments
        return self.process(task)
```

## Self-Monitoring Patterns

### Confidence Calibration

```python
class ConfidenceMonitor:
    """
    Track and calibrate confidence estimates
    """

    def __init__(self):
        self.predictions = []  # (confidence, was_correct)

    def record(self, confidence, actual_correct):
        self.predictions.append((confidence, actual_correct))

    def calibration_error(self, bins=10):
        """
        Expected Calibration Error
        Perfect calibration: confidence == accuracy
        """
        if not self.predictions:
            return 0

        # Bin predictions by confidence
        bin_edges = np.linspace(0, 1, bins + 1)
        ece = 0

        for i in range(bins):
            in_bin = [p for p in self.predictions
                      if bin_edges[i] <= p[0] < bin_edges[i+1]]

            if in_bin:
                avg_confidence = np.mean([p[0] for p in in_bin])
                accuracy = np.mean([p[1] for p in in_bin])
                ece += len(in_bin) * abs(avg_confidence - accuracy)

        return ece / len(self.predictions)

    def should_recalibrate(self, threshold=0.1):
        return self.calibration_error() > threshold
```

### Resource Monitoring

```python
class ResourceMonitor:
    """
    Monitor computational resources used
    """

    def __init__(self, limits):
        self.limits = limits
        self.usage = {
            'time': 0,
            'memory': 0,
            'api_calls': 0
        }

    def start_operation(self):
        self._start_time = time.time()

    def end_operation(self):
        self.usage['time'] += time.time() - self._start_time

    def check_limits(self):
        """Return which limits are approaching/exceeded"""
        warnings = []
        for resource, limit in self.limits.items():
            ratio = self.usage[resource] / limit
            if ratio > 0.9:
                warnings.append(('critical', resource, ratio))
            elif ratio > 0.7:
                warnings.append(('warning', resource, ratio))
        return warnings

    def should_terminate(self):
        """Check if any hard limit exceeded"""
        return any(self.usage[r] >= l for r, l in self.limits.items())
```

## Strategy Selection Patterns

### Multi-Armed Bandit for Strategy Selection

```python
class StrategySelector:
    """
    Use Thompson Sampling to select strategies
    Balances exploration vs exploitation
    """

    def __init__(self, strategies):
        self.strategies = strategies
        # Beta distribution parameters for each strategy
        self.alpha = {s: 1 for s in strategies}  # Successes + 1
        self.beta = {s: 1 for s in strategies}   # Failures + 1

    def select(self):
        """Thompson Sampling: sample from posteriors"""
        samples = {}
        for s in self.strategies:
            samples[s] = np.random.beta(self.alpha[s], self.beta[s])

        return max(samples, key=samples.get)

    def update(self, strategy, success):
        """Update beliefs based on outcome"""
        if success:
            self.alpha[strategy] += 1
        else:
            self.beta[strategy] += 1

    def get_confidence(self, strategy):
        """Return confidence in strategy being best"""
        total = self.alpha[strategy] + self.beta[strategy]
        return self.alpha[strategy] / total
```

### Hierarchical Strategy Selection

```python
class HierarchicalStrategies:
    """
    Strategies organized in hierarchy
    Higher levels are more general
    """

    def __init__(self):
        self.hierarchy = {
            'meta_strategies': {
                'careful': ['verify', 'double_check', 'slow'],
                'fast': ['heuristic', 'approximate', 'parallel'],
                'learning': ['explore', 'experiment', 'analyze']
            },
            'strategies': {}  # Leaf strategies
        }

    def select(self, task, confidence):
        """
        Select strategy based on task and confidence
        Low confidence → careful
        High confidence → fast
        Unknown task → learning
        """
        if confidence < 0.5:
            meta = 'careful'
        elif confidence > 0.9 and self._is_familiar(task):
            meta = 'fast'
        else:
            meta = 'learning'

        # Select specific strategy within meta-category
        candidates = self.hierarchy['meta_strategies'][meta]
        return self._select_from_candidates(candidates, task)
```

## Self-Modeling Patterns

```python
class SelfModel:
    """
    Agent's model of its own capabilities
    """

    def __init__(self):
        self.capabilities = {}
        self.limitations = {}
        self.biases = {}

    def update_capability(self, capability, evidence):
        """Update belief about capability based on evidence"""
        if capability not in self.capabilities:
            self.capabilities[capability] = {
                'strength': 0.5,
                'evidence_count': 0
            }

        # Bayesian update
        cap = self.capabilities[capability]
        cap['evidence_count'] += 1
        # Weight new evidence less as we accumulate more
        weight = 1 / cap['evidence_count']
        cap['strength'] = cap['strength'] * (1 - weight) + evidence * weight

    def can_do(self, task_requirement):
        """Check if self-model suggests capability"""
        if task_requirement not in self.capabilities:
            return None  # Unknown

        return self.capabilities[task_requirement]['strength'] > 0.7

    def known_limitations(self):
        """Return known limitations for self-awareness"""
        return [cap for cap, info in self.capabilities.items()
                if info['strength'] < 0.3]
```
