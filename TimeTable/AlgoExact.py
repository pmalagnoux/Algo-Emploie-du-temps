
from operator import itemgetter
from Student import Student

class AlgoExact:

    def __init__(self, universite):
        self.universite = universite
        self.edt = self.universite.timetable
        self.backtracking(self.universite.ListeCours)
        print(self.edt.show())
        print(self.estimerSolution(self.edt))

    def backtracking(self, listeCoursAPlacer):
        i, h, s = self.nextEmpty()
        if len(listeCoursAPlacer) != 0 and i == -1:
            self.makeFalseNoneAgain()
            return False
        if len(listeCoursAPlacer) == 0 or i == -1: # Si il n'y a plus de cours à placer ou si l'edt est plein
            return True

        ListeEsti = []

        for cours in listeCoursAPlacer: # On cherche le meilleur cours à placer à cet endroit
            self.edt.week[i][h][s] = cours
            ListeEsti.append([cours, self.estimerSolution(self.edt)])
            self.edt.week[i][h][s] = None

        sorted(ListeEsti, key=itemgetter(1), reverse=True) # On trie la liste pour les selectionner dans l'ordre
        for cours, eval in ListeEsti:
            self.edt.week[i][h][s] = cours
            if self.isSolutionPossible(self.edt):
                listeCoursAPlacer.remove(cours)
                if self.backtracking(listeCoursAPlacer[:]):
                    return True
                listeCoursAPlacer.append(cours)
            self.edt.week[i][h][s] = None
        self.edt.week[i][h][s] = False
        return False

    def nextEmpty(self):

        for i in range(len(self.edt.week)):
            for heure in self.edt.week[i].keys():
                for salle in self.edt.week[i][heure].keys():
                    if self.edt.week[i][heure][salle] is None:
                        return i, heure, salle
        return -1, -1, -1

    def makeFalseNoneAgain(self):
        for i in range(len(self.edt.week)):
            for heure in self.edt.week[i].keys():
                for salle in self.edt.week[i][heure].keys():
                    if self.edt.week[i][heure][salle] is False:
                        self.edt.week[i][heure][salle] = None

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
        return score

    def isSolutionPossible(self, edt):
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

    @staticmethod
    def respectDispo(jour, cours):
        return cours.disponibilite[jour]

    @staticmethod
    def respectSallePref(salle, cours):
        return salle == cours.classroom

    def respectCoursMemeTemps(self, cours1, cours2):
        return self.universite.graph[Student.courses.index(cours1.course)][Student.courses.index(cours2.course)] == 0
