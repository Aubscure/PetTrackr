#frontend\style\style.py
import customtkinter as ctk
from tkinter import ttk
# === DASHBOARD ===
# === Appearance ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# === Fonts ===
def get_title_font():
    return ctk.CTkFont(family="Segoe UI", size=28, weight="bold")

def get_button_font():
    return ctk.CTkFont(family="Segoe UI", size=20)

# === Colors ===
PRIMARY_COLOR = "#3b8ed0"
PRIMARY_HOVER_COLOR = "#6bb8f7"
SECONDARY_COLOR = "#8c8c8c"
DANGER_COLOR = "#ff5e5e"
DANGER_HOVER = "#ff3e3e"
TRANSPARENT = "transparent"

# === Components ===
def create_button(master, text, command, color=PRIMARY_COLOR, width=200, **kwargs):
    return ctk.CTkButton(
        master,
        text=text,
        fg_color=color,
        hover_color=PRIMARY_HOVER_COLOR,
        corner_radius=8,
        font=get_button_font(),
        command=command,
        width=width,
        **kwargs
    )

def create_back_button(master, text, command, color=SECONDARY_COLOR, width=200, **kwargs):
    return ctk.CTkButton(
        master,
        text=text,
        fg_color=color,
        hover_color=DANGER_HOVER,
        corner_radius=8,
        font=get_button_font(),
        command=command,
        width=width,
        **kwargs
    )

def create_exit_button(master, text, command, color=DANGER_COLOR, width=200, **kwargs):
    return ctk.CTkButton(
        master,
        text=text,
        fg_color=color,
        hover_color=DANGER_HOVER,
        corner_radius=8,
        font=get_button_font(),
        command=command,
        width=width,
        **kwargs
    )

def create_label(master, text, font=None):
    return ctk.CTkLabel(
        master,
        text=text,
        font=font or get_title_font(),
        text_color="#222222"  # Bright white for dark mode
    )

def create_frame(master, fg_color=TRANSPARENT):
    return ctk.CTkFrame(master, fg_color=fg_color)



# === ADD PET VIEW ===

def create_card_frame(master):
    return ctk.CTkFrame(master, fg_color="#e0e0e0", corner_radius=10)

def create_field_row(master):
    return ctk.CTkFrame(master, fg_color=TRANSPARENT)

def get_subtitle_font():
    return ctk.CTkFont(family="Segoe UI", size=18)

PADDING_Y = 10
PADDING_X = 10

# === Floating Placeholder Entry ===

def get_entry_font():
    return ctk.CTkFont(family="Segoe UI", size=16)

def get_placeholder_font():
    return ctk.CTkFont(family="Segoe UI", size=12)

def get_placeholder_color():
    return "#676767"

def get_placeholder_bg():
    return "#ffffff"  # white background

PLACEHOLDER_OFFSET_Y = -6  # Slightly taller float
ENTRY_HEIGHT = 44


# === View Pets Tab ===

def configure_table_style():
    style = ttk.Style()
    style.configure("Treeview", rowheight=32, font=("Segoe UI", 14))
    style.configure("Treeview.Heading", font=("Segoe UI", 16, "bold"))


# === pet_card.py ===
def create_frame(master, fg_color=TRANSPARENT):
    return ctk.CTkFrame(master, fg_color=fg_color)

def create_label(master, text, font=None, **kwargs):
    return ctk.CTkLabel(
        master,
        text=text,
        font=font or get_title_font(),
        text_color="#222222",
        **kwargs  # This lets you pass justify, anchor, wraplength, etc.
    )

# Add to frontend/style/style.py
def get_card_title_font():
    return ctk.CTkFont(family="Segoe UI", size=16, weight="bold")

def get_card_detail_font():
    return ctk.CTkFont(family="Segoe UI", size=13)

def get_card_icon_font():
    return ctk.CTkFont(family="Segoe UI", size=12)