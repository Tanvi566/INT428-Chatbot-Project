from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Coding Mentor API is running 🚀"}

class Question(BaseModel):
    message: str

@app.post("/chat")
def chat(q: Question):
    return {"reply": "This is a placeholder response"}