from typing import Dict
import logging

from flask import Flask, jsonify, request

from core.config import LabConfig
from core.safety import SafetyError, consent_banner, validate_config
from core.schemas import parse_command
from observability.audit_logger import AuditLogger
from orchestrator.command_router import CommandRouter
from orchestrator.session_registry import SessionRegistry
from simulator.agents.agent import SimulatedAgent
from simulator.telemetry.replay_engine import ReplayEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config: LabConfig | None = None) -> Flask:
    config = config or LabConfig.from_env()
    validate_config(config)

    if config.runtime_banner_required:
        logger.warning("\n%s\n", consent_banner())

    app = Flask(__name__)
    audit = AuditLogger(config.audit_log_path)
    registry = SessionRegistry(config.max_agents)
    agents: Dict[str, SimulatedAgent] = {
        "agent-alpha": SimulatedAgent("agent-alpha", ["linux", "training"], registry),
        "agent-beta": SimulatedAgent("agent-beta", ["windows", "training"], registry),
    }
    replay_engine = ReplayEngine(dataset_dir="datasets/replay_scenarios", max_events=config.max_replay_events)
    router = CommandRouter(config=config, audit=audit, agents=agents, replay_engine=replay_engine)

    @app.route("/")
    def index():
        return "Safe-Lab Orchestrator"

    @app.route("/api/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "simulate_only": config.simulate_only,
                "environment": config.environment_name,
            }
        )

    @app.route("/api/agents")
    def list_agents():
        return jsonify(registry.list_status())

    @app.route("/api/command", methods=["POST"])
    def issue_command():
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"status": "error", "error": "Invalid JSON payload"}), 400
        try:
            envelope = parse_command(payload)
            events = router.route(envelope)
            return jsonify({"status": "ok", "events": events, "correlation_id": envelope.correlation_id})
        except (ValueError, PermissionError) as exc:
            audit.log(
                "command_rejected",
                {
                    "reason": str(exc),
                    "payload": payload,
                },
            )
            return jsonify({"status": "error", "error": str(exc)}), 400
        except (RuntimeError, KeyError, FileNotFoundError) as exc:
            audit.log(
                "command_failed",
                {
                    "reason": str(exc),
                    "payload": payload,
                },
            )
            return jsonify({"status": "error", "error": str(exc)}), 409

    return app


if __name__ == "__main__":
    cfg = LabConfig.from_env()
    try:
        application = create_app(cfg)
    except SafetyError as exc:
        logger.error("Startup blocked by safety guardrail: %s", exc)
        raise SystemExit(2) from exc
    logger.info("Starting safe-lab orchestrator on %s:%s", cfg.bind_host, cfg.orchestrator_port)
    application.run(host=cfg.bind_host, port=cfg.orchestrator_port, debug=False)

