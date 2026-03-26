from dataclasses import dataclass
from typing import Dict
import time
import requests
import psutil


@dataclass
class StructuredMetric:
    cpu: float
    memory: float
    connections: int
    response_time: float
    target_reachable: bool
    observed_at: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "cpu": self.cpu,
            "memory": self.memory,
            "connections": float(self.connections),
            "response_time": self.response_time,
            "target_reachable": 1.0 if self.target_reachable else 0.0,
            "observed_at": self.observed_at,
        }


def collect_metric(target_url: str, timeout: int = 3) -> StructuredMetric:
    start = time.time()
    target_reachable = True
    response_time = -1.0
    try:
        requests.get(target_url, timeout=timeout)
        response_time = time.time() - start
    except requests.RequestException:
        target_reachable = False
    return StructuredMetric(
        cpu=psutil.cpu_percent(interval=0.1),
        memory=psutil.virtual_memory().percent,
        connections=len(psutil.net_connections()),
        response_time=response_time,
        target_reachable=target_reachable,
        observed_at=time.time(),
    )

