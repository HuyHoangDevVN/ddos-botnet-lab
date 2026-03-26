# Network Setup (Safe Defaults)

## Default Binding Policy

- `BIND_HOST=127.0.0.1`
- All services should run on loopback by default.

## Optional Host-only Lab Network

If host-only networking is required for classroom labs:

- Add explicit subnet to `ALLOWLISTED_SUBNETS`
- Keep `SIMULATE_ONLY=true`
- Verify environment isolation before startup

## Prohibited Configuration

- Public Internet exposure
- Unbounded or wildcard network policies
