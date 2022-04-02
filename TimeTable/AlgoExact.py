
from operator import itemgetter
from Student import Student
import numpy as np

from University import University
from Timetable import Timetable


class AlgoExact:

    def __init__(self, universite):
        self.universite = universite
        self.edt = self.universite.timetable
        self.best = - np.inf
        self.backtrackingAllSolution(self.universite.ListeCours.copy(), self.edt)

    def backtrackingAllSolution(self, listeCoursAPlacer, edt):
        """
        Algorithme de Backtracking qui recherche le meilleur emploi du temps possible
        """
        i, h, s = self.nextEmpty(edt)
        if len(listeCoursAPlacer) == 0: # Si il n'y a plus de cours à placer
            self.bestEdt = Timetable(University.classrooms, self.universite.ListeCours, edt.week.copy())
            self.best = self.estimerSolution(self.bestEdt)
            self.bestEdt.show()
            print(self.best)
            return True
        if i == -1: # Permet d'enlever les False placé afin de sauter certaines cases de l'EDT
            self.makeFalseNoneAgain(edt)
        else:
            for cours in listeCoursAPlacer: # On cherche le meilleur cours à placer à cet endroit
                edt.week[i][h][s] = cours
                esti = self.estimerSolution(edt)
                if esti > self.best and self.isSolutionPossible(edt):
                    listeCoursAPlacer.remove(cours)
                    if self.backtrackingAllSolution(listeCoursAPlacer.copy(), Timetable(University.classrooms,self.universite.ListeCours,edt.week.copy())):
                        continue
                    listeCoursAPlacer.append(cours)
                self.edt.week[i][h][s] = None
            self.edt.week[i][h][s] = False
        return False

    def nextEmpty(self, edt):
        """
        Retourne le Prochain emplacement à remplir dans l'EDT
        :return: jour, heure, salle
        """
        for i in range(len(edt.week)):
            for heure in edt.week[i].keys():
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is None:
                        return i, heure, salle
        return -1, -1, -1

    def makeFalseNoneAgain(self, edt):
        """
        Transformes les False en None
        """
        for i in range(len(edt.week)):
            for heure in edt.week[i].keys():
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is False:
                        edt.week[i][heure][salle] = None

    def estimerSolution(self, edt):
        """
        Notation d'un emploi du temps avec les critères suivants :
        # Contraintes fortes
            - Contraites de disponibilité : -1000 à changer
            - Contraites des cours en même temps quand ils sont liés : -1000
        # Contraintes faibles
            - Distances entre deux cours liés par au moins un étudiant : -0.1 par cours qui les séparent * (nb d'étudiants concernés)
            - Salle de préférence : -10
        :
        :return: score
        """
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
                        if (listeCoursMH[j] is not None and listeCoursMH[j] is not False) \
                                and (listeCoursMH[k] is not None and listeCoursMH[k] is not False) \
                                and not self.respectCoursMemeTemps(listeCoursMH[j], listeCoursMH[k]):
                            score -= 1000
                ###########################################
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is not None and edt.week[i][heure][salle] is not False:
                        #### Respect des disponibilités des profs ####
                        if not AlgoExact.respectDispo(i, edt.week[i][heure][salle]):
                            score -= 1000
                        #### Respect de la salle préféré ####
                        if not AlgoExact.respectSallePref(salle, edt.week[i][heure][salle]):
                            score -= 10
                ###########################################
            listeCoursSemaine.append(listeCoursJour)
        #### Distance entre les cours ####
        for i in range(len(listeCoursSemaine)):
            for j in range(len(listeCoursSemaine[i])):
                for k in range(len(listeCoursSemaine[i][j])):
                    if listeCoursSemaine[i][j][k] is not None and listeCoursSemaine[i][j][k] is not False:
                        for l in range(i, len(listeCoursSemaine)):
                            for m in range(j, len(listeCoursSemaine[l])):
                                for n in range(k, len(listeCoursSemaine[l][m])):
                                    if listeCoursSemaine[l][m][n] is not None and listeCoursSemaine[l][m][n] is not False:
                                        distance = abs(k-n) + abs(j-m) + abs(i-l)
                                        nbEtuConcerne = self.universite.graph[Student.courses.index(listeCoursSemaine[i][j][k].course)][Student.courses.index(listeCoursSemaine[l][m][n].course)]
                                        score -= distance * 0.1 * nbEtuConcerne
        ######################################################################################
        return score

    def isSolutionPossible(self, edt):
        """
        Retourne si oui on non l'emploi du temps respecte toutes les contraintes fortes
        :param edt: EDT
        :return: True/False
        """
        for i in range(len(edt.week)):
            for heure in edt.week[i].keys():
                #### Partie respect Cours en Meme Temps ####
                listeCoursMH = list(edt.week[i][heure].values())
                for j in range(len(listeCoursMH)):
                    for k in range(j, len(listeCoursMH)):
                        if (listeCoursMH[j] is not None and listeCoursMH[j] is not False) \
                                and (listeCoursMH[k] is not None and listeCoursMH[k] is not False) \
                                and not self.respectCoursMemeTemps(listeCoursMH[j], listeCoursMH[k]):
                            return False
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is not None and edt.week[i][heure][salle] is not False:

                        #### Respect des disponibilités des profs ####
                        if not AlgoExact.respectDispo(i, edt.week[i][heure][salle]):
                            return False
        return True

    def checkAllCours(self, edt):
        """
        Vérifie si les cours sont tous présents dans l'EDT
        :param edt:
        :return: True/False
        """
        c = 0
        for i in range(len(self.edt.week)):
            for heure in self.edt.week[i].keys():
                for salle in self.edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is not None and edt.week[i][heure][salle] is not False:
                        c += 1
        if c != len(self.universite.ListeCours):
            return False
        return True

    @staticmethod
    def respectDispo(jour, cours):
        """
        Cherche si le cours est sur un jour disponible normalement
        :param jour: jour
        :param cours: Cours
        :return: True/False
        """
        return cours.disponibilite[jour]

    @staticmethod
    def respectSallePref(salle, cours):
        """
        Cherche si le cours se passe dans sa salle préférentielle
        :param salle: Salle
        :param cours: Cours
        :return: True/False
        """
        return salle == cours.classroom

    def respectCoursMemeTemps(self, cours1, cours2):
        """
        Cherche si les cours sont sur le même horaire le même jour
        :param cours1: Cours
        :param cours2: Cours
        :return: True/False
        """
        return self.universite.graph[Student.courses.index(cours1.course)][Student.courses.index(cours2.course)] == 0
