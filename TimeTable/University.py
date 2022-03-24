from Student import Student
from Info import Info
from Art import Art
from Science import Science
from Histoire import Histoire
from Timetable import Timetable
import random

class University:

    classrooms = ["A1", "A2", "A3", "A4"]

    def __init__(self, nbStudent):
        self.nbStudent = nbStudent
        self.students = []
        for _ in range(self.nbStudent):
            temp = random.randint(0,4)
            if temp == 0:
                self.students.append(Info())
            elif temp == 1:
                self.students.append(Art())
            elif temp == 2:
                self.students.append(Histoire())
            elif temp == 3:
                self.students.append(Science())

        self.courses = self.studentInCourse()
        self.timetable = Timetable(self.students)

    def studentInCourse(self):
        courses = {course: 0 for course in Student.courses}
        for student in self.students:
            for course in student.courses:
                courses[course] += 1
        return courses

