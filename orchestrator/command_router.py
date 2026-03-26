from collections import defaultdict, deque
from time import time
from typing import Deque, Dict, List

from core.config import LabConfig
from core.types import CommandEnvelope, SafeCommand
from observability.audit_logger import AuditLogger
from simulator.agents.agent import SimulatedAgent
from simulator.telemetry.replay_engine import ReplayEngine


class CommandRouter:
    def __init__(
        self,
        config: LabConfig,
        audit: AuditLogger,
        agents: Dict[str, SimulatedAgent],
        replay_engine: ReplayEngine,
    ):
        self._config = config
        self._audit = audit
        self._agents = agents
        self._replay_engine = replay_engine
        self._issued_timestamps: Dict[str, Deque[float]] = defaultdict(deque)

    def _enforce_role(self, envelope: CommandEnvelope) -> None:
        if envelope.role not in {"viewer", "operator"}:
            raise PermissionError("Unknown role.")
        if envelope.role == "viewer":
            if envelope.command not in {SafeCommand.PING, SafeCommand.REPORT_STATUS}:
                raise PermissionError("Viewer role cannot issue state mutation commands.")

    def _enforce_rate_limit(self, issued_by: str) -> None:
        now = time()
        queue = self._issued_timestamps[issued_by]
        while queue and now - queue[0] > 60:
            queue.popleft()
        if len(queue) >= self._config.max_commands_per_minute:
            raise RuntimeError("Rate limit exceeded.")
        queue.append(now)

    def route(self, envelope: CommandEnvelope) -> List[dict]:
        if self._config.kill_switch:
            raise RuntimeError("Kill switch active.")
        self._enforce_role(envelope)
        self._enforce_rate_limit(envelope.issued_by)

        self._audit.log(
            "command_received",
            {
                "command": envelope.command.value,
                "agent_id": envelope.agent_id,
                "issued_by": envelope.issued_by,
                "role": envelope.role,
                "correlation_id": envelope.correlation_id,
                "simulate_only": self._config.simulate_only,
            },
        )

        if envelope.command == SafeCommand.REPLAY_DETECTION_SCENARIO:
            scenario = str(envelope.args.get("scenario", "baseline"))
            events = self._replay_engine.replay(
                scenario=scenario,
                audit=self._audit,
                correlation_id=envelope.correlation_id,
            )
            self._audit.log(
                "command_executed",
                {
                    "command": envelope.command.value,
                    "result": "ok",
                    "event_count": len(events),
                    "correlation_id": envelope.correlation_id,
                },
            )
            return events

        agent = self._agents.get(envelope.agent_id)
        if not agent:
            raise KeyError(f"Unknown agent_id: {envelope.agent_id}")
        event = agent.handle(envelope)
        self._audit.log(
            "command_executed",
            {
                "command": envelope.command.value,
                "result": "ok",
                "correlation_id": envelope.correlation_id,
                "agent_id": envelope.agent_id,
            },
        )
        return [event]

