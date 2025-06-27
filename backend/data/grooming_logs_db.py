import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

def init_grooming_logs_db():
    db_path = os.path.join(DATA_DIR, 'grooming_logs.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grooming_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            groom_date TEXT,
            service_type TEXT,
            groomer_name TEXT,
            notes TEXT
        )
    ''')


    conn.commit()
    conn.close()

# Optional: Run this directly
if __name__ == "__main__":
    init_grooming_logs_db()