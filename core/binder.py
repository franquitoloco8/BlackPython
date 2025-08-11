from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os
import sys

class FileBinder:
    @staticmethod
    def bind_to_pdf(original_pdf, payload, output_pdf, debug=False):
        try:
            if debug:
                print(f"[DEBUG] Iniciando bind_to_pdf")
                print(f" - Archivo original: {original_pdf}")
                print(f" - Tamaño payload: {len(payload)} bytes")

            # Validar archivo PDF
            if not os.path.exists(original_pdf):
                raise FileNotFoundError(f"Archivo {original_pdf} no existe")

            # Leer PDF original
            with open(original_pdf, 'rb') as f:
                reader = PdfReader(f)
                if len(reader.pages) == 0:
                    raise ValueError("PDF no contiene páginas")

                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                # Insertar payload en metadatos y texto invisible
                metadata = reader.metadata or {}
                metadata.update({
                    "/Payload": payload,
                    "/Creator": "Microsoft Office Word",
                    "/Producer": "Microsoft® Word para Microsoft 365"
                })
                writer.add_metadata(metadata)

                # Escribir PDF modificado
                with open(output_pdf, 'wb') as f_out:
                    writer.write(f_out)

            if debug:
                print(f"[DEBUG] PDF generado exitosamente en {output_pdf}")
                print(f" - Tamaño original: {os.path.getsize(original_pdf)} bytes")
                print(f" - Tamaño nuevo: {os.path.getsize(output_pdf)} bytes")

        except Exception as e:
            print(f"[ERROR PDF] {str(e)}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            raise

    @staticmethod
    def bind_to_image(original_img, payload, output_img, debug=False):
        try:
            if debug:
                print(f"[DEBUG] Iniciando bind_to_image")
                print(f" - Archivo original: {original_img}")

            img = Image.open(original_img)
            if debug:
                print(f" - Modo: {img.mode}")
                print(f" - Tamaño: {img.width}x{img.height}")

            # Convertir payload a bits
            binary_payload = ''.join(format(ord(c), '08b') for c in payload)
            if debug:
                print(f" - Tamaño payload (bits): {len(binary_payload)}")

            pixels = img.load()
            index = 0
            modified = False

            for i in range(img.width):
                for j in range(img.height):
                    if index < len(binary_payload):
                        r, g, b = pixels[i, j][:3]  # Para imágenes RGBA
                        r = (r & 0xFE) | int(binary_payload[index])
                        pixels[i, j] = (r, g, b) if img.mode == 'RGB' else (r, g, b, 255)
                        index += 1
                        modified = True

            if not modified:
                raise ValueError("Imagen demasiado pequeña para el payload")

            img.save(output_img)
            if debug:
                print(f"[DEBUG] Imagen modificada guardada en {output_img}")

        except Exception as e:
            print(f"[ERROR IMG] {str(e)}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            raise
