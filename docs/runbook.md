# Runbook

## Startup

1. `python lab/deploy.py`
2. `python orchestrator/api.py`
3. `python target/app.py`
4. `python target/monitor.py`

## Health Checks

- `GET /api/health` returns `status=ok`
- `GET /api/agents` returns seeded agents
- Audit log file receives structured events

## Shutdown

- Stop services gracefully (Ctrl+C in each process)
- Archive `lab_audit.jsonl` for analysis
