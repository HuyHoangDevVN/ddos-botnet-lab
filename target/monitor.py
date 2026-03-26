import requests
import time
import psutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerMonitor:
    def __init__(self, target_url, interval=1):
        self.target_url = target_url
        self.interval = interval
    
    def collect_metrics(self):
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        connections = len(psutil.net_connections())
        
        response_time = None
        try:
            start = time.time()
            r = requests.get(self.target_url, timeout=5)
            response_time = time.time() - start
        except:
            response_time = -1
        
        return {
            'cpu': cpu,
            'memory': memory,
            'connections': connections,
            'response_time': response_time
        }
    
    def start_monitoring(self):
        logger.info("[*] Starting monitoring...")
        try:
            while True:
                metric = self.collect_metrics()
                print(f"CPU: {metric['cpu']:.1f}% | MEM: {metric['memory']:.1f}% | "
                      f"CONN: {metric['connections']} | Response: {metric['response_time']:.2f}s")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("[*] Monitoring stopped")

if __name__ == '__main__':
    monitor = ServerMonitor('http://192.168.100.30:5000')
    monitor.start_monitoring()