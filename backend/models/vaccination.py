from datetime import datetime

class Vaccination:
    """
    Represents a vaccination record for a pet.
    """

    def __init__(self, pet_id: int, vaccine_name: str, date_administered: str, next_due: str = ""):
        self.pet_id = pet_id
        self.vaccine_name = vaccine_name
        self.date_administered = date_administered
        self.next_due = next_due
        """
        Initializes a Vaccination instance.

        Args:
            pet_id (int): The ID of the pet this vaccination applies to.
            vaccine_name (str): The name of the vaccine administered.
            date_administered (str): The date the vaccine was administered ('YYYY-MM-DD').
            next_due (str): The date the next dose is due ('YYYY-MM-DD').
        """

    def is_due(self) -> bool:
        """
        Determines if the vaccine is due based on the current date.

        Returns:
            bool: True if the next dose is due or overdue, False otherwise.
        """
        try:
            due = datetime.strptime(self.next_due, '%Y-%m-%d')
            return datetime.today().date() >= due.date()
        except ValueError:
            return False

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "vaccine_name": self.vaccine_name,
            "date_administered": self.date_administered,
            "next_due": self.next_due,
            "is_due": self.is_due()
        }

    def __str__(self):
        """Returns a readable string summary of the vaccination record."""
        status = "✔️ Up to date" if not self.is_due() else "⚠️ Due"
        return f"{self.vaccine_name} (Next due: {self.next_due}) → {status}"