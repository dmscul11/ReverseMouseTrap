import numpy as np
import cv2 as cv
import math
import matplotlib.pyplot as plt
from collections import Counter
from movements.Falling import *


def rotate_pivot(lever, direction):
    lever_coords = lever.get_coordinates()
    center_pixel = lever.centeroid
    new_lever = []

    if direction == "counterclockwise":
        for p in lever_coords:
            # move pixels down left
            if (p[1] < center_pixel[1]) and (p[1] != 0):
                new_lever.append((p[0] + 1, p[1] - 1))

            # move pixels up right
            elif (p[1] > center_pixel[1]) and (p[0] != 0):
                new_lever.append((p[0] - 1, p[1] + 1))

    elif direction == "clockwise":
        for p in lever_coords:
            # move pixels down left
            if (p[0] < center_pixel[0]):
                new_lever.append((p[0] - 1, p[1] - 1))

            # move pixels up right
            elif p[0] > center_pixel[0]:
                new_lever.append((p[0] + 1, p[1] + 1))

    return new_lever