'''
Writer function to generate a csv file with the stepping order output
'''

import csv
from typing import Type

from code.classes.protein_model import Model


def create_csv(protein_string, model):

    folds = model.step_order()
    folds.append(0)

    # Store amino-acid types in list
    aminos = []
    for amino in protein_string:
        aminos.append(amino)

    # Get score of conformation
    score = model.current_score()

    # Open csv file in write mode
    with open('data/output.csv', 'w') as f:

        # Create csv writer
        writer = csv.writer(f)

        # Write header to file
        header = ['amino', 'fold']
        writer.writerow(header)

        # Write rows with amino name and move to file
        for i in range(len(protein_string)):
            writer.writerow([aminos[i], folds[i]])

        # Write score to file
        writer.writerow(['score', score])
