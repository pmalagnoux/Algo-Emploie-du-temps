from AlgoGenetique import AlgoGenetique
from University import University
from AlgoExact import AlgoExact

u = University(100)

t = AlgoGenetique(150, 0.5, 0.8, u)
t.main()
x = AlgoExact(u)

