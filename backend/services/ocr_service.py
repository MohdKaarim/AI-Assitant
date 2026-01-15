
import pytesseract
from PIL import Image
import io

class OCRService:
    @staticmethod
    def extract_text(image_bytes: bytes, lang: str = 'eng') -> str:
        """
        Extracts text from an image using Tesseract OCR.
        
        Args:
            image_bytes (bytes): The raw image data.
            lang (str): Language code (e.g., 'eng', 'ara', 'tam').
            
        Returns:
            str: The extracted text.
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            # pytesseract requires Tesseract-OCR binary to be installed and in PATH
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            print(f"Error in OCR extraction: {e}")
            raise e
