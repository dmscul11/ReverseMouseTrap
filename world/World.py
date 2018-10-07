from world.Reasoner import Reasoner
from movements.Movements import *
from loader.ImageLoader import show_image

import numpy as np


class World:
    def __init__(self, objects, original_image, aggregated_image, binary_image, color_matrix):
        self.terminated = False

        self.world_row = len(original_image)
        self.world_col = len(original_image[0])

        self.objects = objects
        self.original_image = original_image
        self.aggregated_image = aggregated_image
        self.binary_image = binary_image
        self.color_matrix = color_matrix

        self.reasoner = Reasoner()

    def simulate(self):
        """
        Starts the simulation
        :return: Terminated: Bool
        """

        for object_idx in range(1, len(self.objects) + 1):
            move_object_right(object=self.objects[object_idx])

        reconstructed = self.reconstruct_image(self.objects)
        show_image(reconstructed)

        """
        OUR LOGIC
        """

        self.terminated = True

    def reconstruct_image(self, objects):
        reconstructed_image = np.zeros(shape=(self.world_row, self.world_col))

        for object_idx in range(1, len(objects) + 1):
            coordinates = objects[object_idx].get_coordinates()
            color = objects[object_idx].get_color()

            print(objects[object_idx])
            for coord in coordinates:
                reconstructed_image[coord[0]][coord[1]] = 255.

        print(reconstructed_image)
        return reconstructed_image



    def update_render(self):
        """
        Updates state after an iteration
        :return:
        """
        pass

