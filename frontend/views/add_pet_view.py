# frontend/views/add_pet_view.py
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
from backend.models.pet import Pet, Owner
from backend.models.vet_visit import VetVisit
from backend.models.vaccination import Vaccination
from backend.models.feeding_log import FeedingLog
from backend.controllers.pet_controller import PetController
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController
from frontend.components.floating_placeholder_entry import FloatingPlaceholderEntry
from frontend.components.image_uploader import ImageUploader
from frontend.style.style import (
    create_button, create_label, create_frame, 
    get_title_font, get_subtitle_font, create_back_button
)

def create_add_pet_view(parent, show_frame):
    # Clear existing widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Main container setup
    container = create_frame(parent)
    container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)
    container.grid_columnconfigure((0, 1), weight=1)

    # Header
    create_label(container, "➕ Add New Pet", font=get_title_font()).grid(row=0, column=0, columnspan=2, pady=(30, 15))

    # Left side - Image uploader
    left_frame = create_frame(container)
    left_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    image_uploader = ImageUploader(left_frame)
    image_uploader.pack(pady=(0, 10), fill="both", expand=True)

    # Right side - Form and buttons
    right_frame = create_frame(container)
    right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

    # Notebook setup
    notebook = ctk.CTkTabview(right_frame)
    notebook.pack(padx=10, pady=10, fill="both", expand=True)
    pet_tab = notebook.add("Pet Details")
    owner_tab = notebook.add("Owner Details")
    medical_tab = notebook.add("Medical Records")

    # Pet form fields
    name_entry = FloatingPlaceholderEntry(pet_tab, "Pet Name")
    name_entry.pack(pady=8, fill="x")

    breed_entry = FloatingPlaceholderEntry(pet_tab, "Breed (optional)")
    breed_entry.pack(pady=8, fill="x")

    # Birthdate field
    bdate_frame = create_frame(pet_tab)
    bdate_frame.pack(pady=8, fill="x")
    create_label(bdate_frame, "Birthdate", font=get_subtitle_font()).pack(anchor="w")
    bdate_entry = DateEntry(bdate_frame, width=26, date_pattern="yyyy-mm-dd",
                          background="#3b8ed0", foreground="white", borderwidth=2)
    bdate_entry.pack(pady=8, ipady=4, fill="x")

    # Owner form fields
    owner_name_entry = FloatingPlaceholderEntry(owner_tab, "Owner Name")
    owner_name_entry.pack(pady=8, fill="x")

    owner_phone_entry = FloatingPlaceholderEntry(owner_tab, "Contact Number")
    owner_phone_entry.pack(pady=8, fill="x")

    owner_address_entry = FloatingPlaceholderEntry(owner_tab, "Address")
    owner_address_entry.pack(pady=8, fill="x")

    # Medical Records Tab
    medical_notebook = ctk.CTkTabview(medical_tab)
    medical_notebook.pack(fill="both", expand=True, padx=5, pady=5)

    # Helper function to create medical record sections
    def create_medical_section(tab_name, fields):
        tab = medical_notebook.add(tab_name)
        entries = {}

        for field in fields:
            if field["type"] == "date":
                frame = create_frame(tab)
                frame.pack(pady=5, fill="x")
                create_label(frame, field["label"], font=get_subtitle_font()).pack(anchor="w")
                entry = DateEntry(frame, width=26, date_pattern="yyyy-mm-dd", 
                                background="#3b8ed0", foreground="white", borderwidth=2)
                entry.pack(pady=5, fill="x")
                entries[field["name"]] = entry
            elif field["type"] == "textbox":
                entry = ctk.CTkTextbox(tab, height=80, wrap="word")
                entry.pack(pady=8, fill="x")
                entry.insert("0.0", field.get("placeholder", ""))
                entry.bind("<FocusIn>", lambda e, w=entry, p=field.get("placeholder", ""): 
                         w.delete("0.0", "end") if w.get("0.0", "end").strip() == p else None)
                entries[field["name"]] = entry
            else:
                entry = FloatingPlaceholderEntry(tab, field["label"])
                entry.pack(pady=8, fill="x")
                entries[field["name"]] = entry

        return entries

    # Vet Visits
    vet_entries = create_medical_section("Vet Visits", [
        {"name": "visit_date", "label": "Visit Date", "type": "date"},
        {"name": "reason", "label": "Reason for Visit", "type": "entry"},
        {"name": "notes", "label": "Notes", "type": "textbox", "placeholder": "Notes (optional)"}
    ])

    # Vaccinations
    vax_entries = create_medical_section("Vaccinations", [
        {"name": "vaccine_name", "label": "Vaccine Name", "type": "entry"},
        {"name": "date_administered", "label": "Date Administered", "type": "date"},
        {"name": "next_due", "label": "Next Due Date", "type": "date"}
    ])

    # Feeding Logs
    feed_entries = create_medical_section("Feeding Logs", [
        {"name": "food_type", "label": "Food Type", "type": "entry"},
        {"name": "feed_time", "label": "Feeding Time", "type": "entry"},
        {"name": "notes", "label": "Notes", "type": "textbox", "placeholder": "Notes (optional)"}
    ])
    feed_entries["feed_time"].insert(0, datetime.now().strftime("%H:%M"))

    # Medical records storage
    records = {"vet_visits": [], "vaccinations": [], "feeding_logs": []}

    # Button actions
    def add_record(record_type, entries, required_fields, success_msg):
        data = {}
        for name, entry in entries.items():
            if hasattr(entry, "get"):
                if isinstance(entry, ctk.CTkTextbox):
                    data[name] = entry.get("0.0", "end").strip()
                else:
                    data[name] = entry.get()
            else:
                data[name] = entry.get("0.0", "end").strip()
        if not all(data[field] for field in required_fields):
            messagebox.showwarning("Missing Info", f"Please fill all required fields.")
            return

        records[record_type].append(data)
        messagebox.showinfo("Added", success_msg)
        for entry in entries.values():
            if isinstance(entry, ctk.CTkTextbox):
                entry.delete("0.0", "end")
                entry.insert("0.0", "Notes (optional)" if record_type != "feeding_logs" else "")
            elif isinstance(entry, DateEntry):
                entry.set_date(datetime.now())
            else:
                entry.delete(0, "end")
                if entry == feed_entries.get("feed_time"):
                    entry.insert(0, datetime.now().strftime("%H:%M"))

    def save_pet():
        required = {
            "pet": [name_entry.get(), bdate_entry.get()],
            "owner": [owner_name_entry.get(), owner_phone_entry.get()],
            "image": [image_uploader.get_image_path()]
        }

        msgs = {
            "pet": "Pet name and birthdate are required.",
            "owner": "Owner name and contact number are required.",
            "image": "Please select an image for your pet."
        }

        for check, fields in required.items():
            if not all(fields):
                messagebox.showwarning("Missing Info", msgs[check])
                return

        try:
            pet_controller = PetController()
            pet_id = pet_controller.add_pet_with_owner(
                Pet(id=0, name=required["pet"][0], breed=breed_entry.get(), 
                    birthdate=required["pet"][1]),
                Owner(id=0, name=required["owner"][0], 
                     contact_number=required["owner"][1], 
                     address=owner_address_entry.get()),
                required["image"][0]
            )

            controllers = {
                "vet_visits": (VetVisitController, VetVisit),
                "vaccinations": (VaccinationController, Vaccination),
                "feeding_logs": (FeedingLogController, FeedingLog)
            }

            for record_type, (controller_cls, model_cls) in controllers.items():
                ctrl = controller_cls()
                for record in records[record_type]:
                    model_instance = model_cls(pet_id=pet_id, **record)
                    ctrl.db_handler.insert(model_instance)

            messagebox.showinfo("Saved", f"{required['pet'][0]} and all records added successfully!")
            records.update({k: [] for k in records})

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Add buttons for each record type
    tab_map = {
        "vet_visits": vet_entries,
        "vaccinations": vax_entries,
        "feeding_logs": feed_entries
    }
    tab_names = {
        "vet_visits": "Vet Visits",
        "vaccinations": "Vaccinations",
        "feeding_logs": "Feeding Logs"
    }
    required_fields_map = {
        "vet_visits": ["visit_date", "reason"],
        "vaccinations": ["vaccine_name", "date_administered", "next_due"],
        "feeding_logs": ["food_type", "feed_time"]
    }
    success_msgs = {
        "vet_visits": "Vet visit added successfully!",
        "vaccinations": "Vaccination added successfully!",
        "feeding_logs": "Feeding log added successfully!"
    }
    # Get the actual tab objects from the medical_notebook
    vet_visit_tab = medical_notebook.tab("Vet Visits")
    vaccination_tab = medical_notebook.tab("Vaccinations")
    feeding_tab = medical_notebook.tab("Feeding Logs")

    for tab, record_type in zip([vet_visit_tab, vaccination_tab, feeding_tab], ["vet_visits", "vaccinations", "feeding_logs"]):
        create_button(tab, text=f"➕ Add {tab_names[record_type][:-1]}", command=lambda rt=record_type: add_record(
            rt, tab_map[rt], required_fields_map[rt], success_msgs[rt]), width=120).pack(pady=10)

    # Bottom buttons
    btn_frame = create_frame(right_frame)
    btn_frame.pack(pady=(10, 30), fill="x")
    btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="buttons")

    create_back_button(btn_frame, text="BACK", 
                      command=lambda: show_frame("dashboard"), 
                      width=100).grid(row=0, column=0, padx=(0, 5), sticky="ew")
    create_button(btn_frame, text="SAVE", command=save_pet, 
                 width=100).grid(row=0, column=1, padx=(5, 0), sticky="ew")

    return parent