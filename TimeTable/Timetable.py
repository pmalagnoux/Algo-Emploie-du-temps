import numpy as np
from Student import Student

class Timetable:
    day = 3

    def __init__(self, students, classrooms):
        self.classrooms = classrooms
        self.week = [{i: {salle: None for salle in self.classrooms} for i in [8, 10, 14, 16]} for j in range(Timetable.day)]
        self.students = students
        self.graphCourses()

    def show(self):
        l1 = ""
        l2 = ""
        l3 = ""
        l4 = ""

        for day in self.week:
            l1 += "8h-10h  : {}  |  ".format(day[8])
            l2 += "10h-12h : {}  |  ".format(day[10])
            l3 += "14h-16h : {}  |  ".format(day[14])
            l4 += "16h-18h : {}  |  ".format(day[16])
        print(l1)
        print(l2)
        print(l3)
        print(l4)


    def graphCourses(self):
        listCourse = Student.courses
        self.graph = np.zeros((len(listCourse), len(listCourse)), dtype=int)
        for student in self.students:
            for i in range(len(student.courses)):
                for j in range(i, len(student.courses)):
                    self.graph[listCourse.index(student.courses[i])] [listCourse.index(student.courses[j])] += 1
                    self.graph[listCourse.index(student.courses[j])] [listCourse.index(student.courses[i])] += 1
        np.fill_diagonal(self.graph, 0)

        print(self.graph)#print(np.array(self.graph > 0, dtype=int))
