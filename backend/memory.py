# memory.py - SQLite session store and membank
import sqlite3, time, threading, os
DB = "uto_memory.db"
_lock = threading.Lock()

def init_db():
    with _lock:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            meta TEXT,
            created_at REAL
        );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            ts REAL
        );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS membank (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at REAL
        );""")
        conn.commit(); conn.close()

class SessionStore:
    def __init__(self):
        init_db()

    def create_session(self, session_id, user_id, meta=None):
        with _lock:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("INSERT OR REPLACE INTO sessions(session_id, user_id, meta, created_at) VALUES (?, ?, ?, ?)",
                        (session_id, user_id, str(meta), time.time()))
            conn.commit(); conn.close()

    def push_message(self, session_id, role, content):
        with _lock:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("INSERT INTO messages(session_id, role, content, ts) VALUES (?, ?, ?, ?)",
                        (session_id, role, content, time.time()))
            conn.commit(); conn.close()

    def get_history(self, session_id, limit=50):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT role,content,ts FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?", (session_id, limit))
        rows = cur.fetchall()
        conn.close()
        rows.reverse()
        return [{"role": r[0], "content": r[1], "ts": r[2]} for r in rows]

    def membank_set(self, key, value):
        with _lock:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("INSERT OR REPLACE INTO membank(key,value,updated_at) VALUES (?, ?, ?)", (key,str(value), time.time()))
            conn.commit(); conn.close()

    def membank_get(self, key):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT value FROM membank WHERE key=?", (key,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
