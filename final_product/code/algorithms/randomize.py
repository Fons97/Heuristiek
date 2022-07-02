'''
Randomize Algorithm for the Protein Folding Problem in the HP Lattice Model

- This function will randomly fold a protein in a constructive manner
- It receives a protein model and returns the folded version
- This function can be called before an iterative algoritm is run, to generate a starting state
'''

import random
import copy

from code.classes.protein_model import Model


def randomize(model: Model, dimension: int=3) -> Model:

    # Set dimension
    if dimension == 2:
        dimension = [1, -1, 2, -2]

    elif dimension == 3:
        dimension = [1, -1, 2, -2, 3, -3]

    # Places each amino acid on grid at random, so that protein is still valid
    for id in range(1, model.length):

        # Stop at last amino in chain
        if id == model.length - 1:
            break

        # Get coordinates of last placed amino on grid
        garbage, x, y, z = model.protein[id]

        # Place next amino on grid if not yet occupied by an amino, keep going until a free space is found
        while True:
            move = random.choice(dimension)

            filled_coords = model.filled_coordinates()

            if move == -1 and (x - 1, y, z) not in filled_coords:
                x -= 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 1 and (x + 1, y, z) not in filled_coords:
                x += 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == -2 and (x, y - 1, z) not in filled_coords:
                y -= 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 2 and (x, y + 1, z) not in filled_coords:
                y += 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == -3 and (x, y, z - 1) not in filled_coords:
                z -= 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 3 and (x, y, z + 1) not in filled_coords:
                z += 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

    return model
