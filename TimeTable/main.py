from Timetable import Timetable
from University import University
from AlgoGenetique import AlgoGenetique

u = University(100)

t = AlgoGenetique(150, 0.5, 0.8, u)
t.main()
