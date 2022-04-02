from Student import Student
from Info import Info
from Art import Art
from Science import Science
from Histoire import Histoire
from Timetable import Timetable
from Cours import Course
import random
import numpy as np

class University:

    classrooms = ["A1", "A2", "A3", "A4"]

    def __init__(self, nbStudent):
        self.nbStudent = nbStudent
        self.students = []
        for _ in range(self.nbStudent):
            temp = random.randint(0, 3)
            if temp == 0:
                self.students.append(Info())
            elif temp == 1:
                self.students.append(Art())
            elif temp == 2:
                self.students.append(Histoire())
            elif temp == 3:
                self.students.append(Science())

        self.courses = self.studentInCourse()
        self.createListeCours()
        self.graphCourses()
        self.timetable = Timetable(University.classrooms, self.ListeCours)


    def studentInCourse(self):
        """
        Retourne le nombre de participants à chaque cours
        :return: dict {cours : nbEtudiantParticipant}
        """
        courses = {course: 0 for course in Student.courses}
        for student in self.students:
            for course in student.courses:
                courses[course] += 1
        return courses

    def createListeCours(self):
        """
        Créer des cours avec des caractéristiques aléatoires à partir de la liste de cours
        :return: list [Cours]
        """

        self.ListeCours = []
        for course in Student.courses:
            self.ListeCours.append(Course(course,random.choice(University.classrooms)))

    def graphCourses(self):
        """
        Créé la matrice du graphe des interactions entre les cours.
        Un nœud est un cours
        Un lien correspond à un chiffre dans la matrice.
        Ces liens servent à représenter les deux cours ont été choisi par un même étudiant
        Le nombre correspond au nombre d'étudiants concernés
        """
        listCourse = Student.courses
        self.graph = np.zeros((len(listCourse), len(listCourse)), dtype=int)
        for student in self.students:
            for i in range(len(student.courses)):
                for j in range(i, len(student.courses)):
                    self.graph[listCourse.index(student.courses[i])] [listCourse.index(student.courses[j])] += 1
                    self.graph[listCourse.index(student.courses[j])] [listCourse.index(student.courses[i])] += 1
        np.fill_diagonal(self.graph, 0)
        print(self.graph)