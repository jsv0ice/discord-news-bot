import sqlite3
from config import DB_STRING

def initialize_db():
    with sqlite3.connect(DB_STRING) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                          (channel TEXT NOT NULL, sub TEXT NOT NULL)''')
    conn.commit()
