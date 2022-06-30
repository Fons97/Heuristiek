'''
Branch And Bound Algorithm for the Protein Folding Problem in the HP Lattice Model

- This algorithm inherites functionalties from the BeamBreadth algorithm
- Uses breadth first search and reduces the number of branches by
  limiting the probability that a partial conformation will survive if it doesn't
  provide the best score within the partial conformations of the same length
- After all possible and accepted partial conformations are tried, the program returns
  the placement that has generated the best (lowest) score
- Inspired by: https://www.brown.edu/Research/Istrail_Lab/_proFolding/papers/2005/bran-06.pdf
'''

import random
import queue
import copy
import math
from collections import defaultdict

from .beambreadth import BeamBreadth

from code.classes.protein_model import Model

class BranchAndBound(BeamBreadth):

    def __init__(self, model: Model, dimension: int=3):
        super().__init__(model, dimension)

        self.best_scores = defaultdict(int)
        self.all_scores = defaultdict(list)
        self.average_scores = defaultdict(int)
        self.p1 = 0.5
        self.p2 = 0.9
        self.p3 = 0.8

    def update_scores(self, model: Model, index: int, score: int) -> None:
        '''
        Updates the scores of partial conformation
        - Overal Best Score, regardless of length of partial conformation
        - Best Score within partial conformations of same length
        - Average Score of partial conformations of same length
        - Dictionary of lists with all scores of partial conformations of same length
        - Add partial conformation to queue
        '''
        # If current partial conformation has the best score so far, save partial conformation
        if score <= self.top_score:
            self.top_score = score
            self.best_placement = model.copy()

        # Add score to list of scores with same length as current partial conformation
        self.all_scores[index].append(score)

        # Re-calculate the average score for partial conformations of same length
        self.average_scores[index] = math.floor(sum(self.all_scores[index]) / len(self.all_scores[index]))

        # Add partial conformation to queue to build further upon
        self.nr_of_states += 1
        child = model.copy()
        self.queue.put(child)

    def prune(self, model: Model, index: int, score: int) -> None:
        '''
        Decides whether a partial conformation is kept or pruned, based on:
        - Score: partial conformations with best scores have a fifty percent chance of being kept.
          Conformations that score between best and average have eighty percent chance of being pruned.
          Conformations with a score worse than average have ninety percent chance of being pruned.
        ! Lower scores are better scores. Keep this in mind when reading the if-statements below
        '''
        amino = model.protein[index][0]

        # Current score is lower than best score, no pruning occurs
        if score <= self.best_scores[index]:
            if random.random() > self.p1:

                # Update scores & add partial conformations to queue
                self.update_scores(model, index, score)
                self.best_scores[index] = score

        # Current score is worse than average score, most conformations get pruned
        elif score >= self.average_scores[index]:
            if random.random() > self.p2:
                self.update_scores(model, index, score)

        # If current score is better than average, chance of being pruned is less high
        elif score > self.best_scores[index] and self.average_scores[index] > score:
            if random.random() > self.p3:
                self.update_scores(model, index, score)

    def update_status(self, model: Model, index: int, x: int, y: int, z: int) -> None:
        '''
        Assigns coordinates to amino acids, irreversibly placing them on the grid
        Sends new conformation to prune function to determine if new conformation is
        kept
        '''
        model.assign_coordinates([[index + 1, x, y, z]])
        score = self.get_score(model)
        self.prune(model, index, score)

    def last_amino(self, model: Model, index: int) -> None:
        '''
        When algorithm is at last amino of protein chain, score is updated one last
        time to get the final highest score & best folding
        '''
        score = self.get_score(model)
        self.update_scores(model, index, score)
