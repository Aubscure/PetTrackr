import os
import sqlite3
import shutil
from backend.models.pet import Pet

# Define base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
DB_PATH = os.path.abspath(os.path.join(DATA_DIR, 'pets.db'))

def add_pet_with_image(pet: Pet, image_src_path: str):
    """
    Adds a new pet and stores its image in the local images folder.

    Args:
        pet (Pet): Pet instance with name, breed, birthdate.
        image_src_path (str): Path to the selected image file.
    """
    os.makedirs(IMAGES_DIR, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Insert initial record (without image path yet)
        cursor.execute('''
            INSERT INTO pets (name, breed, birthdate)
            VALUES (?, ?, ?)
        ''', (pet.name, pet.breed, pet.birthdate))
        pet_id = cursor.lastrowid

        # Rename and move the image
        ext = os.path.splitext(image_src_path)[1]
        safe_name = pet.name.lower().replace(" ", "_")
        new_filename = f"{safe_name}_{pet_id}{ext}"
        dest_path = os.path.join(IMAGES_DIR, new_filename)

        shutil.copyfile(image_src_path, dest_path)
        image_rel_path = os.path.relpath(dest_path, start=os.path.dirname(DB_PATH))

        # Update row with image path
        cursor.execute('''
            UPDATE pets SET image_path = ? WHERE id = ?
        ''', (image_rel_path, pet_id))

        conn.commit()

def get_all_pets():
    """
    Retrieves all pets from the database.

    Returns:
        list[Pet]: A list of Pet instances.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, breed, birthdate, image_path FROM pets')
        rows = cursor.fetchall()
        return [Pet(*row) for row in rows]