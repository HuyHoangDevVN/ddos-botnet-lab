from typing import Any, Dict

from core.types import CommandEnvelope, SafeCommand, new_correlation_id


def parse_command(payload: Dict[str, Any]) -> CommandEnvelope:
    if not isinstance(payload, dict):
        raise ValueError("Payload must be an object.")
    if "command" not in payload or "agent_id" not in payload or "issued_by" not in payload:
        raise ValueError("Payload missing required fields: command, agent_id, issued_by.")
    raw_command = payload["command"]
    try:
        command = SafeCommand(raw_command)
    except ValueError as exc:
        raise ValueError(f"Unsupported command: {raw_command}") from exc
    args = payload.get("args", {})
    if not isinstance(args, dict):
        raise ValueError("args must be an object.")
    correlation_id = payload.get("correlation_id")
    return CommandEnvelope(
        command=command,
        agent_id=str(payload["agent_id"]),
        issued_by=str(payload["issued_by"]),
        role=str(payload.get("role", "operator")),
        args=args,
        correlation_id=str(correlation_id) if correlation_id else new_correlation_id(),
    )

