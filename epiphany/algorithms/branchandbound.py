'''
- Branch And Bound Algorithm for the Protein Folding Problem in the HP Lattice Model
- Uses breadth first search and reduces the number of branches by
    limiting the probability that a partial conformation will survive if it doesn't
    provide the best score within the partial conformations of the same length
- After all possible and accepted partial conformations are tried, the program returns
    the placement that has generated the best (lowest) score
- Inspired by: https://www.brown.edu/Research/Istrail_Lab/_proFolding/papers/2005/bran-06.pdf
'''

import random
import queue
import copy
import math
from collections import defaultdict
from classes.protein_model import Model
from classes.protein import Protein
from classes.amino import Amino


class BranchAndBound:

    def __init__(self, model, dimension):

        self.main_queue = queue.Queue()
        self.queue = []
        self.model = model.copy()
        self.dimension = dimension
        self.best_placement = None
        self.top_score = 0
        self.best_scores = defaultdict(int)
        self.all_scores = defaultdict(list)
        self.average_scores = defaultdict(int)
        self.p1 = 0.9
        self.p2 = 0.8

    def run(self):
        """
        Runs the branch and bound algorithm until there are no more placements to be generated
        Return the placement with the best score
        """

        # Different direction options for 2D and 3D solution
        if self.dimension == 2:
            directions = [1, -1, 2, -2]
        elif self.dimension == 3:
            directions = [1, -1, 2, -2 ,3, -3]

        # Create protein to build new states with
        # first_protein = copy.deepcopy(self.model)
        first_protein = self.model

        # Place first and second amino of protein on grid, to eliminate protein rotation
        first_protein.assign_coordinates([[0, 0, 0, 0]])
        first_protein.assign_coordinates([[1, 1, 0, 0]])

        # Put starting state in queue
        # self.main_queue.put(first_protein)
        self.queue.append(first_protein)
        print(self.queue)
        # Keep excecuting algorithm until all possible desired solutions have been evaluated
        # while not self.main_queue.empty():
        while self.queue != []:

            # Get next state to evaluate
            # protein = self.main_queue.get()
            protein = self.queue.pop(0)
            print(protein.protein.values(), "protein")

            # Get the id of current amino
            index = self.get_index(protein)
            print(index, "index")

            # If the last amino in protein is reached, update scores and quit
            if index == "last_amino_node":
                score = self.get_score(protein)
                self.update_score(protein, score, index)
                break

            # "Pseudo-place" amino node at each direction
            for direction in directions:

                # Create new protein object for each direction
                # PROBABLY UNECCASSARY 
                partial_protein = self.model.copy()
                print(partial_protein.protein.values(), "values")

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
                    self.prune(partial_protein, amino_node, score, index)

                elif direction == 1 and (x + 1, y, z) not in filled_coordinates:
                    x = x + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == -2 and (x, y - 1, z) not in filled_coordinates:
                    y = y - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == 2 and (x, y + 1, z) not in filled_coordinates:
                    y = y + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == -3 and (x, y, z - 1) not in filled_coordinates:
                    z = z - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == 3 and (x, y, z + 1) not in filled_coordinates:
                    z = z + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

        # If all amino nodes have been placed, return the placement with the best score
        # print(self.best_placement.protein())
            print(self.main_queue)
        return self.best_placement

    def get_index(self, model):
        '''
        Returns the index or id of the last placed amino node
        If the current node is last node of protein, return last node message
        '''
        last_amino = False
        print(model.protein)

        for index, amino in model.protein.items():
            print(index, "index 2")
            if amino[1] == None:
                return index - 1

            last_amino = True

        if last_amino == True:
            return "last_amino_node"

    def get_score(self, model):
        '''
        Returns score of partial conformation
        '''
        score = model.score()
        return score

    def update_score(self, model, score, index):
        '''
        Updates the scores of partial conformation
        - Overal Best Score, regardless of length of partial conformation
        - Best Score within partial conformations of same length
        - Average Score of partial conformations of same length
        - Dictionary of lists with all scores of partial conformations of same length
        '''

        # If current partial conformation has the best score so far, save partial conformation
        if score <= self.top_score:
            self.top_score = score
            self.best_placement = model

        # Add score to list of scores with same length as current partial conformation
        self.all_scores[index].append(score)

        # Re-calculate the average score for partial conformations of same length
        self.average_scores[index] = math.floor(sum(self.all_scores[index]) / len(self.all_scores[index]))

    def score(self):
        '''
        Returns the best score of partial conformations overall
        '''
        return self.top_score

    def prune(self, partial_protein, amino_node, score, index):
        '''
        Decides whether a partial conformation is kept or pruned, based on:
        - Amino type: all possible conformations of type 'P' are kept, 'C' and 'H' are trimmed
        - Score: if a current partial conformation's score is lower than the best score
            of partial conformations of the same length, it has a lower chance of being kept. If the score
            is below the average score of parrtial conformations of the same length, that chance is
            even lower. (That's the way the pruning is supposed to be most efficient anyway, but the
            probabilities can be adjusted.)
        ! The lower the score, the better. Keep this in mind while reading the if-statements below.

        '''

        # Filter amino nodes that could generate points
        if amino_node[0] == 'H' or amino_node[0] == 'C':

            # Current score is lower than best score of same length, new best score, 100% being kept
            if score <= self.best_scores[index]:

                # Update (overall) scores
                self.update_score(partial_protein, score, index)

                # Update best score of partial conformations of same length
                self.best_scores[index] = score

                # Add partial conformation to queue to build further upon
                child = self.model.copy()
                self.main_queue.put(child)

            # Current score is higher than average score, so less chance of being kept
            elif score >= self.average_scores[index]:

                # Generate a random number between 0 and 1
                r = random.random()

                # If random number is higher than self.p1, the partial conformation is kept
                if r > self.p1:

                    self.update_score(partial_protein, score, index)

                    child = self.model.copy()
                    self.main_queue.put(child)

            # If current score is inbetween best_score and average_score, chance of being kept is slightly higher
            elif score > self.best_scores[index] and self.average_scores[index] > score:

                r = random.random()

                if r > self.p2:

                    self.update_score(partial_protein, score, index)

                    child = self.model.copy()
                    self.main_queue.put(child)

        # Keep all partial conformaions if the current amino node is 'P'
        else:

            self.update_score(partial_protein, score, index)

            child = self.model.copy()
            self.main_queue.put(child)
