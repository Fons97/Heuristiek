import random
import matplotlib.pyplot as plt
import numpy as np

class Protein():
    def __init__(self, protein_string):
        self.string = protein_string
        self.amino_dict = {}
        self.move_options = [-1, 1, -2, 2]
        self.previous_move = 0
        self.x = 0
        self.y = 0
        self.used_options = []

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

            move = self.choose_move(self.previous_move)

            while (self.x, self.y) in self.used_options:
                move = self.choose_move(self.previous_move)
                # print(move, index, self.x, self.y)

                if move == -1:
                    self.x = self.x - 1

                elif move == 1:
                    self.x = self.x + 1

                elif move == -2:
                    self.y = self.y - 1

                elif move == 2:
                    self.y = self.y + 1

            self.previous_move = move

            self.amino_dict[index] = [letter, self.x, self.y]
            self.used_options.append((self.x, self.y))
            print(self.used_options)

    def get_coordinates(self):
        return self.amino_dict

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
    string = "HHPHHHPHPHHHPH"

    # create protein object
    protein = Protein(string)

    #  create dict
    test = protein.amino_acid()

    # get dict
    test2 = protein.get_coordinates()
    x_values = []
    y_values = []

    # create dots with color
    for i in test2.values():
        if i[0] == 'H':
            i[0] = 'red'
        elif i[0] == 'P':
            i[0] = 'blue'

        x_values.append(i[1])
        y_values.append(i[2])

        plt.scatter(i[1], i[2], c=i[0], zorder=2)

plt.xticks(np.arange(min(x_values)-1, max(x_values)+1, 1.0))
plt.yticks(np.arange(min(y_values)-1, max(y_values)+1, 1.0))

plt.plot(x_values, y_values, linestyle="dotted", c="grey", zorder=1)

plt.show()
