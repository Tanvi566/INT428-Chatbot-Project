from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from .groq_client import get_ai_response
from .prompts import build_prompt

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS (so your frontend doesn't silently betray you)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from .env
API_KEY = os.getenv("CHAT_API_KEY")

print("Loaded API KEY:", API_KEY)  # Debug (optional)

# Request schema
class ChatRequest(BaseModel):
    query: str

# API key verification
def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Chat endpoint
@app.post("/chat")
def chat(data: ChatRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    # Debug logs (SAFE here)
    print("USER:", data.query)

    prompt = build_prompt(data.query)
    response = get_ai_response(prompt)

    print("AI:", response)

    return {"response": response}