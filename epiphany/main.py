from algorithms.randomize import randomize
from loader import load_protein
from classes.protein import Protein
from algorithms.randomize import randomize
# from algorithms.folding import folding_sequences, folding_singles
# from algorithms.greedy import greed
# from algorithms.depth_first import DepthFirst
from algorithms.branchandbound import BranchAndBound
from algorithms.beambreadth import BeamBreadth
from algorithms.hillclimber import HillClimber
# from algorithms.breadthfirst import BreadthFirst
from classes.protein_model import Model
from plotters import plot_3d
import csv

# BRANCHANDBOUNDMODEL
# Load protein string
# string = load_protein("proteins.txt", '9')
# # Create Model
# protein_model = Model(string)
# # Select algorithm
# algorithm = BranchAndBound(protein_model, 3)
# # Run algorithm
# solution = algorithm.run()
# # Print score
# print("Score:", algorithm.score())
# # Plot solution
# plot_3d(solution, "mand")

# BEAMBREADTHMODELS
# Load protein string
string = load_protein("proteins.txt", '5')
# Create Model
protein_model = Model(string)
# Select algorithm
algorithm = BeamBreadth(protein_model, 3)
# Run algorithm
solution = algorithm.run()
# Print score
print("Score:", algorithm.score())
# Plot solution
plot_3d(solution, "mand")




# folds = eggyolk.step_order()
# folds.append(0)

# Store amino-acid types in list
# aminos = []
# for amino in string:
#     aminos.append(amino)
#
# score = eggyolk.score()
#
# # Open csv file in write mode
# with open('output.csv', 'w') as f:
#
#     # Create csv writer
#     writer = csv.writer(f)
#
#     # Write header to file
#     header = ['amino', 'fold']
#     writer.writerow(header)
#
#     # Write rows with amino name and move to file
#     for i in range(len(string)):
#         writer.writerow([aminos[i], folds[i]])
#
#     # Write score to file
#     writer.writerow(['score', score])
