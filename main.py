from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

# Request model
class Question(BaseModel):
    message: str

# Login API
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

# Signup API
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

# Chat page route
@app.get("/chat-page", response_class=HTMLResponse)
def chat_page():
    with open("templates/chat.html") as f:
        return f.read()