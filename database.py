import sqlite3
import hashlib

db_name = "files/authorisation.db"

def getHash(s):
    return hashlib.sha256(s.encode()).hexdigest()

def init():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dictionary (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    conn.commit()    

def getPasswordHash(username):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT value FROM dictionary WHERE key = ?
    """, (username,))
    result = cursor.fetchone()
    return result[0] if result else None    

def setPassword(username, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()    
    sha256Hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("""
    INSERT INTO dictionary (key, value) VALUES (?, ?)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (username, sha256Hash))
    conn.commit()
    
init()