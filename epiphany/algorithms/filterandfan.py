import random
import math
import copy

from classes.protein import Protein
from classes.amino import Amino


class FilterAndFan():

    def __init__(self, protein_obj):
        # self.amino_data = {index(i): [type(i), coordinates(i), east(i), south(i), west(i), north(i)]}
        self.pull_move = [conformation, node, location, energy]
        self.locations = ['northwest', 'northeast', 'southeast', 'southwest']
        pass

    def run(self):
        pass

        tabu_search(protein_object)

        initialize_tree(protein_object_partial)

        generate_tree(X, n1, n2, L)

    def get_local_conformation(self, amino_index, protein_object):
        # Returns the local conformation code associated with the i-th node

        # A list storing all valid pull moves associated with a conformation
        pull_move_list = []


        local_conformation = copy.deepcopy(protein_object)

        return local_conformation

        data = set_structure(local_conformation)

    def is_legal(self, amino_index, target_location, protein_object, local_conformation):

        # Returns True if displacing node i to location j is a valid pull move, and False otherwise
        pass

    def add_pull_move(self, node, location, pull_move_list):

        # Attaches a valid pull move to the pull move list with initial energy value of zero
        # (actual energy values are then evaluated after executing the pull move)
        pass

    def detect_all_pull_moves(self, protein_object, pull_move_list):
        # 1 implementation of pull move neighbourhood

        # Detect all valid pull_moves
        pass

        local_conformation_index = 0
        pull_move_list = []

        # Needs to be further specified with coords etc
        num_of_locations = 6

        for i in protein_object:
            local_conformation_index = get_local_conformation(i, protein_object)
            # num_of_locations =
            for location in num_of_locations:
                if is_legal(index, location, protein_object, local_conformation_node):
                    add_pull_move(index, location, pull_move_list)

    def get_connected(self, node, location, protein_object, protein_object_copy):

        #  Displaces as many nodes as needed to make the conformation connected after moving the initiating
        #  node to the specified location according to the pull-move rules.

        # Once the move is completed, both the pull-move initiating node and the last
        # displaced node are set 'tabu-active' for a predefined number of iterations (we keep n independent tabu lists throughout the tree search)
        pass

    def execute_pull_move(self, protein_object, pull_move):
        # 2 implementation of pull move neighbourhood

        pass

        partial_protein = copy.deepcopy(protein_object)

        if location == "northwest":
            x = partial_protein_x - 1
            y = partial_protein_y + 1
            get_connected(node, location, protein_object, protein_object_copy)

        elif location == "northeast":
            x = partial_protein_x + 1
            y = partial_protein_y + 1
            get_connected(node, location, protein_object, protein_object_copy)

        elif location == "southeast":
            x = partial_protein_x + 1
            y = partial_protein_y - 1
            get_connected(node, location, protein_object, protein_object_copy)

        elif location == "southwest":
            x = partial_protein_x - 1
            y = partial_protein_y - 1
            get_connected(node, location, protein_object, protein_object_copy)

    def evaluate_energy(self, protein_object):
        # 3 implementation of pull move neighbourhood

        # Calculate energy of conformation
        # H(A) list of 'H' amino's in protein
        # N(h) = indexes of nodes adjacent to node h
        pass

        h_list = []

        energy = 0

        for h in h_list:
            for j in adjacent_nodes_indices:
                if j in h_list and h > j:
                    energy = energy - 1

        return energy

    def evaluate_pull_move_list(self, Xik, Vik):

        # Evaluates the energy value for all pull moves in Vik associated with the i-th
        # best conformation in X(k) and retains the resultant energy value in the corresponding data member of the Pull move structure
        # The standard aspiration is used, which overrides the move tabu status when it improves the best conformations found so far

        # X(k) denotes the set of best conformations at level k
        # Xi(k)/Xik the i-th best conformation in X(k)
        # M(k) the set of best pull-moves associated with X(k)
        # Mik the best i-th pull move in M(k)
        # V(k) denote the set of n moves evaluated at the level k from which the n1 best moves for the (new) collection Mk are selected ....
        pass

    def sort_pull_moves(self, Vk, n):

        # Sorts the n valid pull-moves in V(k) in ascending order of the associated energy values
        pass

    def initialize_tree(protein_object):

        # Procedure used to set up the first level of the filter-and-fan tree
        # basically run
        pass

        detect_all_pull_moves(protein_object, pull_move_list)
        evaluate_pull_move_list(Xik, Vik)
        sort_pull_moves(Vk, n)

        for i in n:
            Xi = protein_object
            execute_pull_move(protein_object, pull_move)

    def append_sets(self, Vk, Vik, n2):

        # Appends the set Vik of n2 moves to the set Vk
        pass

    def update_tabu_list(self, tabu_list):

        # Updates the tabu_list associated with the i-th conformation at the current depth of the tree search
        pass

    def generate_tree(self, X, n1, n2, L):

        # Procedure used to generate L levels of a filter-and-fan neighborhood tree
        # The first-improvement strategy can be used to terminate the tree search once an improvement is found
        pass

        while levels < L:

            for i in n1:
                detect_all_pull_moves(Xik, Vik)
                evaluate_pull_move_list(Xik, Vik)
                sort_pull_moves(Vik, Vik)
                append_sets(Vk, Vik, n2)

            sort_pull_moves(Vk, n1 * n2)

            for i in n1:
                execute_pull_move(Xik, Mik)
                update_tabu_list(tabu_list)
                energy = evaluate_energy(Xik)

                if energy < E*:
                    E* = energy
                    A* = Xi(k + 1)
            k = k + 1

    def tabu_search(self, protein_object):

        # Local search phase is carried out by a simple tabu search that utilizes only a short-term memory component.
        # Search is performed until encountering a sequence of NMAX iterations that fail to decrease the lowest energy value so far.
        pass

        A* = A
        T = []
