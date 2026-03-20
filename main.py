from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    with open("templates/login.html") as f:
        return f.read()

@app.get("/signup-page", response_class=HTMLResponse)
def signup_page():
    with open("templates/signup.html") as f:
        return f.read()

@app.get("/chat-page", response_class=HTMLResponse)
def chat_page():
    with open("templates/chat.html") as f:
        return f.read()