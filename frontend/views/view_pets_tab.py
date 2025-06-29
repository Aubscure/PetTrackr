#frontend/views/view_pets_tab.py
import customtkinter as ctk
from backend.models import owner
from frontend.components.pet_card import PetCard
from backend.controllers.pet_controller import PetController
from frontend.style.style import create_label, create_button, create_frame, get_title_font
from backend.controllers.vet_visit_controller import VetVisitController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.feeding_log_controller import FeedingLogController

def get_vet_visits(pet_id):
    return VetVisitController().get_by_pet_id(pet_id)

def get_vaccinations(pet_id):
    return VaccinationController().get_by_pet_id(pet_id)

def get_feeding_logs(pet_id):
    return FeedingLogController().get_by_pet_id(pet_id)

def show_pet_profile(pet, owner, show_frame):
    show_frame("pet_profile", pet=pet, owner=owner)

    
def create_view_pets_tab(parent, show_frame):
    parent_children = parent.winfo_children()
    [widget.destroy() for widget in parent_children]

    title = create_label(parent, "📋 All Pets", font=get_title_font())
    title.pack(pady=(20, 15))

    # Main container for scrollable content
    main_frame = create_frame(parent)
    main_frame.pack(fill="both", expand=True, padx=15, pady=5)

    # Canvas and scrollbar setup
    canvas = ctk.CTkCanvas(main_frame, bg="white", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(main_frame, command=canvas.yview)
    scrollable_frame = create_frame(canvas)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # Configure grid for 4 columns with equal spacing
    for i in range(4):
        scrollable_frame.columnconfigure(i, weight=1, uniform="column", minsize=240)

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_linux_scroll(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    # Bind mouse wheel events
    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows and Mac
    canvas.bind_all("<Button-4>", _on_linux_scroll)  # Linux (up)
    canvas.bind_all("<Button-5>", _on_linux_scroll)  # Linux (down)
    
    canvas.bind("<Configure>", on_canvas_configure)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add pet cards in a 4-column grid
    thumbnails = []
    controller = PetController()
    pets, owners = controller.get_pets_with_owners()  # Get both pets and owners
    
    for i, (pet, owner) in enumerate(zip(pets, owners)):
        row = i // 4
        col = i % 4
        card = PetCard(
            scrollable_frame,
            pet,
            thumbnails,
            owner=owner,
            on_click=lambda pet, owner: show_frame(
                "pet_profile",
                pet=pet,
                owner=owner,
                vet_visits=get_vet_visits(pet.id),
                vaccinations=get_vaccinations(pet.id),
                feeding_logs=get_feeding_logs(pet.id)
            )

        )
        card.grid(
            row=row,
            column=col,
            padx=12,
            pady=12,
            sticky="nsew"
        )
        scrollable_frame.rowconfigure(row, weight=1)

    # Back button
    btn_wrapper = create_frame(parent)
    btn_wrapper.pack(pady=20)

    back_btn = create_button(
        btn_wrapper,
        text="⬅️ Back to Dashboard",
        command=lambda: show_frame("dashboard"),
        width=220
    )
    back_btn.pack()

    # Clean up bindings when tab is closed
    def cleanup():
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
    
    parent.bind("<Destroy>", lambda e: cleanup())

    return parent