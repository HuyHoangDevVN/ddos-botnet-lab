from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# Route for the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Socket communication
class C2Server:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def start(self):
        print(f'Server listening on {self.host}:{self.port}')
        while True:
            client, addr = self.socket.accept()
            print(f'Connection from {addr}')

if __name__ == '__main__':
    c2_server = C2Server()
    app.run(debug=True)
    c2_server.start()