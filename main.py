import random
import matplotlib.pyplot as plt
import numpy as np
from protein import Protein
from aminoacid import AminoAcid
from algorithm import Algorithm
from loader import load_protein


# This code makes a 3d plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')   

# Here a proteinstring is chosen from the protein.txt file
string = load_protein('protein.txt', '2')

# This turns the string into a protein object
protein = Protein(string)

# This creates a dictionary of aminoacids
# The key is the index of the aminoacid
# The value is a list that contains the type (H, P or C), the x-, y- and z-coordinate
protein_dic = protein.amino_acid()

# These lists contain the coordinates that are used to plot the lines between the aminoacids
x_values = []
y_values = []
z_values = []

# This list contains the coordinates of all the C and P aminoacids that have been placed
special_type_list = []

# The index variable gives an index to every aminoacid
# This way it can be checked if a connection between two neighbours (after folding) exists
# If a connection exists, it won't be considered a fold and there won't be any points allocated 
index = 0

# For every aminoacid (i) a dot with a specific colour based on acid type is created
for i in protein_dic.values():
    if i[0] == 'H':
        i[0] = 'red'
        special_type_list.append((i[1], i[2], i[3], i[0], index))
    elif i[0] == 'P':
        i[0] = 'blue'
    elif i[0] == 'C':
        i[0] = 'green'
        special_type_list.append((i[1], i[2], i[3], i[0], index))

    # The dots are scatterd across a plot by using the aminoacids x, y and z coordinates
    x_values.append(i[1])
    y_values.append(i[2])
    z_values.append(i[3])

    ax.scatter(i[1], i[2], i[3], s=50, c=i[0], zorder=2)

    index += 1

# The score variable keeps track of the current score
score = 0

# A score is calulated using the for loop below
# The list called special_type_list contains all amino acids that can contribute to the score
# This list is iterated over
# When two amino acids are found that are close together:
# - Points are added to the score 
# - A dotted line is drawn between the amino acids to signify a connection
for counter, amino_cords in enumerate(special_type_list, start=1):
    amino_x, amino_y, amino_z, amino_type, amino_index = amino_cords

    for compare_cords in special_type_list[counter:]:
        compare_x, compare_y, compare_z, compare_type, compare_index = compare_cords

        # When two amino acids follow eachother in the protein chain, their locations are not compared
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
        
    


print(score)
ax.set_xticks(np.arange(min(x_values)-1, max(x_values)+1, 1.0))
ax.set_yticks(np.arange(min(y_values)-1, max(y_values)+1, 1.0))
ax.set_zticks(np.arange(min(z_values)-1, max(z_values)+1, 1.0))

ax.plot(x_values, y_values, z_values, linestyle="solid", linewidth=1.2, c="grey", zorder=1)
# print(protein_dic)
plt.show()