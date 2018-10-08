import numpy as np
from objects.Colors import Colors
from objects.Object import Object

class NewObjectDetector:
    def __init__(self, aggregated_image, binary_image, color_matrix):
        self.aggregated_image = aggregated_image
        self.binary_image = binary_image
        self.color_matrix = color_matrix

        self.detected_objects = []
        self.objects = {}

        self.row_len = len(self.aggregated_image)
        self.col_len = len(self.aggregated_image[0])

        self.color_list = ["d", "b", "y", "g"]

        self.label_plane = np.full(shape=(self.row_len, self.col_len), fill_value=0)

    def scan_image(self):
        self.color_segregated, self.segregated_binary = self.segregate_by_color()
        self.find_connected_components()

    def segregate_by_color(self):
        segregated = {}
        segregated_binary = {}

        for color in self.color_list:
            tmp_cordinates = []
            tmp_binary = np.full(shape=(self.row_len, self.col_len), fill_value=0)

            for row in range(self.row_len):
                for pix in range(self.col_len):
                    if self.color_matrix[row][pix] == color:
                        tmp_cordinates.append((row, pix))
                        tmp_binary[row][pix] = 255

            segregated[color] = tmp_cordinates
            segregated_binary[color] = tmp_binary

        return segregated, segregated_binary # dict

    def find_connected_components(self):
        self.number_of_labels = 0
        self.labels = [1]
        self.same_label = {}

        for color in self.color_list:
            for row in range(self.row_len):
                for pix in range(self.col_len):
                    if self.color_matrix[row][pix] != "w":
                        self.check_adjacent_pixels(row, pix)

    def check_adjacent_pixels(self, row, pix):
        connected = False
        lock = False

        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if self.label_plane[row + i][pix + j] != 0.:
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