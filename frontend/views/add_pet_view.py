# frontend/views/add_pet_view.py
import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import font, messagebox

from backend.models.pet import Pet
from backend.controllers.pet_controller import add_pet_with_image  # Only import what exists
from frontend.components.floating_placeholder_entry import FloatingPlaceholderEntry
from frontend.components.image_uploader import ImageUploader
from frontend.style.style import (
    create_button,
    create_label,
    create_frame,
    get_title_font,
    get_subtitle_font,
    create_back_button
)

def create_add_pet_view(parent, show_frame):
    # Clear existing widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Main container with two columns
    container = create_frame(parent)
    container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # Header spanning both columns
    heading = create_label(container, "➕ Add New Pet", font=get_title_font())
    heading.grid(row=0, column=0, columnspan=2, pady=(30, 15))

    # Left side - Image uploader
    left_frame = create_frame(container)
    left_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    image_uploader = ImageUploader(left_frame)
    image_uploader.pack(pady=(0, 10), fill="both", expand=True)

    # Right side - Form and buttons
    right_frame = create_frame(container)
    right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

    # Form fields
    form = create_frame(right_frame)
    form.pack(padx=10, pady=10, fill="x", expand=True)
    form.columnconfigure(0, weight=1)

    name_entry = FloatingPlaceholderEntry(form, "Pet Name")
    name_entry.grid(row=0, column=0, pady=8, sticky="ew")

    breed_entry = FloatingPlaceholderEntry(form, "Breed (optional)")
    breed_entry.grid(row=1, column=0, pady=8, sticky="ew")

    bdate_container = create_frame(form)
    bdate_container.grid(row=2, column=0, pady=8, sticky="ew")

    bdate_label = create_label(bdate_container, "Birthdate", font=get_subtitle_font())
    bdate_label.pack(anchor="w")

    bdate_entry = DateEntry(
        bdate_container,
        width=26,
        date_pattern="yyyy-mm-dd",
        background="#3b8ed0",
        foreground="white",
        borderwidth=2,
        font=font.Font(family="Segoe UI", size=12)
    )
    bdate_entry.pack(pady=8, ipady=4, fill="x")

    def save_pet():
        """Handle pet data saving - now requires an image"""
        name = name_entry.get()
        breed = breed_entry.get()
        bdate = bdate_entry.get()

        if not name or not bdate:
            messagebox.showwarning("Missing Info", "Name and birthdate are required.")
            return

        image_path = image_uploader.get_image_path()
        if not image_path:
            messagebox.showwarning("Image Required", "Please select an image for your pet.")
            return

        pet = Pet(id=None, name=name, breed=breed, birthdate=bdate)

        try:
            add_pet_with_image(pet, image_path)
            messagebox.showinfo("Saved", f"{name} has been added!")
            
            # Reset form
            name_entry.delete(0, ctk.END)
            breed_entry.delete(0, ctk.END)
            bdate_entry.set_date(None)
            image_uploader.reset()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Buttons at the bottom of the right frame
    btn_frame = create_frame(right_frame)
    btn_frame.pack(pady=(10, 30), fill="x")
    btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="buttons")

    back_btn = create_back_button(
        btn_frame,
        text="BACK",
        command=lambda: show_frame("dashboard"),
        width=100
    )
    back_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

    save_btn = create_button(
        btn_frame,
        text="SAVE",
        command=save_pet,
        width=100
    )
    save_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    return parent