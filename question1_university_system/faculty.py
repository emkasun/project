from person import Person


class Faculty(Person):
    def __init__(self, name, age, email, faculty_id):
        super().__init__(name, age, email)
        self.faculty_id = faculty_id

    def calculate_workload(self):
        return "General teaching and administrative duties."


class Professor(Faculty):
    def get_responsibilities(self):
        return "Teach courses, conduct research, and supervise PhD students."

    def calculate_workload(self):
        return "Workload: 3 courses + research supervision."


class Lecturer(Faculty):
    def get_responsibilities(self):
        return "Teach undergraduate and graduate courses."

    def calculate_workload(self):
        return "Workload: 4 courses."


class TeachingAssistant(Faculty):
    def get_responsibilities(self):
        return "Assist faculty in grading, labs, and tutorials."

    def calculate_workload(self):
        return "Workload: 2 courses + lab sessions."
from person import Person

