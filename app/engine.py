import json
import os
import sqlite3
from datetime import datetime
import requests

PHRASES = {
    "hello": ("नमस्ते", "namaste", "hello"),
    "water": ("जलम्", "jalam", "water"),
    "book": ("पुस्तकम्", "pustakam", "book"),
    "friend": ("मित्रम्", "mitram", "friend"),
    "today": ("अद्य", "adya", "today"),
    "I study Sanskrit": ("अहं संस्कृतं पठामि।", "ahaṃ saṃskṛtaṃ paṭhāmi.", "I study Sanskrit"),
    "I speak Sanskrit": ("अहं संस्कृतेन वदामि।", "ahaṃ saṃskṛtena vadāmi.", "I speak Sanskrit"),
    "I am learning Sanskrit": ("अहं संस्कृतं पठामि।", "ahaṃ saṃskṛtaṃ paṭhāmi.", "I am learning Sanskrit"),
}

def norm(text):
    return " ".join(text.lower().strip().replace("।", "").split())

class SanskritBot:
    def __init__(self, db="sanskrit_bot.db"):
        self.db = db
        if db != ":memory:":
            with sqlite3.connect(db) as conn:
                conn.execute("create table if not exists events(ts text, lang text, kind text, payload text)")

    def api_configured(self):
        return bool(os.getenv("OPENAI_API_KEY"))

    def log(self, lang, kind, payload):
        if self.db != ":memory:":
            with sqlite3.connect(self.db) as conn:
                conn.execute("insert into events values(?,?,?,?)",
                             (datetime.utcnow().isoformat(), lang, kind,
                              json.dumps(payload, ensure_ascii=False)))

    def local(self, text):
        for key, value in PHRASES.items():
            if norm(text) in (norm(key), norm(value[2])):
                return {"sanskrit": value[0], "iast": value[1],
                        "english": value[2], "mode": "offline"}
        return None

    def ai(self, prompt):
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            return None
        base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        response = requests.post(
            base + "/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={"model": model,
                  "messages": [
                      {"role": "system", "content": "You are a patient Sanskrit language tutor."},
                      {"role": "user", "content": prompt}],
                  "temperature": 0.2},
            timeout=45,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        return json.loads(content)

    def translate(self, lang, text, level="Beginner"):
        local = self.local(text)
        if local:
            self.log(lang, "translation", local)
            return local
        try:
            result = self.ai(
                f"Return valid JSON with keys sanskrit, iast, english, grammar, correction, reply. "
                f"Translate this learner input from {lang} into natural Sanskrit for a {level} learner. "
                f"Give Devanagari Sanskrit, IAST, English meaning, a short grammar note, and correction advice if useful. "
                f"Input: {text}"
            )
            if result:
                result["mode"] = "AI"
                self.log(lang, "translation", result)
                return result
        except Exception as exc:
            return {"error": f"AI translation failed: {exc}"}
        return {"sanskrit": "कृपया पुनः लिखतु।",
                "iast": "kṛpayā punaḥ likhatu.",
                "english": "Please try again with a short sentence.",
                "grammar": "Offline mode currently supports the built-in phrasebook.",
                "mode": "offline"}

    def converse(self, text, lang, level):
        try:
            result = self.ai(
                f"Return valid JSON with keys reply, english, grammar. "
                f"You are a Sanskrit conversation tutor. Respond naturally in Sanskrit to this learner. "
                f"The learner's support language is {lang}; level is {level}. Learner message: {text}"
            )
            if result:
                self.log(lang, "conversation", result)
                return result
        except Exception as exc:
            return {"error": f"Conversation failed: {exc}"}
        local = self.local(text)
        if local:
            return {"reply": local["sanskrit"], "english": local["english"], "mode": "offline"}
        return {"reply": "नमस्ते! कृपया संस्कृतेन सरलवाक्यं लिखतु।", "mode": "offline"}

    def grammar(self, text, level):
        try:
            result = self.ai(
                f"Return valid JSON with keys explanation, iast. "
                f"Explain the Sanskrit grammar of this text for a {level} learner. "
                f"Identify important forms such as case, number, gender, tense/aspect, person, and sandhi when relevant. "
                f"Text: {text}"
            )
            if result:
                return result
        except Exception as exc:
            return {"error": f"Grammar analysis failed: {exc}"}
        return {"explanation": "AI grammar analysis is not configured. Add OPENAI_API_KEY for sentence-level analysis.",
                "iast": ""}

    def is_correct(self, answer, expected):
        return norm(answer) == norm(expected)

    def record_practice(self, lang, correct, prompt):
        self.log(lang, "practice", {"correct": correct, "prompt": prompt})

    def stats(self):
        if self.db == ":memory__":
            return {"attempts": 0, "correct": 0, "accuracy": 0.0}
        with sqlite3.connect(self.db) as conn:
            rows = conn.execute("select payload from events where kind='practice'").fetchall()
        attempts = len(rows)
        correct = sum(1 for (payload,) in rows if json.loads(payload).get("correct"))
        accuracy = (correct / attempts * 100) if attempts else 0.0
        return {"attempts": attempts, "correct": correct, "accuracy": accuracy}
