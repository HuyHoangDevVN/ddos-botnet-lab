# Incident Stop Procedure

## Immediate Containment

1. Set `LAB_KILL_SWITCH=true`
2. Restart orchestrator
3. Verify command API returns kill-switch block responses

## Follow-up

- Preserve `lab_audit.jsonl`
- Capture environment configuration used
- Review rejected/failed command events
- Reset to known-safe defaults before next run
