# Usage Guide (Simulation-only)

## Command API

Endpoint: `POST /api/command`

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
