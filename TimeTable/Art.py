from Student import Student
import random

class Art(Student):
    courses = ["French", "Drawing", "Painting", "Sculpting", "Sport"]

    def __init__(self):
        super().__init__()
        self.courses = random.sample(Art.courses, 4)
