# Safe-Lab Simulator for Defensive Security Training

## Overview

This repository provides a simulation-only lab for defensive training and detection engineering.

It intentionally avoids offensive execution. The system focuses on:

- event orchestration
- heartbeat and status reporting
- synthetic telemetry
- replay-based detection scenarios
- target service + monitoring for observability exercises

## Safety Defaults

- `SIMULATE_ONLY=true` is mandatory.
- Services default to `127.0.0.1` binding.
- Commands are restricted to a fixed safe allowlist.
- Structured audit logs are written for all command and safety events.
- Kill switch is supported via `LAB_KILL_SWITCH=true`.

## Quickstart

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Run preflight checks:
   - `python lab/deploy.py`
3. Start orchestrator:
   - `python orchestrator/api.py`
4. (Optional) Start target service:
   - `python target/app.py`
5. Run safe demo:
   - `python lab/demo.py`
6. Start monitor:
   - `python target/monitor.py`

## Safe Command Allowlist

- `ping`
- `report_status`
- `simulate_state_transition`
- `simulate_load_profile`
- `replay_detection_scenario`

Any other command is rejected.

## SDN Scenario Pack (Safe Replay)

Available replay scenarios:

- `baseline`
- `sdn_flow_anomaly`
- `sdn_control_plane_stress`
- `sdn_recovery_drill`

Query scenarios via API:

- `GET /api/scenarios`
- `GET /api/scenarios/<scenario_name>`

## Repository Layout

- `core/`: config, schemas, safety guardrails, types
- `orchestrator/`: control plane API and command router
- `simulator/`: simulated agent and telemetry/replay components
- `observability/`: audit logging and structured metrics
- `target/`: demo target app and monitor
- `datasets/replay_scenarios/`: safe replay datasets
- `tests/`: unit/integration/safety tests
