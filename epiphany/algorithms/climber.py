import random
import math
import copy

from classes.protein import Protein
from classes.amino import Amino

# Create starting_state
# Repeat x amount of times
    # Choose substring
    # Manipulate substring
        # If new_substring score is lower than old_substring score:
            # Move start_substring to new_substring
            # Move end_substring to new_substring
        # Else:
            # new_substring = old_substring

class Climber():

    def __init__(self, protein_obj):
        self.protein_obj = protein_obj
        self.score = 0

    def run(self):

        # Herhaal

        # protein = copy.deepcopy(self.protein_obj)

        # score_list = []

        # for i in range(100):
        #
        #     protein = copy.deepcopy(self.protein_obj)
        #     starting_state = self.randomize(protein)
        #     new_score = self.get_score(starting_state)
        #     score_list.append(new_score)
        #
        # print(starting_state.view_protein(), "starting_state")
        # print(score_list, "score+list")
        # if starting_state == "failed":
        #     print("yes failed indeed")

        # Create starting state
        protein = copy.deepcopy(self.protein_obj)
        starting_state = self.randomize(protein)

        for i in range(100):
            print(i, "i")

            # Get starting/previous score
            starting_score = copy.deepcopy(self.score)

            # Get random indexes of substring to manipulate
            start_amino, end_amino = self.get_substring_index(starting_state)

            # From indexes generate substring
            substring = self.get_substring(starting_state, start_amino, end_amino)

            change_protein = self.change_protein(substring, starting_state, start_amino, end_amino)
            # print(self.protein_obj.view_protein(), "changeprotein")

            if change_protein == "Rejected":
                self.protein_obj = starting_state
                continue
                # print("rejected")

            else:
                print(change_protein.view_protein(), "changeprotein")
                new_score = self.get_score(change_protein)
                print(new_score, "newscore")

                if new_score < starting_score:
                    # print("new_score:" , new_score, "starting_score: ", starting_score)
                    self.protein_obj = change_protein
                else:
                    self.protein_obj = starting_state


        print(self.protein_obj.view_protein(), "returned object")
        return self.protein_obj
        # return starting_state

    def get_substring_index(self, protein_object):

        return 2, 8 + 1
        # second choice + 1
        # string = protein_object.view_protein_string()
        #
        # choice1 = random.choice(range(1, len(string)))
        # choice2 = random.choice(range(1, len(string)))
        #
        # if choice1 > choice2:
        #     return choice2, choice1
        # elif choice1 < choice2:
        #     return choice1, choice2
        # else:
        #     return choice1, choice2 + 1

    def get_substring(self, protein_object, start_amino, end_amino):

        substring = protein_object.view_protein()[start_amino:end_amino]

        return substring

    def change_protein(self, substring, protein_object, start_amino, end_amino):

        moves = [1, -1, 2, -2]

        start_amino_old = copy.deepcopy(protein_object.view_protein()[start_amino - 1])
        end_amino_old = copy.deepcopy(protein_object.view_protein()[end_amino - 1])

        # Reset values of amino acids in substring (except first amino acid)
        for i in substring:
            protein_object.assign_coordinates([[i[0], None, None, None]])

        substring_new = protein_object.view_protein()[start_amino:end_amino]

        start_string = self.get_start_string(protein_object, start_amino - 1)
        end_string = self.get_end_string(protein_object, end_amino - 1)
        # print(start_string, "start_string")

        for amino in substring_new:

            amino_node = protein_object.view_protein()[amino[0] - 1]

            # Get current coordinates from amino acids
            id = amino_node[0]
            x = amino_node[1]
            y = amino_node[2]
            z = amino_node[3]

            # while True:
            move = random.choice(moves)

            # Add not in filled coordinates
            if move == -1:
                x = x - 1
                protein_object.assign_coordinates([[id + 1, x, y, z]])
                continue

            elif move == 1:
                x = x + 1
                protein_object.assign_coordinates([[id + 1, x, y, z]])
                continue

            elif move == -2:
                y = y - 1
                protein_object.assign_coordinates([[id + 1, x, y, z]])
                continue

            elif move == 2:
                y = y + 1
                protein_object.assign_coordinates([[id + 1, x, y, z]])
                continue


        start_amino_new = copy.deepcopy(protein_object.view_protein()[start_amino - 1])
        end_amino_new = copy.deepcopy(protein_object.view_protein()[end_amino - 1])

        #Begin string coord difference
        diff_x_start = start_amino_new[1] - start_amino_old[1]
        diff_y_start = start_amino_new[2] - start_amino_old[2]
        diff_z_start = start_amino_new[3] - start_amino_old[3]

        for amino in start_string:

            amino_node = protein_object.view_protein()[amino[0]]

            id = amino_node[0]
            new_x = amino_node[1] + diff_x_start
            new_y = amino_node[2] + diff_y_start
            new_z = amino_node[3] + diff_z_start

            protein_object.assign_coordinates([[id, new_x, new_y, new_z]])

        # End coords difference
        diff_x = end_amino_new[1] - end_amino_old[1]
        diff_y = end_amino_new[2] - end_amino_old[2]
        diff_z = end_amino_new[3] - end_amino_old[3]

        for amino in end_string:

            amino_node = protein_object.view_protein()[amino[0]]

            id = amino_node[0]
            new_x = amino_node[1] + diff_x
            new_y = amino_node[2] + diff_y
            new_z = amino_node[3] + diff_z

            protein_object.assign_coordinates([[id, new_x, new_y, new_z]])

        list_of_coords = protein_object.filled_coordinates()

        duplicates = list(set([ele for ele in list_of_coords if list_of_coords.count(ele) > 1]))

        print(duplicates, "duplicates")
        if len(duplicates) > 0:
            return "Rejected"


        # print("All the duplicates from list are : " + str(res))
        # print("length of duplicates: ", len(res))

        return protein_object

    def get_index(self, protein_obj):

        last_amino = False

        for i in protein_obj.view_protein():
            if i[1] == None:
                return i[0] - 1

    def get_start_string(self, protein_object, start_amino):

        start_amino_list = []

        for i in protein_object.view_protein():
            if i[0] <= start_amino:
                start_amino_list.append(i)

        return start_amino_list

    def get_end_string(self, protein_object, end_amino):

        end_amino_list = []

        for i in protein_object.view_protein():
            if i[0] > end_amino:
                end_amino_list.append(i)

        return end_amino_list

    def get_previous_amino(self, start_amino, protein_object):

        previous_amino = protein_object.view_protein()[start_amino - 1]

        return previous_amino

    def randomize(self, protein_obj):
        string = protein_obj.view_protein_string()

        protein_obj.assign_coordinates([[0,0,0,0]])

        print(protein_obj.view_protein(), "protein_obj")

        status = "good"

        # list = [1, -1, 2, -2 ,3, -3]
        list = [1, -1, 2, -2]

        for id in range(len(string)):
            if id == len(string) - 1:
                break
            amino = protein_obj.view_protein()[id]
            x = amino[1]
            y = amino[2]
            z = amino[3]

            while True:
                move = random.choice(list)

                if move == -1:
                    print("-1")
                    x = x - 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 1:
                    print("1")
                    x = x + 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == -2:
                    print("-2")
                    y = y - 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                elif move == 2:
                    print("-2")
                    y = y + 1
                    protein_obj.assign_coordinates([[id + 1, x, y, z]])
                    break

                # else:
                #     status = "else"
                #     print("else", "else loop")
                #     break
                #     # return "failed"

        # print(status, "status")
        return protein_obj

    def get_score(self, protein_obj):
        '''
        Returns score of partial conformation
        '''

        self.score = protein_obj.reward()
        return self.score
    #
    # def score(self):
    #     '''
    #     Returns the best score of partial conformations overall
    #     '''
    #     return self.score
