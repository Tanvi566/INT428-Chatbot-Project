from chatbot import get_response
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import sqlite3
import database

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
        return {"message": "Login successful", "username": username}
    else:
        return {"message": "Invalid credentials"}

@app.post("/chat")
def chat(q: Question):
    full_message = q.message

    # Extract username and actual message
    try:
        username, user_message = full_message.split(":", 1)
    except:
        return {"reply": "Invalid message format"}

    from chatbot import get_response
    reply = get_response(user_message)

    # SAVE CHAT
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (username, message, response) VALUES (?, ?, ?)",
        (username, user_message, reply)
    )

    conn.commit()
    conn.close()

    return {"reply": reply}

# ------------------ PAGE ROUTES ------------------

@app.get("/signup-page", response_class=HTMLResponse)
def signup_page():
    with open("templates/signup.html") as f:
        return f.read()


@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    with open("templates/login.html") as f:
        return f.read()


from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/chat-page", response_class=HTMLResponse)
def chat_page(request: Request):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # TEMP: show all chats (we'll filter later)
    cursor.execute("SELECT message, response FROM chats")
    chats = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chats": chats
    })


# ------------------ ROOT ------------------

@app.get("/")
def home():
    return {"message": "AI Coding Mentor API is running"}