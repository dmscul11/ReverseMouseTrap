import numpy as np
import cv2 as cv
from objects.Colors import Colors
from objects.Object import Object
from loader.ImageLoader import show_image
from loader.Operations import reconstruct_image
from loader.Operations import reconstruct_single_object

class NewObjectDetector:
    def __init__(self, aggregated_image, binary_image, color_matrix):
        self.aggregated_image = aggregated_image
        self.binary_image = binary_image
        self.color_matrix = color_matrix

        self.objects_array = []
        self.objects = {}
        self.objects_by_color = {}

        self.row_len = len(self.aggregated_image)
        self.col_len = len(self.aggregated_image[0])

        self.color_list = ["d", "b", "g", "y"]

        self.label_plane = np.full(shape=(self.row_len, self.col_len), fill_value=0)

    def scan_image(self):
        self.color_segregated, self.segregated_binary = self.segregate_by_color()
        # self.drop_small_objects()
        self.find_connected_components()

        print("Identified ", len(self.objects_array), "objects")
        """
        print("Blue : ", len(self.objects_by_color["b"]))
        print("Black : ", len(self.objects_by_color["d"]))
        print("Yellow : ", len(self.objects_by_color["y"]))
        print("Green : ", len(self.objects_by_color["g"]))
        """

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
        self.label_counter = 1

        # First pass
        for color in self.color_list:
            binary = self.segregated_binary[color]
            cv.imwrite("./tmp_" + color + ".PNG", binary)
            image = cv.imread("./tmp_" + color + ".PNG", cv.CV_8UC1)
            self.cv_find(image, color)

    def cv_find(self, image, color):
        ret, thresh = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        # You need to choose 4 or 8 for connectivity type
        connectivity = 4
        # Perform the operation
        output = cv.connectedComponentsWithStats(thresh, connectivity, cv.CV_32S)
        # Get the results
        # The first cell is the number of labels
        num_labels = output[0]
        # The second cell is the label matrix
        labels = output[1]
        # The third cell is the stat matrix
        stats = output[2]
        # The fourth cell is the centroid matrix
        centroids = output[3]

        self.gather_coordinates(labels, num_labels, color)

    def gather_coordinates(self, labels, num_labels, color):
        for l in range(1, num_labels):
            tmp_array = []
            for row in range(len(labels)):
                for pix in range(len(labels[0])):
                    if labels[row][pix] == l:
                        tmp_array.append((row, pix))
                        self.label_plane[row][pix] = self.label_counter

            obj = Object(self.label_counter)
            obj.coordinates = tmp_array
            obj.set_color(color)

            self.objects[self.label_counter] = obj
            self.objects_array.append(obj)

            self.label_counter += 1

    def drop_small_objects(self):
        print(self.color_segregated)
        print(self.segregated_binary)

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
        return self.objects

    def get_objects_array(self):
        return self.objects_array

    def get_label_plane(self):
        return self.label_plane