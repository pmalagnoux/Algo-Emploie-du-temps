import random


class Student:
    id = 0
    courses = ["Maths", "IA", "Physics", "Algo", "DeepLearning", "French", "Sport",
               "Lab",
               "Spanish", "English", "Geography", "History",
               "Drawing", "Painting", "Sculpting"]

    def __init__(self):
        self.id = Student.id
        Student.id += 1
        
