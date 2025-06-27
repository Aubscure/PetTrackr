import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

def init_health_notes_db():
    db_path = os.path.join(DATA_DIR, 'health_notes.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            date_logged TEXT,
            symptom TEXT,
            severity TEXT,
            comment TEXT
        )
    ''')



    conn.commit()
    conn.close()

# Optional: Run this directly
if __name__ == "__main__":
    init_health_notes_db()