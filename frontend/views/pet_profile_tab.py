import customtkinter as ctk
from PIL import Image
import os
from frontend.style.style import (
    create_label1, create_frame, create_button,
    get_title_font, get_subtitle_font, get_card_detail_font
)

class PetProfileTab:
    def __init__(self, parent, pet, owner, vet_visits, vaccinations, feeding_logs, show_frame):
        self.parent = parent
        self.pet = pet
        self.owner = owner
        self.vet_visits = vet_visits
        self.vaccinations = vaccinations
        self.feeding_logs = feeding_logs
        self.show_frame = show_frame
        self._build()

    def _build(self):
        self._clear_parent()
        self._setup_main_layout()

    def _clear_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.parent.pack_propagate(False)

    def _setup_main_layout(self):
        ctk.CTkFrame(self.parent, height=36, fg_color="transparent").pack(fill="x", side="top")
        
        main = ctk.CTkFrame(self.parent, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=80, pady=36)
        main.grid_columnconfigure(0, weight=1, minsize=340)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self._image_panel(main)
        self._content_panel(main)
        self._back_button()

    def _image_panel(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="#fff", corner_radius=16, 
                           border_width=1, border_color="#e0e0e0")
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_propagate(False)
        panel.configure(width=340, height=420)

        img = self._get_image()
        ctk.CTkLabel(panel, image=ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300)), 
                    text="").pack(pady=(32, 12))
        create_label1(panel, f"🐾 {self.pet.name}'s Profile", font=get_title_font(), 
                    justify="center").pack(pady=(0, 8))

    def _get_image(self):
        try:
            img_path = os.path.join("backend", "data", getattr(self.pet, 'image_path', "")) if hasattr(self.pet, 'image_path') else None
            return Image.open(img_path).resize((300, 300)) if img_path and os.path.exists(img_path) else Image.new("RGB", (300, 300), "lightgray")
        except Exception:
            return Image.new("RGB", (300, 300), "lightgray")

    def _content_panel(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.grid(row=0, column=1, sticky="nsew", padx=(32, 0))
        
        content = ctk.CTkFrame(scroll, fg_color="#f5f7fa", corner_radius=18, 
                              border_width=2, border_color="#d0d4db")
        content.pack(fill="both", expand=True, ipadx=30, ipady=30)

        self._info_panel(content)

    def _info_panel(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="#fff", corner_radius=16, border_width=1, border_color="#e0e0e0")
        panel.pack(fill="both", expand=True)
        
        content = ctk.CTkFrame(panel, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=24, pady=24)

        self._section(content, "🐶 Pet Information", [
            ("Breed:", self.pet.breed or "Unknown"),
            ("Birthdate:", self.pet.birthdate),
            ("Age:", self.pet.age())
        ])
        
        if self.owner:
            self._section(content, "👤 Owner Information", [
                ("Name:", self.owner.name),
                ("Contact:", self.owner.contact_number),
                ("Address:", self.owner.address)
            ], top=20)

        self._records_section(content, "🩺 Vet Visits", self.vet_visits, self._vet_visit_item, top=20)
        self._records_section(content, "💉 Vaccinations", self.vaccinations, self._vaccine_item, top=20, empty="No vaccination records available")
        self._records_section(content, "🍖 Feeding Logs", self.feeding_logs, self._feeding_item, top=20, empty="No feeding records available")

    def _section(self, parent, title, items, top=0):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(top, 0))
        
        create_label1(frame, title, font=get_subtitle_font(), justify="left").pack(anchor="w", pady=(0, 12))
        
        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(fill="x")
        for i, (label, value) in enumerate(items):
            create_label1(grid, label, font=get_card_detail_font(), text_color="#666").grid(row=i, column=0, sticky="w", padx=(0, 8), pady=4)
            create_label1(grid, value, font=get_card_detail_font(), text_color="#222").grid(row=i, column=1, sticky="w", pady=4)

    def _records_section(self, parent, title, records, item_fn, top=0, empty=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(top, 0))
        
        create_label1(frame, title, font=get_subtitle_font(), justify="left").pack(anchor="w", pady=(0, 12))
        
        if records:
            for rec in records:
                item_fn(frame, rec)
        elif empty:
            self._create_empty_state(frame, empty)

    def _vet_visit_item(self, parent, visit):
        self._create_record_item(
            parent, icon="📅",
            main_text=f"{visit.visit_date}: {visit.reason}",
            secondary_text=f"💰 ₱{getattr(visit, 'cost', 0):,.2f}",
            notes=getattr(visit, 'notes', None)
        )

    def _vaccine_item(self, parent, vaccine):
        self._create_record_item(
            parent, icon="🦠",
            main_text=getattr(vaccine, 'vaccine_name', 'Unknown vaccine'),
            secondary_text=f"💰 ₱{getattr(vaccine, 'price', 0):,.2f}",
            details=[
                f"🗓️ Administered: {getattr(vaccine, 'date_administered', 'Unknown date')}",
                f"🔜 Next Due: {getattr(vaccine, 'next_due', 'Unknown date')}"
            ]
        )

    def _feeding_item(self, parent, log):
        plan = ", ".join([p for p, cond in [
            ("Once a day", getattr(log, 'feed_once', False)),
            ("Twice a day", getattr(log, 'feed_twice', False)),
            ("Thrice a day", getattr(log, 'feed_thrice', False))
        ] if cond]) or "No specific plan"
        self._create_record_item(
            parent, icon="📅",
            main_text=f"{getattr(log, 'start_date', 'Unknown date')} — {getattr(log, 'num_days', '?')} day(s)",
            secondary_text=f"Plan: {plan}",
            notes=getattr(log, 'notes', None)
        )

    def _create_record_item(self, parent, icon, main_text, secondary_text=None, notes=None, details=None):
        item = ctk.CTkFrame(parent, fg_color="transparent")
        item.pack(fill="x", pady=(0, 8))
        
        main_line = ctk.CTkFrame(item, fg_color="transparent")
        main_line.pack(fill="x")
        
        create_label1(main_line, icon, font=get_card_detail_font()).pack(side="left", padx=(0, 6))
        create_label1(main_line, main_text, font=get_card_detail_font()).pack(side="left")
        
        if secondary_text:
            create_label1(main_line, secondary_text, font=get_card_detail_font(), text_color="#666").pack(side="left", padx=(12, 0))
        
        if details:
            [create_label1(item, d, font=get_card_detail_font(), text_color="#666").pack(anchor="w", padx=(20, 0), pady=(2, 0)) for d in details]
        
        if notes:
            create_label1(item, f"📝 {notes}", font=get_card_detail_font(), text_color="#666").pack(anchor="w", padx=(20, 0), pady=(4, 0))

    def _create_empty_state(self, parent, message):
        create_label1(parent, message, font=get_card_detail_font(), text_color="#999").pack(anchor="w", pady=(4, 0))

    def _back_button(self):
        bottom = ctk.CTkFrame(self.parent, fg_color="transparent")
        bottom.pack(fill="x", side="bottom", padx=80, pady=(0, 24))
        bottom.pack_propagate(False)
        bottom.configure(height=48)
        create_button(bottom, text="← Back", command=self._go_back, width=120).pack(side="right")

    def _go_back(self):
        self.show_frame("view_pets")

def create_pet_profile_tab(parent, pet, owner, vet_visits, vaccinations, feeding_logs, show_frame):
    PetProfileTab(parent, pet, owner, vet_visits, vaccinations, feeding_logs, show_frame)
    return parent