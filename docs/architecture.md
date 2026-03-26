# Safe-Lab Simulator Architecture

## Purpose

This project is a simulation-only defensive lab platform. It does not execute offensive actions.

## High-level Components

- `orchestrator/api.py`: control-plane HTTP API with command validation and safety checks.
- `orchestrator/command_router.py`: whitelist enforcement, role checks, rate limiting, command routing.
- `orchestrator/session_registry.py`: thread-safe registry for simulated agents.
- `simulator/agents/agent.py`: stateful simulated agents (heartbeat/status/state transitions).
- `simulator/telemetry/replay_engine.py`: replay of safe, synthetic scenario datasets.
- `observability/audit_logger.py`: structured JSON audit logs.
- `target/app.py`: target application for observability demo.
- `target/monitor.py`: structured metrics collector.
- `core/config.py` + `core/safety.py`: secure-by-default configuration and startup guardrails.

## Trust Boundaries

- Operator/API caller -> Orchestrator API (validated payloads only).
- Orchestrator -> Simulated agents (safe command enum only).
- Replay engine -> Synthetic dataset files (local, controlled format).
- Monitor -> Target endpoint (local host or allowlisted subnet only).

## Safety-by-design Guardrails

- Simulation-only mode is mandatory.
- Localhost binding by default.
- Fixed command allowlist.
- Structured audit logging for accepted/rejected commands.
- Kill switch and rate limits.
