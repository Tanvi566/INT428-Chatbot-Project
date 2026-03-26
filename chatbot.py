import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

SYSTEM_PROMPT = """
You are a cybersecurity expert chatbot.

Only answer questions about:
- Cybersecurity
- Phishing
- Scams
- Password safety
- Online threats

If question is unrelated, say:
"I can only answer cybersecurity-related questions."

Keep answers simple.
"""

def is_cyber(text):
    keywords = ["phishing", "scam", "hack", "password", "otp", "fraud", "malware"]
    return any(k in text.lower() for k in keywords)

def get_response(user_input):
    if not is_cyber(user_input):
        return "Please ask cybersecurity-related questions."

    prompt = SYSTEM_PROMPT + "\nUser: " + user_input

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    try:
        return response.json()[0]["generated_text"]
    except:
        return "Error generating response."