class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def get_responsibilities(self):
        return "General university member responsibilities."

    def __str__(self):
        return f"{self.name} ({self.age}) - {self.email}"


class Staff(Person):
    def __init__(self, name, age, email, role):
        super().__init__(name, age, email)
        self.role = role

    def get_responsibilities(self):
        return f"Staff role: {self.role} - Handles administrative tasks."
