import math

def stair_fold(model):

    string = model.view_protein_string()

    model.assign_coordinates([[0,0,0,0]])

    list = [1, -1, 2, -2 ,3, -3]

    for id in range(len(string)):
        if id == len(string) - 1:
            break

        amino = model.view_protein()[id]
        x = amino[1]
        y = amino[2]
        z = amino[3]

        move = 2

        middle = round(len(string)/2)
        quarter = math.floor(middle/2)

        if id == quarter:
            move = 1

        elif id >= quarter and id < middle:
            move = -2

        elif id == middle:  # middle - 1
            move = 3

        elif id > middle and id < middle + quarter:
            move = 2

        elif id == middle + quarter:
            move = -1

        elif id > middle + quarter:
            move = -2


        while True:

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