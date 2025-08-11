import subprocess
import sys

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[+] Dependencias instaladas correctamente.")
    except Exception as e:
        print(f"[-] Error: {e}")
