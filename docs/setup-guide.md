# Setup Guide (Safe-Lab Simulator)

## Prerequisites

- Python 3.10+ recommended
- Install dependencies:
  - `pip install -r requirements.txt`

## Required Safety Defaults

- `SIMULATE_ONLY=true`
- `BIND_HOST=127.0.0.1`
- `ALLOWLISTED_SUBNETS=127.0.0.0/8`

## Startup

1. Run preflight:
   - `python lab/deploy.py`
2. Start orchestrator:
   - `python orchestrator/api.py`
3. Start target:
   - `python target/app.py`
4. Start monitor:
   - `python target/monitor.py`

If preflight fails, fix configuration before proceeding.
