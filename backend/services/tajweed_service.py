import re

# Arabic to IPA Mapping for Quranic Pronunciation
ARABIC_TO_IPA = {
    'ء': 'ʔ',
    'ا': 'aː',
    'ب': 'b',
    'ت': 't',
    'ث': 'θ',
    'ج': 'dʒ',
    'ح': 'ħ',
    'خ': 'x',
    'د': 'd',
    'ذ': 'ð',
    'ر': 'r',
    'ز': 'z',
    'س': 's',
    'ش': 'ʃ',
    'ص': 'sˤ',
    'ض': 'dˤ',
    'ط': 'tˤ',
    'ظ': 'ðˤ',
    'ع': 'ʕ',
    'غ': 'ɣ',
    'ف': 'f',
    'ق': 'q',
    'ك': 'k',
    'ل': 'l',
    'm': 'm',
    'ن': 'n',
    'ه': 'h',
    'و': 'w',
    'ي': 'j',
    # Short vowels (Harokat) - simplified
    'َ': 'a',
    'ُ': 'u',
    'ِ': 'i',
    'ً': 'an',
    'ٌ': 'un',
    'ٍ': 'in',
    'ّ': 'ː', # Shadda (gemination)
    'ْ': '',  # Sukun (no vowel)
}

# Common Tajweed Error Mappings
TAJWEED_ERRORS = {
    'qalqalah_missing': {
        'code': 'TJ001',
        'title': 'Missing Qalqalah',
        'description': 'Make sure to bounce on the letters (ق ط ب ج د) when they have a Sukun.',
        'severity': 'medium'
    },
    'ghunna_incorrect': {
        'code': 'TJ002',
        'title': 'Incorrect Ghunna',
        'description': 'Ensure proper nasalization timing (2 counts) on Noon and Mim Mushaddadah.',
        'severity': 'high'
    },
    'madd_short': {
        'code': 'TJ003',
        'title': 'Short Madd',
        'description': 'You shortened a long vowel. Stretch the sound for the correct duration.',
        'severity': 'medium'
    },
    'heavy_letter_light': {
        'code': 'TJ004',
        'title': 'Heavy Letter Pronounced Light',
        'description': 'This letter requires raising the back of the tongue (Tafkheem).',
        'severity': 'high'
    }
}

def normalize_arabic(text: str) -> str:
    """
    Removes diacritics (harakat), Tajweed marks, and extra spaces
    to allow for fair text comparison.
    """
    if not text:
        return ""
    
    # List of Arabic diacritics (harakat) and characters to remove
    diacritics_pattern = re.compile(r'[\u064B-\u065F\u06D6-\u06ED\u0610-\u061A\u0640]')
    normalized = diacritics_pattern.sub('', text)
    
    # Normalize Alif variants
    normalized = re.sub(r'[أإآٱ]', 'ا', normalized)
    # Normalize Hamza variants
    normalized = re.sub(r'[ؤئ]', 'ء', normalized)
    # Normalize Ta Marbuta
    normalized = re.sub(r'ة', 'ه', normalized)
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def analyze_word_level(reference_text: str, spoken_text: str) -> list:
    """
    Compares reference and spoken text word-by-word and returns
    accuracy scores (0.0 to 1.0) for each word in the reference.
    """
    ref_words = reference_text.split()
    spoken_words = spoken_text.split()
    
    accuracies = []
    
    # Simple alignment and comparison logic
    # For each word in reference, find the best match in the spoken text
    # around the expected position.
    import difflib
    
    for i, ref_word in enumerate(ref_words):
        norm_ref = normalize_arabic(ref_word)
        if not norm_ref:
            accuracies.append(1.0)
            continue
            
        # Search window in spoken words (to handle omissions/additions)
        window_size = 3
        start = max(0, i - window_size)
        end = min(len(spoken_words), i + window_size + 1)
        
        best_word_score = 0.0
        for j in range(start, end):
            norm_spoken = normalize_arabic(spoken_words[j])
            score = difflib.SequenceMatcher(None, norm_ref, norm_spoken).ratio()
            if score > best_word_score:
                best_word_score = score
        
        accuracies.append(best_word_score)
        
    return accuracies

def get_ipa_transcription(text: str) -> str:
    """
    Basic conversion of Arabic text to IPA.
    """
    ipa_text = []
    for char in text:
        ipa_text.append(ARABIC_TO_IPA.get(char, char))
    return "".join(ipa_text)

def analyze_tajweed_errors(expected_text: str, spoken_text: str):
    """
    Analyze potential Tajweed errors.
    """
    feedback = []
    qalqalah_letters = ['ق', 'ط', 'ب', 'ج', 'د']
    for letter in qalqalah_letters:
        if letter in expected_text and letter not in spoken_text:
             feedback.append(TAJWEED_ERRORS['qalqalah_missing'])
    return feedback
