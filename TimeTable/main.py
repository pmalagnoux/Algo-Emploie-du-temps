from Timetable import Timetable
from University import University
from Node import Node


class AlgoArbre:
    def __init__(self):
        Node = Node(coursesLeftToPlace=Timetable.allCourses())
        Node.printNode()


u = University(100)

t = AlgoGenetique(150, 0.5, 0.8, u)
t.main()
