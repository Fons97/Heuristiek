import copy
import random
import queue

from .randomize import randomize
from classes.protein import Protein
from classes.protein_model import Model


class HillClimber:

    def __init__(self, model):

        self.model = model.copy()
        self.score = self.model.relaxed()
        self.queue = queue.Queue()
        self.possible_moves = self.possible_moves(model.protein.values())

    def fold_protein(self, model):

        folded_proteins = []
        chosen_one = random.randint(0, model.length - 2)

        directions = [0, 1, 2, 3]

        # for direction in directions:
        #     temp_protein = self.model.copy()
        #     temp_protein.rotational_pull_fuck(chosen_one, chosen_one + 1, direction)
        #     folded_proteins.append(temp_protein)

        for move in self.possible_moves:

            temp_protein = self.model.copy()
            temp_protein.rotational_pull_fuck(move[0], move[1], move[2])
            folded_proteins.append(temp_protein)

        return folded_proteins

    def check_protein(self, folded_proteins):

        for obj in folded_proteins:

            temp_score = obj.relaxed()

            # print(temp_score, "tempscore")

            if temp_score <= self.score:
                self.protein = obj
                self.score = temp_score

            # print(self.score, "score")

    def possible_moves(self, amino_list):

        possible_moves = []

        for index in range(len(amino_list)):

            if index < len(amino_list) - 1:
                anchor = index
                swing = index + 1

                for i in range(4):
                    possible_moves.append([anchor, swing, i])

            if index > 0:
                anchor = index -1
                swing = index

                for i in range(4):
                    possible_moves.append([anchor, swing, i])

        return possible_moves

    def run(self, iterations):

            self.iterations = iterations

            for iteration in range(iterations):
                new_protein = self.model.copy()
                folded_proteins = self.fold_protein(new_protein)
                self.check_protein(folded_proteins)
                print(iteration, "iteration")

            return self.protein
