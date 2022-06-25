import random
import math

from classes.protein import Protein



def randomize(model):
    '''
    RANDOMIZE EXPLANATION
    '''

    model.assign_coordinates([[0, 0, 0, 0]])

    list = [1, -1, 2, -2 , 3, -3]

    for id in range(model.length):
        
        if id == model.length - 1:
            break

        garbage, x, y, z = model.protein[id]
   

        while True:
            move = random.choice(list)

            if move == -1 and (x - 1, y, z) not in model.filled_coordinates():
                x = x - 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 1 and (x + 1, y, z) not in model.filled_coordinates():
                x = x + 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == -2 and (x, y - 1, z) not in model.filled_coordinates():
                y = y - 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 2 and (x, y + 1, z) not in model.filled_coordinates():
                y = y + 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == -3 and (x, y, z - 1) not in model.filled_coordinates():
                z = z - 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 3 and (x, y, z + 1) not in model.filled_coordinates():
                z = z + 1
                model.assign_coordinates([[id + 1, x, y, z]])
                break

    return model
            