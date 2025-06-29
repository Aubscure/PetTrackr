# pet_profile_tab.py
import customtkinter as ctk
from PIL import Image
import os
from frontend.style.style import (create_label1, create_frame, create_button, 
                                 get_title_font, get_subtitle_font, get_card_detail_font)

def create_pet_profile_tab(parent, pet, owner, vet_visits, vaccinations, feeding_logs, show_frame):

    print("Vaccinations:", vaccinations)
    print("Feeding Logs:", feeding_logs)
    # Clear previous widgets
    for widget in parent.winfo_children(): widget.destroy()

    # Main scrollable container
    main_scrollable = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    main_scrollable.pack(fill="both", expand=True)

    # Back button
    btn_frame = ctk.CTkFrame(main_scrollable, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(10, 20), padx=20)
    create_button(btn_frame, text="⬅️ Back to Pets", width=180, 
                 command=lambda: show_frame("view_pets")).pack(anchor="w")

    # Main container with two columns
    main_container = ctk.CTkFrame(main_scrollable, fg_color="transparent")
    main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    main_container.grid_columnconfigure(0, weight=6)
    main_container.grid_columnconfigure(1, weight=4)
    main_container.grid_rowconfigure(0, weight=1)

    # Info and image panels
    info_panel = ctk.CTkFrame(main_container, fg_color="transparent")
    info_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    image_panel = ctk.CTkFrame(main_container, fg_color="transparent")
    image_panel.grid(row=0, column=1, sticky="nsew")

    # Title
    create_label1(ctk.CTkFrame(info_panel, fg_color="transparent"), 
                f"🐾 {pet.name}'s Profile", font=get_title_font()).pack(anchor="w", pady=(0, 20))

    # Pet Image
    try:
        img_path = os.path.join("backend", "data", pet.image_path) if hasattr(pet, 'image_path') else None
        image = Image.open(img_path).resize((300, 300)) if img_path and os.path.exists(img_path) else Image.new("RGB", (300, 300), color="lightgray")
    except Exception as e:
        print(f"Error loading image: {e}")
        image = Image.new("RGB", (300, 300), color="lightgray")
    ctk.CTkLabel(image_panel, image=ctk.CTkImage(light_image=image, dark_image=image, size=(300, 300)), text="").pack(pady=20)

    # Details section
    details_frame = ctk.CTkFrame(info_panel, fg_color="transparent")
    details_frame.pack(fill="both", expand=True)

    def create_card(parent, title, items):
        card = ctk.CTkFrame(parent, corner_radius=12, border_width=1, border_color="#e0e0e0")
        card.pack(fill="x", pady=(0, 20))
        create_label1(card, title, font=get_subtitle_font()).pack(anchor="w", padx=15, pady=(10, 5))
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=(0, 15))
        return content

    # Pet Info
    pet_content = create_card(details_frame, "🐶 Pet Information", [
        ("Breed:", pet.breed or "Unknown"),
        ("Birthdate:", pet.birthdate),
        ("Age:", pet.age())
    ])
    for i, (label, value) in enumerate([("Breed:", pet.breed or "Unknown"), ("Birthdate:", pet.birthdate), ("Age:", pet.age())]):
        create_label1(pet_content, label, font=get_card_detail_font()).grid(row=i, column=0, sticky="w", pady=2)
        create_label1(pet_content, value, font=get_card_detail_font()).grid(row=i, column=1, sticky="w", pady=2)

    # Owner Info
    if owner:
        owner_content = create_card(details_frame, "👤 Owner Information", [
            ("Name:", owner.name),
            ("Contact:", owner.contact_number),
            ("Address:", owner.address)
        ])
        for i, (label, value) in enumerate([("Name:", owner.name), ("Contact:", owner.contact_number), ("Address:", owner.address)]):
            create_label1(owner_content, label, font=get_card_detail_font()).grid(row=i, column=0, sticky="w", pady=2)
            create_label1(owner_content, value, font=get_card_detail_font()).grid(row=i, column=1, sticky="w", pady=2)

    # Medical Records
    records_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
    records_frame.pack(fill="both", expand=True)

    # Vet Visits
    if vet_visits:
        visits_content = create_card(records_frame, "🩺 Vet Visits", vet_visits)
        for visit in vet_visits:
            create_label1(visits_content, f"📅 {visit.visit_date}: {visit.reason}", font=get_card_detail_font()).pack(anchor="w", pady=5)
            if visit.notes: create_label1(visits_content, f"   📝 {visit.notes}", font=get_card_detail_font(), text_color="#666666").pack(anchor="w", padx=10)

    # Vaccinations
    vac_content = create_card(records_frame, "💉 Vaccinations", vaccinations or [])
    if vaccinations:
        for v in vaccinations:
            create_label1(vac_content, f"🦠 {getattr(v, 'vaccine_name', 'Unknown vaccine')}", font=get_card_detail_font()).pack(anchor="w", pady=5)
            create_label1(vac_content, f"   🗓️ Administered: {getattr(v, 'date_administered', 'Unknown date')}", font=get_card_detail_font(), text_color="#666666").pack(anchor="w", padx=10)
            create_label1(vac_content, f"   🔜 Next Due: {getattr(v, 'next_due', 'Unknown date')}", font=get_card_detail_font(), text_color="#666666").pack(anchor="w", padx=10)
    else: create_label1(vac_content, "No vaccination records available", font=get_card_detail_font(), text_color="#666666").pack(anchor="w")

    # Feeding Logs
    feed_content = create_card(records_frame, "🍖 Feeding Logs", feeding_logs or [])
    if feeding_logs:
        for f in feeding_logs:
            create_label1(feed_content, f"⏰ {getattr(f, 'feed_time', 'Unknown time')}: {getattr(f, 'food_type', 'Unknown food')}", font=get_card_detail_font()).pack(anchor="w", pady=5)
            if getattr(f, 'notes', None): create_label1(feed_content, f"   📝 {f.notes}", font=get_card_detail_font(), text_color="#666666").pack(anchor="w", padx=10)
    else: create_label1(feed_content, "No feeding records available", font=get_card_detail_font(), text_color="#666666").pack(anchor="w")