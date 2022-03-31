import random

class Timetable:
    day = 3

    def __init__(self, classrooms, listeCours):
        self.classrooms = classrooms
        self.ListeCours = listeCours
        self.week = [{i: {salle: None for salle in self.classrooms} for i in [8, 10, 14, 16]} for j in range(Timetable.day)]



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




    def creerRandomEmploieDuTemps(self):
        random.shuffle(self.ListeCours)
        for cours in self.ListeCours:
            self.PlacerCours(cours)



    def PlacerCours(self, cours):

        if Timetable.day * 4 * len(self.classrooms) >= len(self.ListeCours): #Permet de définir si on peut oui ou non placer tous les cours dans l'edt
            while True:
                i = random.randint(0, Timetable.day - 1)
                heure = random.choice(list(self.week[i].keys()))
                salle = random.choice(list(self.week[i][heure].keys()))
                if self.week[i][heure][salle] is None:
                    self.week[i][heure][salle] = cours.course
                    return
        else:
            print("Trop de cours par rapport à l'edt")

    """ Test template
        for i in range(len(self.week)):
            for heure in self.week[i].keys():
                for salle in self.week[i][heure].keys():
                    if self.week[i][heure][salle] is None:
                        print(i, heure, salle, cours.course)
                        self.week[i][heure][salle] = cours.course
                        return
    """