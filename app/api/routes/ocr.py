from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image

from app.models.ocr import OCRResponse
from app.services.nlp_service import generate_desc_as_json
from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf, preprocess_image

router = APIRouter()


@router.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    """Extract text from uploaded image."""
    try:
        if file.content_type == "application/pdf":
            pdf_bytes = await file.read()  # Read PDF as bytes
            text = await extract_text_from_pdf(pdf_bytes) # Process PDF
            details = await generate_desc_as_json(text)
        else:
            image = Image.open(file.file)
            text = await extract_text_from_image(image)
            details = await generate_desc_as_json(text)

        ocr_response = OCRResponse(name=file.filename, document=details)
        return ocr_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
