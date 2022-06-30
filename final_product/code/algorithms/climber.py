'''
Random HillClimber algorithm for the Protein Folding Problem in the HP Lattice Model

- This itterative algorithm chooses and reassigns random parts of a protein that is already created
  and placed in the grid.
- The algorithm uses depth-first search to create a new possible path for the
  protein-part, as soon as a path is found, new coordinates are assigned and no other
  paths are considered. The rest of the protein is left intact.
- The new conformation is then evaluated, if the new score is better than the old
  score, the new conformation is kept and another part of the protein is randomly
  folded. If the score is lower, the old conformation is kept and randomly folded. This
  is the basis of the HillClimber algorithm.
- We've slightly altered the algorithm above, based on the heuristic assumption that
  keeping conformations with a score slightly below sub-optimal will lead to a better
  score in the end. However, the conformation that has so far generated the best score, is
  always stored just in case.
'''

import random
import math
import copy

from algorithms import randomize

from classes.protein_model import Model


class RandomClimber():

    def __init__(self, model: Model, dimension: int=3):
        self.model = model.copy()
        self.dimension = []
        self.moves = []
        self.best_score = 0
        self.current_score = 0
        self.best_placement = None
        self.current_placement = None
        self.iterations = 0
        self.p1 = 0.2

        self.set_dimension(dimension)

    def set_dimension(self, dimension: int) -> list[int, ...]:
        '''
        Returns different move options, depending on whether a protein will be folded in
        2D or 3D
        '''

        self.set_moves(dimension)

        if dimension == 2:
            self.dimension = [1, -1, 2, -2]
        elif dimension == 3:
            self.dimension = [1, -1, 2, -2, 3, -3]

        return self.dimension

    def set_moves(self, number: int) -> list[tuple[int, int, int], ...]:
        '''
        Returns different options for coordinate mutations, depending on whether a protein will be folded in
        2D or 3D
        '''
        if number == 2:
            self.moves = [(-1, 0, 0), (1, 0, 0),
                          (0, -1, 0), (0, 1, 0)]
        elif number == 3:
            self.moves = [(-1, 0, 0), (1, 0, 0),
                          (0, -1, 0), (0, 1, 0),
                          (0, 0, -1), (0, 0, 1)]

        return self.moves

    def update_score(self, model: Model) -> None:
        '''
        Updates the current and best scores of conformation
        Sub-optimal conformations have a slight chance of being kept
        '''
        score = self.get_score(model)

        # Sometimes accept a score below current best, to try and generate a better score at a later time
        if score == self.best_score + 1 or score == self.best_score + 2:
            if random.random() > self.p1:
                new_protein = model.copy()

                # Check if the new solution is valid and update score
                if self.is_valid(new_protein) == True:
                    self.current_score = self.get_score(new_protein)
                    self.current_placement = new_protein

        # If score is better than current score, update score and perform next mutation on new conformation
        elif score <= self.best_score:

            new_protein = model.copy()

            # Check if new conformation is valid
            if self.is_valid(new_protein) == True:
                self.best_score = self.get_score(new_protein)
                self.current_score = copy.copy(self.best_score)
                self.current_placement = new_protein
                self.best_placement = new_protein

    def is_valid(self, model: Model) -> bool:
        '''
        Checks whether a new conformation is valid, eg no double coordinates and
        self-avoiding
        '''
        # Get a list of current coordinates of new conformation
        coords = model.filled_coordinates()

        # Place duplicate coordinates in a list
        duplicates = list(set([ele for ele in coords if coords.count(ele) > 1]))

        # If there are no duplicate coordinates, the conformation is valid
        if len(duplicates) == 0:
            return True

        return False

    def get_new_path(self, model: Model, begin_index: int, end_index: int) -> Model:
        '''
        Calculates the number of moves that are needed to create a new random path
        Calls the function to generate a new possible path with that length
        '''
        # Length of path/moves needed to get from begin amino to end amino
        path_length = end_index - begin_index

        # Try to create a new protein conformation using Manhatten Distance calculation
        new_protein = self.generate_random_path(model, begin_index, end_index, path_length)

        return new_protein

    def generate_random_path(self, model: Model, begin_index: int, end_index: int, path_length: int) -> Model:
        '''
        Uses the coordinates of the begin- and end amino and the path length to
        generate a new random path for a random part of the conformation
        This is done by using the Manhattan distance calculation to check that the
        new walk has the same length as the old walk, thus ensuring that the begin
        and end amino can stay at the same place on the grid
        '''
        new_protein = model.copy()
        nr_of_moves_made = []

        # Get the coordinates of the amino the moves need to form a path to
        garbage, end_x, end_y, end_z = model.protein[end_index]

        # Choose as many moves as length of the path
        for i in range(path_length):

            # Calculate Manhattan disctance between current amino and end amino
            garbage, begin_x, begin_y, begin_z = new_protein.protein[begin_index - 1 + i]

            delta_x = abs(begin_x - end_x)
            delta_y = abs(begin_y - end_y)
            delta_z = abs(begin_z - end_z)

            MH_distance = delta_x + delta_y + delta_z

            # Choose a random move and evaluate possibilty by comparing new Manhattan distance
            for j in range(6):
                move = random.choice(self.moves)

                # Calculate new Manhatten distance with newly chosen path
                next_x = begin_x + move[0]
                next_y = begin_y + move[1]
                next_z = begin_z + move[2]

                new_delta_x = abs(next_x - end_x)
                new_delta_y = abs(next_y - end_y)
                new_delta_z = abs(next_z - end_z)

                next_MH_distance = new_delta_x + new_delta_y + new_delta_z

                # If the new Manhattan distance is greater than current, new path isn't possible
                if next_MH_distance > MH_distance:
                    continue

                # If the new distance is equal to or smaller, the new path is still possible
                else:

                    # Update coordinates and move on to the next amino on path
                    new_protein.assign_coordinates([[begin_index + i, next_x, next_y, next_z]])
                    nr_of_moves_made.append(move)
                    break

        # If new end coord are the same as before and new path has same length as
        # old, new conformation is possible
        if model.protein[end_index] == new_protein.protein[end_index] and len(nr_of_moves_made) == path_length:
            return new_protein

        # Else, return the model without any alterationse
        return model

    def get_substring_index(self, model: Model) -> tuple[int, int]:
        '''
        Choose a random part of the protein to assign new coordinates to
        '''
        amino_1 = 1
        amino_2 = 0

        while amino_1 >= amino_2:
            amino_1 = random.randint(1, len(model.string) - 2)
            amino_2 = random.randint(0, len(model.string) - 2)

        return amino_1, amino_2

    def get_score(self, model: Model) -> int:
        '''
        Returns score of conformation
        '''
        score = model.current_score()

        return score

    def score(self) -> int:
        '''
        Returns the best score of conformations overall
        '''
        return self.best_score

    def run(self, iterations: int) -> Model:

        self.iterations = iterations

        # Generate starting state, score, current placement etc
        protein = self.model.copy()
        start_score = self.get_score(protein)
        self.current_placement = protein.copy()
        self.best_placement = copy.copy(self.current_placement)

        for i in range(self.iterations):

            # Get previous best conformation
            protein_solution = self.current_placement.copy()

            # If no walks of len are possible because of starting state, generate new starting state
            if protein_solution == protein:
                protein_solution = randomize(protein)

            # Get indexes of part of protein to re-assign coordinates to
            start_amino, end_amino = self.get_substring_index(protein_solution)

            # Get a new path from start amino to end amino
            new_conformation = self.get_new_path(protein_solution, start_amino, end_amino)

            # If the new conformation wasn't possible, continue with the previous one
            if new_conformation == protein_solution:
                continue

            # Update scores/status if a new conformation is created
            self.update_score(new_conformation)

        return self.best_placement
