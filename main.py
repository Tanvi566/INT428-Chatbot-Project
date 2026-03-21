from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Request model
class Question(BaseModel):
    message: str


# ------------------ AUTH APIs ------------------

@app.post("/signup")
def signup(q: Question):
    username, password = q.message.split(",")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return {"message": "User registered successfully"}
    except:
        return {"message": "Username already exists"}
    finally:
        conn.close()


@app.post("/login")
def login(q: Question):
    username, password = q.message.split(",")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}


# ------------------ PAGE ROUTES ------------------

@app.get("/signup-page", response_class=HTMLResponse)
def signup_page():
    with open("templates/signup.html") as f:
        return f.read()


@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    with open("templates/login.html") as f:
        return f.read()


@app.get("/chat-page", response_class=HTMLResponse)
def chat_page():
    with open("templates/chat.html") as f:
        return f.read()


# ------------------ ROOT ------------------

@app.get("/")
def home():
    return {"message": "AI Coding Mentor API is running"}