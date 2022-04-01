import math
from numpy import zeros
import Timetable
import Student


class Node:
    def __init__(self, value, edt= {}, bestParent=None, bestCost=math.inf, parent=None, childrens=[], coursesLeftToPlace):
        self.edt = edt
        self.value = value
        self.childrens = []  # On peut placer les cours
        self.edt = edt
        self.coursesLeftToPlace = coursesLeftToPlace
        self.bestParent = bestParent
        self.bestCost = bestCost


    def main(self):
        listeCoursMH = []
        listeCoursSemaine = []
        estimerSolution(edt) #TODO récupérer variables utiles
        self.childrens.bestCost = [math.inf]
        i = 0
        # Pas utile je crois   childrens = numpy.zeros()
        if listeCoursMH == []: #Si plus aucun cours à placer
            return self.computeCost(listeCoursSemaine) # Retourner le cout
        for cours in listeCoursMH: # Parmis les cours à placer
            self.childrens[i] = Node(coursesLeftToPlace=self.coursesLeftToPlace - cours, edt=self.edt.append(cours), parent=self.Node, value = estimerSolution(edt), bestCost=self.bestCost) # Créer un noeud childrens[i]
            i+=1
            # Plus utile self.childrens.append(childNode) #TODO revoir
            if self.childrens[i].bestCost <= self.bestCost: # New best score
                bestCost = self.childrens[i].bestCost
                self.printnode() # Arbitraire/Debug à chaque fois qu'on a un noeud meilleur que le précédent on le print
            self.childrens[0].bestCost = bestCost # Not sure

    def printnode(self):
        print("Cout : " + self.value)
        print("Emploi du temps : " + edt)
        print("##########################################################################################################")

    def estimerSolution(self, edt):
        """
        Notation des critères :
        # Contraintes fortes
            - contraites de disponibilité : -1000 à changer
            - contraites des cours en même temps quand ils sont liés : + infini
        # Contraintes faibles
            - distances entre deux cours lié par au moins un étudiant : -0.1 par cours qui les sépare * (nb d'étudiant concerné)
            - salle de préférence : +10
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
                            score = math.inf
                ###########################################
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is not None :
                        #### Respect des disponibilités des profs ####
                        if not AlgoGenetique.respectDispo(i, edt.week[i][heure][salle]):
                            score = math.inf
                        #### Respect de la salle préféré ####
                        if not AlgoGenetique.respectSallePref(salle, edt.week[i][heure][salle]):
                            score += 10
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

    def respectDispo(jour, cours):
        return cours.disponibilite[jour]

    @staticmethod
    def respectSallePref(salle, cours):
        return salle == cours.classroom


    def respectCoursMemeTemps(self, cours1, cours2):
        return self.universite.graph[Student.courses.index(cours1.course)][Student.courses.index(cours2.course)] == 0