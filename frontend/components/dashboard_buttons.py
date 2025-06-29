from frontend.style.style import create_bento_button
from backend.controllers.pet_controller import PetController
from backend.controllers.vaccination_controller import VaccinationController
from backend.controllers.vet_visit_controller import VetVisitController

def add_pet_button(parent, show_frame):
    return create_bento_button(
        parent,
        text="➕ Add New Pet",
        command=lambda: show_frame("add_pet"),
        color="#4CCD99"
    )

def view_pets_button(parent, show_frame):
    return create_bento_button(
        parent,
        text="📋 View Pets",
        command=lambda: show_frame("view_pets"),
        color="#6C9BCF"
    )

def vaccinations_button(parent, show_frame):
    return create_bento_button(
        parent,
        text="💉 Vaccinations",
        command=lambda: show_frame("vaccination_visits"),
        color="#FFA447"
    )

def grooming_button(parent, show_frame):
    return create_bento_button(
        parent,
        text="✂️ Groomings",
        command=lambda: show_frame("groomings"),
        color="#D37676"
    )

def daycare_button(parent, show_frame):
    return create_bento_button(
        parent,
        text="🏠 Daycare",
        command=lambda: show_frame("view_feeding_logs"),
        color="#B799FF"
    )
