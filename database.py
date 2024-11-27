import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="files/authorisation.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS dictionary (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        self.conn.commit()

    def setPassword(self, login, password):
        sha256Hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("""
        INSERT INTO dictionary (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (login, sha256Hash))
        self.conn.commit()

    def getHash(self, login):
        self.cursor.execute("""
        SELECT value FROM dictionary WHERE key = ?
        """, (login,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()

database = Database()
database.setPassword("example", "password")
print(database.getHash("example"))