# tests/test_pet_controller.py
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.controllers.pet_controller import add_pet_with_image, get_all_pets
from backend.models.pet import Pet

def add_pet_from_input():
    print("🐾 Add a New Pet")
    name = input("Name: ")
    breed = input("Breed: ")
    birthdate = input("Birthdate (YYYY-MM-DD): ")
    image_path = input("Path to image file (optional): ").strip()

    if image_path and os.path.isfile(image_path):
        pet = Pet(id=None, name=name, breed=breed, birthdate=birthdate, image_path=image_path)
        add_pet_with_image(pet, image_path)
        print("✅ Pet and image saved!")
    else:
        print("❌ Image not found — skipping image.")
        pet = Pet(id=None, name=name, breed=breed, birthdate=birthdate)
        from backend.controllers.pet_controller import add_pet
        add_pet(pet)
        print("✅ Pet saved (without image)")


def list_pets():
    print("\n📋 All Pets:")
    for pet in get_all_pets():
        print(f"- {pet}")

def menu():
    while True:
        print("\n=== PetTrackr CLI Test ===")
        print("1. Add Pet")
        print("2. View Pets")
        print("3. Exit")

        choice = input("Choose: ")
        if choice == "1":
            add_pet_from_input()
        elif choice == "2":
            list_pets()
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()