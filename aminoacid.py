class AminoAcid():
    def __init__(self, amino):
        self.type = amino
        self.x = 0
        self.y = 0
        self.z = 0

    def amino_type(self):
        for i in self.type:
            return i
    
