# tests/test_pet_controller.py
import sys
import os
from typing import Optional
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.controllers.pet_controller import PetController
from backend.models.pet import Pet, Owner

class PetTrackrCLI:
    """Command-line interface for testing PetController functionality."""
    
    def __init__(self):
        self.controller = PetController()
        self._setup_data_directory()

    def _setup_data_directory(self) -> None:
        """Ensure required data directories exist."""
        os.makedirs(os.path.join('..', 'data', 'images'), exist_ok=True)

    def _get_valid_input(self, prompt: str, validator=None) -> str:
        """Helper for getting validated user input."""
        while True:
            try:
                value = input(prompt).strip()
                if validator:
                    validator(value)
                return value
            except ValueError as e:
                print(f"❌ Invalid input: {e}")

    def _validate_date(self, date_str: str) -> None:
        """Validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    def add_pet_from_input(self) -> None:
        """Handles pet addition via user input."""
        print("🐾 Add a New Pet")
        
        # Pet details
        name = self._get_valid_input("Pet Name: ", lambda x: x or ValueError("Name cannot be empty"))
        breed = self._get_valid_input("Breed: ")
        birthdate = self._get_valid_input(
            "Birthdate (YYYY-MM-DD): ", 
            self._validate_date
        )
        image_path = self._get_valid_input("Path to image file (optional): ").strip() or None

        # Owner details
        print("\n👤 Owner Information")
        owner_name = self._get_valid_input("Owner Name: ", lambda x: x or ValueError("Owner name cannot be empty"))
        contact_number = self._get_valid_input("Contact Number: ")
        address = self._get_valid_input("Address: ")

        # Create instances
        pet = Pet(
            id=None, 
            name=name, 
            breed=breed or None, 
            birthdate=birthdate, 
            image_path=None
        )
        owner = Owner(
            id=None,
            name=owner_name,
            contact_number=contact_number or None,
            address=address or None
        )

        # Handle image
        if image_path and not os.path.isfile(image_path):
            print("❌ Image not found — saving without image.")
            image_path = None

        try:
            self.controller.add_pet_with_owner(pet, owner, image_path)
            print("✅ Pet and owner saved successfully!")
        except Exception as e:
            print(f"❌ Error saving pet: {e}")

    def list_pets(self) -> None:
        """Displays all pets with owner information."""
        print("\n📋 All Pets with Owners:")
        
        try:
            pets, owners = self.controller.get_pets_with_owners()
            
            if not pets:
                print("No pets found in database")
                return
            
            for pet, owner in zip(pets, owners):
                print(f"\n- {pet}")
                print(f"  Owner: {owner}" if owner else "  Owner: No owner information")
                
        except Exception as e:
            print(f"❌ Error retrieving pets: {e}")

    def run(self) -> None:
        """Main menu loop."""
        while True:
            print("\n=== PetTrackr CLI Test ===")
            print("1. Add Pet")
            print("2. View Pets")
            print("3. Exit")

            choice = input("Choose: ").strip()
            
            if choice == "1":
                self.add_pet_from_input()
            elif choice == "2":
                self.list_pets()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        cli = PetTrackrCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")