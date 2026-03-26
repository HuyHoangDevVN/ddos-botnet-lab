# Threat Model (Safe-Lab Simulator)

## Assets

- Simulator control-plane integrity
- Audit log integrity
- Safe configuration integrity

## Primary Abuse Scenarios

- Issuing non-allowlisted commands
- Misconfiguring bind host outside allowlist
- Command spam/flood against orchestrator API

## Controls

- Command schema validation + whitelist
- Role checks and rate limits
- Startup safety validation
- Kill switch
- Structured audit logs

## Residual Risks

- Misconfigured environment variables
- Insufficient operator process controls
