'''
Loader function to import protein strings into the program from a text file
'''

import re

def load_protein(filename: str, protein_number: str) -> list[str, ...]:

    amino_acids = []

    with open(filename) as f:
        while True:
            line = f.readline()
            if line == "":
                break
            stripped = line.rstrip("\n")
            if protein_number in stripped:
                stripped = re.sub(r'[0-9]+', '', stripped)
                amino_acids = re.sub(r' ', '', stripped)

    return amino_acids
