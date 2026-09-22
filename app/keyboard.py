"""Virtual keyboards and English-phonetic input for Indian scripts."""

from indic_transliteration import sanscript

SCRIPT_TARGETS = {
    "English": None,
    "Telugu": sanscript.TELUGU,
    "Tamil": sanscript.TAMIL,
    "Kannada": sanscript.KANNADA,
    "Malayalam": sanscript.MALAYALAM,
    "Hindi": sanscript.DEVANAGARI,
    "Bengali": sanscript.BENGALI,
    "Marathi": sanscript.DEVANAGARI,
    "Gujarati": sanscript.GUJARATI,
    "Punjabi": sanscript.GURMUKHI,
    "Odia": sanscript.ORIYA,
}

KEYBOARD_ROWS = {
    "Telugu": ["అ ఆ ఇ ఈ ఉ ఊ ఎ ఏ ఐ ఒ ఓ ఔ", "క ఖ గ ఘ ఙ చ ఛ జ ఝ ఞ", "ట ఠ డ ఢ ణ త థ ద ధ న", "ప ఫ బ భ మ య ర ల వ శ ష స హ", "ా ి ీ ు ూ ె ే ై ొ ో ౌ ం ః ్"],
    "Tamil": ["அ ஆ இ ஈ உ ஊ எ ஏ ஐ ஒ ஓ ஔ", "க ங ச ஜ ஞ ட ண த ந ப ம", "ய ர ல வ ழ ள ற ன", "ா ி ீ ு ூ ெ ே ை ொ ோ ௌ ஂ ஃ"],
    "Kannada": ["ಅ ಆ ಇ ಈ ಉ ಊ ಎ ಏ ಐ ಒ ಓ ಔ", "ಕ ಖ ಗ ಘ ಙ ಚ ಛ ಜ ಝ ಞ", "ಟ ಠ ಡ ಢ ಣ ತ ಥ ದ ಧ ನ", "ಪ ಫ ಬ ಭ ಮ ಯ ರ ಲ ವ ಶ ಷ ಸ ಹ", "ಾ ಿ ೀ ು ೂ ೆ ೇ ೈ ೊ ೋ ೌ ಂ ಃ ್"],
    "Malayalam": ["അ ആ ഇ ഈ ഉ ഊ എ ഏ ഐ ഒ ഓ ഔ", "ക ഖ ഗ ഘ ങ ച ഛ ജ ഝ ഞ", "ട ഠ ഡ ഢ ണ ത ഥ ദ ധ ന", "പ ഫ ബ ഭ മ യ ര ല വ ശ ഷ സ ഹ", "ാ ി ീ ു ൂ െ േ ൈ ൊ ോ ൌ ം ഃ ്"],
    "Hindi": ["अ आ इ ई उ ऊ ए ऐ ओ औ", "क ख ग घ ङ च छ ज झ ञ", "ट ठ ड ढ ण त थ द ध न", "प फ ब भ म य र ल व श ष स ह", "ा ि ी ु ू े ै ो ौ ं ः ्"],
    "Bengali": ["অ আ ই ঈ উ ঊ এ ঐ ও ঔ", "ক খ গ ঘ ঙ চ ছ জ ঝ ঞ", "ট ঠ ড ঢ ণ ত থ দ ধ ন", "প ফ ব ভ ম য র ল শ ষ স হ", "া ি ী ু ূ ে ৈ ো ৌ ং ঃ ্"],
    "Marathi": ["अ आ इ ई उ ऊ ए ऐ ओ औ", "क ख ग घ ङ च छ ज झ ञ", "ट ठ ड ढ ण त थ द ध न", "प फ ब भ म य र ल व श ष स ह", "ा ि ी ु ू े ै ो ौ ं ः ्"],
    "Gujarati": ["અ આ ઇ ઈ ઉ ઊ એ ઐ ઓ ઔ", "ક ખ ગ ઘ ઙ ચ છ જ ઝ ઞ", "ટ ઠ ડ ઢ ણ ત થ દ ધ ન", "પ ફ બ ભ મ ય ર લ વ શ ષ સ હ", "ા િ ી ુ ૂ ે ૈ ો ૌ ં ઃ ્"],
    "Punjabi": ["ਅ ਆ ਇ ਈ ਉ ਊ ਏ ਐ ਓ ਔ", "ਕ ਖ ਗ ਘ ਙ ਚ ਛ ਜ ਝ ਞ", "ਟ ਠ ਡ ਢ ਣ ਤ ਥ ਦ ਧ ਨ", "ਪ ਫ ਬ ਭ ਮ ਯ ਰ ਲ ਵ ਸ ਹ", "ਾ ਿ ੀ ੁ ੂ ੇ ੈ ੋ ੌ ਂ ਃ ੍"],
    "Odia": ["ଅ ଆ ଇ ଈ ଉ ଊ ଏ ଐ ଓ ଔ", "କ ଖ ଗ ଘ ଙ ଚ ଛ ଜ ଝ ଞ", "ଟ ଠ ଡ ଢ ଣ ତ ଥ ଦ ଧ ନ", "ପ ଫ ବ ଭ ମ ଯ ର ଲ ଵ ଶ ଷ ସ ହ", "ା ି ୀ ୁ ୂ େ ୈ ୋ ୌ ଂ ଃ ୍"],
}

def transliterate_english(text: str, language: str) -> str:
    target = SCRIPT_TARGETS.get(language)
    if not target or not text.strip():
        return text
    try:
        return sanscript.transliterate(text, sanscript.ITRANS, target)
    except Exception:
        return text

def keyboard_rows(language: str):
    return KEYBOARD_ROWS.get(language, [])
