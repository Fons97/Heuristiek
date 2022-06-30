'''
Beam Breadth Search algorithm for the Protein Folding Problem in the HP Lattice Model

- Based on a breadth first search strategy
- Limits search options by only keeping track of results that have generated the
  best scores so far - this is set by beam_size
- By using a larger beam_size, more options are considered, so chances of reaching
  a better score are greater, however this increases the running time of the algorithm
- This algorithm also limits the number of options (and thus the running time) by decreasing
  the probability that a new conformation of the same score as current worst score is being kept
'''

import random
import queue
import copy

from classes.protein_model import Model


class BeamBreadth:

    def __init__(self, model: Model, dimension: int=3):
        self.model = model.copy()
        self.dimension = []
        self.queue = queue.Queue()
        self.scores = []
        self.top_score = 0
        self.best_placement = None
        self.nr_of_states = 0
        self.beam_size = 200
        self.p1 = 0.5

        self.set_dimension(dimension)

    def set_dimension(self, dimension: int) -> list[int, ...]:
        '''
        Returns different move options, depending on whether a protein will be folded in
        2D or 3D
        '''
        if dimension == 2:
            self.dimension = [1, -1, 2, -2]
        elif dimension == 3:
            self.dimension = [1, -1, 2, -2, 3, -3]

        return self.dimension

    def get_index(self, model: Model) -> int:
        '''
        Returns the index or id of the last placed amino node
        If the current node is last node of protein, return last node message
        Last node message is needed to prevent the algorithm from trying to place
        a non-existent amino after the last amino acid in chain
        '''
        last_amino = False

        for key, amino in model.protein.items():

            # Amino's not yet placed on grid have value 'None'
            if amino[1] == None:

                # Key - 1 is returned because moves are performed on previously
                # placed amino to determine the new values of current amino
                return key - 1

            # If no amino's have 'None' as values, this means we've reached the end of the protein
            last_amino = True

        if last_amino == True:
            return -1

    def get_score(self, model: Model) -> int:
        '''
        Returns the current score of a partial conformation
        '''
        score = model.current_score()

        return score

    def score(self) -> int:
        '''
        Returns the best score of partial conformations overall
        '''
        return self.top_score

    def beam(self, model: Model, index: int, score: int) -> None:
        '''
        Keeps tracks of highest scores so far and decides whether a new partial
        conformations' score is good enough to build further upon
        '''
        # Keeps the beam at beam_length by checking number of stored scores
        if len(self.scores) > self.beam_size:

            # Determine current overall worst score
            worst_score = max(self.scores)

            # If new score is equal to current worse, give it x percent chance to be kept
            if score == worst_score:

                if random.random() > self.p1:

                    # Remove worst score from beam and update scores
                    self.scores.remove(max(self.scores))
                    self.update_scores(model, score)

            # All partial conformations with better scores than current worst score are kept
            elif score < worst_score:
                    self.scores.remove(max(self.scores))
                    self.update_scores(model, score)

        # Add all new partial conformation to queue to build further upon when beam size is not yet reached
        else:
            self.update_scores(model, score)

    def update_scores(self, model: Model, score: int) -> None:
        '''
        Adds new scores, updates number of states and adds new partial conformations
        to the queue
        Also updates the top score reached so far
        '''
        self.scores.append(score)
        self.nr_of_states = self.nr_of_states + 1
        child = model.copy()
        self.queue.put(child)

        # If new score is better or equal to current top score
        if score <= min(self.scores):

            # Store new top score and protein object
            self.best_placement = child
            self.top_score = score

    def place_amino_acid(self, model: Model, amino: tuple[str, int, int, int], index: int, direction: int) -> None:
        '''
        Places amino acids on grid, based on coordinates of previous placed amino
        and performed move on those coordinates
        Results are transferred to update status function to evaluate and update
        the status of self
        '''
        # Get coordinates of current amino
        x = amino[1]
        y = amino[2]
        z = amino[3]

        # Get a list of coordinates currently occupied by amino acids
        filled_coordinates = model.filled_coordinates()

        # Place next amino node on grid if not yet occupied by an amino
        if direction == -1 and (x - 1, y, z) not in filled_coordinates:

            # Add new coordinates to amino acid and update score, beam and self
            x = x - 1
            self.update_status(model, index, x, y, z)

        elif direction == 1 and (x + 1, y, z) not in filled_coordinates:
            x = x + 1
            self.update_status(model, index, x, y, z)

        elif direction == -2 and (x, y - 1, z) not in filled_coordinates:
            y = y - 1
            self.update_status(model, index, x, y, z)

        elif direction == 2 and (x, y + 1, z) not in filled_coordinates:
            y = y + 1
            self.update_status(model, index, x, y, z)

        elif direction == -3 and (x, y, z - 1) not in filled_coordinates:
            z = z - 1
            self.update_status(model, index, x, y, z)

        elif direction == 3 and (x, y, z + 1) not in filled_coordinates:
            z = z + 1
            self.update_status(model, index, x, y, z)

    def update_status(self, model: Model, index: int, x: int, y: int, z: int) -> None:
        '''
        Assigns coordinates to amino acids, irreversibly placing them on the grid
        Sends new conformation to beam function to determine if new conformation is
        kept
        '''
        model.assign_coordinates([[index + 1, x, y, z]])
        score = self.get_score(model)
        self.beam(model, index, score)

    def last_amino(self, model: Model, index: int) -> None:
        '''
        When algorithm is at last amino of protein chain, score is updated one last
        time to get the final highest score & best folding
        '''
        score = self.get_score(model)
        self.beam(model, index, score)

    def run(self) -> Model:

        # Set directions to work with, results in either a 2D or 3D folding
        directions = self.set_dimension(self.dimension)

        # Create protein to build new states with
        protein = self.model.copy()

        self.queue.put(protein)

        # Continue until every amino acid is placed on grid
        while not self.queue.empty():

            # Get next state to evaluate
            partial_protein = self.queue.get()

            # Index of current amino acid to evaluate
            index = self.get_index(partial_protein)

            # If the last amino in protein is reached, update scores and quit
            if index == -1:
                self.last_amino(partial_protein, index)
                break

            for direction in directions:

                # Get details about current amino
                amino = partial_protein.protein[index]

                # Place next amino at every direction possible to evaluate
                self.place_amino_acid(partial_protein, amino, index, direction)

        # After all amino acids have been placed on grid, return the placement with the best score
        return self.best_placement
