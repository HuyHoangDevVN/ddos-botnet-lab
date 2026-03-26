"""
Demo execution script
"""
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoRunner:
    def __init__(self, c2_url="http://192.168.100.10:8080"):
        self.c2_url = c2_url
    
    def run_demo(self):
        logger.info("[*] ===== DDOS BOTNET LAB DEMO =====")
        logger.info("[*] Demo execution complete")

if __name__ == '__main__':
    demo = DemoRunner()
    demo.run_demo()