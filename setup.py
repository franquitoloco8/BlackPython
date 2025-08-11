import os
import subprocess
from utils.installer import install_dependencies

def setup():
    if not os.path.exists(".env"):
        os.system("python -m venv .env")
    install_dependencies()
    if os.name == "posix":
        subprocess.run(["chmod", "+x", "android/build.sh"])
    print("[+] BlackPython instalado correctamente.")

if __name__ == "__main__":
    setup()
