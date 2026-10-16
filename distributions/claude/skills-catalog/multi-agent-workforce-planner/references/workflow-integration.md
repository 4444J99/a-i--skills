# Workflow Integration

How to integrate multi-agent workforce planning into development workflows.

## Integration Points

### With Product Requirements

```yaml
workflow:
  input: Product Requirements Document (PRD)

  steps:
    - name: "Extract features from PRD"
      tool: product-requirements-designer
      output: feature_list.yaml

    - name: "Create workstream plan"
      tool: multi-agent-workforce-planner
      input: feature_list.yaml
      output: workstream_plan.yaml

    - name: "Execute workstreams"
      tool: agent_orchestrator
      input: workstream_plan.yaml
```

### With Project Manifests

```yaml
integration:
  manifest_file: manifest.yaml

  on_task_complete:
    - update_manifest_thread
    - record_files_created
    - add_relations

  on_workstream_complete:
    - close_thread
    - summarize_accomplishments
```

### With Version Control

```yaml
git_integration:
  branch_strategy: feature_branches

  workstream_mapping:
    - workstream: "Backend API"
      branch: "feature/api-endpoints"

    - workstream: "Frontend UI"
      branch: "feature/ui-components"

  merge_strategy:
    - complete workstream
    - run tests
    - create pull request
    - merge to develop
```

## Execution Orchestration

### Sequential Execution

```yaml
execution:
  mode: sequential

  phases:
    - phase: 1
      tasks: [T1]
      wait: completion

    - phase: 2
      tasks: [T2, T3]
      wait: all_complete

    - phase: 3
      tasks: [T4]
```

### Parallel Execution

```yaml
execution:
  mode: parallel
  max_concurrent: 4

  workstreams:
    - name: "WS-A"
      agent_pool: [agent-1, agent-2]

    - name: "WS-B"
      agent_pool: [agent-3, agent-4]
```

### Hybrid Execution

```yaml
execution:
  mode: hybrid

  phases:
    - name: "Design"
      mode: sequential
      tasks: [D1, D2]

    - name: "Implementation"
      mode: parallel
      tasks: [I1, I2, I3, I4]

    - name: "Integration"
      mode: sequential
      tasks: [T1, T2]
```

## Progress Reporting

### Dashboard Format

```
╔══════════════════════════════════════════════════════════════════╗
║ Multi-Agent Workstream Dashboard                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║ Overall Progress: [████████████░░░░░░░░] 60%                     ║
║                                                                   ║
║ ┌─────────────────────────────────────────────────────────────┐ ║
║ │ Workstream A: Backend API                                    │ ║
║ │ [████████████████████] 100% ✓                               │ ║
║ │ Agent: Edit-1 | Tasks: 5/5 | Duration: 45m                  │ ║
║ └─────────────────────────────────────────────────────────────┘ ║
║                                                                   ║
║ ┌─────────────────────────────────────────────────────────────┐ ║
║ │ Workstream B: Frontend UI                                    │ ║
║ │ [████████████░░░░░░░░] 60%                                  │ ║
║ │ Agent: Edit-2 | Tasks: 3/5 | ETA: 20m                       │ ║
║ │ Current: Implementing form validation                        │ ║
║ └─────────────────────────────────────────────────────────────┘ ║
║                                                                   ║
║ ┌─────────────────────────────────────────────────────────────┐ ║
║ │ Workstream C: Integration                                    │ ║
║ │ [░░░░░░░░░░░░░░░░░░░░] 0% ⏳                                │ ║
║ │ Status: Blocked by B                                         │ ║
║ └─────────────────────────────────────────────────────────────┘ ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

### Metrics Tracking

```yaml
metrics:
  - name: throughput
    description: "Tasks completed per hour"
    current: 4.5

  - name: parallelization_efficiency
    description: "Actual vs theoretical parallel speedup"
    current: 0.75  # 75% efficient

  - name: failure_rate
    description: "Tasks requiring retry or intervention"
    current: 0.08  # 8%

  - name: blocked_time
    description: "Time tasks spent waiting on dependencies"
    current: 15min
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/multi-agent-build.yml
name: Multi-Agent Build

on: [push, pull_request]

jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      workstreams: ${{ steps.plan.outputs.workstreams }}
    steps:
      - uses: actions/checkout@v4
      - id: plan
        run: |
          python scripts/create_workstream_plan.py
          echo "workstreams=$(cat workstream_plan.json)" >> $GITHUB_OUTPUT

  execute:
    needs: plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        workstream: ${{ fromJson(needs.plan.outputs.workstreams) }}
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/execute_workstream.py ${{ matrix.workstream }}

  integrate:
    needs: execute
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/integration_tests.py
```

### Progress Webhook

```yaml
webhooks:
  - event: task_complete
    url: https://api.example.com/progress
    payload:
      task_id: "{{task.id}}"
      status: "{{task.status}}"
      duration: "{{task.duration}}"

  - event: workstream_complete
    url: https://api.example.com/progress
    payload:
      workstream_id: "{{workstream.id}}"
      tasks_completed: "{{workstream.completed}}"
      total_duration: "{{workstream.duration}}"
```

## Monitoring and Alerting

### Health Checks

```yaml
health_checks:
  - name: agent_heartbeat
    interval: 30s
    timeout: 10s
    action_on_failure: reassign_tasks

  - name: progress_stall
    condition: no_progress_for > 10min
    action: alert_supervisor

  - name: error_rate
    threshold: 0.15
    window: 5min
    action: pause_and_investigate
```

### Alert Configuration

```yaml
alerts:
  channels:
    - type: slack
      webhook: ${SLACK_WEBHOOK}
      events: [failure, stall, completion]

    - type: email
      recipients: [team@example.com]
      events: [critical_failure]

  thresholds:
    task_failure: notify_after_3
    workstream_stall: notify_after_15min
    completion: always_notify
```

## Reporting

### Summary Report Template

```markdown
# Workstream Execution Report

**Feature:** {{feature_name}}
**Started:** {{start_time}}
**Completed:** {{end_time}}
**Duration:** {{total_duration}}

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | {{total_tasks}} |
| Completed | {{completed_tasks}} |
| Failed | {{failed_tasks}} |
| Skipped | {{skipped_tasks}} |
| Parallelization | {{parallel_efficiency}}% |

## Workstream Details

{{#workstreams}}
### {{name}}

- **Agent:** {{agent}}
- **Tasks:** {{completed}}/{{total}}
- **Duration:** {{duration}}
- **Status:** {{status}}

{{/workstreams}}

## Issues Encountered

{{#issues}}
- **{{task_id}}:** {{description}}
  - Resolution: {{resolution}}
{{/issues}}

## Artifacts Created

{{#artifacts}}
- `{{path}}` - {{description}}
{{/artifacts}}
```

### Retrospective Data

```yaml
retrospective:
  what_went_well:
    - "Parallel implementation saved 40% time"
    - "Interface-first approach prevented integration issues"

  what_could_improve:
    - "More granular checkpoints needed"
    - "Better failure detection for edge cases"

  action_items:
    - "Add checkpoint after each phase"
    - "Improve test coverage for error paths"

  metrics_comparison:
    planned_duration: 4h
    actual_duration: 3.5h
    efficiency: 114%
```
