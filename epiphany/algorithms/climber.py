import random
import math
import copy
import itertools

from classes.protein import Protein
from classes.amino import Amino

# Create starting_state
# Repeat x amount of times
    # Choose substring
    # Manipulate substring
        # If new_substring score is lower than old_substring score:
            # save state and perform next mutation on saved state
        # Else:
            # keep old state and perform mutation on state

# cashen van die paden??
# opslaan van eerder gedane berekeningen


class Climber():

    def __init__(self, model, dimension):
        self.model = model.copy()
        self.dimension = 3
        self.best_score = 0
        self.best_placement = None

    def run(self):

        # Create starting state
        protein = self.model.copy()
        starting_state = self.randomize(protein)

        # Get a starting score
        self.best_score = self.get_score(starting_state)
        start_score = self.get_score(starting_state)

        # Set starting_state as best placement
        self.best_placement = starting_state.copy()

        for i in range(100):
            print(i, "iteration")

            # Get previous best conformation
            protein_solution = self.best_placement.copy()

            # If no walks of len are possible because of starting state, generate new starting state (only for testings)
            if protein_solution == starting_state:
                protein_solution = self.randomize(protein)

            # Get random indexes of substring to manipulate
            start_amino, end_amino = self.get_substring_index(protein_solution)

            # Get a list of all possible walks from start point of substring to end point of substring
            fitting_walks = self.possible_walks(protein_solution, start_amino, end_amino)

            # If no possible walks, go to next iterations
            if len(fitting_walks) == 0:
                continue

            # Creates new protein objects with all possible walks + create new partial conformations
            self.create_new_walk(fitting_walks, protein_solution, start_amino, end_amino)


        print(starting_state.protein, "startstate")
        print(start_score, "starting score")
        print(self.best_placement.protein, "returned object")
        return self.best_placement

    def create_new_walk(self, walks, protein_obj, start, end):

        walk = random.choice(walks)

        # for walk in walks:
        partial_protein = protein_obj.copy()

        for key, coords in enumerate(walk):

            garbage, x, y, z = partial_protein.protein[start - 1 + key]

            partial_protein.assign_coordinates([[start + key, x + coords[0], y + coords[1], z + coords[2]]])

        # Get score of new partial_protein
        score = self.get_score(partial_protein)

        if score <= self.best_score:

            to_check = partial_protein.copy()

            # Check if new solution is valid and add score etc
            if self.is_valid(to_check) == True:
                self.best_score = self.get_score(to_check)
                self.best_placement = to_check

    def is_valid(self, protein_obj):

        coords_list = protein_obj.filled_coordinates()

        duplicates = list(set([ele for ele in coords_list if coords_list.count(ele) > 1]))

        if len(duplicates) == 0:
            return True

        return False

    def possible_walks(self, model, begin_index, end_index):

        # Determine length of path to travel
        path_length = end_index - begin_index + 2

        # Get all possible walks with that length, regardless of self-avoiding
        all_walks = self.get_walks(path_length)

        # Filter paths (not all of them tho) that aren't self-avoiding
        # self_avoiding_walks = self.path_avoiding_walks(all_walks)

        # Get coords of amino-acid to start counting from
        garbage, model_x, model_y, model_z = model.protein[begin_index - 1]

        # Get coords of amino acid to reach with path
        garbage, model_x_end, model_y_end, model_z_end = model.protein[end_index]

        connecting_walks = []

        for i in all_walks:
            i.pop(0)
            begin_x = model_x
            begin_y = model_y
            begin_z = model_z

            for j in i:
                diff_x, diff_y, diff_z = j[0], j[1], j[2]
                begin_x = begin_x + diff_x
                begin_y = begin_y + diff_y
                begin_z = begin_z + diff_z

            if begin_x == model_x_end and begin_y == model_y_end and begin_z == model_z_end:
                connecting_walks.append(i)

        return connecting_walks

    # def path_avoiding_walks(self, walks):
    #
    #     self_avoiding = []
    #
    #     for walk in walks:
    #         walk.pop(0)
    #
    #         for coords in range(1, len(walk)):
    #             if walk[coords] == (-1, 0, 0) and walk[coords - 1] != (1, 0, 0) or walk[coords] == (1, 0, 0) and walk[coords - 1] != (-1, 0, 0) or walk[coords] == (0, -1, 0) and walk[coords - 1] != (0, 1, 0) or walk[coords] == (0, 1, 0) and walk[coords - 1] != (0, -1, 0) or walk[coords] == (0, 0, -1) and walk[coords - 1] != (0, 0, 1) or walk[coords] == (0, 0, 1) and walk[coords - 1] != (0, 0, -1):
    #                 self_avoiding.append(walk)
    #
    #     self_avoiding.sort()
    #
    #     no_duplicates = list(self_avoiding for self_avoiding,_ in itertools.groupby(self_avoiding))
    #
    #     return no_duplicates

    def get_walks(self, path_length):

        moves = [(-1, 0, 0), (1, 0, 0),
                 (0, -1, 0), (0, 1, 0),
                 (0, 0, -1), (0, 0, 1)]

        # Determine all possible walks that have length path_length

        if path_length == 1:
            return [[0]]
        else:
            walks = []

        for k in self.get_walks(path_length-1):
            for i in moves:
                walks.append(k+[i])

        return walks

    def get_substring_index(self, protein_object):

        amino_1 = 1
        amino_2 = 0

        while amino_1 >= amino_2:
            amino_1 = random.randint(1, 12)
            amino_2 = random.randint(amino_1, amino_1 + 6)

        print(amino_1, amino_2)
        return amino_1, amino_2

    def randomize(self, model):
        '''
        RANDOMIZE EXPLANATION
        '''

        list = [1, -1, 2, -2 , 3, -3]

        for id in range(model.length):

            if id == model.length - 1:
                break

            garbage, x, y, z = model.protein[id]

            while True:
                move = random.choice(list)

                if move == -1 and (x - 1, y, z) not in model.filled_coordinates():
                    x = x - 1
                    model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 1 and (x + 1, y, z) not in model.filled_coordinates():
                    x = x + 1
                    model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -2 and (x, y - 1, z) not in model.filled_coordinates():
                    y = y - 1
                    model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 2 and (x, y + 1, z) not in model.filled_coordinates():
                    y = y + 1
                    model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -3 and (x, y, z - 1) not in model.filled_coordinates():
                    z = z - 1
                    model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 3 and (x, y, z + 1) not in model.filled_coordinates():
                    z = z + 1
                    model.assign_coordinates([[id + 1, x, y, z]])
                    break

        return model

    def get_score(self, model):
        '''
        Returns score of partial conformation
        '''

        score = model.current_score()

        return score

    def score(self):
        '''
        Returns the best score of partial conformations overall
        '''
        return self.best_score
