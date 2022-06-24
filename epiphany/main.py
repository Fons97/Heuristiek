from algorithms.randomize import randomize
from loader import load_protein
from classes.protein import Protein
from algorithms.randomize import randomize, spiral, zigzag, stair_fold, two_fold
# from algorithms.folding import folding_sequences, folding_singles
# from algorithms.greedy import greed
# from algorithms.depth_first import DepthFirst
from algorithms.branchandbound import BranchAndBound
from algorithms.hillclimber import HillClimber
# from algorithms.breadthfirst import BreadthFirst
from plotters import plot_3d
import csv


string = load_protein("proteins.txt", '9')
eggwhite = Protein(string)
# print(eggwhite.view_protein())

randomize(eggwhite)
# print(eggwhite.view_protein())

# algorithm = DepthFirst(eggwhite, 2)
# algorithm = BranchAndBound(eggwhite, 3)
algorithm = HillClimber(eggwhite)

protein_solution = algorithm.run(100000)

print("Score:", protein_solution.current_score())

plot_3d(protein_solution, "mand")

folds = protein_solution.step_order()
folds.append(0)

# Store amino-acid types in list
aminos = []
for amino in string:
    aminos.append(amino)

score = protein_solution.score()

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
