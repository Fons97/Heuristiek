import random
import matplotlib.pyplot as plt
import numpy as np


from loader import load_protein

class Protein():
    def __init__(self, protein_string):
        self.string = protein_string
        self.amino_dict = {}
        self.x = 0
        self.y = 0
        self.z = 0
        self.used_options = []
        self.score_list = []


    def choose_move(self, int):
        if int == 1:
            self.move_options = [1, -2, 2 , -3 , 3]
        elif int == -1:
            self.move_options = [-1, -2, 2, -3, 3]
        elif int == 2:
            self.move_options = [-1, 1, 2, -3, 3]
        elif int == -2:
            self.move_options = [-1, 1, -2, -3, 3]
        elif int == 3:
            self.move_options = [-1, 1, -2, 2, 3]
        elif int == -3:
            self.move_options = [-1, 1, -2, 2, -3]

        move = random.choice(self.move_options)
        return move

    def creat_amino_acid_objects(self):
        for index, letter in enumerate(self.string):
            amino = AminoAcid(index)

            if self.previous_move == 0:
                self.previous_move = random.choice(self.move_options)

            move = self.check_move()

            self.previous_move = move

            self.amino_dict[index] = [letter, self.x, self.y, self.z]
            self.used_options.append((self.x, self.y, self.z))
        

    def get_coordinates(self):
        return self.amino_dict

    def check_move(self):
        x = self.x
        y = self.y
        z = self.z

        while True:
            move = self.choose_move(self.previous_move)

            if move == -1 and (x - 1, y, z) not in self.used_options:
                x = x - 1
                break

            elif move == 1 and (x + 1, y, z) not in self.used_options:
                x = x + 1
                break

            elif move == -2 and (x, y - 1, z) not in self.used_options:
                y = y - 1
                break

            elif move == 2 and (x, y + 1, z) not in self.used_options:
                y = y + 1
                break

            elif move == -3 and (x, y, z - 1) not in self.used_options:
                z = z - 1
                break

            elif move == 3 and (x, y, z + 1) not in self.used_options:
                z = z + 1
                break

        self.x = x
        self.y = y
        self.z = z
        return (self.x, self.y, self.z)


class AminoAcid():
    def __init__(self, amino):
        self.type = amino
        self.x = 0
        self.y = 0
        self.z = 0

    def amino_type(self):
        for i in self.type:
            return i


class Algorithm():

    def __init__(self, proteine_string):
        self.string = proteine_string
        self.directions = []


if __name__ == "__main__":
    
    # Matplotlib 
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')   

    # load string
    string = load_protein('protein.txt', '10')
    string = "".join(string)
    protein = Protein(string)

    #  create dict
    test = protein.amino_acid()

    # get dict
    test2 = protein.get_coordinates()
    x_values = []
    y_values = []
    z_values = []
    h_list = []

    index = 0
    # create dots with color
    for i in test2.values():
        if i[0] == 'H':
            i[0] = 'red'
            h_list.append((i[1], i[2], i[3], i[0], index))
        elif i[0] == 'P':
            i[0] = 'blue'
        elif i[0] == 'C':
            i[0] = 'green'
            h_list.append((i[1], i[2], i[3], i[0], index))

        x_values.append(i[1])
        y_values.append(i[2])
        z_values.append(i[3])
    
        ax.scatter(i[1], i[2], i[3], s=50, c=i[0], zorder=2)

        index += 1

        
    score = 0

    counting_variable = 0
    for amino_cords in h_list:
        amino_x, amino_y, amino_z, amino_type, amino_index = amino_cords

        counting_variable += 1

        for compare_cords in h_list[counting_variable:]:
            compare_x, compare_y, compare_z, compare_type, compare_index = compare_cords

            if amino_index - compare_index <= 1 and amino_index - compare_index >= -1:
                continue
            
            temp_x = amino_x - compare_x
            temp_y = amino_y - compare_y
            temp_z = amino_z - compare_z
            temp = (temp_x, temp_y, temp_z)

            if (temp == (1,0,0) or temp == (-1,0,0) or temp == (0,1,0) or temp == (0,-1,0) or temp == (0,0,1) or temp == (0,0,-1)):
                if amino_type == compare_type:
                    if amino_type == "red":
                        score -= 1
                    elif amino_type == "green":
                        score -= 5
                elif (amino_type == "red" and compare_type == "green") or (amino_type == "green" and compare_type == "red"):
                    score -=1
                x_score_values = [amino_x, compare_x]
                y_score_values = [amino_y, compare_y]
                z_score_values = [amino_z, compare_z]
                ax.plot(x_score_values, y_score_values, z_score_values, linestyle="dotted", linewidth=3, c="green", zorder=1)
            
        

total_score = score
print(total_score)
ax.set_xticks(np.arange(min(x_values)-1, max(x_values)+1, 1.0))
ax.set_yticks(np.arange(min(y_values)-1, max(y_values)+1, 1.0))
ax.set_zticks(np.arange(min(z_values)-1, max(z_values)+1, 1.0))

ax.plot(x_values, y_values, z_values, linestyle="solid", linewidth=1.2, c="grey", zorder=1)

plt.show()