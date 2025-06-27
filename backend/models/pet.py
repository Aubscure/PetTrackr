from datetime import datetime

class Pet:
    """
    Represents a pet with identifying information and helper methods.
    """

    def __init__(self, id: int, name: str, breed: str, birthdate: str, image_path: str = None):
        self.id = id
        self.name = name
        self.breed = breed
        self.birthdate = birthdate
        self.image_path = image_path
        """
        Initializes a Pet instance.

        Args:
            id (int): The unique pet ID from the database.
            name (str): The pet's name.
            breed (str): The pet's breed.
            birthdate (str): The pet's birthdate in 'YYYY-MM-DD' format.
            image_path (str, optional): Path to the pet's photo, if available.
        """
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.breed,
            "birthdate": self.birthdate,
            "age": self.age(),
            "image_path": self.image_path
        }

    def age(self) -> int | str:
        """
        Calculates the pet's age in years.

        Returns:
            int: Age in years.
            str: "Unknown" if birthdate format is invalid.
        """
        try:
            birth = datetime.strptime(self.birthdate, "%Y-%m-%d")
            today = datetime.today()
            return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        except ValueError:
            return "Unknown"

    def __str__(self):
        """Returns a readable string summary of the pet."""
        return f"{self.name} ({self.breed}) — Age: {self.age()}"