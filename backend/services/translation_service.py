from deep_translator import GoogleTranslator

# Custom mapping for Arabic to Romanized English (Simple Transliteration)
# This is designed for readability/learning, not strict academic transliteration.
ARABIC_TO_ROMAN = {
    'ء': "'", 'ا': "a", 'أ': "a", 'إ': "i", 'آ': "aa",
    'ب': "b", 'ت': "t", 'ث': "th", 'ج': "j", 'ح': "H", 'خ': "kh",
    'د': "d", 'ذ': "dh", 'ر': "r", 'ز': "z", 'س': "s", 'ش': "sh",
    'ص': "S", 'ض': "D", 'ط': "T", 'ظ': "Z", 'ع': "'", 'غ': "gh",
    'ف': "f", 'ق': "q", 'ك': "k", 'ل': "l", 'م': "m", 'ن': "n",
    'ه': "h", 'و': "w", 'ي': "y", 'ة': "h", 'ى': "a",
    # Vowels/Diacritics
    'َ': "a", 'ُ': "u", 'ِ': "i",
    'ً': "an", 'ٌ': "un", 'ٍ': "in",
    'ّ': "", # Shadda handled by logic ideally, but simplified here
    'ْ': ""
}

def translate_to_english(text: str) -> str:
    """
    Translates Arabic text to English using Google Translate.
    """
    try:
        translator = GoogleTranslator(source='auto', target='en')
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return "Transformation unavailable"

def transliterate_arabic(text: str) -> str:
    """
    Converts Arabic script to Romanized English (Readable Transliteration).
    """
    result = []
    for char in text:
        result.append(ARABIC_TO_ROMAN.get(char, char))
    
    # Simple post-processing to clean up
    transliterated = "".join(result)
    return transliterated
