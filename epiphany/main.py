from loader import load_protein
from classes.protein import Protein
from algorithms import randomize


string = load_protein("proteins.txt", '1')
eggwhit = Protein(string)
randomize(eggwhit)
print(eggwhit.score())

print(eggwhit.step_order())
