# tests/test_pet_controller.py
import sys, os
from datetime import datetime
import random
import string
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controllers.pet_controller import PetController
from backend.models.pet import Pet, Owner
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController
from backend.services.daycare_prices import compute_total_fee

class PetTrackrCLI:
    def __init__(self):
        self.controller, self.vet_visit_controller = PetController(), VetVisitController()
        self.vaccination_controller, self.feeding_log_controller = VaccinationController(), FeedingLogController()
        os.makedirs(os.path.join('..', 'data', 'images'), exist_ok=True)

    def _get_valid_input(self, prompt, validator=None):
        while True:
            try:
                v = input(prompt).strip()
                if validator: validator(v)
                return v
            except ValueError as e:
                print(f"❌ Invalid input: {e}")

    def _validate_date(self, s): datetime.strptime(s, "%Y-%m-%d")

    def add_pet_from_input(self):
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
        if image_path and not os.path.isfile(image_path): print("❌ Image not found — saving without image."); image_path = None
        try:
            pet_id = self.controller.add_pet_with_owner(pet, owner, image_path)
            print("\n✅ Pet and owner saved successfully!")
            self.view_pet_profile(pet_id)
        except Exception as e:
            print(f"❌ Error saving pet: {e}")

    def list_pets(self):
        print("\n📋 All Pets with Owners:")
        try:
            pets, owners = self.controller.get_pets_with_owners()
            if not pets: print("No pets found in database"); return
            for i, (pet, owner) in enumerate(zip(pets, owners), 1):
                print(f"\n{i}. {pet}\n   Owner: {owner if owner else 'No owner information'}")
            while True:
                choice = input("\nEnter pet number to view profile (or 'back' to return): ").strip().lower()
                if choice == 'back': return
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(pets): self.view_pet_profile(pets[idx].id); return
                    print("❌ Invalid pet number")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
        except Exception as e:
            print(f"❌ Error retrieving pets: {e}")

    def view_pet_profile(self, pet_id):
        try:
            pet, owner = self.controller.get_pet_by_id(pet_id)
            if not pet: print(f"❌ Pet with ID {pet_id} not found"); return
            while True:
                print("\n" + "="*40 + f"\n🐾 {pet.name}'s Profile\n" + "="*40)
                print(f"Breed: {pet.breed}\nBirthdate: {pet.birthdate}")
                if pet.image_path and os.path.exists(os.path.join(self.controller.data_dir, pet.image_path)):
                    print(f"Image: {pet.image_path}")
                if owner: print(f"\n👤 Owner Information:\nName: {owner.name}\nContact: {owner.contact_number}\nAddress: {owner.address}")
                for label, ctrl, attr, fmt in [
                    ("🩺 Vet Visits", self.vet_visit_controller, "get_by_pet_id", lambda v: f"  - {v.visit_date}: {v.reason}" + (f"\n    Notes: {v.notes}" if v.notes else "")),
                    ("💉 Vaccinations", self.vaccination_controller, "get_by_pet_id", lambda v: f"  - {v.vaccine_name} (Administered: {v.date_administered}, Next Due: {v.next_due})"),
                    ("🍖 Feeding Logs", self.feeding_log_controller, "get_by_pet_id", None),
                ]:
                    try:
                        items = getattr(ctrl, attr)(pet_id)
                        if items:
                            print(f"\n{label}:")
                            if label == "🍖 Feeding Logs":
                                print("  --- Feeding Log Receipt ---")
                                total = 0
                                for v in items:
                                    plan = ", ".join([desc for desc, flag in [("Once", v.feed_once), ("Twice", v.feed_twice), ("Thrice", v.feed_thrice)] if flag]) or "No feeding"
                                    # Compute fee breakdown
                                    base = 350
                                    if v.feed_once:
                                        addon = 85
                                        plan_desc = "Once"
                                    elif v.feed_twice:
                                        addon = 170
                                        plan_desc = "Twice"
                                    elif v.feed_thrice:
                                        addon = 255
                                        plan_desc = "Thrice"
                                    else:
                                        addon = 0
                                        plan_desc = "No feeding"
                                    fee = v.num_days * (base + addon)
                                    total += fee
                                    print(f"  - {v.start_date} | {v.num_days} day(s) | Plan: {plan}")
                                    print(f"    Breakdown: {v.num_days} x (₱{base} base + ₱{addon} feeding) = ₱{fee}")
                                print("  --------------------------")
                                print(f"  TOTAL FEEDING INVOICE: ₱{total}")
                            else:
                                [print(fmt(v)) for v in items]
                    except Exception as e:
                        print(f"\n⚠️ Could not load {label.lower()}: {str(e)}")
                print("\nOptions:\n1. Add Vet Visit\n2. Add Vaccination\n3. Add Feeding Log\n4. Back to Menu")
                choice = input("\nChoose an option: ").strip()
                if choice == "1": self._add_vet_visit(pet.id)
                elif choice == "2": self._add_vaccination(pet.id)
                elif choice == "3": self._add_feeding_log(pet.id)
                elif choice == "4": return
                else: print("❌ Invalid choice. Please try again.")
        except Exception as e:
            print(f"❌ Error accessing pet profile: {e}")

    def _add_vet_visit(self, pet_id):
        print("\n🩺 Add Vet Visit")
        data = {
            "pet_id": pet_id,
            "visit_date": self._get_valid_input("Visit Date (YYYY-MM-DD): ", self._validate_date),
            "reason": input("Reason: "),
            "notes": input("Notes (optional): ")
        }
        self.vet_visit_controller.create(data)
        print("✅ Vet Visit saved.")

    def _add_vaccination(self, pet_id):
        print("\n💉 Add Vaccination")
        data = {
            "pet_id": pet_id,
            "vaccine_name": input("Vaccine Name: "),
            "date_administered": self._get_valid_input("Date Administered (YYYY-MM-DD): ", self._validate_date),
            "next_due": self._get_valid_input("Next Due Date (YYYY-MM-DD): ", self._validate_date)
        }
        self.vaccination_controller.create(data)
        print("✅ Vaccination saved.")

    def _add_feeding_log(self, pet_id):
        print("\n🍖 Add Feeding Log (Daycare Enrollment)")
        start_date = self._get_valid_input("Start Date (YYYY-MM-DD): ", self._validate_date)
        while True:
            try:
                num_days = int(self._get_valid_input("Number of days: ", lambda x: int(x) > 0 or ValueError("Must be positive")))
                break
            except ValueError:
                print("❌ Please enter a valid positive integer for days.")
        print("Feeding Plan:\n1. Once a day\n2. Twice a day\n3. Thrice a day\n4. No feeding")
        feed_choice = self._get_valid_input("Choose feeding plan (1/2/3/4): ", lambda x: x in {"1", "2", "3", "4"})
        feed_once = feed_choice == "1"
        feed_twice = feed_choice == "2"
        feed_thrice = feed_choice == "3"
        # Compute total fee
        total_fee = compute_total_fee(num_days, feed_once, feed_twice, feed_thrice)
        print(f"💰 Total Fee: ₱{total_fee}")
        data = {
            "pet_id": pet_id,
            "start_date": start_date,
            "num_days": num_days,
            "feed_once": feed_once,
            "feed_twice": feed_twice,
            "feed_thrice": feed_thrice
        }
        self.feeding_log_controller.create(data)
        print("✅ Feeding log saved.")

    def _random_string(self, length=6):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def _random_phone(self):
        return '09' + ''.join(random.choices(string.digits, k=9))

    def _random_date(self, start_year=2015, end_year=2024):
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year:04d}-{month:02d}-{day:02d}"

    def add_random_pet(self):
        name = self._random_string()
        breed = random.choice(['Shih Tzu', 'Poodle', 'Bulldog', 'Aspin'])
        birthdate = self._random_date(2015, 2022)
        image_path = None
        owner_name = self._random_string()
        contact_number = self._random_phone()
        address = f"{random.randint(1,999)} {self._random_string(8)} St."
        pet = Pet(id=None, name=name, breed=breed, birthdate=birthdate, image_path="")
        owner = Owner(id=None, name=owner_name, contact_number=contact_number, address=address)
        try:
            pet_id = self.controller.add_pet_with_owner(pet, owner, image_path)
            print(f"\n✅ Random pet and owner saved! Pet ID: {pet_id}")
            self._add_random_feeding_log(pet_id)
        except Exception as e:
            print(f"❌ Error saving random pet: {e}")

    def _add_random_feeding_log(self, pet_id):
        start_date = self._random_date(2024, 2025)
        num_days = random.randint(1, 14)
        feed_plan = random.choice([1, 2, 3, 4])
        feed_once = feed_plan == 1
        feed_twice = feed_plan == 2
        feed_thrice = feed_plan == 3
        total_fee = compute_total_fee(num_days, feed_once, feed_twice, feed_thrice)
        print(f"Random Feeding Log: {num_days} days, plan {feed_plan}, fee ₱{total_fee}")
        data = {
            "pet_id": pet_id,
            "start_date": start_date,
            "num_days": num_days,
            "feed_once": feed_once,
            "feed_twice": feed_twice,
            "feed_thrice": feed_thrice
        }
        self.feeding_log_controller.create(data)
        print("✅ Random feeding log saved.")

    def run(self):
        menu = {
            "1": self.add_pet_from_input,
            "2": self.list_pets,
            "3": lambda: exit(print("Goodbye!")),
            "4": self.add_random_pet  # Add this line for random input
        }
        while True:
            print("\n=== PetTrackr Main Menu ===\n1. Add Pet\n2. View Pets\n3. Exit\n4. Add Random Pet")
            menu.get(input("\nChoose an option: ").strip(), lambda: print("❌ Invalid choice. Please try again."))()

if __name__ == "__main__":
    try:
        PetTrackrCLI().run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")