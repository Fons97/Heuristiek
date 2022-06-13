import random
import matplotlib.pyplot as plt
import numpy as np
from aminoacid import AminoAcid

class Protein():
    def __init__(self, protein_string):
        self.string = protein_string
        self.amino_dict = {}
        self.move_options = [-1, 1, -2, 2, -3, 3]
        self.previous_move = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.used_options = []
        self.score_list = []
        self.move_list = []

    def choose_move(self, previous_move):
        '''
        Choose a move at random constrained by previous executed move 
        Return move 
        '''

        if previous_move == 1:
            self.move_options = [1, -2, 2 , -3 , 3]
        elif previous_move == -1:
            self.move_options = [-1, -2, 2, -3, 3]
        elif previous_move == 2:
            self.move_options = [-1, 1, 2, -3, 3]
        elif previous_move == -2:
            self.move_options = [-1, 1, -2, -3, 3]
        elif previous_move == 3:
            self.move_options = [-1, 1, -2, 2, 3]
        elif previous_move == -3:
            self.move_options = [-1, 1, -2, 2, -3]

        move = random.choice(self.move_options)

        return move

    def amino_acid(self):
        '''
        MOVE TO ALGORTIHM CLASS
        '''

        for index, letter in enumerate(self.string):
            amino = AminoAcid(index)

            if self.previous_move == 0:
                self.previous_move = random.choice(self.move_options)

            move = self.check_move()

            self.previous_move = move

            self.amino_dict[index] = [letter, self.x, self.y, self.z]
            self.used_options.append((self.x, self.y, self.z))

        return self.amino_dict
        

    def check_move(self):
        '''
        Checks if it's possible to place next amino-acid at coordinates
        Returns tuple of coordinates 
        '''
        x = self.x
        y = self.y
        z = self.z

        while True:
            move = self.choose_move(self.previous_move)

            if move == -1 and (x - 1, y, z) not in self.used_options:
                x = x - 1
                break

            elif move == 1 and (x + 1, y, z) not in self.used_options:
                x = x + 1
                break

            elif move == -2 and (x, y - 1, z) not in self.used_options:
                y = y - 1
                break

            elif move == 2 and (x, y + 1, z) not in self.used_options:
                y = y + 1
                break

            elif move == -3 and (x, y, z - 1) not in self.used_options:
                z = z - 1
                break

            elif move == 3 and (x, y, z + 1) not in self.used_options:
                z = z + 1
                break

        self.x = x
        self.y = y
        self.z = z

        return (self.x, self.y, self.z)