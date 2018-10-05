import cv2 as cv
import numpy as np

from objects.Object import Object

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
                if self.color_matrix[row][pix] != b'w':
                    self.check_adjacent_area(row, pix)

    def check_adjacent_area(self, row, pix):
        connected = False
        lock = False
        try:
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if self.label_plane[row + i][pix + j] != 0.:
                        connected = True
                        label = self.label_plane[row + i][pix + j]
                        self.label_plane[row][pix] = label

                        if lock is False:
                            self.objects[label].insert_coordinate(coordinate=(row, pix))
                            lock = True

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
                self.objects[label] = obj # Dict
                # Set color
                self.objects[label].set_color(self.color_matrix[row][pix])

        except:
            # Exception when pixel is at the boundary
            # Do nothing
            pass

    def print_label_plane(self):
        for row in self.label_plane:
            for pix in range(len(row)):
                print(row[pix], end="\t")
            print()

    def get_objects(self):
        return self.objects

    def get_stats(self):
        return self.number_of_labels


