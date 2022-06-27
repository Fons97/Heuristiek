import random
import math

from algorithms.hillclimber import HillClimber

from classes.protein_model import Model

class SimulatedAnnealing(HillClimber):
    """
    The SimulatedAnnealing class that changes a random node in the model to a random valid value.
    Each improvement or equivalent solution is kept for the next iteration.
    Also sometimes accepts solutions that are worse, depending on the current temperature.
    Most of the functions are similar to those of the HillClimber class, which is why
    we use that as a parent class.
    """
    def __init__(self, model, temperature=1):
        # Use the init of the Hillclimber class
        super().__init__(model)

        self.T0 = temperature
        self.T = temperature
        self.counter = 0

    def update_temperature(self):
        self.T = self.T - (self.T0 / self.iterations)

    def check_protein(self, folded_proteins):


        for obj in folded_proteins:

            temp_score = obj.relaxed()

            delta = temp_score - self.score
            probability = math.exp(-delta / self.T)

    

            if random.random() < probability:
                self.model = obj
                self.score = temp_score

        if temp_score == self.score:
            self.counter += 1

        if self.counter == 200:
            self.T = 1
            print("reheat--------------------------------------------")
            self.counter = 0

        # Update the temperature
        self.update_temperature()