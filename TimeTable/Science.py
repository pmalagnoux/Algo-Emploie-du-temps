from Student import Student
import random

class Science(Student):
    courses = ["Maths", "Physics", "Algo", "French", "Lab", "Sport"]
    def __init__(self):
        super().__init__()
        self.courses = random.sample(Science.courses, 4)