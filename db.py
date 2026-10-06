import sqlite3
from datetime import datetime

DB_NAME = 'trends.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trend_runs
                 (id INTEGER PRIMARY KEY, niche TEXT, topic TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def log_run(niche, topic):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO trend_runs (niche, topic, timestamp) VALUES (?, ?, ?)",
              (niche, topic, datetime.now().isoformat()))
    conn.commit()
    conn.close()
