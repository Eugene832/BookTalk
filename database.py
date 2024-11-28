import sqlite3
import hashlib

db_name = "files/authorisation.db"
sekretKey = "3fac1504251a027465981346fb5b0d57d398e4df4a03253a4c7d1926e40e9907"

def getHash(s):
    s += sekretKey
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    text TEXT NOT NULL
    );
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
    sha256Hash = getHash(password)
    cursor.execute("""
    INSERT INTO dictionary (key, value) VALUES (?, ?)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (username, sha256Hash))
    conn.commit()
    
init()