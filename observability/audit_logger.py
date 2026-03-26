import json
import logging
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict


class AuditLogger:
    def __init__(self, path: str):
        self.path = path
        self._lock = Lock()
        self._logger = logging.getLogger("audit")

    def log(self, event_type: str, payload: Dict[str, Any]) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            **payload,
        }
        line = json.dumps(record, sort_keys=True)
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        self._logger.info("%s", line)

