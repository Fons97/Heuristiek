import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from code.classes.protein_model import Model
from code.algorithms.climber import RandomClimber


def make_histogram(model: Model, scoring: list[int, ...], filename: str) -> None:

    scores = scoring

    plt.hist(scores, bins=10)
    plt.show()

def plot_3d(model: Model, filename: str) -> None:

    # Matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # amino_list = model.protein.values()
    # print(amino_list)
    # create list to be filled with coordinates of special_connections
    special_list = []

    x_values = []
    y_values = []
    z_values = []

    # hlabel = ['H', model.protein]

    for key, amino in model.protein.items():

        # Plots amino nodes on 3D graph
        if amino[0] == 'H':
            special_list.append([key, amino[1], amino[2], amino[3]])
            ax.scatter(amino[1], amino[2], amino[3], s=50, c='red', zorder=2, label=[key, 'H'])

        elif amino[0] == 'C':
            special_list.append([key, amino[1], amino[2], amino[3]])
            ax.scatter(amino[1], amino[2], amino[3], s=50, c='green', zorder=2, label=[key, 'C'])

        elif amino[0] == 'P':
            ax.scatter(amino[1], amino[2], amino[3], s=50, c='blue', zorder=2, label=[key, 'P'])

        # Used to plot lines in between amino_nodes
        x_values.append(amino[1])
        y_values.append(amino[2])
        z_values.append(amino[3])


    ax.set_xticks(np.arange(min(x_values)-1, max(x_values)+1, 1.0))
    ax.set_yticks(np.arange(min(y_values)-1, max(y_values)+1, 1.0))
    ax.set_zticks(np.arange(min(z_values)-1, max(z_values)+1, 1.0))

    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")

    ax.set_title(f'Score: {model.current_score()}')

    ax.legend(handles=[mpatches.Patch(color='red', label='H'),
                       mpatches.Patch(color='blue', label='P'),
                       mpatches.Patch(color='green', label='C')])

    ax.plot(x_values, y_values, z_values, linestyle="solid",
    linewidth=1.2, c="grey", zorder=1)

    # Needed to prevent a dotted line beeing drawn twice
    counting_variable = 0

    # This for loop draws the dotted lines
    for amino in special_list:

        counting_variable += 1

        for compare_amino in special_list[counting_variable:]:

            if amino[0] - compare_amino[0] <= 1 and amino[0] - compare_amino[0] >= -1:
                continue

            delta_x = amino[1] - compare_amino[1]
            delta_y = amino[2] - compare_amino[2]
            delta_z = amino[3] - compare_amino[3]
            delta_coords = (delta_x, delta_y, delta_z)

            if (delta_coords == (1,0,0) or delta_coords == (-1,0,0) or
            delta_coords == (0,1,0) or delta_coords == (0,-1,0) or
            delta_coords == (0,0,1) or delta_coords == (0,0,-1)):

                x_axis_interactions = [amino[1], compare_amino[1]]
                y_axis_interactions = [amino[2], compare_amino[2]]
                z_axis_interactions = [amino[3], compare_amino[3]]

                ax.plot(x_axis_interactions, y_axis_interactions,
                z_axis_interactions, linestyle="dotted",
                linewidth=3, c="green", zorder=1)


    plt.show()
