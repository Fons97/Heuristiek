import copy

class DepthFirst:
    
    def __init__(self, protein_obj, dimension):
        self.dimension = dimension
        self.protein_obj = protein_obj
        self.best_placement = None
        self.best_score = 0
        self.main_stack = []
        self.depth = True


    def run(self):

        # Different direction options for 2D and 3D solution
        if self.dimension == 2:
            directions = [1, -1, 2, -2]
        elif self.dimension == 3:
            directions = [1, -1, 2, -2 ,3, -3]

        # Create protein to build new states with
        first_protein = copy.deepcopy(self.protein_obj)

        # Place first and second amino of protein on grid, to eliminate protein rotation
        first_protein.assign_coordinates([[0, 0, 0, 0]])
        first_protein.assign_coordinates([[1, 1, 0, 0]])

        # Put starting state in queue
        self.main_stack = []
        self.main_stack.append(first_protein)

        # Keep excecuting algorithm until all possible solutions have been generated
        while self.main_stack != []:

            # Get next state
            protein = self.get_next_protein()


            # Get the id of current amino node
            index = self.get_index(protein)

            # If the last amino in protein is reached, update scores and quit
            if index == "last_amino_acid" and self.depth == True:
                continue
            elif index == "last_amino_acid" and self.depth == False:
                break
                

            # Create a new state for each possible move for next amino
            for direction in directions:


                # Create new protein object for direction
                partial_protein = copy.deepcopy(protein)

                # Get details about current amino node
                amino_node = partial_protein.view_protein()[index]

                # Assign coordinates of amino node
                x = amino_node[1]
                y = amino_node[2]
                z = amino_node[3]

                # Place next amino node on grid if possible, based on direction
                if direction == -1 and (x - 1, y, z) not in partial_protein.filled_coordinates():


                    # Update coordinates of next amino node
                    x = x - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    # Get the current score of partial conformation
                    self.get_score(partial_protein)

                    # Add partial conformation to queue to build further upon
                    child = copy.deepcopy(partial_protein)
                    self.main_stack.append(child)


                elif direction == 1 and (x + 1, y, z) not in partial_protein.filled_coordinates():
                    x = x + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    self.main_stack.append(child)


                elif direction == -2 and (x, y - 1, z) not in partial_protein.filled_coordinates():
                    y = y - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    self.main_stack.append(child)


                elif direction == 2 and (x, y + 1, z) not in partial_protein.filled_coordinates():
                    y = y + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    self.main_stack.append(child)


                elif direction == -3 and (x, y, z - 1) not in partial_protein.filled_coordinates():
                    z = z - 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    self.main_stack.append(child)


                elif direction == 3 and (x, y, z + 1) not in partial_protein.filled_coordinates():
                    z = z + 1
                    partial_protein.assign_coordinates([[index + 1, x, y, z]])

                    self.get_score(partial_protein)

                    child = copy.deepcopy(partial_protein)
                    self.main_stack.append(child)


        # If all amino nodes have been placed, return the placement with the best score
        return self.best_placement

            

    def get_index(self, protein_obj):
        '''
        Returns the index or id of the last placed amino node
        If the current node is last node of protein, return last node message
        '''
        last_amino = False

        for i in protein_obj.view_protein():

            if i[1] == None:
                return i[0] - 1

            last_amino = True

        if last_amino == True:
            return "last_amino_acid"

    
    def get_score(self, protein_obj):
        '''
        Returns score of partial conformation
        '''
        score = protein_obj.current_score()

        if score <= self.best_score:
            self.best_score = score
            self.best_placement = protein_obj

    def score(self):
        '''
        Returns the best score of partial conformations overall
        '''
        return self.best_score

    def get_next_protein(self):
        return self.main_stack.pop()

