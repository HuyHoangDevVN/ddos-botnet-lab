# FAQ

## Why are some commands rejected?

Only the safe command whitelist is supported. Unknown commands are blocked and audited.

## Why does startup fail with a safety error?

Startup fails closed when configuration violates guardrails (for example: non-allowlisted bind host or disabled simulation mode).

## How do I stop all command execution quickly?

Set `LAB_KILL_SWITCH=true` and restart the orchestrator.

## Where are logs written?

By default, structured audit logs are written to `lab_audit.jsonl`.
