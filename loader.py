

def load_protein(filename):

    filename = "protein.txt"
    aminoacids = []
    with open(filename) as file:
        while True:
            line = file.readline()
            if line == "":
                break
            stripped = line.rstrip("\n")
            for amin in stripped:
                aminoacids.append(amin)
    return aminoacids
