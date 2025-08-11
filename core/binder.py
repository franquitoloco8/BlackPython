from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os
import sys
from io import BytesIO
import zlib

class FileBinder:
    @staticmethod
    def bind_to_pdf(original_pdf, payload, output_pdf, debug=False):
        """
        Inyecta payload en PDF de 3 formas:
        1. Metadatos
        2. Streams de página ocultos
        3. Objetos JavaScript (opcional)
        """
        try:
            if debug:
                print("[+] Modo debug activado")
                print(f"Payload size: {len(payload)} bytes")

            # Validar archivo de entrada
            if not os.path.exists(original_pdf):
                raise FileNotFoundError(f"Archivo {original_pdf} no existe")

            # Leer PDF original
            with open(original_pdf, 'rb') as f:
                reader = PdfReader(f)
                writer = PdfWriter()

                if debug:
                    print(f"Páginas en original: {len(reader.pages)}")
                    print(f"Metadatos originales: {reader.metadata}")

                # Inyectar en cada página
                for i, page in enumerate(reader.pages):
                    # 1. Añadir contenido oculto
                    payload_stream = f"""
                    /Contents <</Length {len(payload)}>>
                    stream
                    BT /F1 1 Tf 0 0 Td ({payload}) Tj ET
                    endstream
                    """
                    page.merge_page(PdfReader(BytesIO(payload_stream.encode())).pages[0])
                    
                    # 2. Añadir como anotación invisible
                    writer.add_annotation(
                        page_number=i,
                        annotation={
                            '/Type': '/Annot',
                            '/Subtype': '/Text',
                            '/Rect': [0, 0, 0, 0],  # Invisible
                            '/Contents': payload,
                            '/NM': 'Payload',
                            '/Flags': 4  # Invisible
                        }
                    )
                    writer.add_page(page)

                # 3. Añadir en metadatos y objetos
                writer.add_metadata({
                    '/Payload': payload,
                    '/Author': 'Microsoft Office',
                    '/Creator': 'Microsoft Word'
                })

                # Comprimir payload en un objeto PDF
                compressed = zlib.compress(payload.encode())
                writer.add_object({
                    '/Type': '/EmbeddedFile',
                    '/Filter': '/FlateDecode',
                    '/Params': {'/Size': len(payload)},
                    '/Length': len(compressed)
                }, data=compressed)

                # Guardar PDF modificado
                with open(output_pdf, 'wb') as f_out:
                    writer.write(f_out)

            if debug:
                print(f"[+] PDF generado: {output_pdf}")
                print(f"Tamaño original: {os.path.getsize(original_pdf)} bytes")
                print(f"Tamaño modificado: {os.path.getsize(output_pdf)} bytes")
                print("Inyecciones realizadas:")
                print("- Payload en streams de página")
                print("- Payload en metadatos")
                print("- Payload comprimido como objeto")

        except Exception as e:
            print(f"[ERROR] {str(e)}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            raise

    @staticmethod
    def bind_to_image(original_img, payload, output_img, debug=False):
        """
        Inyecta payload en imágenes usando:
        1. LSB Steganography (RGB)
        2. Metadatos EXIF
        """
        try:
            if debug:
                print("[+] Modo debug activado para imagen")
                print(f"Payload size: {len(payload)} bytes")

            img = Image.open(original_img)
            if debug:
                print(f"Formato: {img.format}")
                print(f"Modo: {img.mode}")
                print(f"Tamaño: {img.width}x{img.height}")

            # Convertir payload a bits
            binary_payload = ''.join(format(ord(c), '08b') for c in payload)
            if debug:
                print(f"Bits a esconder: {len(binary_payload)}")

            # Inyectar en LSB (Least Significant Bit)
            pixels = img.load()
            index = 0
            modified = False

            for y in range(img.height):
                for x in range(img.width):
                    if index < len(binary_payload):
                        r, g, b = pixels[x, y][:3]
                        # Modificar solo el LSB del canal Rojo
                        r = (r & 0xFE) | int(binary_payload[index])
                        pixels[x, y] = (r, g, b) if img.mode == 'RGB' else (r, g, b, 255)
                        index += 1
                        modified = True

            if not modified:
                raise ValueError("Imagen demasiado pequeña para el payload")

            # Añadir en metadatos EXIF
            exif = img.info.get('exif', {})
            exif[0x9286] = payload  # UserComment
            img.save(output_img, exif=exif)

            if debug:
                print(f"[+] Imagen modificada guardada en: {output_img}")
                print("Técnicas aplicadas:")
                print("- LSB Steganography (canal Rojo)")
                print("- Metadatos EXIF (UserComment)")

        except Exception as e:
            print(f"[ERROR] {str(e)}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            raise

    @staticmethod
    def extract_from_pdf(pdf_path, debug=False):
        """Extrae payload de un PDF modificado"""
        # Implementación opcional para pruebas
        pass

    @staticmethod
    def extract_from_image(img_path, debug=False):
        """Extrae payload de una imagen modificada"""
        # Implementación opcional para pruebas
        pass
