import random

def folding_sequencies(protein_obj):
    """
    This is a algorithm that assigns random coordinates to the aminoacids
    without changing their order in the protein string.
    """

    string = protein_obj.view_protein_string()

    protein_obj.assign_coordinates([[0,0,0,0]])


    for id in range(len(string)):
        direction_list = [1, -1, 2, -2 ,3, -3]
        if id == len(string) - 1:
            break
        amino = protein_obj.view_protein()[id]
        x = amino[1]
        y = amino[2]
        z = amino[3]

        print(string[id])
        print(string[id + 1], "next")

        if id == 0:
            move = random.choice(direction_list)
            past_move = move
        elif string[id] != string[id + 1]:
            move = past_move

        elif string[id] == string[id + 1]:
            direction_list.remove(past_move)
            move = random.choice(direction_list)
            

        while True:

            if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
                x = x - 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
                x = x + 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                past_move = move
                break

            elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
                y = y - 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                past_move = move
                break

            elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
                y = y + 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                past_move = move
                break

            elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
                z = z - 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                past_move = move
                break

            elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
                z = z + 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                past_move = move
                break
            else:
                move = random.choice(direction_list)
