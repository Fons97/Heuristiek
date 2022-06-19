'''
!!! if probabilities are set too high, chances are that a non-complete confonformation
    is returned. If all places around a amino node are filled, the next amino isn't placed
    on the grid.

- Branch And Bound Algorithm for the Protein Folding Problem in the HP Lattice Model
- Uses breadth first search, but limits the number of branches by
    limiting the probability that a partial conformation will survive if it doesn't
    provide the best score within the partial conformations of the same length
- Inspired by: https://www.brown.edu/Research/Istrail_Lab/_proFolding/papers/2005/bran-06.pdf
'''

import random
import queue
import copy
import math
from collections import defaultdict

from classes.protein import Protein
from classes.amino import Amino


class BranchAndBound():

    def __init__(self, protein_obj, dimension):

        self.main_queue = queue.Queue()
        self.dimension = dimension
        self.protein_obj = protein_obj
        self.best_placement = None
        self.top_score = 0
        self.best_scores = defaultdict(int)
        self.all_scores = defaultdict(list)
        self.average_scores = defaultdict(int)
        self.p1 = 0.9
        self.p2 = 0.8

    def run(self):
        """
        Runs the branch and bound algorithm until there are no more solutions to be generated
        Return the solution with the best score
        """

        # Different direction options for 2D and 3D solution
        if self.dimension == 2:
            directions = [1, -1, 2, -2]
        elif self.dimension == 3:
            directions = [1, -1, 2, -2 ,3, -3]

        # Create protein to build new states with
        first_protein = copy.deepcopy(self.protein_obj)

        # Place first and second amino of protein on grid, to eliminate protein rotation
        first_protein.assign_coordinates([[0, 0, 0, 0]])
        first_protein.assign_coordinates([[1, 1, 0, 0]])

        # Put starting state in queue
        self.main_queue.put(first_protein)

        # Keep excecuting algorithm until all possible desired solutions have been evaluated
        while not self.main_queue.empty():

            # Get next state to evaluate
            protein = self.main_queue.get()

            # Get the id of current amino
            index = self.get_index(protein)

            # If the last amino in protein is reached, update scores and quit
            if index == "last_amino_node":
                score = self.get_score(protein)
                self.update_score(protein, score, index)
                break

            # "Pseudo-place" amino node at each direction
            for direction in directions:

                # Create new protein object for each direction
                partial_protein = copy.deepcopy(protein)

                # Get details about current amino node
                amino_node = partial_protein.view_protein()[index]

                # Assign coordinates of amino node
                x = amino_node[1]
                y = amino_node[2]
                z = amino_node[3]

                # Place next amino node on grid if possible, based on direction
                if direction == -1 and (x - 1, y, z) not in partial_protein.filled_coordinates():

                    # Update coordinates of next amino node
                    x = x - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    # Get the current score of partial conformation
                    score = self.get_score(partial_protein)

                    # Decide whether to keep current partial conformation, based on score
                    self.prune(partial_protein, amino_node, score, index)

                elif direction == 1 and (x + 1, y, z) not in partial_protein.filled_coordinates():
                    x = x + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == -2 and (x, y - 1, z) not in partial_protein.filled_coordinates():
                    y = y - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == 2 and (x, y + 1, z) not in partial_protein.filled_coordinates():
                    y = y + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == -3 and (x, y, z - 1) not in partial_protein.filled_coordinates():
                    z = z - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

                elif direction == 3 and (x, y, z + 1) not in partial_protein.filled_coordinates():
                    z = z + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    self.prune(partial_protein, amino_node, score, index)

        # If all amino nodes have been placed, return the placement with the best score
        print(self.best_placement.view_protein())
        return self.best_placement

    def get_index(self, protein_obj):
        '''
        Returns the index or id of the last placed amino node
        If the current node is last node of protein, return last node message
        '''
        last_amino = False

        for i in protein_obj.view_protein():
            if i[1] == None:
                return i[0] - 1

            last_amino = True

        if last_amino == True:
            return "last_amino_node"

    def get_score(self, protein_obj):
        '''
        Returns score of partial conformation
        '''

        score = protein_obj.reward()
        return score

    def update_score(self, protein_obj, score, index):
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
            self.best_placement = protein_obj

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
        - Amino type: all possible conformations of type 'P' (none points) are kept
        -
        '''

        if amino_node[4] == 'H' or amino_node[4] == 'C':

            # Current score is lower (aka better) than best score, aka new best score
            if score <= self.best_scores[index]:

                # Update scores
                self.update_score(partial_protein, score, index)

                # Update overall best score
                self.best_scores[index] = score

                # Add partial conformation to queue
                child = copy.deepcopy(partial_protein)
                self.main_queue.put(child)

            # Current score is higher (aka worse) than average score, benefit is below average
            elif score >= self.average_scores[index]:

                r = random.random()

                # Prune with probability p1
                if r > self.p1:

                    # Update scores
                    self.update_score(partial_protein, score, index)

                    # Add partial_conformation to main queue / pc
                    child = copy.deepcopy(partial_protein)
                    self.main_queue.put(child)

            # Current score is somewhere between best_score and average_score
            elif score > self.best_scores[index] and self.average_scores[index] > score:

                r = random.random()

                # Prune with probability p2
                if r > self.p2:

                    # Update scores
                    self.update_score(partial_protein, score, index)

                    # Add partial_conformation to main queue / pc
                    child = copy.deepcopy(partial_protein)
                    self.main_queue.put(child)
        else:

            # Update scores
            self.update_score(partial_protein, score, index)

            # Add partial conformation to queue
            child = copy.deepcopy(partial_protein)
            self.main_queue.put(child)
