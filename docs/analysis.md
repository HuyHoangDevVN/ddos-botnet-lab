# Analysis Guide (Safe Simulator)

## What to Analyze

- Agent state transitions over time.
- Correlation between replay events and target metrics.
- Differences between nominal and degraded simulated profiles.

## Suggested Questions

- Which command types are most frequent?
- Are there bursts in replay events that align with monitor metrics?
- How quickly does the simulated system recover after a degraded transition?

## Data Sources

- `lab_audit.jsonl` from `observability/audit_logger.py`
- monitor output from `target/monitor.py`
- replay datasets in `datasets/replay_scenarios/`
