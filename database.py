import sqlite3
import hashlib

def create_tables():
    conn = sqlite3.connect('event.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        date TEXT,
        location TEXT
    )''')

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_event(title, desc, date, location):
    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    c.execute("INSERT INTO events (title, description, date, location) VALUES (?, ?, ?, ?)",
              (title, desc, date, location))
    conn.commit()
    conn.close()

def get_events(filter_term=""):
    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    if filter_term:
        c.execute("SELECT * FROM events WHERE title LIKE ?", ('%' + filter_term + '%',))
    else:
        c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return events
