import random
import queue
import copy
import math

from classes.protein import Protein
from classes.amino import Amino


class BeamBreadth:

    def __init__(self, model, dimension):
        self.model = model.copy()
        self.dimension = []
        self.queue = queue.Queue()
        self.scores = []
        self.top_score = 0
        self.best_placement = None
        self.nr_of_states = 0
        self.beam_size = 100

        self.set_dimension(dimension)

    def set_dimension(self, int):
        if int == 2:
            self.dimension = [1, -1, 2, -2]
        elif int == 3:
            self.dimension = [1, -1, 2, -2, -3, 3]

        return self.dimension

    def get_index(self, model):
        '''
        Returns the index or id of the last placed amino node
        If the current node is last node of protein, return last node message
        '''
        last_amino = False

        for key, amino in model.protein.items():
            if amino[1] == None:
                return key - 1

            last_amino = True

        if last_amino == True:
            return "last_amino_node"

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
        return self.top_score

    def beam(self, index, partial_protein, score):

        # print("Amino id:", index, "|", "Nr of states:", self.nr_of_states, "|", "Best score:", self.top_score)

        # Keep the beam at 20
        if len(self.scores) > self.beam_size:

            # Determine current worst score
            worst_score = max(self.scores)

            if score <= worst_score:
                self.scores.remove(max(self.scores))
                self.scores.append(score)

                # Add partial conformation to queue to build further upon
                self.nr_of_states = self.nr_of_states + 1
                child = partial_protein.copy()
                self.queue.put(child)

                if score <= min(self.scores):
                    print("Amino id:", index, "|", "Nr of states:", self.nr_of_states, "|", "Best score:", self.top_score)

                    # Update current best partial conformation
                    self.best_placement = partial_protein
                    self.top_score = score

        else:
            # Add partial conformation to queue to build further upon
            self.scores.append(score)
            self.nr_of_states = self.nr_of_states + 1
            child = partial_protein.copy()
            self.queue.put(child)


    def run(self):

        directions = self.set_dimension(self.dimension)

        # Create protein to build new states with
        protein = self.model.copy()

        # Place first and second amino of protein on grid, to eliminate protein rotation
        protein.assign_coordinates([[1, 1, 0, 0]])

        # Put starting state in queue
        self.queue.put(protein)

        while not self.queue.empty():

            # Get next state to evaluate
            partial_protein = self.queue.get()

            # Get the id of current amino
            index = self.get_index(partial_protein)

            # If the last amino in protein is reached, update scores and quit
            if index == "last_amino_node":
                break

            # "Pseudo-place" amino node at each direction
            for direction in directions:

                # Get details about current amino node
                amino_node = partial_protein.protein[index]

                # Assign coordinates of amino node
                x = amino_node[1]
                y = amino_node[2]
                z = amino_node[3]

                filled_coordinates = partial_protein.filled_coordinates()

                # Place next amino node on grid if possible, based on direction
                if direction == -1 and (x - 1, y, z) not in filled_coordinates:

                    # Update coordinates of next amino node
                    x = x - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    # Get the current score of partial conformation
                    score = self.get_score(partial_protein)

                    # Decide whether to keep current partial conformation, based on score
                    self.beam(index, partial_protein, score)

                elif direction == 1 and (x + 1, y, z) not in filled_coordinates:
                    x = x + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.beam(index, partial_protein, score)

                elif direction == -2 and (x, y - 1, z) not in filled_coordinates:
                    y = y - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.beam(index, partial_protein, score)

                elif direction == 2 and (x, y + 1, z) not in filled_coordinates:
                    y = y + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.beam(index, partial_protein, score)

                elif direction == -3 and (x, y, z - 1) not in filled_coordinates:
                    z = z - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.beam(index, partial_protein, score)

                elif direction == 3 and (x, y, z + 1) not in filled_coordinates:
                    z = z + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.beam(index, partial_protein, score)

        # If all amino nodes have been placed, return the placement with the best score
        print("Number of states:", self.nr_of_states)
        print(self.best_placement.protein, "best placement")
        print(self.best_placement.step_order())

        return self.best_placement
