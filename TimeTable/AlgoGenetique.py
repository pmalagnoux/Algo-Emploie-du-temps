import random

import numpy as np
from Timetable import Timetable
from University import University
from Student import Student
from math import ceil
class AlgoGenetique:

    def __init__(self, population, tReproduction, tMutation, universite):
        self.universite = universite # contient les données du problème

        self.population = []
        self.tR = tReproduction
        self.tM = tMutation
        self.creerPopulationInitiale() #On initialise la population initiale
        self.best = None
        self.nbEstimation = 0

    def creerPopulationInitiale(self):
        for i in range(len(self.population)):
            self.population.append((Timetable(University.classrooms, self.universite.ListeCours), 0))
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
        pass

    def reproduction(self, parent1, parent2):
        pass

    def remplacementPopulation(self, enfant):
        pass

    def reparerSolution(self, solution):
        pass

    def main(self):
        while self.nbEstimation < 100000:
            enfants = []
            for i in range(ceil(self.tR*self.population)):
                parent1, parent2 = random.sample(self.population, 2)
                enfant = self.reproduction(parent1[0], parent2[0])
                if random.random() < self.tM:
                    enfant = self.mutation(enfant)
                enfants.append(enfant)

            self.remplacementPopulation(enfants)
