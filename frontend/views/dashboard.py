import customtkinter as ctk

from frontend.style.style import (
    create_button,
    create_label,
    create_frame,
    get_title_font,
    create_exit_button,
    create_bento_button

)

def create_dashboard(parent, show_frame):
    for widget in parent.winfo_children():
        widget.destroy()

    # Title
    title = create_label(parent, "🐾 PetTrackr Dashboard")
    title.pack(pady=(20, 10))

    # Main container for bento grid
    main_frame = create_frame(parent)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Bento grid container (2x2)
    grid_frame = create_frame(main_frame)
    grid_frame.pack(expand=True)

    # First row
    row1 = create_frame(grid_frame)
    row1.pack(pady=5)

    add_btn = create_bento_button(
        row1,
        text="➕ Add New Pet",
        command=lambda: show_frame("add_pet"),
        color="#4CCD99"  # Green
    )
    add_btn.pack(side="left", padx=5)

    view_btn = create_bento_button(
        row1,
        text="📋 View Pets",
        command=lambda: show_frame("view_pets"),
        color="#6C9BCF"  # Blue
    )
    view_btn.pack(side="left", padx=5)

    # Second row
    row2 = create_frame(grid_frame)
    row2.pack(pady=5)

    vaccinations_btn = create_bento_button(
        row2,
        text="💉 Vaccinations",
        command=lambda: show_frame("vaccinations"),
        color="#FFA447"  # Orange
    )
    vaccinations_btn.pack(side="left", padx=5)

    grooming_btn = create_bento_button(
        row2,
        text="✂️ Groomings",
        command=lambda: show_frame("groomings"),
        color="#D37676"  # Red
    )
    grooming_btn.pack(side="left", padx=5)

    # Exit button (bottom right)
    exit_frame = create_frame(main_frame)
    exit_frame.pack(side="bottom", fill="x", pady=20)

    exit_btn = create_exit_button(
        exit_frame,
        text="Exit",
        command=parent.quit,
        width=100
    )
    exit_btn.pack(anchor="e")

    return parent