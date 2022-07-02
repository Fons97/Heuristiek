'''
Breadth First Algorithm for the Protein Folding Problem in the HP Lattice Model

- Navigates down the possible state tree, using a breadth first search strategy
- Covers the entire state-space
- Inherites functionalities from the Depth First algorithm
'''

from .depth_first import DepthFirst

from code.classes.protein_model import Model


class BreadthFirst(DepthFirst):

    def __init__(self, model: Model, dimension: int=3):
        super().__init__(model, dimension)
        self.depth = False

    def get_next_protein(self) -> Model:
        """
        Method to get the next state in a 'first in first out' manner, creating 
        a breadth first approach
        """
        return self.main_stack.pop(0)
