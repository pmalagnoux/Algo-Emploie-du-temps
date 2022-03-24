from Student import Student
import random

class Histoire(Student):
    courses = ["French", "Spanish", "English", "Geography", "History", "Sport"]
    def __init__(self):
        super().__init__()
        self.courses = random.sample(Histoire.courses, 4)
