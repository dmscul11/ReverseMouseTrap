import numpy as np
from objects.Colors import Colors

def reconstruct_image(objects, world_row, world_col):
    reconstructed_image = np.full(shape=(world_row, world_col, 3),
                                  fill_value=get_color_BGR(color_string="w"))

    for object_idx in range(1, len(objects)):
        coordinates = objects[object_idx].get_coordinates()
        color = objects[object_idx].get_color()

        for coord in coordinates:
            # Push color
            reconstructed_image[coord[0]][coord[1]] = get_color_BGR(color)

    return reconstructed_image


def reconstruct_single_object(obj, world_row, world_col):
    reconstructed_image = np.full(shape=(world_row, world_col, 3),
                                  fill_value=get_color_BGR(color_string="w"))

    coordinates = obj.get_coordinates()
    color = obj.get_color()

    for coord in coordinates:
        # Push color
        try:
            reconstructed_image[coord[0]][coord[1]] = get_color_BGR(color)
        except:
            pass

    return reconstructed_image

def get_color_BGR(color_string):
        if color_string == "w":
            return Colors.W.value

        if color_string == "d":
            return Colors.D.value

        if color_string == "b":
            return Colors.B.value

        if color_string == "y":
            return Colors.Y.value

        if color_string == "g":
            return Colors.G.value