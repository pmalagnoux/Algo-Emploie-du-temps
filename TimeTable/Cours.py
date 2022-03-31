import random
from Timetable import Timetable

class Course:

    def __init__(self, course, classroom):
        self.course = course
        self.classroom = classroom # Définir la salle salle de preference pour le cours
        self.disponibilite = [random.random() > 0.2 for _ in range(Timetable.day)]
        #Critère abitraire pour ajouer du random à la génération



    def isInSameClassroom(self, other):
        if self.classroom == other.classroom:
            return True
        return False
