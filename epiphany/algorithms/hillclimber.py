import copy
import random
import queue


from .randomize import randomize
from classes.protein import Protein

class HillClimber:

    def __init__(self, random_protein):
        
        self.protein = copy.deepcopy(random_protein)
        self.score = self.protein.relaxed()
        self.queue = queue.Queue()
        self.possible_moves = self.possible_moves(self.protein.view_protein_string())


    def fold_amino(self, temp_protein):
    
        #temp_protein.fold_amino_ran(temp_protein)
        pass


    def fold_protein(self, protein):
        amino_list = protein.view_protein()
        folded_proteins = []
        length = len(amino_list) - 2
        chosen_one = random.randint(0, length)

        directions = [0, 1, 2, 3]

        for direction in directions:
            temp_protein = copy.deepcopy(protein)
            temp_protein.rotational_pull_fuck(chosen_one, chosen_one + 1, direction)
            folded_proteins.append(temp_protein)


        # for move in self.possible_moves:

        #     temp_protein = copy.deepcopy(protein)
        #     temp_protein.rotational_pull_fuck(move[0], move[1], move[2])
        #     folded_proteins.append(temp_protein)

        return folded_proteins


    def check_protein(self, folded_proteins):

        for obj in folded_proteins:
       
            temp_score = obj.relaxed()
       
            # print(temp_score)
            
            if temp_score <= self.score:
                self.protein = obj
                self.score = temp_score

            print(self.score)


    def run(self, iterations):
       
        self.iterations = iterations

        for iteration in range(iterations):
            new_protein = copy.deepcopy(self.protein)
            folded_proteins = self.fold_protein(new_protein)
            self.check_protein(folded_proteins)
            print(iteration, "iteration")
       
        return self.protein

        
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


