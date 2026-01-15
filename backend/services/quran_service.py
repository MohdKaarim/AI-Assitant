import requests
from typing import Dict, List, Optional

# AlQuran Cloud API Base URL
API_BASE_URL = "https://api.alquran.cloud/v1"

# Cache for surah metadata (all 114 surahs)
SURAH_METADATA = [
    {"number": 1, "name_arabic": "الفاتحة", "name_english": "Al-Fatihah", "verses_count": 7},
    {"number": 2, "name_arabic": "البقرة", "name_english": "Al-Baqarah", "verses_count": 286},
    {"number": 3, "name_arabic": "آل عمران", "name_english": "Ali 'Imran", "verses_count": 200},
    {"number": 4, "name_arabic": "النساء", "name_english": "An-Nisa", "verses_count": 176},
    {"number": 5, "name_arabic": "المائدة", "name_english": "Al-Ma'idah", "verses_count": 120},
    {"number": 6, "name_arabic": "الأنعام", "name_english": "Al-An'am", "verses_count": 165},
    {"number": 7, "name_arabic": "الأعراف", "name_english": "Al-A'raf", "verses_count": 206},
    {"number": 8, "name_arabic": "الأنفال", "name_english": "Al-Anfal", "verses_count": 75},
    {"number": 9, "name_arabic": "التوبة", "name_english": "At-Tawbah", "verses_count": 129},
    {"number": 10, "name_arabic": "يونس", "name_english": "Yunus", "verses_count": 109},
    {"number": 11, "name_arabic": "هود", "name_english": "Hud", "verses_count": 123},
    {"number": 12, "name_arabic": "يوسف", "name_english": "Yusuf", "verses_count": 111},
    {"number": 13, "name_arabic": "الرعد", "name_english": "Ar-Ra'd", "verses_count": 43},
    {"number": 14, "name_arabic": "ابراهيم", "name_english": "Ibrahim", "verses_count": 52},
    {"number": 15, "name_arabic": "الحجر", "name_english": "Al-Hijr", "verses_count": 99},
    {"number": 16, "name_arabic": "النحل", "name_english": "An-Nahl", "verses_count": 128},
    {"number": 17, "name_arabic": "الإسراء", "name_english": "Al-Isra", "verses_count": 111},
    {"number": 18, "name_arabic": "الكهف", "name_english": "Al-Kahf", "verses_count": 110},
    {"number": 19, "name_arabic": "مريم", "name_english": "Maryam", "verses_count": 98},
    {"number": 20, "name_arabic": "طه", "name_english": "Taha", "verses_count": 135},
    {"number": 21, "name_arabic": "الأنبياء", "name_english": "Al-Anbya", "verses_count": 112},
    {"number": 22, "name_arabic": "الحج", "name_english": "Al-Hajj", "verses_count": 78},
    {"number": 23, "name_arabic": "المؤمنون", "name_english": "Al-Mu'minun", "verses_count": 118},
    {"number": 24, "name_arabic": "النور", "name_english": "An-Nur", "verses_count": 64},
    {"number": 25, "name_arabic": "الفرقان", "name_english": "Al-Furqan", "verses_count": 77},
    {"number": 26, "name_arabic": "الشعراء", "name_english": "Ash-Shu'ara", "verses_count": 227},
    {"number": 27, "name_arabic": "النمل", "name_english": "An-Naml", "verses_count": 93},
    {"number": 28, "name_arabic": "القصص", "name_english": "Al-Qasas", "verses_count": 88},
    {"number": 29, "name_arabic": "العنكبوت", "name_english": "Al-'Ankabut", "verses_count": 69},
    {"number": 30, "name_arabic": "الروم", "name_english": "Ar-Rum", "verses_count": 60},
    {"number": 31, "name_arabic": "لقمان", "name_english": "Luqman", "verses_count": 34},
    {"number": 32, "name_arabic": "السجدة", "name_english": "As-Sajdah", "verses_count": 30},
    {"number": 33, "name_arabic": "الأحزاب", "name_english": "Al-Ahzab", "verses_count": 73},
    {"number": 34, "name_arabic": "سبإ", "name_english": "Saba", "verses_count": 54},
    {"number": 35, "name_arabic": "فاطر", "name_english": "Fatir", "verses_count": 45},
    {"number": 36, "name_arabic": "يس", "name_english": "Ya-Sin", "verses_count": 83},
    {"number": 37, "name_arabic": "الصافات", "name_english": "As-Saffat", "verses_count": 182},
    {"number": 38, "name_arabic": "ص", "name_english": "Sad", "verses_count": 88},
    {"number": 39, "name_arabic": "الزمر", "name_english": "Az-Zumar", "verses_count": 75},
    {"number": 40, "name_arabic": "غافر", "name_english": "Ghafir", "verses_count": 85},
    {"number": 41, "name_arabic": "فصلت", "name_english": "Fussilat", "verses_count": 54},
    {"number": 42, "name_arabic": "الشورى", "name_english": "Ash-Shuraa", "verses_count": 53},
    {"number": 43, "name_arabic": "الزخرف", "name_english": "Az-Zukhruf", "verses_count": 89},
    {"number": 44, "name_arabic": "الدخان", "name_english": "Ad-Dukhan", "verses_count": 59},
    {"number": 45, "name_arabic": "الجاثية", "name_english": "Al-Jathiyah", "verses_count": 37},
    {"number": 46, "name_arabic": "الأحقاف", "name_english": "Al-Ahqaf", "verses_count": 35},
    {"number": 47, "name_arabic": "محمد", "name_english": "Muhammad", "verses_count": 38},
    {"number": 48, "name_arabic": "الفتح", "name_english": "Al-Fath", "verses_count": 29},
    {"number": 49, "name_arabic": "الحجرات", "name_english": "Al-Hujurat", "verses_count": 18},
    {"number": 50, "name_arabic": "ق", "name_english": "Qaf", "verses_count": 45},
    {"number": 51, "name_arabic": "الذاريات", "name_english": "Adh-Dhariyat", "verses_count": 60},
    {"number": 52, "name_arabic": "الطور", "name_english": "At-Tur", "verses_count": 49},
    {"number": 53, "name_arabic": "النجم", "name_english": "An-Najm", "verses_count": 62},
    {"number": 54, "name_arabic": "القمر", "name_english": "Al-Qamar", "verses_count": 55},
    {"number": 55, "name_arabic": "الرحمن", "name_english": "Ar-Rahman", "verses_count": 78},
    {"number": 56, "name_arabic": "الواقعة", "name_english": "Al-Waqi'ah", "verses_count": 96},
    {"number": 57, "name_arabic": "الحديد", "name_english": "Al-Hadid", "verses_count": 29},
    {"number": 58, "name_arabic": "المجادلة", "name_english": "Al-Mujadila", "verses_count": 22},
    {"number": 59, "name_arabic": "الحشر", "name_english": "Al-Hashr", "verses_count": 24},
    {"number": 60, "name_arabic": "الممتحنة", "name_english": "Al-Mumtahanah", "verses_count": 13},
    {"number": 61, "name_arabic": "الصف", "name_english": "As-Saf", "verses_count": 14},
    {"number": 62, "name_arabic": "الجمعة", "name_english": "Al-Jumu'ah", "verses_count": 11},
    {"number": 63, "name_arabic": "المنافقون", "name_english": "Al-Munafiqun", "verses_count": 11},
    {"number": 64, "name_arabic": "التغابن", "name_english": "At-Taghabun", "verses_count": 18},
    {"number": 65, "name_arabic": "الطلاق", "name_english": "At-Talaq", "verses_count": 12},
    {"number": 66, "name_arabic": "التحريم", "name_english": "At-Tahrim", "verses_count": 12},
    {"number": 67, "name_arabic": "الملك", "name_english": "Al-Mulk", "verses_count": 30},
    {"number": 68, "name_arabic": "القلم", "name_english": "Al-Qalam", "verses_count": 52},
    {"number": 69, "name_arabic": "الحاقة", "name_english": "Al-Haqqah", "verses_count": 52},
    {"number": 70, "name_arabic": "المعارج", "name_english": "Al-Ma'arij", "verses_count": 44},
    {"number": 71, "name_arabic": "نوح", "name_english": "Nuh", "verses_count": 28},
    {"number": 72, "name_arabic": "الجن", "name_english": "Al-Jinn", "verses_count": 28},
    {"number": 73, "name_arabic": "المزمل", "name_english": "Al-Muzzammil", "verses_count": 20},
    {"number": 74, "name_arabic": "المدثر", "name_english": "Al-Muddaththir", "verses_count": 56},
    {"number": 75, "name_arabic": "القيامة", "name_english": "Al-Qiyamah", "verses_count": 40},
    {"number": 76, "name_arabic": "الانسان", "name_english": "Al-Insan", "verses_count": 31},
    {"number": 77, "name_arabic": "المرسلات", "name_english": "Al-Mursalat", "verses_count": 50},
    {"number": 78, "name_arabic": "النبإ", "name_english": "An-Naba", "verses_count": 40},
    {"number": 79, "name_arabic": "النازعات", "name_english": "An-Nazi'at", "verses_count": 46},
    {"number": 80, "name_arabic": "عبس", "name_english": "'Abasa", "verses_count": 42},
    {"number": 81, "name_arabic": "التكوير", "name_english": "At-Takwir", "verses_count": 29},
    {"number": 82, "name_arabic": "الإنفطار", "name_english": "Al-Infitar", "verses_count": 19},
    {"number": 83, "name_arabic": "المطففين", "name_english": "Al-Mutaffifin", "verses_count": 36},
    {"number": 84, "name_arabic": "الإنشقاق", "name_english": "Al-Inshiqaq", "verses_count": 25},
    {"number": 85, "name_arabic": "البروج", "name_english": "Al-Buruj", "verses_count": 22},
    {"number": 86, "name_arabic": "الطارق", "name_english": "At-Tariq", "verses_count": 17},
    {"number": 87, "name_arabic": "الأعلى", "name_english": "Al-A'la", "verses_count": 19},
    {"number": 88, "name_arabic": "الغاشية", "name_english": "Al-Ghashiyah", "verses_count": 26},
    {"number": 89, "name_arabic": "الفجر", "name_english": "Al-Fajr", "verses_count": 30},
    {"number": 90, "name_arabic": "البلد", "name_english": "Al-Balad", "verses_count": 20},
    {"number": 91, "name_arabic": "الشمس", "name_english": "Ash-Shams", "verses_count": 15},
    {"number": 92, "name_arabic": "الليل", "name_english": "Al-Layl", "verses_count": 21},
    {"number": 93, "name_arabic": "الضحى", "name_english": "Ad-Duhaa", "verses_count": 11},
    {"number": 94, "name_arabic": "الشرح", "name_english": "Ash-Sharh", "verses_count": 8},
    {"number": 95, "name_arabic": "التين", "name_english": "At-Tin", "verses_count": 8},
    {"number": 96, "name_arabic": "العلق", "name_english": "Al-'Alaq", "verses_count": 19},
    {"number": 97, "name_arabic": "القدر", "name_english": "Al-Qadr", "verses_count": 5},
    {"number": 98, "name_arabic": "البينة", "name_english": "Al-Bayyinah", "verses_count": 8},
    {"number": 99, "name_arabic": "الزلزلة", "name_english": "Az-Zalzalah", "verses_count": 8},
    {"number": 100, "name_arabic": "العاديات", "name_english": "Al-'Adiyat", "verses_count": 11},
    {"number": 101, "name_arabic": "القارعة", "name_english": "Al-Qari'ah", "verses_count": 11},
    {"number": 102, "name_arabic": "التكاثر", "name_english": "At-Takathur", "verses_count": 8},
    {"number": 103, "name_arabic": "العصر", "name_english": "Al-'Asr", "verses_count": 3},
    {"number": 104, "name_arabic": "الهمزة", "name_english": "Al-Humazah", "verses_count": 9},
    {"number": 105, "name_arabic": "الفيل", "name_english": "Al-Fil", "verses_count": 5},
    {"number": 106, "name_arabic": "قريش", "name_english": "Quraysh", "verses_count": 4},
    {"number": 107, "name_arabic": "الماعون", "name_english": "Al-Ma'un", "verses_count": 7},
    {"number": 108, "name_arabic": "الكوثر", "name_english": "Al-Kawthar", "verses_count": 3},
    {"number": 109, "name_arabic": "الكافرون", "name_english": "Al-Kafirun", "verses_count": 6},
    {"number": 110, "name_arabic": "النصر", "name_english": "An-Nasr", "verses_count": 3},
    {"number": 111, "name_arabic": "المسد", "name_english": "Al-Masad", "verses_count": 5},
    {"number": 112, "name_arabic": "الإخلاص", "name_english": "Al-Ikhlas", "verses_count": 4},
    {"number": 113, "name_arabic": "الفلق", "name_english": "Al-Falaq", "verses_count": 5},
    {"number": 114, "name_arabic": "الناس", "name_english": "An-Nas", "verses_count": 6}
]

def get_all_surahs() -> List[Dict]:
    """
    Returns metadata for all surahs.
    """
    return SURAH_METADATA

def get_surah_verses(surah_number: int) -> Optional[Dict]:
    """
    Fetches verses for a specific surah from AlQuran Cloud API.
    Returns both Arabic (ar.alafasy - with diacritics) and English (en.asad) editions.
    """
    try:
        # Using ar.alafasy for readable Arabic with Tajweed marks
        # en.asad for meaning, en.transliteration for pronunciation
        url = f"{API_BASE_URL}/surah/{surah_number}/editions/ar.alafasy,en.asad,en.transliteration"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("code") != 200:
            return None
        
        # Parse the response
        editions = data.get("data", [])
        if len(editions) < 3:
            return None
        
        arabic_edition = editions[0]
        english_edition = editions[1]
        trans_edition = editions[2]
        
        # Fetch Word-level data from Quran.com for translations
        word_data = {}
        try:
            word_url = f"https://api.quran.com/api/v4/verses/by_chapter/{surah_number}?words=true&word_fields=text_uthmani&translation_fields=text"
            word_res = requests.get(word_url, timeout=10)
            if word_res.status_code == 200:
                words_json = word_res.json()
                for verse in words_json.get("verses", []):
                    v_num = verse.get("verse_number")
                    word_list = []
                    for w in verse.get("words", []):
                        if w.get("char_type_name") == "word":
                            word_list.append({
                                "arabic": w.get("text_uthmani"),
                                "english": w.get("translation", {}).get("text", "")
                            })
                    word_data[v_num] = word_list
        except Exception as we:
            print(f"Error fetching word data: {we}")

        # Combine verses
        verses = []
        for i, arabic_verse in enumerate(arabic_edition.get("ayahs", [])):
            v_num = arabic_verse.get("numberInSurah")
            english_verse = english_edition.get("ayahs", [])[i] if i < len(english_edition.get("ayahs", [])) else None
            trans_verse = trans_edition.get("ayahs", [])[i] if i < len(trans_edition.get("ayahs", [])) else None
            
            verses.append({
                "number": v_num,
                "text_arabic": arabic_verse.get("text"),
                "text_english": english_verse.get("text") if english_verse else "",
                "text_transliteration": trans_verse.get("text") if trans_verse else "",
                "audio_url": arabic_verse.get("audio", ""),
                "words": word_data.get(v_num, []) # New word-level data
            })
        
        return {
            "number": arabic_edition.get("number"),
            "name_arabic": arabic_edition.get("name"),
            "name_english": arabic_edition.get("englishName"),
            "verses_count": arabic_edition.get("numberOfAyahs"),
            "verses": verses
        }
    
    except Exception as e:
        print(f"Error fetching surah {surah_number}: {e}")
        return None

def get_verse(surah_number: int, verse_number: int) -> Optional[Dict]:
    """
    Get a specific verse from a surah.
    """
    surah_data = get_surah_verses(surah_number)
    if not surah_data:
        return None
    
    verses = surah_data.get("verses", [])
    for verse in verses:
        if verse.get("number") == verse_number:
            return verse
    
    return None
