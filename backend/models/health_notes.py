class HealthNote:
    def __init__(self, id, pet_id, date_logged, symptom, severity, comment):
        self.id = id
        self.pet_id = pet_id
        self.date_logged = date_logged
        self.symptom = symptom
        self.severity = severity
        self.comment = comment