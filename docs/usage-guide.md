# Usage Guide (Simulation-only)

## Command API

Endpoint: `POST /api/command`

Scenario discovery endpoints:
- `GET /api/scenarios`
- `GET /api/scenarios/<scenario_name>`

Required fields:
- `command`
- `agent_id`
- `issued_by`

Optional:
- `role` (`viewer` or `operator`)
- `args`
- `correlation_id`

## Allowed commands

- `ping`
- `report_status`
- `simulate_state_transition`
- `simulate_load_profile`
- `replay_detection_scenario`

Any other command is blocked and logged.

## Demo

Run:
- `python lab/demo.py`

This invokes only safe simulation commands and replay dataset scenarios.

## SDN Replay Examples

- `sdn_flow_anomaly`: flow-table growth and queue-delay observations
- `sdn_control_plane_stress`: controller CPU/API latency/packet-in spike markers
- `sdn_recovery_drill`: failover and recovery sequence markers
