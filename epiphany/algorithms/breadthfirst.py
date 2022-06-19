# state saving
# pickle.dump(object, file_path)
# variabele = pickle,load(file_path)

import random
import queue
import copy

from classes.protein import Protein
from classes.amino import Amino

class BreadthFirst():

    def __init__(self, protein_obj, dimension):

        self.dimension = dimension
        self.protein_obj = protein_obj
        self.best_placement = None
        self.best_score = 0

    def run(self):

        # Difference between 2D and 3D
        if self.dimension == 2:
            directions = [1, -1, 2, -2]
        elif self.dimension == 3:
            directions = [1, -1, 2, -2 ,3, -3]

        # Copy protein
        first_protein = copy.deepcopy(self.protein_obj)

        # Place first and second amino on grid
        first_protein.assign_coordinates([[0, 0, 0, 0]])
        first_protein.assign_coordinates([[1, 1, 0, 0]])

        # Put starting state in queue
        main_queue = queue.Queue()
        main_queue.put(first_protein)

        # Continue while there are still branches
        while not main_queue.empty():

            # Get conformation that's next in line from queue, partial_conformation needs to change format
            protein = main_queue.get()

            # Update id of amino in chain
            index = self.get_index(protein)

            if index == "last_amino_acid":
                break
                print(index, "index")

            # Check every possible move direction
            for direction in directions:

                # Create new protein object
                partial_protein = copy.deepcopy(protein)

                amino_node = partial_protein.view_protein()[index]

                # Get coordinates of amino acid
                x = amino_node[1]
                y = amino_node[2]
                z = amino_node[3]

                if direction == -1 and (x - 1, y, z) not in partial_protein.filled_coordinates():
                    x = x - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    main_queue.put(child)

                    continue

                elif direction == 1 and (x + 1, y, z) not in partial_protein.filled_coordinates():
                    x = x + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    main_queue.put(child)

                    continue

                elif direction == -2 and (x, y - 1, z) not in partial_protein.filled_coordinates():
                    y = y - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    main_queue.put(child)

                    continue

                elif direction == 2 and (x, y + 1, z) not in partial_protein.filled_coordinates():
                    y = y + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    main_queue.put(child)

                    continue

                elif direction == -3 and (x, y, z - 1) not in partial_protein.filled_coordinates():
                    z = z - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    main_queue.put(child)

                    continue

                elif direction == 3 and (x, y, z + 1) not in partial_protein.filled_coordinates():
                    z = z + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    score = self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    main_queue.put(child)

                    continue

        return self.best_placement

    def get_index(self, protein_obj):

        last_amino = False
        amino_index = 0

        for i, j  in enumerate(protein_obj.view_protein()):
            amino_index = i

            if j[1] == None:
                return j[0] - 1

            last_amino = True

        if last_amino == True:
            return "last_amino_acid"


    def get_score(self, protein_obj):

        score = protein_obj.reward()

        if score <= self.best_score:
            self.best_score = score
            self.best_placement = protein_obj

    def score(self):
        return self.best_score
