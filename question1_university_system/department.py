class Course:
    def __init__(self, code, name, credits, max_students=30, prerequisites=None):
        self.code = code
        self.name = name
        self.credits = credits
        self.max_students = max_students
        self.prerequisites = prerequisites if prerequisites else []
        self.enrolled_students = []

    def enroll_student(self, student):
        if len(self.enrolled_students) >= self.max_students:
            print(f"Course {self.name} is full.")
            return False
        if not all(pr in student.courses for pr in self.prerequisites):
            print(f"{student.name} has not completed prerequisites for {self.name}.")
            return False
        self.enrolled_students.append(student)
        student.enroll_course(self.name)
        return True

    def __str__(self):
        return f"{self.code} - {self.name} ({self.credits} credits)"


class Department:
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.faculty = []

    def add_course(self, course):
        self.courses.append(course)

    def assign_faculty(self, faculty):
        self.faculty.append(faculty)

    def __str__(self):
        return f"Department of {self.name} with {len(self.courses)} courses."
