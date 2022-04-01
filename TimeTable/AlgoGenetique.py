import random
from operator import itemgetter
from Timetable import Timetable
from University import University
from Student import Student
from math import ceil
class AlgoGenetique:

    def __init__(self, population, tReproduction, tMutation, universite):
        self.universite = universite # contient les données du problème
        self.taille = population
        self.population = []
        self.nbEstimation = 0
        self.tR = tReproduction
        self.tM = tMutation
        self.creerPopulationInitiale() #On initialise la population initiale
        self.best = (None, None)


    def creerPopulationInitiale(self):
        for i in range(self.taille):
            self.population.append([Timetable(University.classrooms, self.universite.ListeCours), 0])
            self.population[i][0].creerRandomEmploieDuTemps()
            self.population[i][1] = self.estimerSolution(self.population[i][0])

    def estimerSolution(self, edt):
        """
        Notation des critères :
        # Contraintes fortes
            - contraites de disponibilité : -1000 à changer
            - contraites des cours en même temps quand ils sont liés : -1000
        # Contraintes faibles
            - distances entre deux cours lié par au moins un étudiant : -0.1 par cours qui les sépare * (nb d'étudiant concerné)
            - salle de préférence : -10
            -
        """
        self.nbEstimation += 1
        score = 0

        listeCoursSemaine = []
        for i in range(len(edt.week)):
            listeCoursJour = []
            for heure in edt.week[i].keys():
                listeCoursJour.append(list(edt.week[i][heure].values()))
                #### Partie respect Cours en Meme Temps ####
                listeCoursMH = list(edt.week[i][heure].values())

                for j in range(len(listeCoursMH)):
                    for k in range(j, len(listeCoursMH)):
                        if listeCoursMH[j] is not None and listeCoursMH[k] is not None \
                                and not self.respectCoursMemeTemps(listeCoursMH[j], listeCoursMH[k]):
                            score -= 1000
                ###########################################
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is not None :
                        #### Respect des disponibilités des profs ####
                        if not AlgoGenetique.respectDispo(i, edt.week[i][heure][salle]):
                            score -= 1000
                        #### Respect de la salle préféré ####
                        if not AlgoGenetique.respectSallePref(salle, edt.week[i][heure][salle]):
                            score -= 10
                ###########################################
            listeCoursSemaine.append(listeCoursJour)

        for i in range(len(listeCoursSemaine)):
            for j in range(len(listeCoursSemaine[i])):
                for k in range(len(listeCoursSemaine[i][j])):
                    if listeCoursSemaine[i][j][k] is not None:
                        for l in range(i, len(listeCoursSemaine)):
                            for m in range(j, len(listeCoursSemaine[l])):
                                for n in range(k, len(listeCoursSemaine[l][m])):
                                    if listeCoursSemaine[l][m][n] is not None :
                                        distance = abs(k-n) + abs(j-m) + abs(i-l)
                                        nbEtuConcerne = self.universite.graph[Student.courses.index(listeCoursSemaine[i][j][k].course)][Student.courses.index(listeCoursSemaine[l][m][n].course)]
                                        score -= distance * 0.1 * nbEtuConcerne
        return score
    @staticmethod
    def respectDispo(jour, cours):
        return cours.disponibilite[jour]

    @staticmethod
    def respectSallePref(salle, cours):
        return salle == cours.classroom


    def respectCoursMemeTemps(self, cours1, cours2):
        return self.universite.graph[Student.courses.index(cours1.course)][Student.courses.index(cours2.course)] == 0


    def mutation(self, solution):
        j1, j2 = random.sample(range(Timetable.day), 2)

        h1 = random.choice(list(solution.week[j1]))
        h2 = random.choice(list(solution.week[j2]))

        s1 = random.choice(list(solution.week[j1][h1]))
        s2 = random.choice(list(solution.week[j2][h2]))

        ctemp = solution.week[j2][h2][s2]
        solution.week[j2][h2][s2] = solution.week[j1][h1][s1]
        solution.week[j1][h1][s1] = ctemp

        return [solution, self.estimerSolution(solution)]

    def reproductionAmeliore(self, parent1, parent2):

        enfant1 = Timetable(University.classrooms, self.universite.ListeCours)
        enfant2 = Timetable(University.classrooms, self.universite.ListeCours)

        for i, cours in enumerate(self.universite.ListeCours):
            i1, h1, s1 = self.chercherCour(cours, parent1)
            i2, h2, s2 = self.chercherCour(cours, parent2)
            if i % 2 == 0:
                if enfant1.week[i1][h1][s1] is None:
                    enfant1.week[i1][h1][s1] = cours
                else:
                    enfant1.week[i2][h2][s2] = cours

                if enfant2.week[i2][h2][s2] is None:
                    enfant2.week[i2][h2][s2] = cours
                else:
                    enfant1.week[i1][h1][s1] = cours
            else:
                if enfant1.week[i2][h2][s2] is None:
                    enfant1.week[i2][h2][s2] = cours
                else:
                    enfant1.week[i1][h1][s1] = cours

                if enfant2.week[i1][h1][s1] is None:
                    enfant2.week[i1][h1][s1] = cours
                else:
                    enfant1.week[i2][h2][s2] = cours

        eval1 = self.estimerSolution(enfant1)
        eval2 = self.estimerSolution(enfant2)

        if eval1 >= eval2:
            return [enfant1, eval1]
        else:
            return [enfant2, eval2]


    def chercherCour(self, cours, edt):
        for i in range(len(edt.week)):
            for heure in edt.week[i].keys():
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is not None and edt.week[i][heure][salle].course == cours.course:
                        return i, heure, salle




    def reproduction(self, parent1, parent2):

        enfant1 = Timetable(University.classrooms, self.universite.ListeCours)
        enfant2 = Timetable(University.classrooms, self.universite.ListeCours)
        for i in range(len(parent1.week)):
            for heure in parent1.week[i].keys():
                for salle in parent1.week[i][heure].keys():
                    if i % 2 == 0:
                        enfant1.week[i][heure][salle] = parent1.week[i][heure][salle]
                        enfant2.week[i][heure][salle] = parent2.week[i][heure][salle]
                    else :
                        enfant1.week[i][heure][salle] = parent2.week[i][heure][salle]
                        enfant2.week[i][heure][salle] = parent1.week[i][heure][salle]

        eval1 = self.estimerSolution(enfant1)
        eval2 = self.estimerSolution(enfant2)

        if eval1 >= eval2:
            return [enfant1, eval1]
        else:
            return [enfant2, eval2]



    def remplacementPopulation(self, enfant):

        self.population += enfant
        sorted(self.population, key=itemgetter(1), reverse=True)
        self.population = self.population[:self.taille]

    def reparerSolution(self, solution):
        pass

    def main(self):

        while self.nbEstimation < 100000:

            enfants = []
            for i in range(ceil(self.tR*self.taille)):
                parent1, parent2 = random.sample(self.population, 2)
                enfant = self.reproductionAmeliore(parent1[0], parent2[0])
                if random.random() < self.tM:

                    if self.best[1] is not None and enfant[1] > self.best[1]: # Au cas ou on veille muter une solution meilleure que celle actuelle
                        self.best = enfant
                    else:
                        enfant = self.mutation(enfant[0])
                enfants.append(enfant)

            self.remplacementPopulation(enfants)

            sorted(self.population, key=itemgetter(1), reverse=True)
            if self.best[0] is None or self.best[1] < self.population[0][1]:
                self.best = self.population[0]

        print(self.best[0].show())
        print(self.best[1])
