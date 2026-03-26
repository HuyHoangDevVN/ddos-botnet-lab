from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
import uuid


class SafeCommand(str, Enum):
    PING = "ping"
    REPORT_STATUS = "report_status"
    SIMULATE_STATE_TRANSITION = "simulate_state_transition"
    SIMULATE_LOAD_PROFILE = "simulate_load_profile"
    REPLAY_DETECTION_SCENARIO = "replay_detection_scenario"


def new_correlation_id() -> str:
    return str(uuid.uuid4())


@dataclass
class CommandEnvelope:
    command: SafeCommand
    agent_id: str
    issued_by: str
    role: str = "operator"
    args: Dict[str, Any] = field(default_factory=dict)
    correlation_id: str = field(default_factory=new_correlation_id)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class AgentStatus:
    agent_id: str
    state: str
    last_heartbeat: str
    load_profile: str = "nominal"
    labels: List[str] = field(default_factory=list)

