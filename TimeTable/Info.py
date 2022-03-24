from Student import Student
import random

class Info(Student):
    courses = ["Maths", "IA", "Physics", "Algo", "DeepLearning", "French", "Sport"]
    def __init__(self):
        super().__init__()
        self.courses = random.sample(Info.courses, 4)
