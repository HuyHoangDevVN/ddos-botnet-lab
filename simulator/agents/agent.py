from typing import Dict, List

from core.types import CommandEnvelope, SafeCommand
from orchestrator.session_registry import SessionRegistry
from simulator.telemetry.synthetic_events import heartbeat_event, status_event


class SimulatedAgent:
    def __init__(self, agent_id: str, labels: List[str], registry: SessionRegistry):
        self.agent_id = agent_id
        self.labels = labels
        self.registry = registry
        self.state = "idle"
        self.load_profile = "nominal"
        self.registry.register(agent_id, labels)

    def handle(self, envelope: CommandEnvelope) -> Dict[str, str]:
        if envelope.agent_id != self.agent_id:
            raise ValueError("agent_id mismatch")
        if envelope.command == SafeCommand.PING:
            self.registry.heartbeat(self.agent_id)
            return heartbeat_event(self.agent_id, self.state)
        if envelope.command == SafeCommand.REPORT_STATUS:
            self.registry.heartbeat(self.agent_id)
            return status_event(self.agent_id, self.state, self.load_profile)
        if envelope.command == SafeCommand.SIMULATE_STATE_TRANSITION:
            next_state = str(envelope.args.get("state", "idle"))
            if next_state not in {"idle", "observing", "degraded", "recovered"}:
                raise ValueError("Unsupported state transition.")
            self.state = next_state
            self.registry.update_state(self.agent_id, self.state, self.load_profile)
            return status_event(self.agent_id, self.state, self.load_profile)
        if envelope.command == SafeCommand.SIMULATE_LOAD_PROFILE:
            profile = str(envelope.args.get("profile", "nominal"))
            self.load_profile = profile
            self.registry.update_state(self.agent_id, self.state, self.load_profile)
            return status_event(self.agent_id, self.state, self.load_profile)
        raise ValueError("Unsupported command for simulated agent")

