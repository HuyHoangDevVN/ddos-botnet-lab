from flask import Flask, jsonify, request
from datetime import datetime
import logging
from core.config import LabConfig
from core.safety import SafetyError, validate_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cfg = LabConfig.from_env()

@app.route('/')
def index():
    return "Target Server - OK"

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'client_ip': request.remote_addr,
        'simulate_only': cfg.simulate_only,
    })

if __name__ == '__main__':
    try:
        validate_config(cfg)
    except SafetyError as exc:
        logger.error("Target startup blocked by safety guardrail: %s", exc)
        raise SystemExit(2) from exc
    logger.info("[*] Target server starting on %s:%s", cfg.bind_host, cfg.target_port)
    app.run(host=cfg.bind_host, port=cfg.target_port, debug=False, threaded=True)
