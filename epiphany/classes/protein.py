from numpy import savez_compressed
from classes.amino import Amino
import random

class Protein():

    def __init__(self, string):
        self.string = string
        # self.amino_list = self.create_amino_list(string)

    def get_string(self):
        return self.string

    def assign_coordinates(self, amino_list):
        for amino in amino_list:
            id, x, y, z = amino
            self.amino_list[id].set_coords(x, y, z)

    def current_score(self):
        protein = self.view_protein()
        current_state = []
        point_list = []

        for amino in protein:
            if amino[1] != None:
                current_state.append(amino)

        for amino in current_state:
            if amino[4] != "P":
                    point_list.append(amino)

        current_score = 0

        counting_variable = 0
        for amino_coords in point_list:
            amino_id, amino_x, amino_y, amino_z, amino_type  = amino_coords

            counting_variable += 1

            for compare_coords in point_list[counting_variable:]:
                compare_id, compare_x, compare_y, compare_z, compare_type = compare_coords

                if amino_id - compare_id <= 1 and amino_id - compare_id >= -1:
                    continue

                temp_x = amino_x - compare_x
                temp_y = amino_y - compare_y
                temp_z = amino_z - compare_z
                temp = (temp_x, temp_y, temp_z)

                if (temp == (1,0,0) or temp == (-1,0,0) or temp == (0,1,0) or temp == (0,-1,0) or temp == (0,0,1) or temp == (0,0,-1)):
                    if amino_type == compare_type:
                        if amino_type == "H":
                            current_score -= 1
                        elif amino_type == "C":
                            current_score -= 5
                    elif (amino_type == "H" and compare_type == "C") or (amino_type == "C" and compare_type == "H"):
                        current_score -=1

        return current_score


    def score(self):
        full_list = self.view_protein()
        special_list = []
        for amino in full_list:
            if amino[4] != "P":
                special_list.append(amino)

        total_score = 0

        counting_variable = 0
        for amino_coords in special_list:
            amino_id, amino_x, amino_y, amino_z, amino_type  = amino_coords

            counting_variable += 1

            for compare_coords in special_list[counting_variable:]:
                compare_id, compare_x, compare_y, compare_z, compare_type = compare_coords

                if amino_id - compare_id <= 1 and amino_id - compare_id >= -1:
                    continue

                temp_x = amino_x - compare_x
                temp_y = amino_y - compare_y
                temp_z = amino_z - compare_z
                temp = (temp_x, temp_y, temp_z)

                if (temp == (1,0,0) or temp == (-1,0,0) or temp == (0,1,0) or temp == (0,-1,0) or temp == (0,0,1) or temp == (0,0,-1)):
                    if amino_type == compare_type:
                        if amino_type == "H":
                            total_score -= 1
                        elif amino_type == "C":
                            total_score -= 5
                    elif (amino_type == "H" and compare_type == "C") or (amino_type == "C" and compare_type == "H"):
                        total_score -=1

        return total_score

    def relaxed(self):

        filled_list = self.filled_coordinates()

        duplicates = list(set([ele for ele in filled_list if filled_list.count(ele) > 1]))

        score = self.score()

        score += len(duplicates) * 10

        return score


    def step_order(self):
        step_order_list = []
        for id, amino in enumerate(self.amino_list):
            if id == len(self.amino_list) - 1:
                break
            I_x, I_y, I_z = amino.show_coords()
            II_x, II_y, II_z = self.amino_list[id + 1].show_coords()

            if II_x - I_x != 0:
                direction = II_x - I_x
            elif II_y - I_y != 0:
                direction = (II_y - I_y) * 2
            elif II_z - I_z != 0:
                direction = (II_z - I_z) * 3

            step_order_list.append(direction)
        return step_order_list


    def rotational_pull(self, anchor, swing, pull_move):
        """
        Pull move 0-3
        0 1 horizantal
        2 3 vertical
        """
        amino_list = self.view_protein()

        anchor = amino_list[anchor]
        swing = list(amino_list[swing])

        options = []

        for i in range(1,4):
            distance = swing[i] - anchor[i]
            if distance != 1 and distance != -1:
                options.append(i)
                options.append(i * -1)
            else:
                follow_axis_1 = i
                saved_pos = swing[follow_axis_1]
                swing[i] = anchor[i]

        pull_move = options[pull_move]

        if pull_move > 0:
            swing[pull_move] += 1
            follow_axis_2 = pull_move
        else:
            swing[pull_move * -1] -= 1
            follow_axis_2 = pull_move * -1

        direction = swing[0] - anchor[0]
        after_swing = swing[0] + direction

        same_axis = None

        for i in range(1,4):
            if follow_axis_1 != i and follow_axis_2 != i:
                same_axis = i

        coords_list = [[swing[0], swing[1], swing[2], swing[3]]]

        if after_swing >= 0 and after_swing < len(amino_list):
            pass
        else:
            return

        if amino_list[after_swing][follow_axis_1] == saved_pos and amino_list[after_swing][follow_axis_2] == swing[follow_axis_2]:
            return
        else:
            template = [after_swing, None, None, None]
            template[follow_axis_2] = swing[follow_axis_2]
            template[follow_axis_1] = saved_pos
            template[same_axis] = amino_list[swing[0]][same_axis]

            coords_list.append(template)

        if direction > 0 and after_swing + 1 < len(amino_list):

            for i in range(after_swing + 1, after_swing + len(amino_list[after_swing:])):
                amino = [i, amino_list[i-2][1], amino_list[i-2][2], amino_list[i-2][3]]
                coords_list.append(amino)

        if direction < 0 and after_swing - 1 >= 0:
            for i in range(len(amino_list[:after_swing])):
                amino = [i, amino_list[i+2][1], amino_list[i+2][2], amino_list[i+2][3]]
                coords_list.append(amino)

        self.assign_coordinates(coords_list)
    #
