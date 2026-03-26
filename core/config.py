import ipaddress
import os
from dataclasses import dataclass, field
from typing import List


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name, str(default)).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    return int(raw)


def _env_list(name: str, default: List[str]) -> List[str]:
    raw = os.getenv(name)
    if not raw:
        return list(default)
    return [part.strip() for part in raw.split(",") if part.strip()]


@dataclass
class LabConfig:
    simulate_only: bool = True
    dry_run: bool = False
    bind_host: str = "127.0.0.1"
    orchestrator_port: int = 8080
    target_port: int = 5000
    allowlisted_subnets: List[str] = field(default_factory=lambda: ["127.0.0.0/8"])
    max_commands_per_minute: int = 60
    max_agents: int = 25
    max_replay_events: int = 500
    audit_log_path: str = "lab_audit.jsonl"
    kill_switch: bool = False
    runtime_banner_required: bool = True
    environment_name: str = "safe-lab"

    @classmethod
    def from_env(cls) -> "LabConfig":
        return cls(
            simulate_only=_env_bool("SIMULATE_ONLY", True),
            dry_run=_env_bool("DRY_RUN", False),
            bind_host=os.getenv("BIND_HOST", "127.0.0.1"),
            orchestrator_port=_env_int("ORCHESTRATOR_PORT", 8080),
            target_port=_env_int("TARGET_PORT", 5000),
            allowlisted_subnets=_env_list("ALLOWLISTED_SUBNETS", ["127.0.0.0/8"]),
            max_commands_per_minute=_env_int("MAX_COMMANDS_PER_MINUTE", 60),
            max_agents=_env_int("MAX_AGENTS", 25),
            max_replay_events=_env_int("MAX_REPLAY_EVENTS", 500),
            audit_log_path=os.getenv("AUDIT_LOG_PATH", "lab_audit.jsonl"),
            kill_switch=_env_bool("LAB_KILL_SWITCH", False),
            runtime_banner_required=_env_bool("RUNTIME_BANNER_REQUIRED", True),
            environment_name=os.getenv("LAB_ENV_NAME", "safe-lab"),
        )

    def bind_in_allowlist(self) -> bool:
        try:
            host_ip = ipaddress.ip_address(self.bind_host)
        except ValueError:
            return False

        for subnet in self.allowlisted_subnets:
            try:
                network = ipaddress.ip_network(subnet, strict=False)
            except ValueError:
                return False
            if host_ip in network:
                return True
        return False

