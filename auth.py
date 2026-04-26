import sqlite3
import bcrypt
import os

DB_PATH = "edu_vision.db"

def init_db():
    """Initialize SQLite tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# Initialize on import
init_db()

def signup(username, email, password):
    """Register a new user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                  (username, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login(username, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        stored_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    return False

def get_user(username):
    """Fetch user details."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, email FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return {"username": result[0], "email": result[1]}
    return None
