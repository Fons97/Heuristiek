import random
import matplotlib.pyplot as plt
import numpy as np
import re

from loader import load_protein

class Protein():
    def __init__(self, protein_string):
        self.string = protein_string
        self.amino_dict = {}
        self.move_options = [-1, 1, -2, 2]
        self.previous_move = 0
        self.x = 0
        self.y = 0
        self.used_options = []
        self.score_list = []

    def choose_move(self, int):
        if int == 1:
            self.move_options = [1, -2, 2]
        elif int == -1:
            self.move_options = [-1, -2, 2]
        elif int == 2:
            self.move_options = [-1, 1, 2]
        elif int == -2:
            self.move_options = [-1, 1, -2]

        move = random.choice(self.move_options)
        return move

    def amino_acid(self):
        for index, letter in enumerate(self.string):
            amino = AminoAcid(index)

            if self.previous_move == 0:
                self.previous_move = random.choice(self.move_options)

            move = self.check_move()

            self.previous_move = move

            self.amino_dict[index] = [letter, self.x, self.y]
            self.used_options.append((self.x, self.y))
        

    def get_coordinates(self):
        return self.amino_dict

    def check_move(self):
        x = self.x
        y = self.y

        while True:
            move = self.choose_move(self.previous_move)

            if move == -1 and (x - 1, y) not in self.used_options:
                x = x - 1
                break

            elif move == 1 and (x + 1, y) not in self.used_options:
                x = x + 1
                break

            elif move == -2 and (x, y - 1) not in self.used_options:
                y = y - 1
                break

            elif move == 2 and (x, y + 1) not in self.used_options:
                y = y + 1
                break

        self.x = x
        self.y = y
        return (self.x, self.y)


class AminoAcid():
    def __init__(self, amino):
        self.type = amino
        self.x = 0
        self.y = 0

    def amino_type(self):
        for i in self.type:
            return i


class Algorithm():

    def __init__(self, proteine_string):
        self.string = proteine_string
        self.directions = []


if __name__ == "__main__":

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
    h_list = []

    index = 0
    # create dots with color
    for i in test2.values():
        print(i, "i")
        if i[0] == 'H':
            i[0] = 'red'
            h_list.append((i[1], i[2], i[0], index))
        elif i[0] == 'P':
            i[0] = 'blue'
        elif i[0] == 'C':
            i[0] = 'green'
            h_list.append((i[1], i[2], i[0], index))

        x_values.append(i[1])
        y_values.append(i[2])

        plt.scatter(i[1], i[2], c=i[0], zorder=2)

        index += 1

        
    score = 0


    for amino_cords in h_list:
        amino_x, amino_y, amino_type, amino_index = amino_cords


        for compare_cords in h_list:
            compare_x, compare_y, compare_type, compare_index = compare_cords

            if amino_index - compare_index <= 1 and amino_index - compare_index >= -1:
                continue
            
            temp_x = amino_x - compare_x
            temp_y = amino_y - compare_y
            temp = (temp_x, temp_y)

            if (temp == (1,0) or temp == (-1,0) or temp == (0, 1) or temp == (0, -1)):
                if amino_type == compare_type:
                    if amino_type == "red":
                        score -= 1
                    elif amino_type == "green":
                        score -= 5
                elif (amino_type == "red" and compare_type == "green") or (amino_type == "green" and compare_type == "red"):
                    score -=1
                x_score_values = [amino_x, compare_x]
                y_score_values = [amino_y, compare_y]
                plt.plot(x_score_values, y_score_values, linestyle="dotted", c="green", zorder=1)
            
        


score = score / 2

total_score = score
print(total_score)
plt.xticks(np.arange(min(x_values)-1, max(x_values)+1, 1.0))
plt.yticks(np.arange(min(y_values)-1, max(y_values)+1, 1.0))

plt.plot(x_values, y_values, linestyle="solid", c="grey", zorder=1)

# plt.show()