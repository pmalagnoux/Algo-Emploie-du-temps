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
        """
        Créé une population d'EDT aléatoires
        """
        for i in range(self.taille):
            self.population.append([Timetable(University.classrooms, self.universite.ListeCours), 0])
            self.population[i][0].creerRandomEmploieDuTemps()
            self.population[i][1] = self.estimerSolution(self.population[i][0])

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
        #### Distance entre les cours ####
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
        ######################################################################################
        return score
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


    def mutation(self, solution):
        """
        Modifie légèrement la solution en échangeant 2 cours aléatoire dans l'emploi du temps
        :param solution: EDT
        :return: [solutionMuté, NouvelleEvaluation]
        """
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
        """
        Méthode de reproduction entre deux emploi du temps parents
        :param parent1: EDT
        :param parent2: EDT
        :return: enfant : EDT
        """
        enfant1 = Timetable(University.classrooms, self.universite.ListeCours)
        enfant2 = Timetable(University.classrooms, self.universite.ListeCours)

        listeConflict1 = []
        listeConflict2 = []

        for i, cours in enumerate(self.universite.ListeCours): # On cherche a placer tous les cours
            i1, h1, s1 = self.chercherCour(cours, parent1)
            i2, h2, s2 = self.chercherCour(cours, parent2)
            if i % 2 == 0:
                if enfant1.week[i1][h1][s1] is None:
                    enfant1.week[i1][h1][s1] = cours
                elif enfant1.week[i2][h2][s2] is None:
                    enfant1.week[i2][h2][s2] = cours
                else:
                    listeConflict1.append(cours)

                if enfant2.week[i2][h2][s2] is None:
                    enfant2.week[i2][h2][s2] = cours
                elif enfant2.week[i1][h1][s1] is None:
                    enfant2.week[i1][h1][s1] = cours
                else:
                    listeConflict2.append(cours)

            else:
                if enfant1.week[i2][h2][s2] is None:
                    enfant1.week[i2][h2][s2] = cours
                elif enfant1.week[i1][h1][s1] is None:
                    enfant1.week[i1][h1][s1] = cours
                else:
                    listeConflict1.append(cours)

                if enfant2.week[i1][h1][s1] is None:
                    enfant2.week[i1][h1][s1] = cours
                elif enfant2.week[i2][h2][s2] is None:
                    enfant2.week[i2][h2][s2] = cours
                else:
                    listeConflict2.append(cours)
        # On place ceux que l'on a pas pu placer avec notre méthode
        for cours in listeConflict1:
            enfant1.PlacerCours(cours)
        for cours in listeConflict2:
            enfant2.PlacerCours(cours)

        eval1 = self.estimerSolution(enfant1)
        eval2 = self.estimerSolution(enfant2)

        if eval1 >= eval2: # On retourne le meilleur enfant
            return [enfant1, eval1]
        else:
            return [enfant2, eval2]


    def chercherCour(self, cours, edt):
        """
        Retourne la position du cours dans l'emploie du temps
        :param cours: Cours
        :param edt: EDT
        :return: jour, heure, salle
        """
        for i in range(len(edt.week)):
            for heure in edt.week[i].keys():
                for salle in edt.week[i][heure].keys():
                    if edt.week[i][heure][salle] is not None and edt.week[i][heure][salle].course == cours.course:
                        return i, heure, salle



    def remplacementPopulation(self, enfants):
        """
        Méthode de remplacement de la population élitiste
        (on ne garde que ceux ayant la meilleure évaluation)
        :param enfants: Liste Enfants
        """
        self.population += enfants
        self.population = sorted(self.population, key=itemgetter(1), reverse=True)
        self.population = self.population[:self.taille]



    def main(self):

        while self.nbEstimation < 10000:

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

            self.population = sorted(self.population, key=itemgetter(1), reverse=True)
            if self.best[0] is None or self.best[1] < self.population[0][1]:
                self.best = self.population[0]
                self.best[0].show()
                print(self.best[1])
