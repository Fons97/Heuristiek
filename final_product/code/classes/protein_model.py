'''
This model contains all data and functionalities needed to run the algorithms to fold proteins
It represents the data structure of a protein folding
'''

import copy


class Model:

    def __init__(self, string: str):
        self.string = string
        self.protein = {}
        self.special_list = []
        self.length = len(self.string)
        self.iterations = []

        self.make_protein_dict()
        self.make_special_list()

    def make_protein_dict(self) -> None:
        '''
        Creates the data structure for the protein object as follows:
        {'amino-index': (amino-type, x-coord, y-coord, z-coord), 'amino-index': (amino-type, x-coord, y-coord, z-coord) ....etc}
        Amino index is the index in the string, amino-type is 'H', 'P' or 'C', amino's
        not yet placed on grid get coords 'None'
        '''
        for index, amino_type in enumerate(self.string):

            self.protein[index] = (amino_type, None, None, None)

        # The first two protein are always placed on the grid to prevent protein rotation and
        # unnecessary double conformations when executing constructive algorithms
        self.protein[0] = (self.string[0], 0, 0, 0)
        self.protein[1] = (self.string[1], 1, 0, 0)

    def make_special_list(self) -> None:
        '''
        Creates a list of the 'H' and 'C' type amino acids
        '''
        special_list = []
        for index, amino_type in self.protein.items():
            if amino_type != "P":
                self.special_list.append(index)

    def current_score(self) -> int:
        '''
        Calculates the score of current placement of amino acids
        '''
        current_state = []
        points = []
        
        # Add aminos with coordinates to current state list
        for key in self.protein:
            if self.protein[key][1] != None:
                aminos = [key, self.protein[key][0], self.protein[key][1], self.protein[key][2], self.protein[key][3]]
                current_state.append(aminos)
        
        # Add aminos that can generate points to points list 
        for amino in current_state:
            if amino[1] != "P":
                    points.append(amino)

        current_score = 0
        counter = 0
        
        # Compare aminos in points list to see if they've generated points 
        for amino_coords in points:
            amino_id, amino_type, amino_x, amino_y, amino_z  = amino_coords

            counter += 1

            for compare_coords in points[counter:]:
                compare_id, compare_type, compare_x, compare_y, compare_z = compare_coords
                
                # Filter out aminos that are next to each other in the protein, because they don't generate points  
                if amino_id - compare_id <= 1 and amino_id - compare_id >= -1:
                    continue
                
                # Generate coord structure that shows how far away aminos are from each other on grid 
                temp_x = amino_x - compare_x
                temp_y = amino_y - compare_y
                temp_z = amino_z - compare_z
                temp = (temp_x, temp_y, temp_z)
                
                # Add points for aminos that are one space away from each other 
                if (temp == (1,0,0) or temp == (-1,0,0) or temp == (0,1,0) or temp == (0,-1,0) or temp == (0,0,1) or temp == (0,0,-1)):
                    if amino_type == compare_type:
                        if amino_type == "H":
                            current_score -= 1
                        elif amino_type == "C":
                            current_score -= 5
                    elif (amino_type == "H" and compare_type == "C") or (amino_type == "C" and compare_type == "H"):
                        current_score -=1

        return current_score

    def filled_coordinates(self) -> list[tuple[int, int, int]]:
        '''
        Generates and returns a list with coordinates occupied by amino acids in grid
        Coorindates can be 'None'
        '''
        in_grid = []

        for amino in self.protein.values():
            in_grid.append(amino[1:])

        return in_grid

    def step_order(self) -> list[int]:
        '''
        Converts coordinates into directions and returns the directions
        Stepping order is defined as follows:
        - Positive movement on x-axis: 1, negative movement on x-axis: -1
        - Positive movement on y-axis: 2, negative movement on y-axis: -2
        - Positive movement on z-axis: 3, negative movement on z-axis: -3
        Stepping_order is also used to generate a CSV file to show what steps are made between aminos 
        '''
        stepping_order = []

        for index in range(self.length):
            if index == self.length - 1:
                break

            garbage ,I_x, I_y, I_z = self.protein[index]
            garbage ,II_x, II_y, II_z = self.protein[index + 1]
            
            # Generates the stepping order 1, -1, -2, 2, -3, 3 
            if II_x - I_x != 0:
                direction = II_x - I_x
            elif II_y - I_y != 0:
                direction = (II_y - I_y) * 2
            elif II_z - I_z != 0:
                direction = (II_z - I_z) * 3

            stepping_order.append(direction)

        return stepping_order

    def assign_coordinates(self, amino_list: list[list[int, int, int, int]]) -> None:
        '''
        Assigns coordinates to amino acids
        '''
        for amino in amino_list:
            self.protein[amino[0]] = (self.string[amino[0]], amino[1], amino[2], amino[3])

    def copy(self) -> 'Model':
        """
        Copies a model from itself
        """
        new_model = copy.copy(self)
        new_model.protein = copy.copy(self.protein)

        return new_model
