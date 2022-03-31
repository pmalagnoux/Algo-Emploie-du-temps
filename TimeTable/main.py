from Timetable import Timetable
from University import University
from AlgoGenetique import AlgoGenetique

u = University(100)

t = AlgoGenetique(100, 0.5, 0.5, u)
t.main()
