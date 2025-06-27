from datetime import datetime

class GroomingLog:
    """
    Represents a grooming log entry for a pet.
    """

    def __init__(self, id: int, pet_id: int, groom_date: str, service_type: str,
                 groomer_name: str, notes: str = ""):
        self.id = id
        self.pet_id = pet_id
        self.groom_date = groom_date
        self.service_type = service_type
        self.groomer_name = groomer_name
        self.notes = notes
        """
        Initializes a GroomingLog instance.

        Args:
            id (int): The unique grooming log ID from the database.
            pet_id (int): The ID of the pet this log is associated with.
            groom_date (str): The date of grooming in 'YYYY-MM-DD' format.
            service_type (str): The type of service provided (e.g., 'Bath', 'Haircut').
            groomer_name (str): Name of the groomer who performed the service.
            notes (str, optional): Additional notes about the session.
        """

    def to_dict(self):
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "groom_date": self.groom_date,
            "service_type": self.service_type,
            "groomer_name": self.groomer_name,
            "notes": self.notes
        }

    def __str__(self):
        """Returns a readable string summary of the grooming log."""
        return f"{self.groom_date} — {self.service_type} by {self.groomer_name}"