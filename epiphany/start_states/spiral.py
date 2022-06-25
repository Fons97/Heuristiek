def spiral(model):
    moves = [-2, 1, 2, 2, -1, -1, -2, -2, -2, 1, 1, 1, 2, 2, 2, 2, -1, -1, -1, -1, -2, -2, -2, -2, -2, 1, 1, 1, 1, 1,
              2, 2, 2, 2, 2, 2, -1, -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2]

    string = model.view_protein_string()

    model.assign_coordinates([[0,0,0,0]])

    for id in range(len(string)):
        if id == len(string) - 1:
            break

        # view_protein geeft je alle aminozuren/hele eiwit, id is aminozuur index
        amino = model.view_protein()[id]

        model.assign_coordinates([[0,0,0,0]])

        move = moves[id]
        x = amino[1]
        y = amino[2]
        z = amino[3]

        if move == -1 and (x - 1, y, z) not in model.filled_coordinates():
            x = x - 1
            model.assign_coordinates([[id + 1, x, y, z]])

        elif move == 1 and (x + 1, y, z) not in model.filled_coordinates():
            x = x + 1
            model.assign_coordinates([[id + 1, x, y, z]])

        elif move == -2 and (x, y - 1, z) not in model.filled_coordinates():
            y = y - 1
            model.assign_coordinates([[id + 1, x, y, z]])

        elif move == 2 and (x, y + 1, z) not in model.filled_coordinates():
            y = y + 1
            model.assign_coordinates([[id + 1, x, y, z]])

        elif move == -3 and (x, y, z - 1) not in model.filled_coordinates():
            z = z - 1
            model.assign_coordinates([[id + 1, x, y, z]])

        elif move == 3 and (x, y, z + 1) not in model.filled_coordinates():
            z = z + 1
            model.assign_coordinates([[id + 1, x, y, z]])