import streamlit as st
from .language import LANGUAGES
from .engine import SanskritBot,PHRASES
st.set_page_config(page_title="Sanskrit Fluency Bot",page_icon="🌺",layout="wide")
if "bot" not in st.session_state:st.session_state.bot=SanskritBot()
if "chat" not in st.session_state:st.session_state.chat=[]
with st.sidebar:
 lang=st.selectbox("I know / I speak",list(LANGUAGES),format_func=lambda x:f"{LANGUAGES[x]['native']} — {x}")
 level=st.select_slider("Level",["Beginner","Elementary","Intermediate","Advanced"],value="Beginner")
st.title(f"{LANGUAGES[lang]['native']} → संस्कृतम् → English")
st.caption(f"Multilingual Sanskrit fluency coach • {level}")
a,b,c,d=st.tabs(["🔄 Translate","💬 Chat","🧠 Practice","📊 Progress"])
with a:
 text=st.text_area(f"Type in {lang}",placeholder="Example: hello / a short sentence")
 if st.button("Convert to Sanskrit",type="primary") and text.strip():
  r=st.session_state.bot.translate(lang,text)
  if "error" in r:st.error(r["error"])
  else:
   x,y,z=st.columns(3);x.metric("संस्कृतम्",r.get("sanskrit",""));y.metric("IAST",r.get("iast",""));z.metric("English",r.get("english",""))
   if r.get("grammar"):st.info("Grammar: "+r["grammar"])
with b:
 for role,msg in st.session_state.chat:
  with st.chat_message(role):st.write(msg)
 q=st.chat_input("संस्कृतेन वदतु…")
 if q:
  st.session_state.chat.append(("user",q)); r=st.session_state.bot.translate("Sanskrit",q)
  st.session_state.chat.append(("assistant",r.get("reply") or "साधु! कृपया संस्कृतेन पुनः उत्तरं ददातु।"));st.rerun()
with c:
 st.subheader("Active recall"); item=next(iter(PHRASES.values()));st.write("Translate into Sanskrit:",item[2]);ans=st.text_input("Your answer")
 if st.button("Check"):
  if ans.strip().lower().replace("।","")==item[0].lower().replace("।",""):st.success("साधु! Correct.")
  else:st.warning(f"Suggested: {item[0]} ({item[1]})")
 st.write("Modes: translation • vocabulary • grammar • free response • conversation • IAST reading")
with d:
 st.subheader("Learning dashboard");st.write("Multilingual translation, adaptive practice, conversation, grammar feedback and local progress storage.")
 st.info("Set OPENAI_API_KEY for broad multilingual coverage; the offline phrasebook works without an API key.")