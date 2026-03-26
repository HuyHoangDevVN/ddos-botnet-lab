from datetime import datetime, timezone
from typing import Any, Dict


SAFE_LOAD_PROFILES = {"nominal", "high_cpu", "high_memory", "network_latency"}


def heartbeat_event(agent_id: str, state: str) -> Dict[str, Any]:
    return {
        "event_type": "agent_heartbeat",
        "agent_id": agent_id,
        "state": state,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def status_event(agent_id: str, state: str, load_profile: str) -> Dict[str, Any]:
    if load_profile not in SAFE_LOAD_PROFILES:
        raise ValueError(f"Unsupported load profile: {load_profile}")
    return {
        "event_type": "agent_status",
        "agent_id": agent_id,
        "state": state,
        "load_profile": load_profile,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def replay_marker(scenario: str, step: int) -> Dict[str, Any]:
    return {
        "event_type": "scenario_replay_step",
        "scenario": scenario,
        "step": step,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

