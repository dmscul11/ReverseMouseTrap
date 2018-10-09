import numpy as np
import cv2 as cv
import math
import matplotlib.pyplot as plt
from collections import Counter
from movements.Falling import *


def rotate_pivot(obj_detector, image, lever, pivot_center, direction):

    # passes objects detector
    objects = obj_detector.get_objects()
    lever_coords = objects[lever].get_coordinates()
    center_coords = objects[pivot_center].get_coordinates()
    center_pixel = get_centroid(obj_detector, pivot_center)

    new_lever = []
    if direction == "counterclockwise":
        for p in lever_coords:

            # move pixels down left
            if (p[1] < center_pixel[1]) and (p[1] != 0) and (p[0] < image.shape[0]):
                new_lever.append((p[0] + 1, p[1] - 1))

            # move pixels up right
            elif (p[1] > center_pixel[1]) and (p[0] != 0) and (p[1] < image.shape[1]):
                new_lever.append((p[0] - 1, p[1] + 1))

    elif direction == "clockwise":
        for p in lever_coords:

            # move pixels down left
            if (p[1] < center_pixel[1]) and (p[0] != 0) and (p[1] != 1):
                new_lever.append((p[0] - 1, p[1] - 1))

            # move pixels up right
            elif p[1] > center_pixel[1] and (p[0] < image.shape[0]) and (p[1] < image.shape[1]):
                new_lever.append((p[0] + 1, p[1] + 1))

    # remove old pixels then add new ones to image, read yellow to image
    for p in lever_coords:
        image[p[0], p[1], :] = [255., 255., 255.]
    new_lever = list(set(new_lever))
    for p in new_lever:
        image[p[0], p[1], :] = [255., 0., 0.]
    for p in center_coords:
        image[p[0], p[1], :] = [0., 255., 255.]

    new_center = list(center_coords)

    return image, new_lever, new_center
