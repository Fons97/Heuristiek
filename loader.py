import re

def load_protein(filename, protein_number):

    aminoacids = []
    with open(filename) as file:
        while True:
            line = file.readline()
            if line == "":
                break
            stripped = line.rstrip("\n")
            if protein_number in stripped:
                stripped = re.sub(r'[0-9]+', '', stripped)
                stripped = re.sub(r' ', '', stripped)
                for amin in stripped:
                    aminoacids.append(amin)
    return aminoacids
