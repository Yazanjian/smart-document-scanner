import pytesseract
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_bytes


# Tesseract Approach
def preprocess_image(image: Image.Image) -> Image.Image:
    """Convert image to grayscale and apply thresholding for better OCR."""
    open_cv_image = np.array(image.convert("RGB"))  # Convert PIL image to NumPy
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return Image.fromarray(gray)


def extract_text_from_image(image: Image.Image) -> str:
    """Extract text from an image using Tesseract OCR."""
    preprocessed_image = preprocess_image(image)
    text = pytesseract.image_to_string(preprocessed_image, config="--psm 6")
    return text


def extract_text_from_pdf(pdf_bytes: bytes) -> str | dict:
    """Convert PDF pages to images and extract text from each page."""
    pages = "This is a PDF document, extract the useful information and give a brief summarization of the pages if it is a general document. \n\n"

    images = convert_from_bytes(pdf_bytes)
    text = "\n============\n".join(extract_text_from_image(img) for img in images)

    return pages + text
