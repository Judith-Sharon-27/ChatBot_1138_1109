# Sanskrit Fluency Bot 🌺

Multilingual Sanskrit-learning chatbot.

## Learner flow
Choose the language you know (Telugu, Tamil, Kannada, Malayalam, Hindi, Bengali, Marathi, Gujarati, Punjabi, Odia or English) → enter text → receive:
1. Sanskrit in Devanagari
2. IAST transliteration
3. English meaning
4. Grammar/correction support when AI mode is enabled

Includes conversation mode, active-recall practice, level selection, local SQLite history, and an offline phrasebook.

## Run
pip install -r requirements.txt
streamlit run app/main.py

For broad multilingual open-ended translation, set OPENAI_API_KEY, optionally OPENAI_BASE_URL and OPENAI_MODEL.

The offline mode is intentionally conservative; a production release should add curated Sanskrit lexicons and a Sanskrit morphological analyzer.
