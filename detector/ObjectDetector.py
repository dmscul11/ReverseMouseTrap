import cv2 as cv
import numpy as np

class ObjectDetector:
    labels = [1]
    objects = []

    def __init__(self, image, binary_image):
        self.image = image
        self.binary_image = binary_image

        self.label_plane = np.zeros(shape=(len(image), len(image[0])))

        self.scan_image()

        for row in self.label_plane:
            for pix in range(len(row)):
                print(row[pix], end="\t")
            print()

    def scan_image(self):
        for row in range(len(self.image)):
            row_len = len(self.image[row])

            for pix in range(row_len):
                if self.binary_image[row][pix] != 255:
                    self.check_adjacent_area(row, pix)

    def check_adjacent_area(self, row, pix):
        connected = False
        try:
            for i in range(-1, 3):
                for j in range(-1, 3):
                    if self.label_plane[row + i][pix + j] != 0.:
                        connected = True
                        label = self.label_plane[row + i][pix + j]
                        self.label_plane[row][pix] = label

            if connected is False:
                if len(self.labels) == 1:
                    label = 1
                    self.labels.append(label)
                else:
                    label = self.labels[len(self.labels) - 1] + 1
                    self.labels.append(label)

                self.label_plane[row][pix] = label
        except:
            # Exception when pixel at the boundary
            return False



