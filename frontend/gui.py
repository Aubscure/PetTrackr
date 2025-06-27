import customtkinter as ctk
from frontend.views.dashboard import create_dashboard
from frontend.views.add_pet_view import create_add_pet_view
from frontend.views.view_pets_tab import create_view_pets_tab
from frontend.style.style import configure_table_style



def launch_gui():
    """Initializes the main application window and sets up dynamic view navigation."""
    
    ctk.set_appearance_mode("light")  # Optional: can be moved into style.py
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("PetTrackr")
    root.attributes("-fullscreen", True)

    # Main container for dynamic views
    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.pack(expand=True, fill="both")

    def show_frame(name: str):
        if name == "dashboard":
            create_dashboard(main_frame, show_frame)
        elif name == "add_pet":
            create_add_pet_view(main_frame, show_frame)
        elif name == "view_pets":
            create_view_pets_tab(main_frame, show_frame)

    # (Optional) Apply custom ttk styles
    # configure_custom_styles()

    configure_table_style()


    show_frame("dashboard")
    root.mainloop()