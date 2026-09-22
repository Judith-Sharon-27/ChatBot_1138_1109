import streamlit as st
from app.language import LANGUAGES
from app.engine import SanskritBot, PHRASES

st.set_page_config(page_title="Sanskrit Fluency Coach", page_icon="🌺", layout="wide")
if "bot" not in st.session_state:
    st.session_state.bot = SanskritBot()
if "chat" not in st.session_state:
    st.session_state.chat = []
if "practice_index" not in st.session_state:
    st.session_state.practice_index = 0

bot = st.session_state.bot

with st.sidebar:
    st.title("🌺 Sanskrit Fluency")
    lang = st.selectbox("I know / I speak", list(LANGUAGES),
                        format_func=lambda x: f"{LANGUAGES[x]['native']} — {x}")
    level = st.select_slider("Your level",
                             ["Beginner", "Elementary", "Intermediate", "Advanced"],
                             value="Beginner")
    st.divider()
    st.caption("AI mode")
    st.write("🟢 OpenAI enabled" if bot.api_configured() else "🟡 Offline phrasebook")
    if not bot.api_configured():
        st.caption("Set OPENAI_API_KEY in deployment secrets for open-ended translation.")

st.title(f"{LANGUAGES[lang]['native']} → संस्कृतम्")
st.caption(f"Sanskrit Fluency Coach • {level}")

translate_tab, chat_tab, practice_tab, grammar_tab, progress_tab = st.tabs(
    ["🔄 Translate", "💬 Conversation", "🧠 Practice", "📚 Grammar", "📊 Progress"]
)

with translate_tab:
    st.subheader("Turn your thought into Sanskrit")
    learner_text = st.text_area(f"Write in {lang}", height=140,
                                placeholder="Example: I am learning Sanskrit.")
    if st.button("Convert to Sanskrit", type="primary", use_container_width=True):
        if not learner_text.strip():
            st.warning("Please enter a word or sentence first.")
        else:
            with st.spinner("Preparing Sanskrit..."):
                result = bot.translate(lang, learner_text, level)
            if result.get("error"):
                st.error(result["error"])
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("संस्कृतम्", result.get("sanskrit", "—"))
                c2.metric("IAST", result.get("iast", "—"))
                c3.metric("English", result.get("english", "—"))
                if result.get("grammar"):
                    st.info("📚 Grammar: " + result["grammar"])
                if result.get("correction"):
                    st.warning("✏️ Correction: " + result["correction"])
                st.caption("Mode: " + result.get("mode", "offline"))

with chat_tab:
    st.subheader("Practice a Sanskrit conversation")
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
    grammar_text = st.text_input("Enter a Sanskrit word or sentence",
                                 placeholder="अहं संस्कृतं पठामि।")
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
