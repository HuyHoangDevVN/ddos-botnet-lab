# Operator Guide

## Roles

- `viewer`: read-only commands (`ping`, `report_status`)
- `operator`: can run all safe simulation commands

## API workflow

1. Check health: `GET /api/health`
2. List agents: `GET /api/agents`
3. Issue safe command: `POST /api/command`

## Operational Practices

- Track correlation IDs for each exercise.
- Review `lab_audit.jsonl` after every run.
- Enable kill switch immediately if unexpected behavior appears.
