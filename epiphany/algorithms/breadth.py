import random
import queue
import copy

# Procedure: Searching (Ek-1, k)

# Create a set of possible sites for placement of amino-acid
## Compute Mk as the set of possible sites for monomer k

# Monte Caro biopolymer strucure simulation and optimazilation via fragment regrowth monte carlo

class BranchAndBound():

    def __init__(self, string):
        self.string = string
        self.side = []
        self.best = None
        # self.protein = Protein(string)

def searching(protein_obj):

    # Score of current pseudo placement, key will be length/index, value score (Ek)
    current_score = 0

    # Best score that has been generated so far, key will be length/index, value score (Uk)
    best_score = {}

    # Average score of different pseudo placements of current length/amino acid placement so far, key will be length/index, value score (Zk)
    average_score = {}

    # Protein string
    string = protein_obj.view_protein_string()

    # Place first and second amino on grid
    protein_obj.assign_coordinates([[0, 0, 0, 0]])
    protein_obj.assign_coordinates([[1, 1, 0, 0]])

    # Starting state of queue aka second amino
    second_amino = protein_obj.view_protein()[1]

    amino_node_nr = 2

    # Probabilities
    p1 = 0.8
    p2 = 0.5

    # Create main queue for different branches

    ##  queue format: (HHP, HHPH, HHPHH, HHPHHH, HHPHHHPH) or (HHP1, HHP2, HHP3) ((HHP1: HHPHH1, HHPHH2, HHPHH3), (HHP2: HHPHH1, HHPHH2, HHPHH3))
    main_queue = queue.Queue()
    main_queue.put(second_amino)

    # Create side queue for branch-level
    ##  side-queue format:  (HHP1, HHP2, HHP3) (HHPHH1, HHPHH2, HHPHH3)
    side_queue = queue.Queue()
    # side_queue.put(second_amino)

    # Outer queue
    # One queue for keeping track of all different states on one level of n length
        # At and of that loop, add n + 1 levels to next queue, and move one level up in that queue

    # Continue while there are still branches
    while not main_queue.empty():

        # Get conformation that's next in line from queue, partial_conformation needs to change format
        partial_conformation = main_queue.get()
        print(partial_conformation)

        # Add to side_queue (pak die uit main)
        child = copy.deepcopy(partial_conformation)
        child += i
        side_queue.put(child)

        # Decide whether branch is pruned or not, level all of same length n
        while not side_queue.empty():

            # Create list to keep track of average score of partial_conformation, maybe different place?
            average_score_list = []

            # Partial_conformation om te testen met verschillende directions
            partial_conformation_side_q = side_queue.get()

            # Check every possible move direction
            for direction in [1, -1, 2, -2 ,3, -3]:

                # Store partially placed protein to later put to queue
                # Add 'new' coordinates (aka coordinates of next amino acid) to dict
                partial = []

                amino_node = protein_obj.view_protein()[amino_node_nr]
                # amino_node = partial_conformation_side_q[0]
                x = amino_node[1]
                y = amino_node[2]
                z = amino_node[3]

                # 'Pseudo' place amino acid (not yet pseudo atm) ???
                pseudo_move = self.place(protein_obj, direction, x, y, z)

                # Get current score of pseudo placement
                current_score = protein_obj.reward()

                # Best score init for new lengths
                if amino_node_nr not in best_score.keys():
                    best_score[amino_node_nr] = current_score

                # Average score update
                average_score_list.append(current_score)

                # If amino is of type 'H'
                if amino_node.show_type() == 'H' or amino_node.show_type() == 'C':

                    # Current score is lower (aka better) than best score
                    if current_score <= best_score[amino_node_nr]:

                        # Get new partial_conformation based on new coordinates
                        coords = protein_obj.filled_coordinates()
                        pc = coords[amino_node_nr + 1]

                        # Add partial_conformation to main queue / pc
                        child = copy.deepcopy(partial_conformation)
                        child += i
                        main_queue.put(child)

                        # Update best score
                        best_score[amino_node_nr] = current_score

                        # Add / update coords to self to keep track of best placing
                        self.best = pc

                        # Go to next direction
                        break

                    # Current score is higher (aka worse) than average score, benefit is below average
                    elif current_score > average_score:

                        r = random.random()

                        # Prune with probability p1
                        if r > p1:

                            # Get new partial_conformation based on new coordinates
                            coords = protein_obj.filled_coordinates()
                            pc = coords[amino_node_nr + 1]

                            # Add partial_conformation to main queue / pc
                            child = copy.deepcopy(partial_conformation)
                            child += i
                            main_queue.put(child)

                            # Go to next direction
                            break

                    # Current score is somewhere between best_score and average_score
                    elif current_score > best_score and average_score >= current_score:

                        r = random.random()

                        # Prune with probability p2
                        if r > p2:

                            # Get new partial_conformation based on new coordinates
                            coords = protein_obj.filled_coordinates()
                            pc = coords[amino_node_nr + 1]

                            # Add partial_conformation to main queue / pc
                            child = copy.deepcopy(partial_conformation)
                            child += i
                            main_queue.put(child)

                            # Go to next direction
                            break

                    # If amino of type 'P'
                    else:

                        # Update average score
                        new_average = sum(average_score_list) / len(average_score_list)
                        average_score[amino_node_nr] = new_average
                        break

            amino_node_nr =+ 1

    print(self.best)

def place(protein_obj, direction, x, y, z):
    while True:

        if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
            x = x - 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])
            break

        elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
            x = x + 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])
            break

        elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
            y = y - 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])
            break

        elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
            y = y + 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])
            break

        elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
            z = z - 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])
            break

        elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
            z = z + 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])
            break
