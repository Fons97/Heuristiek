from classes.amino import Amino

class Protein():

    def __init__(self, string):
        self.string = string
        self.amino_list = self.create_amino_list(string)

    def create_amino_list(self, string):

        amino_list = []

        for id, amino_type in enumerate(string):
            amino_list.append(Amino(id, amino_type))

        return amino_list

    def view_protein_string(self):
        return self.string

    def view_protein(self):
        protein_view = []
        for amino in self.amino_list:
            x, y, z = amino.show_cords()
            id = amino.show_id()
            amino_type = amino.show_type()
            protein_view.append((id, x, y, z, amino_type))

        return protein_view

    def assign_cordinates(self, amino_list):
        for amino in amino_list:
            id, x, y, z = amino
            self.amino_list[id].set_cords(x, y, z)

    def score(self):
        full_list = self.view_protein()
        print(full_list)
        special_list = []
        for amino in full_list:
            if amino[4] != "P":
                special_list.append(amino)


        total_score = 0

        counting_variable = 0
        for amino_cords in special_list:
            amino_id, amino_x, amino_y, amino_z, amino_type  = amino_cords

            counting_variable += 1

            for compare_cords in special_list[counting_variable:]:
                compare_id, compare_x, compare_y, compare_z, compare_type = compare_cords

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


    def step_order(self):
        step_order_list = []
        for id, amino in enumerate(self.amino_list):
            if id == len(self.amino_list) - 1:
                break
            I_x, I_y, I_z = amino.show_cords()
            II_x, II_y, II_z = self.amino_list[id + 1].show_cords()

            if II_x - I_x != 0:
                direction = II_x - I_x 
            elif II_y - I_y != 0:
                direction = (II_y - I_y) * 2
            elif II_z - I_z != 0:
                direction = (II_z - I_z) * 3

            step_order_list.append(direction)
        return step_order_list

    def filled_cordinates(self):
        filled_cordinates_list = []
        for amino in self.amino_list:
            x, y, z = amino.show_cords()
            if x is not None:
                filled_cordinates_list.append((x, y ,z))
        return filled_cordinates_list
