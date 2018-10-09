import cv2 as cv
import numpy as np
import time

from objects.Object import Object
from objects.Colors import Colors

class ObjectDetector:
    labels = [1]
    objects = {}

    number_of_labels = 0

    def __init__(self, image, binary_image, color_matrix):
        self.image = image
        self.binary_image = binary_image
        self.color_matrix = color_matrix

        self.label_plane = np.zeros(shape=(len(self.image), len(self.image[0])))

    def scan_image(self):
        self.label_plane = np.zeros(shape=(len(self.image), len(self.image[0])))

        for row in range(len(self.image)):
            row_len = len(self.image[row])

            for pix in range(row_len):
                # if pixel not white
                if self.color_matrix[row][pix] != "w":
                    self.check_adjacent_area(row, pix)

        sorted_objects = {}
        id_count = 0

        for idx in range(1, len(self.objects)):
            self.objects[idx].object_post_processing()
            if self.objects[idx].size > 100:
                print(self.objects[idx].get_color(), " ", self.objects[idx].get_coordinates())

                new_obj = Object(id_count)
                new_obj.coordinates = self.objects[idx].get_coordinates()
                new_obj.set_color(self.objects[idx].get_color())

                sorted_objects[id_count] = new_obj
                id_count += 1

        self.objects = None
        self.objects = sorted_objects

        print("Detected ", len(self.objects), " objects")

    def check_adjacent_area(self, row, pix):
        connected = False
        lock = False

        for i in range(-2, 3):
            for j in range(-2, 3):
                try:
                    if self.label_plane[row + i][pix + j] != 0.:
                        if self.color_matrix[row + i][pix + j] == self.color_matrix[row][pix]:
                            connected = True

                            label = self.label_plane[row + i][pix + j]
                            self.label_plane[row][pix] = label

                            if lock is False:
                                self.objects[label].insert_coordinate(coordinate=(row, pix))
                                lock = True
                except:
                    pass


        # Encountering of a new object
        if connected is False:
            self.number_of_labels += 1
            # Very first object
            if len(self.labels) == 1:
                label = 1
                self.labels.append(label)
            else:
                label = self.labels[len(self.labels) - 1] + 1
                self.labels.append(label)

            self.label_plane[row][pix] = label

            # Create an object // Object id >> label
            obj = Object(label)
            # Insert initial coordinate
            obj.insert_coordinate(coordinate=(row, pix))
            self.objects[label] = obj  # Dict
            # Set color
            self.objects[label].set_color(self.color_matrix[row][pix])

    def post_process_objects(self):
        for idx in range(1, len(self.objects)):
            self.objects[idx].object_post_processing()

    def drop_small_objects(self):
        new_objects = {}
        for idx in range(1, len(self.objects)):

            if self.objects[idx].size < 100:
                new_objects = self.remove_object(objects=self.objects, key=idx)

        self.objects = None
        self.objects = new_objects
        print(self.objects)

        for idx in range(1, len(new_objects)):
            print(new_objects[idx].size)

    def remove_object(self, objects, key):
        r = dict(objects)
        del r[key]
        return r

    def print_label_plane(self):
        for row in self.label_plane:
            for pix in range(len(row)):
                print(row[pix], end="\t")
            print()

    def get_objects(self):
        object_list = []
        return self.objects

    def get_stats(self):
        return self.number_of_labels

    def get_label_plane(self):
        return self.label_plane


