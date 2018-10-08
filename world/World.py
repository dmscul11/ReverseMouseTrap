from world.Reasoner import Reasoner
from movements.Movements import *
from loader.ImageLoader import show_image
from objects.Colors import Colors
from movements import Movements
from movements import Falling

import numpy as np


class World:
    def __init__(self, objects, original_image, aggregated_image, binary_image, color_matrix, object_detector):
        self.terminated = False

        self.world_row = len(original_image)
        self.world_col = len(original_image[0])

        self.objects = objects
        self.original_image = original_image
        self.aggregated_image = aggregated_image
        self.binary_image = binary_image
        self.color_matrix = color_matrix

        self.object_detector = object_detector

        self.reasoner = Reasoner()

        self.initial_reconstructed = self.reconstruct_image(self.objects)

    def simulate(self):
        """
        Starts the simulation
        :return: Terminated: Bool
        """

        for cluster_id in self.objects.keys():
            stability = Falling.check_instability(obj_detector=self.object_detector, cluster_id=cluster_id)
            print(stability)


        """
        OUR LOGIC
        """

        self.terminated = True

    def get_color_BGR(self, color_string):
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

    def get_initial_reconstructed_image(self):
        return self.initial_reconstructed

    def update_render(self):
        """
        Updates state after an iteration
        :return:
        """
        pass

    def reconstruct_image(self, objects):
        reconstructed_image = np.full(shape=(self.world_row, self.world_col, 3), fill_value=self.get_color_BGR(color_string="w"))

        for object_idx in range(1, len(objects)):
            coordinates = objects[object_idx].get_coordinates()
            color = objects[object_idx].get_color()

            for coord in coordinates:
                # Push color
                reconstructed_image[coord[0]][coord[1]] = self.get_color_BGR(color)

        return reconstructed_image

    def reconstruct_single_object(self, obj):
        reconstructed_image = np.full(shape=(self.world_row, self.world_col, 3), fill_value=self.get_color_BGR(color_string="w"))

        coordinates = obj.get_coordinates()
        color = obj.get_color()

        for coord in coordinates:
            # Push color
            try:
                reconstructed_image[coord[0]][coord[1]] = self.get_color_BGR(color)
            except:
                pass

        return reconstructed_image

