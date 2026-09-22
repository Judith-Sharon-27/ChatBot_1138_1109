import streamlit as st
from app.language import LANGUAGES
from app.engine import SanskritBot, PHRASES
from app.keyboard import keyboard_rows, transliterate_english

st.set_page_config(page_title="Sanskrit Fluency Coach", page_icon="🌺", layout="wide")

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@500;600;700&display=swap');
.stApp {
    background:
      radial-gradient(circle at 8% 8%, rgba(255,196,120,.28), transparent 25%),
      radial-gradient(circle at 92% 14%, rgba(128,186,255,.22), transparent 24%),
      linear-gradient(135deg, #fffaf2 0%, #f6f8ff 48%, #f3fbf8 100%);
    font-family: 'Noto Sans', sans-serif;
}
.block-container {max-width: 1180px; padding-top: 1.5rem;}
.hero {
    padding: 2.2rem 2.4rem;
    border-radius: 28px;
    background: linear-gradient(120deg, rgba(84,43,132,.97), rgba(20,105,100,.94));
    color: white;
    box-shadow: 0 18px 55px rgba(54,38,83,.20);
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "ॐ  संस्कृतम्  नमस्ते  🪷";
    position:absolute; right:2rem; bottom:1rem;
    font-size: 1.1rem; opacity:.22; letter-spacing:.12rem;
}
.hero h1 {font-size: clamp(2rem, 4vw, 3.4rem); margin:0; letter-spacing:-.04em;}
.hero p {font-size:1.08rem; margin:.55rem 0 0; opacity:.88;}
.card {
    padding: 1.15rem 1.25rem;
    border: 1px solid rgba(70,55,90,.10);
    border-radius: 20px;
    background: rgba(255,255,255,.78);
    box-shadow: 0 10px 30px rgba(40,35,55,.07);
}
.kb-title {font-weight:800; font-size:1.1rem; margin:.3rem 0 .75rem;}
.kb-row {margin-bottom:.45rem;}
.small-note {color:#666; font-size:.88rem;}
div[data-testid="stButton"] button {
    border-radius: 12px;
    border: 1px solid rgba(84,43,132,.12);
}
</style>
""", unsafe_allow_html=True)

if "bot" not in st.session_state:
    st.session_state.bot = SanskritBot()
if "chat" not in st.session_state:
    st.session_state.chat = []
if "practice_index" not in st.session_state:
    st.session_state.practice_index = 0
if "native_text" not in st.session_state:
    st.session_state.native_text = ""

bot = st.session_state.bot

with st.sidebar:
    st.title("🌺 Sanskrit Fluency")
    lang = st.selectbox(
        "I know / I speak",
        list(LANGUAGES),
        format_func=lambda x: f"{LANGUAGES[x]['native']} — {x}",
    )
    level = st.select_slider(
        "Your level",
        ["Beginner", "Elementary", "Intermediate", "Advanced"],
        value="Beginner",
    )
    st.divider()
    st.caption("Input tools")
    st.write("⌨️ Virtual keyboard")
    st.write("🔤 English → native script")
    st.divider()
    st.caption("AI mode")
    st.write("🟢 OpenAI enabled" if bot.api_configured() else "🟡 Offline phrasebook")
    if not bot.api_configured():
        st.caption("Set OPENAI_API_KEY in deployment secrets for open-ended translation.")

st.markdown(f"""
<div class="hero">
  <h1>संस्कृतम् • Sanskrit Fluency Coach</h1>
  <p>{LANGUAGES[lang]['native']} → संस्कृतम् &nbsp; · &nbsp; Learn by typing, speaking and practising</p>
</div>
""", unsafe_allow_html=True)

translate_tab, chat_tab, practice_tab, grammar_tab, progress_tab = st.tabs(
    ["🔄 Translate", "💬 Conversation", "🧠 Practice", "📚 Grammar", "📊 Progress"]
)

with translate_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("✨ Smart multilingual input")
    st.write(
        f"Type English phonetically and see it become **{LANGUAGES[lang]['native']}**. "
        "Or use the on-screen keyboard below."
    )

    english_input = st.text_input(
        "English phonetic typing",
        placeholder="Try: namaste, amma, nenu, vanakkam...",
        key=f"english_phonetic_{lang}",
    )
    live_native = transliterate_english(english_input, lang) if english_input else ""
    if live_native:
        st.markdown("**Live native-script preview**")
        st.code(live_native, language=None)
        if st.button("Use this text", key=f"use_live_{lang}", use_container_width=True):
            st.session_state.native_text = live_native
            st.rerun()

    st.markdown('<div class="kb-title">⌨️ Virtual keyboard</div>', unsafe_allow_html=True)
    st.caption("Tap characters to build your sentence. The layout changes with your selected language.")

    rows = keyboard_rows(lang)
    if rows:
        for r_idx, row in enumerate(rows):
            chars = row.split()
            cols = st.columns(min(len(chars), 12))
            for i, char in enumerate(chars):
                with cols[i % len(cols)]:
                    if st.button(char, key=f"kb_{lang}_{r_idx}_{i}", use_container_width=True):
                        st.session_state.native_text += char
                        st.rerun()
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Space", key=f"space_{lang}", use_container_width=True):
                st.session_state.native_text += " "
                st.rerun()
        with c2:
            if st.button("⌫ Backspace", key=f"back_{lang}", use_container_width=True):
                st.session_state.native_text = st.session_state.native_text[:-1]
                st.rerun()
        with c3:
            if st.button("Clear", key=f"clear_{lang}", use_container_width=True):
                st.session_state.native_text = ""
                st.rerun()

    native_text = st.text_area(
        f"{LANGUAGES[lang]['native']} input",
        key="native_text",
        height=120,
        placeholder=f"Type or build your sentence in {lang}...",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 Convert to Sanskrit", type="primary", use_container_width=True):
        if not native_text.strip():
            st.warning("Please enter a word or sentence first.")
        else:
            with st.spinner("Preparing Sanskrit..."):
                result = bot.translate(lang, native_text, level)
            if result.get("error"):
                st.error(result["error"])
            else:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.metric("संस्कृतम्", result.get("sanskrit", "—"))
                c2.metric("IAST", result.get("iast", "—"))
                c3.metric("English", result.get("english", "—"))
                if result.get("grammar"):
                    st.info("📚 Grammar: " + result["grammar"])
                if result.get("correction"):
                    st.warning("✏️ Correction: " + result["correction"])
                st.caption("Mode: " + result.get("mode", "offline"))
                st.markdown('</div>', unsafe_allow_html=True)

with chat_tab:
    st.subheader("💬 Practice a Sanskrit conversation")
    if st.button("Clear conversation"):
        st.session_state.chat = []
        st.rerun()
    for role, message in st.session_state.chat:
        with st.chat_message(role):
            st.write(message)
    prompt = st.chat_input("संस्कृतेन वदतु…")
    if prompt:
        st.session_state.chat.append(("user", prompt))
        with st.spinner("Thinking in Sanskrit..."):
            result = bot.converse(prompt, lang, level)
        reply = result.get("reply") or result.get("sanskrit") or "कृपया पुनः प्रयतताम्।"
        st.session_state.chat.append(("assistant", reply))
        if result.get("english"):
            st.session_state.chat.append(("assistant", "English: " + result["english"]))
        st.rerun()

with practice_tab:
    st.subheader("🧠 Active recall")
    phrase_items = list(PHRASES.items())
    key, item = phrase_items[st.session_state.practice_index % len(phrase_items)]
    st.write("Translate this into Sanskrit:")
    st.markdown(f"### {item[2]}")
    answer = st.text_input("Your Sanskrit answer", key=f"answer_{st.session_state.practice_index}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Check answer", use_container_width=True):
            if bot.is_correct(answer, item[0]):
                st.success("साधु! Correct.")
                bot.record_practice(lang, True, item[2])
            else:
                st.warning(f"Suggested answer: **{item[0]}**")
                st.caption(f"IAST: {item[1]}")
                bot.record_practice(lang, False, item[2])
    with c2:
        if st.button("Next phrase", use_container_width=True):
            st.session_state.practice_index += 1
            st.rerun()
    st.divider()
    st.write("Practice modes: vocabulary • translation • IAST reading • grammar • conversation")

with grammar_tab:
    st.subheader("📚 Sanskrit grammar helper")
    grammar_text = st.text_input(
        "Enter a Sanskrit word or sentence",
        placeholder="अहं संस्कृतं पठामि।",
    )
    if st.button("Explain grammar", use_container_width=True):
        if not grammar_text.strip():
            st.warning("Enter Sanskrit text first.")
        else:
            with st.spinner("Analyzing..."):
                result = bot.grammar(grammar_text, level)
            if result.get("error"):
                st.error(result["error"])
            else:
                st.markdown(result.get("explanation", "No explanation returned."))
                if result.get("iast"):
                    st.write("**IAST:**", result["iast"])

with progress_tab:
    st.subheader("📊 Your learning dashboard")
    stats = bot.stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("Practice attempts", stats["attempts"])
    c2.metric("Correct", stats["correct"])
    c3.metric("Accuracy", f'{stats["accuracy"]:.0f}%')
    st.progress(stats["accuracy"] / 100 if stats["attempts"] else 0)
    st.write(f"Current language: **{LANGUAGES[lang]['native']} — {lang}**")
    st.write("Your practice history is stored locally in SQLite.")
    st.info("For broad multilingual translation and richer grammar feedback, configure OPENAI_API_KEY.")
