class Connection():

    def __init__(self, amino_1, amino_2):
        self.amino_1 = amino_1
        self.amino_2 = amino_2
        self.coordinates_1 = self.amino_1.coordinates
        self.coordinates_2 = self.amino_2.coordinates
        self.direction = get_orientation(self.coordinates_1, self.coordinates_2)


    def get_orientation(cord_1, cord_2):
        if cord_1.x != cord_2.x:
            if cord_1.x > cord_2.x:
                direction = "west"
            elif cord_1.x < cord_2.x:
                direction = "east"

        elif cord_1.y != cord_2.y:
            if cord_1.y < cord_2.y:
                direction = "north"
            elif cord_1.y > cord_2.y:
                direction = "south"

        else:
            direction = None

        return direction

class Amino():

    def __init__(self, aminotype, coordinates):
        self.aminotype = aminotype
        self.coordinates = coordinates
