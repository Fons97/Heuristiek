'''
Randomize Algorithm for the Protein Folding Problem in the HP Lattice Model

- This algorithm will randomly fold a protein in a constructive manner
- It receives a protein model and returns the folded version
- This function can be called before an iterative algoritm is run, to generate a starting state
'''

import random

from classes.protein_model import Model


class Randomize:

    def __init__(self, model: Model, dimension: int=3):
        self.model = model.copy()
        self.dimension = []

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

    def run(self) -> Model:

        # Places each amino acid on grid at random, so that protein is still valid
        for id in range(1, self.model.length):

            # Stop at last amino in chain
            if id == self.model.length - 1:
                break

            # Get coordinates of last placed amino on grid
            garbage, x, y, z = self.model.protein[id]

            # Place next amino on grid if not yet occupied by an amino, keep going until a free space is found
            while True:
                move = random.choice(self.dimension)

                filled_coords = self.model.filled_coordinates()

                if move == -1 and (x - 1, y, z) not in filled_coords:
                    x -= 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 1 and (x + 1, y, z) not in filled_coords:
                    x += 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -2 and (x, y - 1, z) not in filled_coords:
                    y -= 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 2 and (x, y + 1, z) not in filled_coords:
                    y += 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -3 and (x, y, z - 1) not in filled_coords:
                    z -= 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 3 and (x, y, z + 1) not in filled_coords:
                    z += 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

        return self.model
