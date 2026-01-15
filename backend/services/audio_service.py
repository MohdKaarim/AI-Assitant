
import speech_recognition as sr
import Levenshtein
import io
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_SPEECH_API_KEY")

class AudioService:
    @staticmethod
    def analyze_pronunciation(audio_bytes: bytes, reference_text: str) -> dict:
        """
        Analyzes audio pronunciation against a reference text.
        
        Args:
            audio_bytes (bytes): The raw audio data (wav/webm usually).
            reference_text (str): The text the user tried to read.
            
        Returns:
            dict: Analysis results including accuracy score and feedback.
        """
        recognizer = sr.Recognizer()
        
        # Audio data handling - SpeechRecognition likes files or specific audio sources
        # We'll write to a temp file to be safe as formats can be tricky
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            tmp_audio.write(audio_bytes)
            tmp_path = tmp_audio.name
            
        try:
            with sr.AudioFile(tmp_path) as source:
                # Listen and recognize
                audio_data = recognizer.record(source)
                try:
                    # Using Google Speech Recognition (requires internet)
                    # For offline, one would need pocketsphinx or similar
                    transcribed_text = recognizer.recognize_google(audio_data, key=GOOGLE_API_KEY)
                except sr.UnknownValueError:
                    return {
                        "score": 0,
                        "transcribed_text": "",
                        "feedback": "Could not understand the audio. Please try again."
                    }
                except sr.RequestError as e:
                     return {
                        "score": 0,
                        "transcribed_text": "",
                        "feedback": f"Speech service error: {e}"
                    }

            # Calculate similarity
            # High similarity = Good pronunciation (roughly)
            # We use Levenshtein ratio: 0 (no match) to 1 (perfect match)
            ratio = Levenshtein.ratio(reference_text.lower(), transcribed_text.lower())
            percentage = round(ratio * 100, 2)
            
            feedback = "Excellent!"
            if percentage < 90:
                feedback = "Good, but try to be more clear."
            if percentage < 70:
                feedback = "Keep practicing, some words were missed."
            if percentage < 50:
                 feedback = "Quite different. Try reading slower."

            return {
                "score": percentage,
                "transcribed_text": transcribed_text,
                "feedback": feedback
            }

        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
