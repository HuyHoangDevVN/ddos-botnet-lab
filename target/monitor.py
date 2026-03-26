import time
import logging
from core.config import LabConfig
from core.safety import SafetyError, validate_config
from observability.audit_logger import AuditLogger
from observability.metrics_collector import collect_metric

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerMonitor:
    def __init__(self, target_url, interval=1, audit_log_path="lab_audit.jsonl"):
        self.target_url = target_url
        self.interval = interval
        self.audit = AuditLogger(audit_log_path)
    
    def collect_metrics(self):
        return collect_metric(self.target_url).to_dict()
    
    def start_monitoring(self):
        logger.info("[*] Starting monitoring...")
        try:
            while True:
                metric = self.collect_metrics()
                print(f"CPU: {metric['cpu']:.1f}% | MEM: {metric['memory']:.1f}% | "
                      f"CONN: {int(metric['connections'])} | Response: {metric['response_time']:.2f}s")
                self.audit.log(
                    "target_metric",
                    {
                        "component": "monitor",
                        "metric": metric,
                    },
                )
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("[*] Monitoring stopped")

if __name__ == '__main__':
    cfg = LabConfig.from_env()
    try:
        validate_config(cfg)
    except SafetyError as exc:
        logger.error("Monitor startup blocked by safety guardrail: %s", exc)
        raise SystemExit(2) from exc
    monitor = ServerMonitor(f'http://{cfg.bind_host}:{cfg.target_port}', audit_log_path=cfg.audit_log_path)
    monitor.start_monitoring()
