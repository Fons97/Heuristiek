class Amino():

    def __init__(self, id, amino_type):
        self.id = id
        self.x = None
        self.y = None
        self.z = None
        self.type = amino_type

    def set_cords(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def show_cords(self):
        return self.x, self.y, self.z

    def show_id(self):
        return self.id

    def show_type(self):
        return self.type
