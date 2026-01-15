from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import pytesseract
from PIL import Image
import speech_recognition as sr

# Optional: python-levenshtein for better string matching
try:
    import difflib
except ImportError:
    difflib = None

# Configure Tesseract path for Windows
import platform
if platform.system() == 'Windows':
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Users\Dell\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:4200",  # Angular default port
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpeechAnalysisRequest(BaseModel):
    reference_text: str

@app.get("/")
def read_root():
    return {"message": "AI Language Tutor API is running"}

@app.post("/api/ocr")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Create temp file
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Open image and perform OCR
        # Note: Tesseract must be installed on the system
        # configuration for multiple languages: English, Arabic, Tamil
        try:
             text = pytesseract.image_to_string(Image.open(temp_file), lang='eng+ara+tam')
        except pytesseract.TesseractError as e:
             # Fallback or error handling if languages are missing
             print(f"Tesseract Error: {e}")
             text = pytesseract.image_to_string(Image.open(temp_file)) # Fallback to default (eng)

        os.remove(temp_file)
        
        return {"extracted_text": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ... imports ...
from services import tajweed_service, translation_service, quran_service

# ... existing code ...

@app.get("/api/surahs")
async def get_surahs():
    """
    Get list of all surahs with metadata.
    """
    try:
        surahs = quran_service.get_all_surahs()
        return {"surahs": surahs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/surah/{surah_number}")
async def get_surah(surah_number: int):
    """
    Get all verses for a specific surah.
    """
    try:
        surah_data = quran_service.get_surah_verses(surah_number)
        if not surah_data:
            raise HTTPException(status_code=404, detail="Surah not found")
        return surah_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_speech(audio: UploadFile = File(...), reference_text: str = Form("")):
    try:
        # Save audio file temporarily
        temp_audio = f"temp_{audio.filename}"
        with open(temp_audio, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
            
        recognizer = sr.Recognizer()
        
        # Load audio file
        # Convert to compatible format if necessary (wav is best for sr)
        with sr.AudioFile(temp_audio) as source:
            audio_data = recognizer.record(source)
            
        try:
            # Recognize speech using Google Web Speech API
            # Ideally try to detect language or use a generic one, or loop through expected
            spoken_text = recognizer.recognize_google(audio_data, language="ar-SA") # Try Arabic first, or default
        except sr.UnknownValueError:
            spoken_text = ""
        except sr.RequestError as e:
            # Fallback to English/default if Arabic fails or just report error
            try:
                 spoken_text = recognizer.recognize_google(audio_data)
            except:
                 spoken_text = ""
            
        os.remove(temp_audio)
        
        # Calculate match score using normalized text
        match_score = 0.0
        if difflib and spoken_text:
             norm_ref = tajweed_service.normalize_arabic(reference_text)
             norm_spoken = tajweed_service.normalize_arabic(spoken_text)
             match_score = difflib.SequenceMatcher(None, norm_ref, norm_spoken).ratio()
        
        # Word-level analysis
        word_accuracies = tajweed_service.analyze_word_level(reference_text, spoken_text)
        
        # Tajweed Analysis
        expected_ipa = tajweed_service.get_ipa_transcription(reference_text)
        spoken_ipa = tajweed_service.get_ipa_transcription(spoken_text)
        tajweed_errors = tajweed_service.analyze_tajweed_errors(reference_text, spoken_text)

        return {
            "spoken_text": spoken_text,
            "reference_text": reference_text,
            "match_score": match_score,
            "word_accuracies": word_accuracies,
            "ipa_transcription": {
                "expected": expected_ipa,
                "spoken": spoken_ipa
            },
            "tajweed_errors": tajweed_errors
        }

    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/translate")
async def translate_text_endpoint(text: str = Form(...)):
    """
    Endpoint to translate and transliterate Arabic text.
    """
    try:
        translation = translation_service.translate_to_english(text)
        transliteration = translation_service.transliterate_arabic(text)
        
        return {
            "original": text,
            "translation": translation,
            "transliteration": transliteration
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
