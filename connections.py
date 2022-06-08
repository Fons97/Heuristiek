class Connection():

    def __init__(self, amino_1, amino_2):
        self.amino_1 = amino_1
        self.amino_2 = amino_2
        self.cordinates_1 = self.amino_1.cordinates
        self.cordinates_2 = self.amino_2.cordinates
        self.direction = get_orientation(self.cordinates_1, self.cordinates_2)


    def get_orientation(cord_1, cord_2):
        if cord_1.x != cord_2.x:
            if cord_1.x > cord_2.x:
                direction = "west"
            elif cord_1.x < cord_2.x:
                deriction = "east"

        elif cord_1.y != cord_2.y:
            if cord_1.y < cord_2.y:
                direction = "north"
            elif cord_1.y > cord_2.y:
                deriction = "south"

        else:
            deriction = None

        return direction

class Amino():

    def __init__(self, aminotype, cordinates):
        
