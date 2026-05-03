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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key
API_KEY = os.getenv("CHAT_API_KEY")
print("Loaded API KEY:", API_KEY)

# 🧠 In-memory chat sessions
chat_sessions = {}

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

    session_id = x_api_key  # simple session handling

    # Initialize session if not exists
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

        # 👇 Add system prompt ONCE per session
        chat_sessions[session_id].append({
            "role": "system",
            "content": build_prompt("You are initialized.")
        })

    # Add user message
    chat_sessions[session_id].append({
        "role": "user",
        "content": data.query
    })

    print("USER:", data.query)

    # Optional: limit history (prevents token explosion)
    if len(chat_sessions[session_id]) > 12:
        chat_sessions[session_id] = chat_sessions[session_id][-12:]

    # Get AI response with full history
    response = get_ai_response(chat_sessions[session_id])

    # Add AI response to history
    chat_sessions[session_id].append({
        "role": "assistant",
        "content": response
    })

    print("AI:", response)

    return {"response": response}