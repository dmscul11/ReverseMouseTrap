from world.Reasoner import Reasoner
from movements.Movements import *
from objects.Colors import Colors

from movements.Falling import *
from movements.Pivoting import *
from movements.StringMover import *

from detector.NewObjectDetector import NewObjectDetector

import cv2 as cv

import os
import numpy as np


class World:
    def __init__(self, objects, original_image, aggregated_image, binary_image, color_matrix, object_detector):
        self.terminated = False
        self.steps = 0
        self.stability_count = 0

        self.world_row = len(original_image)
        self.world_col = len(original_image[0])

        self.objects = objects
        self.original_image = original_image
        self.aggregated_image = aggregated_image
        self.binary_image = binary_image
        self.color_matrix = color_matrix

        self.object_detector = object_detector

        self.reasoner = Reasoner()

    def simulate(self):
        """
        Starts the simulation
        :return: Terminated: Bool
        """
        print("Step : ", self.steps)

        # part 1 test
        unstable = 1
        all_neighbors = {}
        all_neighbors[1] = range(1, len(self.objects) + 1)
        print(all_neighbors)
        while unstable:
            unstable = self.simulate_falling()
            reconstructed_image = self.reconstruct_image(self.objects)
            self.update_render(self.steps, reconstructed_image)
            self.reload_image(step=self.steps)
            self.steps += 1

        # part 1 test
        for i in range(10):
            print("Move all : ", str(i))
            self.contact_interaction(all_neighbors)
            reconstructed_image = self.reconstruct_image(self.objects)
            self.update_render(self.steps, reconstructed_image)
            self.reload_image(step=self.steps)
            self.steps += 1

        # neighbors = self.detect_contact(unstable)
        # self.contact_interaction(neighbors)

        try:
            reconstructed_image = self.reconstruct_image(self.objects)
            self.update_render(self.steps, reconstructed_image)
            self.reload_image(step=self.steps)
        except:
            # Bound reached exception. Leave this for now.
            self.terminated = True

        # part 1 test
        self.terminated = True

        self.steps += 1
        if len(unstable) == 0:
            self.stability_count += 1
        else:
            self.stability_count = 0

        if self.stability_count == 3:
            self.terminated = True

    def simulate_falling(self):
        unstable_objects, unstable_centeroids = self.reasoner.check_stability_of_all_objects(self.object_detector,
                                                                                             self.objects)
        print("Unstable Objects: ", unstable_objects)
        print("Unstable Centeroids: ", unstable_centeroids)

        self.move_unstable_objects_down(unstable_objects)
        return unstable_objects

    def move_unstable_objects_down(self, unstable_objects):
        for unstable_id in unstable_objects:
            move_object_down(self.objects[unstable_id])

    def detect_contact(self, unstable):
        neighbors = {}
        for obj_id in unstable:
            neighbor = get_neighbors(self.object_detector, obj_id)
            if len(neighbor) > 1:
                neighbors[obj_id] = neighbor[1:]

        print(neighbors)
        return neighbors

    def contact_interaction(self, neighbors):
        for key in neighbors.keys():
            # key == id of the ball
            neighbor_id = neighbors[key][0]
            if self.objects[neighbor_id].pivoted is True:
                new_image, new_coord, new_center = rotate_pivot(self.object_detector, self.aggregated_image,
                                                                neighbor_id, self.objects[neighbor_id].pivoted_by, 'counterclockwise')
                self.objects[neighbor_id].coordinates = new_coord

            elif self.objects[neighbor_id].color == 'g':
                string_coords = self.objects[neighbor_id].coordinates
                if not self.objects[neighbor_id].front_end:
                    edges, front_end, back_end = get_string_ends(string_coords, self.color_matrix)
                    width = get_string_width(edges)
                else:
                    front_end = self.objects[neighbor_id].front_end
                    back_end = self.objects[neighbor_id].back_end
                    width = self.objects[neighbor_id].width
                self.aggregated_image, new_string, new_front_end, new_back_end = pull_string(self.aggregated_image,
                                                            string_coords, 'front', front_end, 'up', back_end, width)

                self.objects[neighbor_id].coordinates = list(new_string)
                self.objects[neighbor_id].front_end = list(new_front_end)
                self.objects[neighbor_id].back_end = list(new_back_end)
                self.objects[neighbor_id].width = width

    def reload_image(self, step):
        if step != 0:
            # reload previous image
            dir_path = os.path.join(os.path.dirname(__file__), "render_files")
            path = os.path.join(dir_path, str(step).zfill(5) + ".png")
            self.original_image, self.aggregated_image, self.binary_image, self.color_matrix = reload(path)

            # Run detector, but update its object externally
            det = NewObjectDetector(self.original_image, self.binary_image, self.color_matrix)
            det.scan_image()
            det.objects = self.objects
            self.object_detector = det

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

    def update_render(self, step, reconstructed_image):
        """
        Updates state after an iteration
        :return:
        """
        dir_path = os.path.join(os.path.dirname(__file__), "render_files")
        try:
            os.mkdir(dir_path)
        except:
            pass

        path = os.path.join(dir_path, str(step).zfill(5) + ".png")
        cv.imwrite(path, reconstructed_image)

    def reconstruct_image(self, objects):
        reconstructed_image = np.full(shape=(self.world_row, self.world_col, 3), fill_value=self.get_color_BGR(color_string="w"))

        for object_idx in range(1, len(objects) + 1):
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

