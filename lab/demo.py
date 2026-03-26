"""
Safe simulator demo script.
"""
import logging
import requests

from core.config import LabConfig
from core.safety import SafetyError, validate_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DemoRunner:
    def __init__(self, orchestrator_url: str):
        self.orchestrator_url = orchestrator_url

    def run_demo(self) -> None:
        logger.info("[*] ===== SAFE-LAB SIMULATOR DEMO =====")
        commands = [
            {"command": "ping", "agent_id": "agent-alpha", "issued_by": "demo", "role": "operator"},
            {"command": "report_status", "agent_id": "agent-alpha", "issued_by": "demo", "role": "operator"},
            {
                "command": "simulate_state_transition",
                "agent_id": "agent-alpha",
                "issued_by": "demo",
                "role": "operator",
                "args": {"state": "degraded"},
            },
            {
                "command": "replay_detection_scenario",
                "agent_id": "agent-alpha",
                "issued_by": "demo",
                "role": "operator",
                "args": {"scenario": "baseline"},
            },
        ]
        for payload in commands:
            response = requests.post(f"{self.orchestrator_url}/api/command", json=payload, timeout=5)
            response.raise_for_status()
            body = response.json()
            logger.info("[demo] command=%s correlation_id=%s", payload["command"], body.get("correlation_id"))
        logger.info("[*] Demo execution complete")


if __name__ == '__main__':
    cfg = LabConfig.from_env()
    try:
        validate_config(cfg)
    except SafetyError as exc:
        logger.error("Demo blocked by safety guardrail: %s", exc)
        raise SystemExit(2) from exc
    demo = DemoRunner(orchestrator_url=f"http://{cfg.bind_host}:{cfg.orchestrator_port}")
    demo.run_demo()
