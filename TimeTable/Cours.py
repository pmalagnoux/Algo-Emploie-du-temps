import random
from Timetable import Timetable

class Course:

    def __init__(self, course, classroom):
        self.course = course
        self.classroom = classroom # Définir la salle salle de preference pour le cours
        self.disponibilite = [random.random() > 0.2 for _ in range(Timetable.day)]
        if sum(self.disponibilite) == 0:
            self.disponibilite[random.randint(0, Timetable.day-1)] = True
        #Critère abitraire pour ajouer du random à la génération



    def isInSameClassroom(self, other):
        if self.classroom == other.classroom:
            return True
        return False

    def __str__(self):
        return self.course

    def __repr__(self):
        return self.course