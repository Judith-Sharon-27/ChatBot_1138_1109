# Sanskrit Fluency Bot 

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


## Docker

Build the chatbot image:

```bash
docker build -t sanskrit-chatbot:1.0 .
```

Run it offline:

```bash
docker run --name sanskrit-chatbot -p 8501:8501 sanskrit-chatbot:1.0
```

Then open http://localhost:8501.

To enable the OpenAI-compatible online mode, provide the API key at runtime. Do not put the key in the Dockerfile or commit it to GitHub.

PowerShell:

```powershell
$env:OPENAI_API_KEY="sk-your-real-key"
docker run --name sanskrit-chatbot -p 8501:8501 -e OPENAI_API_KEY=$env:OPENAI_API_KEY sanskrit-chatbot:1.0
```

Or with Docker Compose:

```powershell
$env:OPENAI_API_KEY="sk-your-real-key"
docker compose up --build
```

Stop the Compose deployment:

```powershell
docker compose down
```

Check the container:

```powershell
docker ps
docker logs sanskrit-chatbot
```

The Docker image packages the existing Streamlit application; it does not replace the chatbot architecture with FastAPI/Ollama.
