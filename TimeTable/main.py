from Timetable import Timetable
from University import University
from Node import Node


u = University(100)

t = AlgoGenetique(150, 0.5, 0.8, u)
t.main()
