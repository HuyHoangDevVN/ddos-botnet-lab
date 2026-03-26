# Analysis Guide (Safe Simulator)

## What to Analyze

- Agent state transitions over time.
- Correlation between replay events and target metrics.
- Differences between nominal and degraded simulated profiles.
- SDN scenario behavior patterns from replay datasets.

## Suggested Questions

- Which command types are most frequent?
- Are there bursts in replay events that align with monitor metrics?
- How quickly does the simulated system recover after a degraded transition?
- For SDN scenarios, which event types indicate control-plane stress vs. recovery?

## Data Sources

- `lab_audit.jsonl` from `observability/audit_logger.py`
- monitor output from `target/monitor.py`
- replay datasets in `datasets/replay_scenarios/`

## SDN-specific Replay Scenarios

- `sdn_flow_anomaly`
- `sdn_control_plane_stress`
- `sdn_recovery_drill`
