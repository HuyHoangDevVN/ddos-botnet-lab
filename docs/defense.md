# Defensive Focus and Controls

## Defensive Training Goals

- Observe and reason about event orchestration.
- Build telemetry analysis workflows.
- Validate detection pipelines with replayed scenarios.

## Built-in Controls

- Safe command whitelist
- Role-based restriction (`viewer` cannot mutate simulation state)
- Kill switch (`LAB_KILL_SWITCH=true`)
- Command rate limits
- Structured audit logs with correlation IDs
- Startup config validation (fail closed)

## Recommended Monitoring

- Track `command_received`, `command_executed`, `command_rejected`, `command_failed`.
- Monitor command volume per `issued_by`.
- Alert on repeated rejected commands and kill-switch activations.
