from datetime import datetime

class Vaccination:
    def __init__(self, id, pet_id, vaccine_name, date_administered, next_due):
        self.id = id
        self.pet_id = pet_id
        self.vaccine_name = vaccine_name
        self.date_administered = date_administered
        self.next_due = next_due  # format: 'YYYY-MM-DD'

    def is_due(self):
        try:
            due = datetime.strptime(self.next_due, '%Y-%m-%d')
            return datetime.today().date() >= due.date()
        except ValueError:
            return False

    def __str__(self):
        status = "✔️ Up to date" if not self.is_due() else "⚠️ Due"
        return f"{self.vaccine_name} (Next due: {self.next_due}) → {status}"