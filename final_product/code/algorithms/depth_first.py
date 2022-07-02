'''
Depth First Algorithm for the Protein Folding Problem in the HP Lattice Model

- Navigates down the possible state tree, using a depth first search strategy
- Covers the entire state-space
'''

import copy

from code.classes.protein_model import Model


class DepthFirst:

    def __init__(self, model: Model, dimension: int=3):
        self.model = model.copy()
        self.dimension = dimension
        self.best_placement = None
        self.best_score = 0
        self.main_stack = []
        self.depth = True

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
        '''
        last_amino = False

        for key, amino in model.protein.items():
            if amino[1] == None:
                return key - 1

            last_amino = True

        if last_amino == True:
            return -1

    def get_score(self, model: Model) -> int:
        '''
        Returns score of partial conformation
        '''
        score = model.current_score()

        if score <= self.best_score:
            self.best_score = score
            self.best_placement = model

        return score

    def score(self) -> int:
        '''
        Returns the best score of partial conformations overall
        '''
        return self.best_score

    def get_next_protein(self) -> Model:
        return self.main_stack.pop()

    def update_states(self, model: Model, index: int, x: int, y: int, z: int):
        '''
        Assigns new coordinates to amino acid, updates the score and places
        new children on the stack
        '''
        model.assign_coordinates([[index + 1, x, y, z]])
        self.get_score(model)
        child = model.copy()
        self.main_stack.append(child)

    def run(self) -> Model:

        # Create protein to build new states with
        first_protein = self.model.copy()

        # Put starting state in queue
        self.main_stack = []
        self.main_stack.append(first_protein)

        # Keep excecuting algorithm until all possible solutions have been generated
        while self.main_stack != []:

            # Get next state
            partial_protein = self.get_next_protein()

            # Get the id of current amino node
            index = self.get_index(partial_protein)

            # If the last amino in protein is reached, update scores and quit
            if index == -1 and self.depth == True:
                continue
            elif index == -1 and self.depth == False:
                break

            # Create a new state for each possible move for next amino
            for direction in self.dimension:

                # Get details about current amino node
                amino = partial_protein.protein[index]

                # Assign coordinates of amino node
                x = amino[1]
                y = amino[2]
                z = amino[3]

                filled_coordinates = partial_protein.filled_coordinates()

                # Place next amino node on grid if possible, based on direction
                if direction == -1 and (x - 1, y, z) not in filled_coordinates:

                    # Update coordinates of next amino and create new state
                    x = x - 1
                    self.update_states(partial_protein, index, x, y, z)

                elif direction == 1 and (x + 1, y, z) not in filled_coordinates:
                    x = x + 1
                    self.update_states(partial_protein, index, x, y, z)

                elif direction == -2 and (x, y - 1, z) not in filled_coordinates:
                    y = y - 1
                    self.update_states(partial_protein, index, x, y, z)

                elif direction == 2 and (x, y + 1, z) not in filled_coordinates:
                    y = y + 1
                    self.update_states(partial_protein, index, x, y, z)

                elif direction == -3 and (x, y, z - 1) not in filled_coordinates:
                    z = z - 1
                    self.update_states(partial_protein, index, x, y, z)

                elif direction == 3 and (x, y, z + 1) not in filled_coordinates:
                    z = z + 1
                    self.update_states(partial_protein, index, x, y, z)

        # If all amino nodes have been placed, return the placement with the best score
        return self.best_placement
