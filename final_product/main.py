"""
This programm allows you to choose 1 out of 9 proteïns that you can fold.
Than it allows you to choose the algorithm that you want to use and the amount of iterations.
To choose an option, just enter the right integer.
"""

import csv

from code.algorithms.randomize import randomize
from code.algorithms.greedy import greed
from code.algorithms.depth_first import DepthFirst
from code.algorithms.branchandbound import BranchAndBound
from code.algorithms.beambreadth import BeamBreadth
from code.algorithms.simannealing import SimulatedAnnealing
from code.algorithms.climber import Climber
from code.algorithms.breadthfirst import BreadthFirst

from code.tools.loader import load_protein
from code.tools.plotters import plot_3d

from code.classes.protein_model import Model

if name == "__main__":
    print("Hello and welcome to our program!")

    while True:
        string_number = input("please, enter a protein string number (int: 1-9): \n")

        if string_number.isnumeric():
            break

    str(string_number)
    string = load_protein("proteins.txt", string_number)

    # Create Model
    protein_model = Model(string)


    # Choose your kind of algorithm.
    while True:
        print("Do you want to use a constructive or a iterative algorithm? \n",
                "1. constructive \n",
                "2. iterative \n")
        con_or_it = input("> ")
        con_or_it =  int(con_or_it)

        if con_or_it >= 1 and con_or_it <= 2:
            break

    # choose your constructive algorithm.
    if con_or_it == 1:
        while True:
            print("Now please, enter an algorithm you want to use. The options are: \n",
                "1. Depth first \n",
                "2. Breadth first \n",
                "3. Branch and bound \n",
                "4. Beam breadth \n",
                "5. randomize \n",
                "6. greedy \n") 

            alg = input("> ")
            alg = int(alg)
            if alg >= 1 and alg <= 6:
                break

        # choose if you want to fold in 2D or 3D.
        while True:
            print("Now please, if you want to fold the protein in 2d or 3d. \n",
                "2. 2d \n",
                "3. 3d \n") 

            dimension = input("> ")
            dimension = int(dimension)
            if dimension == 2 or dimension == 3:
                break

    elif con_or_it == 2:
        while True:
            print("Now please, enter an algorithm you want to use. The options are: \n",
                "7. Hill climber \n",
                "8. Simulated annealing \n")        
            alg = input("> ")
            alg = int(alg)
            if alg == 7 or alg == 8:
                break

        # choose the amount of iterations
        while True:
            iterations = input("please, enter the amount of iterations you want: \n")
            iterations = int(iterations)
            if iterations > 0:
                break

        randomize(protein_model)

    # assign chosen algorithm
    if alg == 1:
        algorithm = DepthFirst(protein_model, dimension)

    elif alg == 2:
        algorithm = BreadthFirst(protein_model, dimension)

    elif alg == 3:
        algorithm = BranchAndBound(protein_model, dimension)

    elif alg == 4:
        algorithm = BeamBreadth(protein_model, dimension)

    elif alg == 5:
        algorithm = randomize(protein_model, dimension)

    elif alg == 6:
        algorithm = greed(protein_model, dimension)

    elif alg == 7:
        for i in range(100):
            algorithm = Climber(protein_model)

    elif alg == 8:
        algorithm = SimulatedAnnealing(protein_model)

    # Run algorithm
    if con_or_it == 1:
        solution = algorithm.run()

    else:
        for i in range(1):
            solution = algorithm.run(iterations)

    # Print score
    print("Score:", solution.score())

    # Plot solution
    plot_3d(solution, "mand")

