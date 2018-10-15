from movements.Movements import *
from objects.Colors import Colors
from world.Reasoner import *
from objects.Updater import *

from movements.Pivoting import *

import cv2 as cv

import os
import numpy as np


class World:
    # Half - Singleton. Will not construct itself.
    # Must not call get_instance before construction.
    __instance = None

    def __init__(self):
        if World.__instance != None:
            raise Exception("World already exists")
        else:
            World.__instance = self

    @staticmethod
    def get_instance():
        if World.__instance is None:
            World()
        return World.__instance

    def create_world(self, objects, objects_dict, label_plane):
        self.terminated = False
        self.step_count = 0
        self.stability_count = 0

        self.world_row = len(label_plane)
        self.world_col = len(label_plane[0])

        self.objects = objects
        self.objects_dict = objects_dict

        self.label_plane = label_plane

        self.unstable_objects = []
        self.maniputated_objects = []

    def set_object_stack(self, object_stack):
        self.object_stack = object_stack

    def simulate(self):
        """
        Starts the simulation
        :return: Terminated: Bool
        """
        print("Step : ", self.step_count)
        # self.print_all_objects_properties()

        # detect movement for next object
        obj = self.object_stack.pop() # This is the object id and direction tuple
        objects_affected = self.move_object(obj)
        self.object_stack.extend(objects_affected)   # add affected objects

        # Check boundary condition
        for obj in self.objects:
             tip = will_tip(obj)

        # Update objects that are changed
        update_objects(objects_to_update=self.maniputated_objects, label_plane=self.label_plane)

        # Reconstruct image & Update label_plane
        reconstructed_image = self.reconstruct_image(self.objects_dict)
        # Tipping
        tipping_objects = ()
        for obj in self.objects:
            tipping_objects = will_tip(obj) # (Bool, direction)
            # print(obj.centeroid, "  ", obj.point_of_impact)
            try:
                if tipping_objects[0]:
                    # Move it right or left
                    # Unstable_objects cleared so we can append tuple
                    self.unstable_objects.append((obj, tipping_objects[1]))
            except:
                pass

        if len(self.unstable_objects) != 0:
            self.move_tipping_objects(self.unstable_objects)

        # Render and output image
        self.update_render(self.steps, reconstructed_image)

        # Check termination condition
        self.steps += 1
        if len(self.unstable_objects) == 0:
            self.stability_count += 1
        else:
            self.stability_count = 0

        if self.stability_count == 3:
            self.terminated = True


    def move_object(self, obj):
        if obj[1] == 'down':
            self.move_unstable_objects_down(self.objects_dict[obj[0]])

    def move_unstable_objects_down(self, unstable_objects):
        self.stability_count = 0 # Reset stability count 0 This operation is need for all object manipulation algorithms
        try:
            unstable_objects[0]

            for object in unstable_objects:
                self.maniputated_objects.append(object)
                move_object_down(object)

            self.unstable_objects.clear()
        except:
            self.maniputated_objects.append(unstable_objects)
            move_object_down(unstable_objects)

            self.unstable_objects.clear()



    def move_tipping_objects(self, tipping_objects):
        self.stability_count = 0
        for object in tipping_objects:
            self.maniputated_objects.append(object[0])
            if object[1] == "right":
                move_object_right(object[0])
                move_object_right(object[0])
                move_object_right(object[0])
            elif object[1] == "left":
                move_object_left(object[0])
                move_object_left(object[0])
                move_object_left(object[0])

        self.unstable_objects.clear()

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
        Updates state after an iteration outputs the image
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
        self.label_plane = np.zeros(shape=(self.world_row, self.world_col))
        reconstructed_image = np.full(shape=(self.world_row, self.world_col, 3), fill_value=self.get_color_BGR(color_string="w"))

        for object_idx in range(1, len(objects) + 1):
            coordinates = objects[object_idx].get_coordinates()
            color = objects[object_idx].get_color()

            for coord in coordinates:
                # Push color
                reconstructed_image[coord[0]][coord[1]] = self.get_color_BGR(color)
                self.label_plane[coord[0]][coord[1]] = objects[object_idx].object_id

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

    def print_all_objects_properties(self):
        for obj in self.objects:
            obj.print_properties()