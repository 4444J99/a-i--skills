---
name: agent-testing-patterns
description: Test AI agent systems including tool use, multi-turn conversations, error recovery, and non-deterministic outputs. Covers mock strategies, evaluation metrics, and regression testing for agent workflows. Triggers on AI agent testing, LLM evaluation, or agent quality assurance requests.
license: MIT
complexity: advanced
time_to_learn: 30min
tags:
  - agent-testing
  - llm-evaluation
  - tool-use-testing
  - non-deterministic
  - mocking
governance_phases: [prove]
governance_norm_group: quality-gate
organ_affinity: [all]
triggers: [user-asks-about-agent-testing, context:llm-testing, context:agent-evaluation, context:tool-use-testing]
complements: [testing-patterns, tdd-workflow, verification-loop, agent-swarm-orchestrator]
---

# Agent Testing Patterns

Test AI agent systems that use tools, make decisions, and produce non-deterministic outputs.

## Testing Challenges

| Challenge | Cause | Strategy |
|-----------|-------|----------|
| Non-deterministic output | LLM randomness | Assert on structure, not exact text |
| Tool use sequences | Agent autonomy | Verify tool calls, not call order |
| Multi-turn state | Conversation context | Snapshot-based assertions |
| Cost | API calls | Mock LLM in unit tests |
| Latency | API round-trips | Parallel test execution |
| Flakiness | Model updates | Semantic assertions, not string matches |

## Test Pyramid for Agents

```
        ╱╲
       ╱  ╲        E2E Agent Tests (few, expensive)
      ╱────╲       Full agent loop with real LLM
     ╱      ╲
    ╱────────╲     Integration Tests (moderate)
   ╱          ╲    Tool execution, state management
  ╱────────────╲
 ╱   Unit Tests ╲  Tool implementations, parsers, validators
╱────────────────╲
```

## Unit Testing (No LLM)

### Tool Implementation Tests

```python
import pytest

def test_file_read_tool():
    tool = FileReadTool()
    result = tool.execute({"path": "test.txt"})
    assert result["content"] == "expected content"
    assert result["success"] is True

def test_file_read_tool_missing_file():
    tool = FileReadTool()
    result = tool.execute({"path": "nonexistent.txt"})
    assert result["success"] is False
    assert "not found" in result["error"].lower()

def test_tool_input_validation():
    tool = FileReadTool()
    with pytest.raises(ValueError, match="path is required"):
        tool.execute({})
```

### Response Parser Tests

```python
def test_parse_tool_call():
    raw = '{"tool": "search", "args": {"query": "python"}}'
    result = parse_tool_call(raw)
    assert result.tool == "search"
    assert result.args == {"query": "python"}

def test_parse_malformed_tool_call():
    raw = "not json at all"
    result = parse_tool_call(raw)
    assert result is None
```

## Integration Testing (Mocked LLM)

### Mock LLM Client

```python
class MockLLMClient:
    def __init__(self, responses: list[dict]):
        self.responses = iter(responses)
        self.calls: list[dict] = []

    async def generate(self, messages: list[dict], tools: list[dict] = None) -> dict:
        self.calls.append({"messages": messages, "tools": tools})
        return next(self.responses)

@pytest.fixture
def mock_agent():
    client = MockLLMClient(responses=[
        {"content": None, "tool_calls": [{"name": "search", "args": {"query": "python packaging"}}]},
        {"content": "Based on the search results, here's how to package Python..."},
    ])
    return Agent(llm=client, tools=[SearchTool(), FileReadTool()])
```

### Tool Execution Sequence Tests

```python
@pytest.mark.asyncio
async def test_agent_uses_search_then_responds(mock_agent):
    result = await mock_agent.run("How do I package a Python project?")

    # Verify tool was called
    assert len(mock_agent.tool_history) == 1
    assert mock_agent.tool_history[0].tool_name == "search"
    assert "python" in mock_agent.tool_history[0].args["query"].lower()

    # Verify final response exists
    assert result.content is not None
    assert len(result.content) > 0
```

### State Management Tests

```python
@pytest.mark.asyncio
async def test_session_preserves_context(mock_agent):
    await mock_agent.run("My name is Alice")
    result = await mock_agent.run("What's my name?")

    # Verify conversation history maintained
    assert len(mock_agent.messages) == 4  # 2 user + 2 assistant
```

## E2E Testing (Real LLM)

### Structural Assertions

```python
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_agent_creates_file(real_agent, tmp_path):
    result = await real_agent.run(f"Create a Python hello world script at {tmp_path}/hello.py")

    # Assert on outcome, not exact content
    hello_file = tmp_path / "hello.py"
    assert hello_file.exists()
    content = hello_file.read_text()
    assert "print" in content  # Must use print
    assert content.strip()  # Non-empty

    # Verify it's valid Python
    compile(content, "hello.py", "exec")
```

### Semantic Assertions

```python
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_agent_explains_concept(real_agent):
    result = await real_agent.run("Explain what a circuit breaker pattern is in 2-3 sentences")

    # Semantic checks (not exact string matching)
    assert len(result.content) > 50
    assert len(result.content) < 1000
    assert any(term in result.content.lower() for term in ["fault", "failure", "threshold", "open", "closed"])
```

### Evaluation Metrics

```python
@dataclass
class AgentEvalResult:
    task_completed: bool
    tool_calls_count: int
    tokens_used: int
    latency_ms: float
    error_recovery_count: int

async def evaluate_agent(agent, test_cases: list[dict]) -> list[AgentEvalResult]:
    results = []
    for case in test_cases:
        start = time.perf_counter()
        try:
            result = await agent.run(case["prompt"])
            completed = case["validator"](result)
        except Exception:
            completed = False
        latency = (time.perf_counter() - start) * 1000

        results.append(AgentEvalResult(
            task_completed=completed,
            tool_calls_count=len(agent.tool_history),
            tokens_used=agent.total_tokens,
            latency_ms=latency,
            error_recovery_count=agent.error_count,
        ))
    return results
```

## Regression Testing

### Golden File Tests

```python
def test_tool_call_format_regression():
    """Ensure tool call format hasn't changed."""
    response = agent.format_tool_call("search", {"query": "test"})
    expected = load_golden("tool_call_format.json")
    assert response == expected
```

### Benchmark Suite

```python
BENCHMARK_CASES = [
    {"prompt": "List all Python files in the project", "expected_tools": ["glob"], "max_tokens": 500},
    {"prompt": "Fix the syntax error in app.py", "expected_tools": ["read", "edit"], "max_tokens": 2000},
]

async def run_benchmark(agent):
    for case in BENCHMARK_CASES:
        result = await agent.run(case["prompt"])
        tools_used = {t.tool_name for t in agent.tool_history}
        assert tools_used.issubset(set(case["expected_tools"] + ["think"]))
        assert agent.total_tokens <= case["max_tokens"]
```

## Anti-Patterns

- **Asserting exact LLM output** — Models change; assert structure and semantics
- **No mocking in unit tests** — Real API calls make tests slow, expensive, and flaky
- **Testing only happy path** — Test error recovery, malformed responses, tool failures
- **No cost tracking** — Monitor token usage in E2E tests to catch regressions
- **Ignoring non-determinism** — Run E2E tests multiple times; set pass threshold (e.g., 4/5)
- **Testing agent internals** — Test outcomes and tool call patterns, not internal state
