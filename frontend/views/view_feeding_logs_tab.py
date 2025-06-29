import customtkinter as ctk
from backend.controllers.pet_controller import PetController
from frontend.components.pet_card_with_feeding_logs import PetCardWithFeedingLogs
from frontend.style.style import create_label, create_frame, create_back_button

def create_view_feeding_logs_tab(master, show_frame):
    # Clear the master frame
    for widget in master.winfo_children():
        widget.destroy()

    # Configure master grid
    master.grid_rowconfigure(0, weight=1)  # For main container
    master.grid_rowconfigure(1, weight=0)  # For bottom frame
    master.grid_columnconfigure(0, weight=1)

    # Create main container frame
    main_container = ctk.CTkFrame(master)
    main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 0))
    
    # Configure main container grid
    main_container.grid_rowconfigure(0, weight=0)  # Title
    main_container.grid_rowconfigure(1, weight=1)  # Content
    main_container.grid_columnconfigure(0, weight=1)

    # Title label at the top
    title_label = create_label(main_container, "🏠 Daycare & Feeding Logs")
    title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")

    # Content frame that will hold the cards
    content_frame = create_frame(main_container)
    content_frame.grid(row=1, column=0, sticky="nsew")
    
    # Configure content frame grid
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    # Cards frame for pet cards
    cards_frame = create_frame(content_frame)
    cards_frame.grid(row=0, column=0, sticky="nsew")
    cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

    pet_controller = PetController()
    pets, owners = pet_controller.get_pets_with_feeding_logs()
    image_store = []

    if not pets:
        no_pets_label = create_label(cards_frame, "No pets with feeding logs found.")
        no_pets_label.grid(row=0, column=0, pady=40)
    else:
        for idx, (pet, owner) in enumerate(zip(pets, owners)):
            card = PetCardWithFeedingLogs(cards_frame, pet, image_store, owner=owner)
            row, col = divmod(idx, 3)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

    # Bottom frame for the back button (outside main container)
    bottom_frame = ctk.CTkFrame(master)
    bottom_frame.grid(row=1, column=0, sticky="se", padx=20, pady=(0, 20))
    bottom_frame.grid_columnconfigure(0, weight=1)

    # Back button aligned to the right
    back_button = ctk.CTkButton(
        bottom_frame,
        text="Back",
        command=lambda: show_frame("dashboard"),
        width=120
    )
    back_button.grid(row=0, column=0, sticky="e", padx=0, pady=0)

    return master