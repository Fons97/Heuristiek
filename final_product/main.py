"""
Choose protein string to fold and algorithm to use to fold it
"""

import csv

from code.algorithms.randomize import randomize
from code.algorithms.greedy import Greedy
from code.algorithms.depth_first import DepthFirst
from code.algorithms.branchandbound import BranchAndBound
from code.algorithms.beambreadth import BeamBreadth
from code.algorithms.simulatedannealing import SimulatedAnnealing
from code.algorithms.climber import RandomClimber
from code.algorithms.breadthfirst import BreadthFirst

from code.tools.loader import load_protein
from code.tools.plotters import plot_3d

from code.classes.protein_model import Model

if __name__ == "__main__":
    print("Hello and welcome to our protein folding program!\n")

    # Protein string selection
    while True:
        string_number = input("1 HHPHHHPH\n2 HHPHHHPHPHHHPH\n3 HPHPPHHPHPPHPHHPPHPH\n4 PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP\n5 HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH\n6 PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP\n7 CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC\n8 HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH\n9 HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH\nEnter a protein string number (int: 1-9): \n")

        if string_number.isnumeric():
            break

    str(string_number)
    string = load_protein("data/proteins.txt", string_number)

    # Create protein model
    protein_model = Model(string)

    # Choose algorithm
    while True:
        print("Do you want to use a constructive or an iterative algorithm?\n",
                "1. Constructive \n",
                "2. Iterative \n")
        con_or_it = input("> ")
        con_or_it = int(con_or_it)

        if con_or_it >= 1 and con_or_it <= 2:
            break

    # Constructive
    if con_or_it == 1:
        while True:
            print("Select an algorithm you would like to use. The options are: \n",
                "1. Depth First \n",
                "2. Breadth First \n",
                "3. Branch And Bound \n",
                "4. Beam Breadth Search \n",
                "5. Randomize \n",
                "6. Greedy \n")

            alg = input("> ")
            alg = int(alg)
            if alg >= 1 and alg <= 6:
                break

        # Use 2D grid or 3D grid
        while True:
            print("Do you want to fold the protein in 2D or in 3D?. \n",
                "2. 2D \n",
                "3. 3D \n")

            dimension = input("> ")
            dimension = int(dimension)
            if dimension == 2 or dimension == 3:
                break

    # Iterative
    elif con_or_it == 2:
        while True:
            print("Select an algorithm you would like to use. The options are: \n",
                "7. Hill Climber \n",
                "8. Simulated Annealing \n")
            alg = input("> ")
            alg = int(alg)
            if alg == 7 or alg == 8:
                break

        # Amount of iterations
        while True:
            iterations = input("Enter the amount of iterations you would like to use: \n")
            iterations = int(iterations)
            if iterations > 0:
                break

        randomize(protein_model)

    # Assign chosen algorithm
    if alg == 1:
        algorithm = DepthFirst(protein_model, dimension)

    elif alg == 2:
        algorithm = BreadthFirst(protein_model, dimension)

    elif alg == 3:
        algorithm = BranchAndBound(protein_model, dimension)

    elif alg == 4:
        algorithm = BeamBreadth(protein_model, dimension)

    elif alg == 5:
        solution = randomize(protein_model, dimension)

    elif alg == 6:
        algorithm = Greedy(protein_model, dimension)

    elif alg == 7:
        algorithm = RandomClimber(protein_model)

    elif alg == 8:
        algorithm = SimulatedAnnealing(protein_model)

    # Run the algorithm
    if con_or_it == 1:
        if alg != 5:
            solution = algorithm.run()

    else:
        for i in range(1):
            solution = algorithm.run(iterations)

    # Print score to terminal
    print("Score:", solution.current_score())

    # Plot a visualization of the solution
    plot_3d(solution, "plot_visualization")
