from loader import load_protein
from classes.protein import Protein
from algorithms.randomize import randomize, spiral
from plotters import plot_3d
import csv


string = load_protein("proteins.txt", '1')
eggwhite = Protein(string)

# dir = {-1: 0, 1: 0, -2: 0, 2: 0, -3: 0, 3: 0}
# tot_score = 0

# for i in range(100001):
#     randomize(eggwhite)
#     folds = eggwhite.step_order()
#     folds.append(0)
#     print(i, "i")
#     for fold in folds:
#         if fold == -1:
#             dir[-1] += 1
#         elif fold == 1:
#             dir[1] += 1
#         elif fold == -2:
#             dir[-2] += 1
#         elif fold == 2:
#             dir[2] += 1
#         elif fold == -3:
#             dir[-3] += 1
#         elif fold == 3:
#             dir[3] += 1
#     score = eggwhite.score()
#     tot_score = tot_score + score
        
        

# spiral(eggwhite)
print(eggwhite.score())
plot_3d(eggwhite, "mand")

print(dir)
print(tot_score/100000)


'''
Generate file 'output.csv' containing amino-types, move and total score
'''

# Store folds in list, append 0 to list because no folding is needed at end of string
folds = eggwhite.step_order()
folds.append(0)

# Store amino-acid types in list
aminos = []
for i in string:
    aminos.append(i)

# Store score in variable
score = eggwhite.score()

# Open csv file in write mode
with open('output.csv', 'w') as f:

    # Create csv writer
    writer = csv.writer(f)

    # Write header to file
    header = ['amino', 'fold']
    writer.writerow(header)

    # Write rows with amino name and move to file
    for i in range(len(string)):
        writer.writerow([aminos[i], folds[i]])

    # Write score to file
    writer.writerow(['score', score])
