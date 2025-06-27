#frontend/components/pet_card.py
import os
from PIL import Image
import customtkinter as ctk
from frontend.style.style import (
    create_label, 
    create_frame, 
    get_subtitle_font,
    get_card_title_font,
    get_card_detail_font,
    get_card_icon_font
)

class PetCard(ctk.CTkFrame):
    def __init__(self, master, pet, image_store, *args, **kwargs):
        super().__init__(
            master, 
            fg_color="white", 
            corner_radius=12,
            border_width=1,
            border_color="#e0e0e0",
            *args, **kwargs
        )
        self.pet = pet
        self.image_store = image_store
        self.configure(width=240)  # Slightly wider for better content
        self.columnconfigure(0, weight=1)
        self._build_card()

    def _build_card(self):
        # Main container with consistent padding
        container = create_frame(self, "white")
        container.pack(padx=12, pady=12, fill="both", expand=True)
        
        # Image section - larger and centered
        thumbnail = self._get_pet_thumbnail()
        image_frame = create_frame(container, "white")
        image_frame.pack(pady=(0, 10))
        
        label_image = ctk.CTkLabel(
            image_frame, 
            image=thumbnail, 
            text="",
            compound="top"
        )
        label_image.pack()

        # Info section
        info_frame = create_frame(container, "white")
        info_frame.pack(fill="x")

        # Name with larger font
        label_name = create_label(
            info_frame, 
            self.pet.name, 
            font=get_card_title_font()
        )
        label_name.pack(pady=(0, 8))

        # Details with icon-text pairs
        details_frame = create_frame(info_frame, "white")
        details_frame.pack(fill="x", padx=8)

        # Breed row
        breed_row = create_frame(details_frame, "white")
        breed_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            breed_row, 
            text="🐶", 
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            breed_row, 
            self.pet.breed or "Unknown", 
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Birthdate row
        birth_row = create_frame(details_frame, "white")
        birth_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            birth_row, 
            text="📅", 
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            birth_row, 
            self.pet.birthdate, 
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

        # Age row
        age_row = create_frame(details_frame, "white")
        age_row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            age_row, 
            text="🕒", 
            font=get_card_icon_font(),
            width=24,
            anchor="w"
        ).pack(side="left")
        create_label(
            age_row, 
            self.pet.age(), 
            font=get_card_detail_font(),
            anchor="w"
        ).pack(side="left", padx=5)

    def _get_pet_thumbnail(self):
        try:
            img_path = os.path.join("backend", "data", self.pet.image_path)
            image = Image.open(img_path).resize((140, 140))  # Larger image
        except Exception:
            image = Image.new("RGB", (140, 140), color="lightgray")

        thumb = ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
        self.image_store.append(thumb)
        return thumb