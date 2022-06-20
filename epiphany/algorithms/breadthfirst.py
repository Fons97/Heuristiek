from .depth_first import DepthFirst


class BreadthFirst(DepthFirst):
    """"
    A Depth First algorithm that builds a queue of graphs with a unique assignment of nodes for each instance.
    Almost all of the functions are eqal to those of the DepthFirst class, which is why
    we use that as a parent class.
    """
    
    def __init__(self, protein_obj, dimension):
        self.dimension = dimension
        self.protein_obj = protein_obj
        self.best_placement = None
        self.best_score = 0
        self.main_stack = []
        self.depth = False


    def get_next_protein(self):
        """
        Method that gets the next state from the list of states.
        For Breadth First we need the first one; we use a queue.
        """
        return self.main_stack.pop(0)