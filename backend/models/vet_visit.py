from datetime import datetime

class VetVisit:
    """
    Represents a veterinary visit record for a pet.
    """

    def __init__(self,  pet_id: int, visit_date: str, reason: str, notes: str = ""):
        self.pet_id = pet_id
        self.visit_date = visit_date
        self.reason = reason
        self.notes = notes
        """
        Initializes a VetVisit instance.

        Args:
            id (int): The unique vet visit ID from the database.
            pet_id (int): The ID of the pet associated with the visit.
            visit_date (str): The date of the vet visit (e.g., '2025-06-27').
            reason (str): The reason for the visit (e.g., 'Annual check-up').
            notes (str, optional): Additional notes about the visit or diagnosis.
        """

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "visit_date": self.visit_date,
            "reason": self.reason,
            "notes": self.notes
        }

    def __str__(self):
        """Returns a readable string summary of the vet visit."""
        return f"{self.visit_date} — {self.reason}"