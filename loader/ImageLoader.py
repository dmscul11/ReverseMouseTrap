import os
import path
from enum import Enum

import numpy as np
import cv2 as cv

import matplotlib.pyplot as plt

class Difficulty(Enum):
    EASY = os.path.join(path.Path.getcwd().parent, 'images', 'Easy.png')
    MEDIUM = os.path.join(path.Path.getcwd().parent, "images", "Medium.png")
    HARD = os.path.join(path.Path.getcwd().parent, "images", "Hard.png")

def load_image(Difficulty):
    """
    Blue [255. 0. 0.]
    Yellow [255. 255. 0.]
    Green [0. 128. 0.]

    Black [0. 0. 0.]
    White [255. 255. 255.]

    Red discarded

    in BGR color space.

    :param Difficulty: Enum for images path
    :return: original_image, new_image(color matched), integer_image(experimental)
    """
    original_image = np.array(cv.imread(Difficulty.value, cv.IMREAD_LOAD_GDAL))

    new_image, integer_image = aggregate_colors(original_image)

    return original_image, new_image, integer_image

def aggregate_colors(image):
    """

    :param image: image in numpy array
    :return: new_image, integer_image(experimental)
    """
    new_img = np.zeros(shape=image.shape)
    integer_img = np.zeros(shape=image.shape)

    for row in range(len(image)):
        row_len = len(image[row])
        for pix in range(row_len):
            r = image[row][pix][2]
            g = image[row][pix][1]
            b = image[row][pix][0]

            # Black boost
            if r < 5 and g < 5 and b < 5:
                new_img[row][pix] = np.array([0., 0., 0., 0.])
                integer_img[row][pix] = 4
            # White boost
            elif r > 250 and g > 250 and b > 250:
                new_img[row][pix] = np.array([255., 255., 255., 0.])
                integer_img[row][pix] = 0

            # Blue designation
            elif r + 10 < b and g + 10 < b:
                new_img[row][pix] = np.array([255., 0., 0., 0.])
                integer_img[row][pix] = 1

            # Green designation
            elif r + 10 < g and b + 10 < g:
                if g > 200 and r > 200:
                    new_img[row][pix] = np.array([0., 255., 255., 0.])
                else:
                    new_img[row][pix] = np.array([0., 128., 0., 0.])
                    integer_img[row][pix] = 2

            elif g + 10 < r and b + 10 < r:
                # Yellow designation
                if g > 100 and r > 100:
                    new_img[row][pix] = np.array([0., 255., 255., 0.])
                # Red designation convert red to white
                else:
                    new_img[row][pix] = np.array([255., 255., 255., 0.])
                    integer_img[row][pix] = 3
            else:
                new_img[row][pix] = np.array([255., 255., 255., 0.])
                integer_img[row][pix] = 0

    return new_img, integer_img


def show_image(Difficulty):
    original_image, new_image, integer_image = load_image(Difficulty)
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', new_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def show_image(image):
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()