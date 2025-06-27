from datetime import datetime

class HealthNote:
    """
    Represents a health note entry for a pet.
    """

    def __init__(self, id: int, pet_id: int, date_logged: str,
                 symptom: str, severity: str, comment: str = ""):
        self.id = id
        self.pet_id = pet_id
        self.date_logged = date_logged
        self.symptom = symptom
        self.severity = severity
        self.comment = comment
        """
        Initializes a HealthNote instance.

        Args:
            id (int): The unique health note ID from the database.
            pet_id (int): The ID of the pet this note is associated with.
            date_logged (str): The date the note was recorded (e.g., '2025-06-27').
            symptom (str): Description of the symptom observed.
            severity (str): The severity level (e.g., 'Mild', 'Moderate', 'Severe').
            comment (str, optional): Additional comments or context provided by the caretaker or vet.
        """

    def to_dict(self):
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "date_logged": self.date_logged,
            "symptom": self.symptom,
            "severity": self.severity,
            "comment": self.comment
        }

    def __str__(self):
        """Returns a readable string summary of the health note."""
        return f"{self.date_logged} — {self.symptom} ({self.severity})"