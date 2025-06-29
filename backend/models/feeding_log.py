from datetime import datetime

class FeedingLog:
    """
    Represents a feeding log entry for a pet.
    """

    def __init__(self, pet_id: int, feed_time: str, food_type: str, notes: str = ""):
        self.pet_id = pet_id
        self.feed_time = feed_time
        self.food_type = food_type
        self.notes = notes
        """
        Initializes a FeedingLog instance.

        Args:
            id (int): The unique feeding log ID from the database.
            pet_id (int): The ID of the pet this log is associated with.
            feed_time (str): The date and time the pet was fed (e.g., '2025-06-27 18:30').
            food_type (str): The type of food given (e.g., 'Dry Kibble', 'Wet Food').
            notes (str, optional): Additional notes about the feeding session.
        """

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "feed_time": self.feed_time,
            "food_type": self.food_type,
            "notes": self.notes
        }

    def __str__(self):
        """Returns a readable string summary of the feeding log."""
        return f"{self.feed_time} — Fed {self.food_type} to pet #{self.pet_id}"