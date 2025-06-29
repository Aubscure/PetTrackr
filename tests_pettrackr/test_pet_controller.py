# tests/test_pet_controller.py
import sys
import os
from typing import Optional
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controllers.pet_controller import PetController
from backend.models.pet import Pet, Owner
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController

class PetTrackrCLI:
    def __init__(self):
        self.controller = PetController()
        self.vet_visit_controller = VetVisitController()
        self.vaccination_controller = VaccinationController()
        self.feeding_log_controller = FeedingLogController()
        self._setup_data_directory()

    def _setup_data_directory(self) -> None:
        os.makedirs(os.path.join('..', 'data', 'images'), exist_ok=True)

    def _get_valid_input(self, prompt: str, validator=None) -> str:
        while True:
            try:
                value = input(prompt).strip()
                if validator:
                    validator(value)
                return value
            except ValueError as e:
                print(f"❌ Invalid input: {e}")

    def _validate_date(self, date_str: str) -> None:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    def add_pet_from_input(self) -> None:
        print("\n🐾 Add a New Pet")
        name = self._get_valid_input("Pet Name: ", lambda x: x or ValueError("Name cannot be empty"))
        breed = self._get_valid_input("Breed: ")
        birthdate = self._get_valid_input("Birthdate (YYYY-MM-DD): ", self._validate_date)
        image_path = self._get_valid_input("Path to image file (optional): ").strip() or None

        print("\n👤 Owner Information")
        owner_name = self._get_valid_input("Owner Name: ", lambda x: x or ValueError("Owner name cannot be empty"))
        contact_number = self._get_valid_input("Contact Number: ")
        address = self._get_valid_input("Address: ")

        pet = Pet(id=None, name=name, breed=breed or "", birthdate=birthdate, image_path="")
        owner = Owner(id=None, name=owner_name, contact_number=contact_number or "", address=address or "")

        if image_path and not os.path.isfile(image_path):
            print("❌ Image not found — saving without image.")
            image_path = None

        try:
            pet_id = self.controller.add_pet_with_owner(pet, owner, image_path)  # Capture the returned pet_id
            print("\n✅ Pet and owner saved successfully!")
            self.view_pet_profile(pet_id)  # Use the returned pet_id
        except Exception as e:
            print(f"❌ Error saving pet: {e}")

    def list_pets(self) -> None:
        print("\n📋 All Pets with Owners:")
        try:
            pets, owners = self.controller.get_pets_with_owners()
            if not pets:
                print("No pets found in database")
                return
            for i, (pet, owner) in enumerate(zip(pets, owners), 1):
                print(f"\n{i}. {pet}")
                print(f"   Owner: {owner}" if owner else "   Owner: No owner information")
            
            # Allow selecting a pet to view its profile
            while True:
                choice = input("\nEnter pet number to view profile (or 'back' to return): ").strip().lower()
                if choice == 'back':
                    return
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(pets):
                        self.view_pet_profile(pets[index].id)  # Pass ID instead of name
                        return
                    else:
                        print("❌ Invalid pet number")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
        except Exception as e:
            print(f"❌ Error retrieving pets: {e}")

    def view_pet_profile(self, pet_id: int) -> None:
        try:
            # Get pet and owner information
            pet, owner = self.controller.get_pet_by_id(pet_id)
            
            if not pet:
                print(f"❌ Pet with ID {pet_id} not found")
                return
                
            while True:
                print("\n" + "="*40)
                print(f"🐾 {pet.name}'s Profile")
                print("="*40)
                print(f"Breed: {pet.breed}")
                print(f"Birthdate: {pet.birthdate}")
                if pet.image_path and os.path.exists(os.path.join(self.controller.data_dir, pet.image_path)):
                    print(f"Image: {pet.image_path}")
                if owner:
                    print("\n👤 Owner Information:")
                    print(f"Name: {owner.name}")
                    print(f"Contact: {owner.contact_number}")
                    print(f"Address: {owner.address}")
                
                # Display vet visits
                try:
                    vet_visits = self.vet_visit_controller.get_by_pet_id(pet_id)
                    if vet_visits:
                        print("\n🩺 Vet Visits:")
                        for visit in vet_visits:
                            print(f"  - {visit.visit_date}: {visit.reason}")
                            if visit.notes:
                                print(f"    Notes: {visit.notes}")
                except Exception as e:
                    print(f"\n⚠️ Could not load vet visits: {str(e)}")
                
                # Display vaccinations
                try:
                    vaccinations = self.vaccination_controller.get_by_pet_id(pet_id)
                    if vaccinations:
                        print("\n💉 Vaccinations:")
                        for vaccine in vaccinations:
                            print(f"  - {vaccine.vaccine_name} (Administered: {vaccine.date_administered}, Next Due: {vaccine.next_due})")
                except Exception as e:
                    print(f"\n⚠️ Could not load vaccinations: {str(e)}")
                
                # Display feeding logs
                try:
                    feeding_logs = self.feeding_log_controller.get_by_pet_id(pet_id)
                    if feeding_logs:
                        print("\n🍖 Feeding Logs:")
                        for log in feeding_logs:
                            print(f"  - {log.feed_time}: {log.food_type}")
                            if log.notes:
                                print(f"    Notes: {log.notes}")
                except Exception as e:
                    print(f"\n⚠️ Could not load feeding logs: {str(e)}")
                
                print("\nOptions:")
                print("1. Add Vet Visit")
                print("2. Add Vaccination")
                print("3. Add Feeding Log")
                print("4. Back to Menu")
                
                choice = input("\nChoose an option: ").strip()
                
                if choice == "1":
                    self._add_vet_visit(pet.id)
                elif choice == "2":
                    self._add_vaccination(pet.id)
                elif choice == "3":
                    self._add_feeding_log(pet.id)
                elif choice == "4":
                    return
                else:
                    print("❌ Invalid choice. Please try again.")
                    
        except Exception as e:
            print(f"❌ Error accessing pet profile: {e}")

    def _add_vet_visit(self, pet_id: int) -> None:
        print("\n🩺 Add Vet Visit")
        visit_date = self._get_valid_input("Visit Date (YYYY-MM-DD): ", self._validate_date)
        reason = input("Reason: ")
        notes = input("Notes (optional): ")
        data = {"pet_id": pet_id, "visit_date": visit_date, "reason": reason, "notes": notes}
        self.vet_visit_controller.create(data)
        print("✅ Vet Visit saved.")

    def _add_vaccination(self, pet_id: int) -> None:
        print("\n💉 Add Vaccination")
        name = input("Vaccine Name: ")
        date_admin = self._get_valid_input("Date Administered (YYYY-MM-DD): ", self._validate_date)
        next_due = self._get_valid_input("Next Due Date (YYYY-MM-DD): ", self._validate_date)
        data = {"pet_id": pet_id, "vaccine_name": name, "date_administered": date_admin, "next_due": next_due}
        self.vaccination_controller.create(data)
        print("✅ Vaccination saved.")

    def _add_feeding_log(self, pet_id: int) -> None:
        print("\n🍖 Add Feeding Log")
        feed_time = self._get_valid_input("Feed Time (YYYY-MM-DD HH:MM): ")
        food_type = input("Food Type: ")
        notes = input("Notes (optional): ")
        data = {"pet_id": pet_id, "feed_time": feed_time, "food_type": food_type, "notes": notes}
        self.feeding_log_controller.create(data)
        print("✅ Feeding log saved.")

    def run(self) -> None:
        while True:
            print("\n=== PetTrackr Main Menu ===")
            print("1. Add Pet")
            print("2. View Pets")
            print("3. Exit")

            choice = input("\nChoose an option: ").strip()

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