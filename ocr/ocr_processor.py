import pytesseract

from PIL import Image
from pdf2image import convert_from_bytes
from io import BytesIO


def extract_text_from_image(image):

    text = pytesseract.image_to_string(image)

    return text


def extract_text_from_scanned_pdf(pdf_bytes):

    pages = convert_from_bytes(pdf_bytes)

    full_text = ""

    for page in pages:

        text = pytesseract.image_to_string(page)

        full_text += text + "\n"

    return full_text