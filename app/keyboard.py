"""Virtual keyboards and lightweight English-phonetic input for Indian scripts.

This module intentionally uses only the Python standard library so the chatbot
can run in restricted Windows and Docker environments without native DLLs.
"""

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

# Basic phonetic mappings used by the UI preview. This is deliberately small
# and dependency-free; the virtual keyboard remains the reliable input method.
_TELUGU = {
    "aa":"ఆ","ii":"ఈ","uu":"ఊ","ai":"ఐ","au":"ఔ","a":"అ","i":"ఇ","u":"ఉ","e":"ఎ","o":"ఒ",
    "kh":"ఖ","gh":"ఘ","ch":"చ","jh":"ఝ","th":"థ","dh":"ధ","ph":"ఫ","bh":"భ",
    "k":"క","g":"గ","c":"చ","j":"జ","t":"త","d":"ద","n":"న","p":"ప","b":"బ","m":"మ",
    "y":"య","r":"ర","l":"ల","v":"వ","w":"వ","s":"స","h":"హ",
}

def transliterate_english(text: str, language: str) -> str:
    if not text.strip() or language == "English":
        return text
    if language != "Telugu":
        return text

    result = []
    i = 0
    lower = text.lower()
    keys = sorted(_TELUGU, key=len, reverse=True)
    while i < len(text):
        matched = False
        for key in keys:
            if lower.startswith(key, i):
                result.append(_TELUGU[key])
                i += len(key)
                matched = True
                break
        if not matched:
            result.append(text[i])
            i += 1
    return "".join(result)

def keyboard_rows(language: str):
    return KEYBOARD_ROWS.get(language, [])
