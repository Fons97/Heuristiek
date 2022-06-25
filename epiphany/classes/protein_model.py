import copy 

from algorithms.randomize import randomize

class Model:

    def __init__(self, string):
        self.string = string
        self.protein = {}
        self.make_protein_dict()
        self.length = len(self.protein)
        # special_list = []
        # self.make_special_list()
        

    def make_protein_dict(self):
        '''
        Creates the data structure for alterations on protein
        '''

        for index, amino_type in enumerate(self.string):
            
            self.protein[index] = (amino_type, None, None, None)

        self.protein[0] = (self.string[0], 0, 0, 0)

    def view_string(self):
        return self.string

    def make_special_list(self):
        '''
        Creates a list of the 'H' and 'C' type amino acids that can generate points 
        '''
        special_list = []
        for amino in self.protein.values():

            if amino[0] != "P" and amino[1] != None:

                special_list.append(amino)

        return special_list

    def make_special_dict(self):
        '''
        Creates a list of the 'H' and 'C' type amino acids that can generate points 
        '''
        special_dict = {}

        for key, amino in self.protein.items():

            if amino[0] != "P" and amino[1] != None:

                special_dict[key] = amino

        return special_dict
        
        
    def score(self):
        '''
        Calculates the score of current placement of amino acids 
        '''
        
        score = 0

        special_dict = self.make_special_dict()
    
        counter = 0

        for amino_id, amino_coords in special_dict.items():
            # print(amino_id, "amino_id")

            amino_type, amino_x, amino_y, amino_z  = amino_coords

            for compare_id in range(amino_id + 1, len(special_dict.keys())):

                if amino_id - compare_id <= 1 and amino_id - compare_id >= -1:
                    continue
                
                # print(compare_id, "J")
                compare_type, compare_x, compare_y, compare_z = self.protein[compare_id]


                temp_x = amino_x - compare_x
                temp_y = amino_y - compare_y
                temp_z = amino_z - compare_z
                temp = (temp_x, temp_y, temp_z)

                if (temp == (1,0,0) or temp == (-1,0,0) or temp == (0,1,0) or temp == (0,-1,0) or temp == (0,0,1) or temp == (0,0,-1)):
                    if amino_type == compare_type:
                        if amino_type == "H":
                            score -= 1
                        elif amino_type == "C":
                            score -= 5
                    elif (amino_type == "H" and compare_type == "C") or (amino_type == "C" and compare_type == "H"):
                        score -=1
        print(score, "score, score")
        return score

    def relaxed(self):
        '''
        Adds points if amino acids are placed on the same place on grid 
        '''

        filled_list = self.filled_coordinates()

        duplicates = list(set([ele for ele in filled_list if filled_list.count(ele) > 1]))

        score = self.score()

        score += len(duplicates) * 10

        return score

    def filled_coordinates(self):
        '''
        Creates a list with coordinates occupied by amino acids
        '''
        filled_list = []

        for amino in self.protein.values():
            filled_list.append(amino[1:])

        return filled_list

    def step_order(self):
        '''
        Converts coordinates into directions
        '''
        step_order_list = []

        for index in range(self.length):
            if index == self.length - 1:
                break

            garbage ,I_x, I_y, I_z = self.protein[index]
            garbage ,II_x, II_y, II_z = self.protein[index + 1]

            if II_x - I_x != 0:
                direction = II_x - I_x
            elif II_y - I_y != 0:
                direction = (II_y - I_y) * 2
            elif II_z - I_z != 0:
                direction = (II_z - I_z) * 3

            step_order_list.append(direction)
        return step_order_list

    def assign_coordinates(self, amino_list):
        '''
        Assigns coordinates to amino acids 
        '''

        for amino in amino_list:
            self.protein[amino[0]] = (self.string[amino[0]], amino[1], amino[2], amino[3])

    def rotational_pull_fuck(self, anchor_nr, swing_nr, pull_move):
        """
        Pull move 0-3
        0 1 horizantal
        2 3 vertical
        """

        amino_list = []

        for amino in self.protein.values():
            amino_list.append([amino[0], amino[1], amino[2], amino[3]])

        
        anchor = amino_list[anchor_nr]
        swing = amino_list[swing_nr]
     

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

        direction = swing_nr - anchor_nr
        after_swing = swing_nr + direction

        same_axis = None

        for i in range(1,4):
            if follow_axis_1 != i and follow_axis_2 != i:
                same_axis = i

        coords_list = [[swing_nr, swing[1], swing[2], swing[3]]]

        if after_swing >= 0 and after_swing < len(self.protein):
            pass
        else:
            return

        if amino_list[after_swing][follow_axis_1] == saved_pos and amino_list[after_swing][follow_axis_2] == swing[follow_axis_2]:
            return
        else:
            template = [after_swing, None, None, None]
            template[follow_axis_2] = swing[follow_axis_2]
            template[follow_axis_1] = saved_pos
            template[same_axis] = amino_list[swing_nr][same_axis]

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

    def copy(self):
        """
        Copies a model from itself
        """
        new_model = copy.copy(self)
        new_model.protein = copy.copy(self.protein)

        return new_model






    
    
    
