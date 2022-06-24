from classes.protein import Protein
import random

def greed(protein_obj):
    
    string = protein_obj.view_protein_string()

    direction_list = [-1, 1, -2, 2 ,-3, 3]
    protein_obj.assign_coordinates([[0,0,0,0]])
    
    for id in range(len(string)):
        if id == len(string) - 1:
            break

        amino = protein_obj.view_protein()[id]

        x = amino[1]
        y = amino[2]
        z = amino[3]


        highest_score = protein_obj.current_score()
        best_move = 1

        for move in direction_list:
            change_in_score = False
            if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
                if (x - 2, y -1, z) and (x - 2, y + 1, z) and (x - 2, y, z - 1) and (x - 2, y, z + 1) not in protein_obj.filled_coordinates():
                    protein_obj.assign_coordinates([[id + 1, x - 1, y, z]])
                    temp_score = protein_obj.current_score()
                    if temp_score > highest_score:
                        highest_score = temp_score
                        best_move = -1
                        change_in_score = True
                    protein_obj.assign_coordinates([[id + 1, None, None, None]])
                

            elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
                if (x + 2, y -1, z) and (x + 2, y + 1, z) and (x + 2, y, z - 1) and (x + 2, y, z + 1) not in protein_obj.filled_coordinates():
                    protein_obj.assign_coordinates([[id + 1, x + 1, y, z]])
                    temp_score = protein_obj.current_score()
                    if temp_score > highest_score:
                        highest_score = temp_score
                        best_move = 1
                        change_in_score = True
                    protein_obj.assign_coordinates([[id + 1, None, None, None]])
                

            elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
                if (x - 1, y - 2, z) and (x + 1, y - 2, z) and (x, y - 2, z - 1) and (x, y - 2, z + 1) not in protein_obj.filled_coordinates():
                    protein_obj.assign_coordinates([[id + 1, x, y - 1, z]])
                    temp_score = protein_obj.current_score()
                    if temp_score > highest_score:
                        highest_score = temp_score
                        best_move = -2
                        change_in_score = True
                    protein_obj.assign_coordinates([[id + 1, None, None, None]])
                

            elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
                if (x - 1, y + 2, z) and (x + 1, y + 2, z) and (x, y + 2, z - 1) and (x, y + 2, z + 1) not in protein_obj.filled_coordinates():
                    protein_obj.assign_coordinates([[id + 1, x, y + 1, z]])
                    temp_score = protein_obj.current_score()
                    if temp_score > highest_score:
                        highest_score = temp_score
                        best_move = 2
                        change_in_score = True
                    protein_obj.assign_coordinates([[id + 1, None, None, None]])
                

            elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
                if (x - 1, y, z - 2) and (x + 1, y, z - 2) and (x, y - 1, z - 2) and (x, y + 1, z - 2) not in protein_obj.filled_coordinates():
                    protein_obj.assign_coordinates([[id + 1, x, y, z - 1]])
                    temp_score = protein_obj.current_score()
                    if temp_score > highest_score:
                        highest_score = temp_score
                        best_move = -3
                        change_in_score = True
                    protein_obj.assign_coordinates([[id + 1, None, None, None]])
                

            elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
                if (x - 1, y, z + 2) and (x + 1, y, z + 2) and (x, y - 1, z + 2) and (x, y + 1, z + 2) not in protein_obj.filled_coordinates():
                    protein_obj.assign_coordinates([[id + 1, x, y, z + 1]])
                    temp_score = protein_obj.current_score()
                    if temp_score > highest_score:
                        highest_score = temp_score
                        best_move = 3
                        change_in_score = True
                    protein_obj.assign_coordinates([[id + 1, None, None, None]])
     

        if change_in_score == False:
            best_move = random.choice(direction_list)


        while True:
            move = best_move
        

            if move == -1 and (x - 1, y, z) not in protein_obj.filled_coordinates():
                x = x - 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 1 and (x + 1, y, z) not in protein_obj.filled_coordinates():
                x = x + 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == -2 and (x, y - 1, z) not in protein_obj.filled_coordinates():
                y = y - 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 2 and (x, y + 1, z) not in protein_obj.filled_coordinates():
                y = y + 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == -3 and (x, y, z - 1) not in protein_obj.filled_coordinates():
                z = z - 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                break

            elif move == 3 and (x, y, z + 1) not in protein_obj.filled_coordinates():
                z = z + 1
                protein_obj.assign_coordinates([[id + 1, x, y, z]])
                break
            else:
                best_move = random.choice(direction_list)