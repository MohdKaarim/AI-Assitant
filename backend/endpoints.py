
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.services.ocr_service import OCRService
from backend.services.audio_service import AudioService

router = APIRouter()

@router.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...), lang: str = Form("eng")):
    """
    Receives an image file and returns the extracted text.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    try:
        content = await file.read()
        text = OCRService.extract_text(content, lang=lang)
        return {"extracted_text": text, "language": lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_endpoint(
    audio: UploadFile = File(...), 
    reference_text: str = Form(...)
):
    """
    Receives an audio file and reference text.
    Returns pronunciation score and feedback.
    """
    try:
        content = await audio.read()
        # Ensure we have some text to compare against
        if not reference_text.strip():
             raise HTTPException(status_code=400, detail="Reference text cannot be empty.")
             
        result = AudioService.analyze_pronunciation(content, reference_text)
        return result
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
