
class Course:

    def __init__(self, course, classroom):
        self.course = course
        self.classroom = classroom
        # Définir des salles de préférences pour le cours


    def isInSameClassroom(self, other):
        if self.classroom == other.classroom:
            return True
        return False
