# Herhaal:
#     Kies een random start state
#     Kies start temperatuur
#     Herhaal N iteraties:
#         Doe een kleine random aanpassing
#         Als random( ) > kans(oud, nieuw, temperatuur):
#             Maak de aanpassing ongedaan
#         Verlaag temperatuur

import random
import math
import copy

# from algorithms.randomize import randomize
from classes.protein import Protein
from classes.amino import Amino


class SimulatedAnnealing():

    def __init__(self, protein_obj):
        self.protein_obj = protein_obj
        self.score = 0
        self.decay_rate = 0


    def run(self):

        # Herhaal

        # Create starting_state
        protein = copy.deepcopy(self.protein_obj)
        starting_state = self.randomize(protein)

        # Create random stepping sequence
        random_sequence = starting_state.step_order()

        # Choose iterations
        iters = 100
        iterations = [i for i in range(iters)]

        # Choose starting temperature for each iterations
        starting_temperature = 10

        # for i in random_sequence:
            # print(i)

        # temperatures = [starting_temperature/float(i + 1) for i in iterations]
        print(type(starting_state))
        return starting_state

# print(starting_state.view_protein())

    def randomize(self, protein_obj):
        string = protein_obj.view_protein_string()

        protein_obj.assign_coordinates([[0,0,0,0]])

        list = [1, -1, 2, -2 ,3, -3]

        for id in range(len(string)):
            if id == len(string) - 1:
                break
            amino = protein_obj.view_protein()[id]
            x = amino[1]
            y = amino[2]
            z = amino[3]

            while True:
                move = random.choice(list)

                if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
                    x = x - 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
                    x = x + 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
                    y = y - 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
                    y = y + 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
                    z = z - 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
                    z = z + 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

        return protein_obj

    def get_score(self, protein_obj):
        '''
        Returns score of partial conformation
        '''

        self.score = protein_obj.reward()
        # return score

    def score(self):
        '''
        Returns the best score of partial conformations overall
        '''
        return self.score
