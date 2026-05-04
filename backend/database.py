import sqlite3
import os
from datetime import datetime

# Determine the absolute path to the database file within the backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chats.db")

def get_connection():
    # connect to the SQLite database. Check_same_thread=False allows FastAPI to use it across multiple request threads.
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def ensure_session_exists(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO sessions (id) VALUES (?)', (session_id,))
    conn.commit()
    conn.close()

def add_message(session_id: str, role: str, content: str):
    ensure_session_exists(session_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def get_session_messages(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC',
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    # format into dictionary list
    messages = [{"role": row[0], "content": row[1]} for row in rows]
    return messages

def get_all_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all sessions, ordered by most recently created
    cursor.execute('SELECT id FROM sessions ORDER BY created_at DESC')
    session_rows = cursor.fetchall()
    
    sessions = []
    for (sid,) in session_rows:
        # Get the first user message for the summary
        cursor.execute(
            'SELECT content FROM messages WHERE session_id = ? AND role = "user" ORDER BY id ASC LIMIT 1',
            (sid,)
        )
        msg_row = cursor.fetchone()
        summary = msg_row[0] if msg_row else "Previous Session"
        # truncate summary
        if len(summary) > 25:
            summary = summary[:25] + "..."
            
        sessions.append({"session_id": sid, "summary": summary})
        
    conn.close()
    return sessions
