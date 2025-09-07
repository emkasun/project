from person import Person

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.courses = []
        self.grades = {}

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            print(f"{self.name} enrolled in {course}")
        else:
            print(f"{self.name} is already enrolled in {course}")

    def drop_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            print(f"{self.name} dropped {course}")
        else:
            print(f"{self.name} is not enrolled in {course}")

    def add_grade(self, course, grade):
        if course in self.courses:
            self.grades[course] = grade
        else:
            print(f"{self.name} is not enrolled in {course}, cannot assign grade.")

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        return round(sum(self.grades.values()) / len(self.grades), 2)

    def get_academic_status(self):
        gpa = self.calculate_gpa()
        if gpa >= 3.5:
            return "Dean's List"
        elif gpa >= 2.0:
            return "Good Standing"
        else:
            return "Probation"


class UndergraduateStudent(Student):
    def get_responsibilities(self):
        return "Attend lectures, complete assignments, and exams."


class GraduateStudent(Student):
    def get_responsibilities(self):
        return "Conduct research, attend seminars, and publish papers."


# 🔹 Encapsulation + Validation
class SecureStudentRecord:
    def __init__(self, student_id, gpa=0.0, max_courses=5):
        self.__student_id = student_id    # private attribute
        self.__gpa = 0.0                  # private attribute
        self.__courses = []
        self.max_courses = max_courses

        # Validate GPA on initialization
        self.set_gpa(gpa)

    # Getter for student_id
    def get_student_id(self):
        return self.__student_id

    # GPA Getter/Setter with validation
    def get_gpa(self):
        return self.__gpa

    def set_gpa(self, value):
        if 0.0 <= value <= 4.0:
            self.__gpa = value
        else:
            raise ValueError("GPA must be between 0.0 and 4.0")

    # Course management with limit checks
    def enroll_course(self, course):
        if len(self.__courses) >= self.max_courses:
            print(f"Enrollment failed: max limit of {self.max_courses} courses reached.")
            return False
        if course in self.__courses:
            print(f"Already enrolled in {course}.")
            return False
        self.__courses.append(course)
        print(f"Enrolled in {course}.")
        return True

    def drop_course(self, course):
        if course in self.__courses:
            self.__courses.remove(course)
            print(f"Dropped {course}.")
            return True
        else:
            print(f"Not enrolled in {course}.")
            return False

    def get_courses(self):
        return list(self.__courses)   # return a copy (not direct reference)

    def __str__(self):
        return f"SecureStudentRecord(Student ID: {self.__student_id}, GPA: {self.__gpa}, Courses: {len(self.__courses)})"
