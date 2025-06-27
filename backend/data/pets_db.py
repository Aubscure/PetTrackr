import sqlite3
import os

class PetDatabaseInitializer:
    """
    Handles initialization of the pets.db database and creation of the pets table.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, '..', 'data')
        self.db_path = os.path.join(self.data_dir, 'pets.db')

    def initialize(self):
        """Creates the pets table if it does not already exist."""
        os.makedirs(self.data_dir, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    breed TEXT,
                    birthdate TEXT,
                    image_path TEXT
                )
            ''')

            conn.commit()

# Optional standalone run
if __name__ == "__main__":
    PetDatabaseInitializer().initialize()