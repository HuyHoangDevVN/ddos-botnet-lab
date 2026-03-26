# Operator Guide

## Roles

- `viewer`: read-only commands (`ping`, `report_status`)
- `operator`: can run all safe simulation commands

## API workflow

1. Check health: `GET /api/health`
2. List agents: `GET /api/agents`
3. List scenarios: `GET /api/scenarios`
4. Inspect scenario metadata: `GET /api/scenarios/<scenario_name>`
5. Issue safe command: `POST /api/command`

## Operational Practices

- Track correlation IDs for each exercise.
- Review `lab_audit.jsonl` after every run.
- Enable kill switch immediately if unexpected behavior appears.

## SDN scenario operation tips

- Start with `sdn_flow_anomaly`, then `sdn_control_plane_stress`, and end with `sdn_recovery_drill`.
- Validate expected event sequence from `datasets/replay_scenarios/catalog.json`.
