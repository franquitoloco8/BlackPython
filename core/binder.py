from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

class FileBinder:
    @staticmethod
    def bind_to_pdf(original_pdf, payload, output_pdf):
        writer = PdfWriter()
        reader = PdfReader(original_pdf)
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({"/Payload": payload})
        with open(output_pdf, "wb") as f:
            writer.write(f)

    @staticmethod
    def bind_to_image(original_img, payload, output_img):
        img = Image.open(original_img)
        binary_payload = ''.join(format(ord(c), '08b') for c in payload)
        pixels = img.load()
        index = 0
        for i in range(img.width):
            for j in range(img.height):
                if index < len(binary_payload):
                    r, g, b = pixels[i, j]
                    r = (r & 0xFE) | int(binary_payload[index])
                    pixels[i, j] = (r, g, b)
                    index += 1
        img.save(output_img)
