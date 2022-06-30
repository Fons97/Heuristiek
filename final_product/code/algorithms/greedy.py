"""
Randomize Algorithm for the Protein Folding Problem in the HP Lattice Model

- It takes a protein string, checks in a constructive manner the placement that
  generates the best score at that moment.
- If there is no best option, it will choose a move at random.
"""

import random

from classes.protein_model import Model


class Greedy:

    def __init__(self, model: Model, dimension: int=3):
        self.model = model.copy()
        self.dimension = []

        self.set_dimension(dimension)

    def run(self) -> Model:

        for id in range(1, self.model.length):
            if id == self.model.length - 1:
                break

            # Get coordinates of current amino acid
            garbage, x, y, z = self.model.protein[id]

            # Current best score
            best_score = self.model.current_score()

            # Default of best move
            best_move = 1

            # Loop through directions, check if move is possible and increases score
            # If it does, best move is updated, but no definite changes are made to the coords
            for move in self.dimension:
                change_in_score = False
                filled_coordinates = self.model.filled_coordinates()

                if move == -1 and (x - 1, y, z) not in filled_coordinates:
                    if (x - 2, y -1, z) and (x - 2, y + 1, z) and (x - 2, y, z - 1) and (x - 2, y, z + 1) not in filled_coordinates:
                        self.model.assign_coordinates([[id + 1, x - 1, y, z]])
                        temp_score = self.model.current_score()
                        if temp_score > best_score:
                            best_score = temp_score
                            best_move = -1
                            change_in_score = True
                        self.model.assign_coordinates([[id + 1, None, None, None]])

                elif move == 1 and (x + 1, y, z) not in filled_coordinates:
                    if (x + 2, y -1, z) and (x + 2, y + 1, z) and (x + 2, y, z - 1) and (x + 2, y, z + 1) not in filled_coordinates:
                        self.model.assign_coordinates([[id + 1, x + 1, y, z]])
                        temp_score = self.model.current_score()
                        if temp_score > best_score:
                            best_score = temp_score
                            best_move = 1
                            change_in_score = True
                        self.model.assign_coordinates([[id + 1, None, None, None]])

                elif move == -2 and (x, y - 1, z) not in filled_coordinates:
                    if (x - 1, y - 2, z) and (x + 1, y - 2, z) and (x, y - 2, z - 1) and (x, y - 2, z + 1) not in filled_coordinates:
                        self.model.assign_coordinates([[id + 1, x, y - 1, z]])
                        temp_score = self.model.current_score()
                        if temp_score > best_score:
                            best_score = temp_score
                            best_move = -2
                            change_in_score = True
                        self.model.assign_coordinates([[id + 1, None, None, None]])

                elif move == 2 and (x, y + 1, z) not in filled_coordinates:
                    if (x - 1, y + 2, z) and (x + 1, y + 2, z) and (x, y + 2, z - 1) and (x, y + 2, z + 1) not in filled_coordinates:
                        self.model.assign_coordinates([[id + 1, x, y + 1, z]])
                        temp_score = self.model.current_score()
                        if temp_score > best_score:
                            best_score = temp_score
                            best_move = 2
                            change_in_score = True
                        self.model.assign_coordinates([[id + 1, None, None, None]])

                elif move == -3 and (x, y, z - 1) not in filled_coordinates:
                    if (x - 1, y, z - 2) and (x + 1, y, z - 2) and (x, y - 1, z - 2) and (x, y + 1, z - 2) not in filled_coordinates:
                        self.model.assign_coordinates([[id + 1, x, y, z - 1]])
                        temp_score = self.model.current_score()
                        if temp_score > best_score:
                            best_score = temp_score
                            best_move = -3
                            change_in_score = True
                        self.model.assign_coordinates([[id + 1, None, None, None]])

                elif move == 3 and (x, y, z + 1) not in filled_coordinates:
                    if (x - 1, y, z + 2) and (x + 1, y, z + 2) and (x, y - 1, z + 2) and (x, y + 1, z + 2) not in filled_coordinates:
                        self.model.assign_coordinates([[id + 1, x, y, z + 1]])
                        temp_score = self.model.current_score()
                        if temp_score > best_score:
                            best_score = temp_score
                            best_move = 3
                            change_in_score = True
                        self.model.assign_coordinates([[id + 1, None, None, None]])

            if change_in_score == False:
                best_move = random.choice(self.dimension)

            # Amino coords get updated with the move that generated the best score
            # If no move increased the score, a random move is chosen
            while True:
                move = best_move

                if move == -1 and (x - 1, y, z) not in filled_coordinates:
                    x = x - 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 1 and (x + 1, y, z) not in filled_coordinates:
                    x = x + 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -2 and (x, y - 1, z) not in filled_coordinates:
                    y = y - 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 2 and (x, y + 1, z) not in filled_coordinates:
                    y = y + 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -3 and (x, y, z - 1) not in filled_coordinates:
                    z = z - 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 3 and (x, y, z + 1) not in filled_coordinates:
                    z = z + 1
                    self.model.assign_coordinates([[id + 1, x, y, z]])
                    break
                else:
                    best_move = random.choice(self.dimension)

        return self.model
