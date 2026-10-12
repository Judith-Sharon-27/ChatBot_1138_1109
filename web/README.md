# BhashaSetu web prototype

A responsive multilingual language-learning website concept with:
- Chat, learning, and translate modes
- 13 Indian languages plus English and Sanskrit in the selectors
- Native-script virtual keyboard and a basic English-letter keyboard
- Browser speech synthesis for spoken responses
- Browser speech recognition where supported (typically Chrome on HTTPS)
- Learning level selector and language swapping
- Optional AI backend hook via `window.BHASHASETU_API_URL`

## Run locally
Open `index.html` in a browser, or serve the repository using a static web server. For microphone access, use localhost or HTTPS.

## AI integration status
This is a front-end prototype. Without a configured API endpoint it intentionally uses sample learning responses; it is **not** yet an open-ended AI chatbot. To connect a backend, set `window.BHASHASETU_API_URL` before `app.js` loads, for example in a local development-only script:

```html
<script>window.BHASHASETU_API_URL = "http://localhost:8000/api/chat";</script>
<script src="./app.js"></script>
```

The endpoint should accept POST JSON:
```json
{
  "message": "How do I introduce myself?",
  "mode": "learn",
  "nativeLanguage": "te",
  "targetLanguage": "sa",
  "level": "beginner",
  "scriptMode": "native"
}
```

It should return JSON such as:
```json
{
  "reply": "An explanation in the learner's comfort language.",
  "translation": "A phrase in the target language.",
  "targetText": "Optional alternative field"
}
```

Use a server-side AI provider integration for true language detection, natural multilingual dialogue, translations, pronunciation guidance and grammar explanations. Store API credentials only in server-side environment variables, never in browser JavaScript or GitHub. Add rate limiting, validation, privacy disclosures, and safeguards before public deployment.

## Current limitations
- The keyboard offers native script characters and a basic Latin keyboard; Latin keys do not yet perform phonetic transliteration into Indic scripts.
- Speech recognition and voices depend on browser/OS support and installed language packs.
- The built-in phrase examples are illustrative and should be reviewed by fluent speakers before being used as instructional content.
