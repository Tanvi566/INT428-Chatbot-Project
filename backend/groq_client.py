import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_ai_response(prompt: str):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
    "model": "llama-3.1-8b-instant",  # ✅ updated model
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3,
    "max_tokens": 300
}

    res = requests.post(url, headers=headers, json=data)

    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)

    if res.status_code != 200:
        return "Error talking to AI"

    return res.json()["choices"][0]["message"]["content"]