from dataclasses import asdict
from datetime import datetime, timezone
from threading import Lock
from typing import Dict, List

from core.types import AgentStatus


class SessionRegistry:
    def __init__(self, max_agents: int):
        self._max_agents = max_agents
        self._lock = Lock()
        self._agents: Dict[str, AgentStatus] = {}

    def register(self, agent_id: str, labels: List[str]) -> AgentStatus:
        now = datetime.now(timezone.utc).isoformat()
        with self._lock:
            if agent_id not in self._agents and len(self._agents) >= self._max_agents:
                raise ValueError("Agent capacity exceeded.")
            status = self._agents.get(agent_id) or AgentStatus(
                agent_id=agent_id,
                state="idle",
                last_heartbeat=now,
                labels=labels,
            )
            status.last_heartbeat = now
            self._agents[agent_id] = status
            return status

    def heartbeat(self, agent_id: str) -> AgentStatus:
        with self._lock:
            if agent_id not in self._agents:
                raise KeyError(f"Unknown agent_id: {agent_id}")
            agent = self._agents[agent_id]
            agent.last_heartbeat = datetime.now(timezone.utc).isoformat()
            return agent

    def update_state(self, agent_id: str, state: str, load_profile: str) -> AgentStatus:
        with self._lock:
            if agent_id not in self._agents:
                raise KeyError(f"Unknown agent_id: {agent_id}")
            agent = self._agents[agent_id]
            agent.state = state
            agent.load_profile = load_profile
            agent.last_heartbeat = datetime.now(timezone.utc).isoformat()
            return agent

    def list_status(self) -> Dict[str, Dict[str, str]]:
        with self._lock:
            return {agent_id: asdict(status) for agent_id, status in self._agents.items()}

