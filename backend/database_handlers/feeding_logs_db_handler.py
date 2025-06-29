# File: backend/database/feeding_logs_db_handler.py
import sqlite3
import os
from backend.models.feeding_log import FeedingLog

class FeedingLogDB:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', 'data', 'feeding_logs.db')

    def connect(self):
        return sqlite3.connect(self.db_path)

    def insert(self, log: FeedingLog):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO feeding_logs (pet_id, feed_time, food_type, notes)
                VALUES (?, ?, ?, ?)
                """,
                (log.pet_id, log.feed_time, log.food_type, log.notes)
            )
            conn.commit()
            return cursor.lastrowid

    def update(self, log: FeedingLog):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE feeding_logs
                SET pet_id = ?, feed_time = ?, food_type = ?, notes = ?
                WHERE id = ?
                """,
                (log.pet_id, log.feed_time, log.food_type, log.notes)
            )
            conn.commit()

    def get_by_pet_id(self, pet_id: int) -> list[FeedingLog]:
        """Get all feeding logs for a specific pet ID"""
        with self.connect() as conn:
            cursor = conn.cursor()
            # Removed the pet existence check since it's causing errors
            cursor.execute("""
                SELECT pet_id, feed_time, food_type, notes
                FROM feeding_logs
                WHERE pet_id = ?
                ORDER BY feed_time DESC
            """, (pet_id,))
            return [FeedingLog(*row) for row in cursor.fetchall()]

    def delete(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM feeding_logs WHERE id = ?", (record_id,))
            conn.commit()

    def fetch_by_id(self, record_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM feeding_logs WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            return FeedingLog(*row) if row else None

    def fetch_all(self, pet_id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM feeding_logs WHERE pet_id = ? ORDER BY feed_time DESC", (pet_id,))
            return [FeedingLog(*row) for row in cursor.fetchall()]