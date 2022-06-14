from classes.protein import Protein
import random

def randomize(protein_obj):

    moves = [-2, 1, 2, 2, -1, -1, -2, -2, -2, 1, 1, 1, 2, 2, 2, 2, -1, -1, -1, -1, -2]

    string = protein_obj.view_protein_string()

    #
    protein_obj.assign_coordinates([[0,0,0,0]])

    for id in range(len(string)):
        if id == len(string) - 1:
            break

        # view_protein geeft je alle aminozuren/hele eiwit, id is aminozuur index
        amino = protein_obj.view_protein()[id]

        move = moves[id]
        x = amino[1]
        y = amino[2]
        z = amino[3]

        if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
            x = x - 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])

        elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
            x = x + 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])

        elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
            y = y - 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])

        elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
            y = y + 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])

        elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
            z = z - 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])

        elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
            z = z + 1
            protein_obj.assign_coordinates([[id + 1, x, y, z]])


    print(protein_obj.view_protein())
    print(protein_obj.score())
#
#     for id in range(len(string)):
#         if id == len(string) - 1:
#             break
#         amino = protein_obj.view_protein()[id]
#         x = amino[1]
#         y = amino[2]
#         z = amino[3]
#         print(amino)
#
#         while True:
#             move = random.choice(list)
#
#             if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
#                 x = x - 1
#                 protein_obj.assign_coordinates([[id + 1, x, y, z]])
#                 break
#
#             elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
#                 x = x + 1
#                 protein_obj.assign_coordinates([[id + 1, x, y, z]])
#                 break
#
#             elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
#                 y = y - 1
#                 protein_obj.assign_coordinates([[id + 1, x, y, z]])
#                 break
#
#             elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
#                 y = y + 1
#                 protein_obj.assign_coordinates([[id + 1, x, y, z]])
#                 break
#
#             elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
#                 z = z - 1
#                 protein_obj.assign_coordinates([[id + 1, x, y, z]])
#                 break
#
#             elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
#                 z = z + 1
#                 protein_obj.assign_coordinates([[id + 1, x, y, z]])
#                 break
#
# def spiral(protein_obj):
#     string = protein_obj.view_protein_string()
#
#     protein_obj.assign_coordinates([[0,0,0,0]])
#
#     list = [1, -1, 2, -2 ,3, -3]
#
#     for id in range(len(string)):
#         if id == len(string) - 1:
#             break
#
#         amino = protein_obj.view_protein()[id]
#         x = amino[1]
#         y = amino[2]
#         z = amino[3]
#
#     print(x, y, z)
#     moves = [-2, 1, 2, 2, -1, -1, -2, -2]
#     # moves = [-2, 1, 2, 2, -1, -1, -2, -2], -2, 1, 1, 1, 2, 2, 2, 2, -1, -1, -1, -1, -1]
#     #
#     # for move in moves:
#     #     if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
#     #         x = x - 1
#     #         protein_obj.assign_coordinates([[id + 1, x, y, z]])
#     #         break
#     #
#     #     elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
#     #         x = x + 1
#     #         protein_obj.assign_coordinates([[id + 1, x, y, z]])
#     #         break
#     #
#     #     elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
#     #         y = y - 1
#     #         protein_obj.assign_coordinates([[id + 1, x, y, z]])
#     #         break
#     #
#     #     elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
#     #         y = y + 1
#     #         protein_obj.assign_coordinates([[id + 1, x, y, z]])
#     #         break
#     #
#     #     elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
#     #         z = z - 1
#     #         protein_obj.assign_coordinates([[id + 1, x, y, z]])
#     #         break
#     #
#     #     elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
#     #         z = z + 1
#     #         protein_obj.assign_coordinates([[id + 1, x, y, z]])
#     #         break
