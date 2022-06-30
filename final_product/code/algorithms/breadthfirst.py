from .depth_first import DepthFirst

from classes.protein_model import Model


class BreadthFirst(DepthFirst):
    """"
    A Depth First algorithm that builds a queue of graphs with a unique assignment of nodes for each instance.
    Almost all of the functions are eqal to those of the DepthFirst class, which is why
    we use that as a parent class.
    """

    def __init__(self, model: Model, dimension: int=3):
        super().__init__(model, dimension)
        self.depth = False

    def get_next_protein(self) -> Model:
        """
        Method that gets the next state from the list of states.
        For Breadth First we need the first one; we use a queue.
        """
        return self.main_stack.pop(0)
