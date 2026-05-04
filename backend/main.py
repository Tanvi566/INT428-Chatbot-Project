from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Import the updated Groq client and prompts
from groq_client import call_groq_api
from prompts import ACADEMIC_SYSTEM_PROMPT, QUIZ_SYSTEM_PROMPT, CODE_SYSTEM_PROMPT
from database import create_tables, add_message, get_session_messages, get_all_sessions

app = FastAPI(title="Academic CS Assistant API (Groq Powered)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_tables()

# IMPORTANT: Paste your Groq API Key here (starts with gsk_...)
DEFAULT_GROQ_KEY = os.environ.get("GROQ_API_KEY", "") 

class ChatRequest(BaseModel):
    message: str
    session_id: str
    mode: str

class QuizRequest(BaseModel):
    syllabus: str
    type: str
    level: str
    session_id: str

class CodeRequest(BaseModel):
    prompt: str
    language: str
    session_id: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest, x_api_key: str = Header(None)):
    # Check for API key
    api_key = x_api_key if x_api_key and x_api_key != "demo" else DEFAULT_GROQ_KEY
    
    if not api_key:
        return {"response": "⚠️ **API Key Missing!** Please add your Groq API key in `main.py` (line 21) to make me hear you again."}
    
    # Save user message to database
    add_message(req.session_id, "user", req.message)
    
    # Fetch full history for the session
    history = get_session_messages(req.session_id)
    
    messages = [{"role": "system", "content": ACADEMIC_SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    # Inject the Mode instructions into the final user message for Groq
    if messages and messages[-1]["role"] == "user":
        messages[-1]["content"] = f"Mode: {req.mode}\n\nQuestion: {messages[-1]['content']}"
    
    response = await call_groq_api(messages, api_key=api_key)
    
    # Save the assistant's response to the database
    add_message(req.session_id, "assistant", response)
    
    return {"response": response}

@app.get("/sessions")
async def get_sessions():
    return {"sessions": get_all_sessions()}

@app.get("/sessions/{session_id}")
async def get_session_history(session_id: str):
    return {"messages": get_session_messages(session_id)}

@app.post("/quiz")
async def quiz_endpoint(req: QuizRequest, x_api_key: str = Header(None)):
    api_key = x_api_key if x_api_key and x_api_key != "demo" else DEFAULT_GROQ_KEY
    
    if not api_key:
        return {"response": "⚠️ **API Key Missing!** Add your key to generate quizzes."}

    prompt = f"Generate a {req.level} level {req.type} quiz for these topics: {req.syllabus}"
    messages = [
        {"role": "system", "content": QUIZ_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    response = await call_groq_api(messages, api_key=api_key)
    return {"response": response}

@app.post("/code")
async def code_endpoint(req: CodeRequest, x_api_key: str = Header(None)):
    api_key = x_api_key if x_api_key and x_api_key != "demo" else DEFAULT_GROQ_KEY
    
    if not api_key:
        return {"response": "⚠️ **API Key Missing!** Add your key to generate code."}

    prompt = f"Language: {req.language}\n\nTask: {req.prompt}"
    messages = [
        {"role": "system", "content": CODE_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    response = await call_groq_api(messages, api_key=api_key)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    # Make sure to run the script using: python main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)