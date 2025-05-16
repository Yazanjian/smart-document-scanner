from PIL import Image
from langchain_core.prompts import ChatPromptTemplate
from pdf2image import convert_from_bytes
from starlette.concurrency import run_in_threadpool

from app import logger
from app.logger import logger
import base64
from io import BytesIO

from app.services.nlp_service import LlmModel


# Tesseract Approach
def preprocess_image(image: Image.Image) -> str:
    """Convert image to grayscale and apply thresholding for better OCR."""
    # Convert PIL Image to bytes
    img_byte_arr = BytesIO()

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    save_format = 'JPEG'
    image.save(img_byte_arr, format=save_format)
    img_byte_arr.seek(0)
    img_byte_arr = img_byte_arr.getvalue()

    # Encode the image as base64
    base64_image = base64.b64encode(img_byte_arr).decode('utf-8')

    # Format image URL for OpenAI
    image_url = f"data:image/jpeg;base64,{base64_image}"

    return image_url


async def extract_text_from_image(image: Image.Image) -> str:
    """Extract text from an image using Tesseract OCR."""
    try:
        image_url = await run_in_threadpool(preprocess_image, image)

        llm_model = LlmModel()
        model = llm_model.vision_model

        # Create prompt template with image
        prompt = ChatPromptTemplate.from_messages([
            ("human", [
                {"type": "text",
                 "text": "Extract all text from this image. Return only the text content without any explanations."},
                {"type": "image_url", "image_url": {"url": image_url}}
            ])
        ])

        # Create chain and invoke
        chain = prompt | model
        response = await chain.ainvoke({})
        generated_text = response.content


        return generated_text

    except Exception as e:
        logger.error(e)
        return "Error. No content extracted from this image. "


async def extract_text_from_pdf(pdf_bytes: bytes) -> str | dict:
    """Convert PDF pages to images and extract text from each page."""
    pages = "This is a PDF document, extract the useful information and give a brief summarization of the pages if it is a general document. \n\n"

    images = convert_from_bytes(pdf_bytes, dpi=200, fmt="jpeg") # Higher DPI for better quality

    extracted_text = ""
    for img in images:
        text = await extract_text_from_image(img)
        extracted_text = extracted_text + text + "\n============\n"


    return pages + extracted_text
