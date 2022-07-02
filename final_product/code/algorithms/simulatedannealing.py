'''
Simulated Annealing algorithm for the Protein Folding Problem in the HP Lattice Model

- Class inherites functions from the Random HillClimber algorithm.
- This is done by lowering the 'temperature' when the iterations increase. This heuristic is
  performed in the assumption that to get out of a local optimum and reach a global optimum,
  conformations with lower scores should be evaluated.
- Just as with the Random HillClimber, the best conformation so far is savesd as well as a
  current conformation with perhaps a sub-optimal score.
'''

import random
import math
import copy
import itertools

from code.algorithms.climber import RandomClimber

from code.classes.protein_model import Model


class SimulatedAnnealing(RandomClimber):

    def __init__(self, model: Model, dimension: int=3, temperature: int or float=1):
        super().__init__(model, dimension)

        self.T0 = temperature
        self.T = temperature
        self.counter = 0

    def update_temperature(self) -> None:
        '''
        If conformations of the same score are generated a number of times in a row,
        the 'temperature' is recalculated
        '''
        self.T = self.T - (self.T0 / (self.iterations * 0.8))

    def update_score(self, model: Model) -> None:
        '''
        Updates scores and self based on new conformation
        '''
        if self.is_valid(model) == True:
            new_protein = model.copy()
            new_score = self.get_score(new_protein)

            # Save best conformations created so far
            if new_score < self.best_score:
                self.best_score = new_score
                self.best_placement = new_protein

            # If new score isn't the best score so far, determine whether to keep current conformation
            self.sub_optimal_score(new_protein, new_score)

            # Recalculate the temperature
            self.update_temperature()

    def sub_optimal_score(self, model: Model, score: int) -> None:
        '''
        If current score is worse than best, this function determines whether to
        keep the current conformation, based on the chance set by the temperature
        If the temperature has a higher value, the chances of sub-optimal conformations
        being kept is higher
        '''
        delta = score - self.best_score
        probability = math.exp(-delta/self.T)

        if random.random() < probability:

            protein = model.copy()
            self.current_score = self.get_score(protein)
            self.current_placement = protein
