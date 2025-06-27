import customtkinter as ctk
from frontend.style.style import (
    create_button,
    create_label,
    create_frame,
    get_title_font,
    create_exit_button

)

def create_dashboard(parent, show_frame):
    for widget in parent.winfo_children():
        widget.destroy()

    # Title
    title = create_label(parent, "🐾 PetTrackr Dashboard")
    title.pack(pady=(20, 10))

    # Button container
    btn_frame = create_frame(parent)
    btn_frame.pack(pady=10)

    add_btn = create_button(
        btn_frame,
        text="➕ Add New Pet",
        command=lambda: show_frame("add_pet")
    )
    add_btn.grid(row=0, column=0, padx=10, pady=5)

    view_btn = create_button(
        btn_frame,
        text="📋 View All Pets",
        command=lambda: show_frame("view_pets")
    )
    view_btn.grid(row=1, column=0, padx=10, pady=5)

    # Exit button (bottom right)
    exit_frame = create_frame(parent)
    exit_frame.pack(side="bottom", fill="x", pady=20, padx=20)

    exit_btn = create_exit_button(
        exit_frame,
        text="Exit",
        command=parent.quit,
        width=100
    )
    exit_btn.pack(anchor="e")

    return parent