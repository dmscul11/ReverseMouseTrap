import os
#import path
from enum import Enum

import numpy as np
import cv2 as cv

import matplotlib.pyplot as plt

class Difficulty(Enum):
    root_path = os.path.dirname(__file__)
    EASY = os.path.join(root_path, 'images', 'Easy.png')
    MEDIUM = os.path.join(root_path, "images", "Medium.png")
    HARD = os.path.join(root_path, "images", "Hard.png")
    TEST = os.path.join(root_path, "images", "Test.png")
    TEST_SMALL = os.path.join(root_path, "images", "Test_Small.png")
    TEST_SMALL_2 = os.path.join(root_path, "images", "Test_Small_2.png")

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
    :return: original_image, new_image(color matched), binary_image
    """
    print("Loading Image with difficulty : ", Difficulty.name)
    original_image = np.array(cv.imread(Difficulty.value))
    print("Image dimension : ", original_image.shape)

    new_image, binary_image, color_matrix = aggregate_colors(original_image)

    return original_image, new_image, binary_image, color_matrix

def second_load_image(image):
    original_image = image
    print("Image dimension : ", original_image.shape)

    new_image, binary_image, color_matrix = aggregate_colors(original_image)

    return original_image, new_image, binary_image, color_matrix

def aggregate_colors(image):
    """

    :param image: image in numpy array
    :return: new_image, integer_image(experimental)
    """
    new_img = np.zeros(shape=image.shape)
    binary_image = np.zeros(shape=(len(image), len(image[0])))

    # g, b(blue), y, w, d(black)
    color_matrix = np.zeros(shape=(len(image), len(image[0])), dtype=str)
    for row in range(len(image)):
        row_len = len(image[row])
        for pix in range(row_len):
            r = image[row][pix][2]
            g = image[row][pix][1]
            b = image[row][pix][0]

            # Black boost
            if r < 5 and g < 5 and b < 5:
                new_img[row][pix] = np.array([0., 0., 0.])
                color_matrix[row][pix] = "d"
            # White boost
            elif r > 250 and g > 250 and b > 250:
                new_img[row][pix] = np.array([255., 255., 255.])
                color_matrix[row][pix] = "w"

            # Blue designation
            elif r + 10 < b and g + 10 < b:
                new_img[row][pix] = np.array([255., 0., 0.])
                color_matrix[row][pix] = "b"

            # Green designation
            elif r + 10 < g and b + 10 < g:
                # Yellow
                if g > 200 and r > 200:
                    new_img[row][pix] = np.array([0., 255., 255.])
                    color_matrix[row][pix] = "y"
                # Green
                else:
                    new_img[row][pix] = np.array([0., 128., 0.])
                    color_matrix[row][pix] = "g"

            elif g + 10 < r and b + 10 < r:
                # Yellow designation
                if g > 100 and r > 100:
                    new_img[row][pix] = np.array([0., 255., 255.])
                    color_matrix[row][pix] = "y"
                # Red designation convert red to white
                else:
                    new_img[row][pix] = np.array([255., 255., 255.])
                    color_matrix[row][pix] = "w"
            else:
                new_img[row][pix] = np.array([255., 255., 255.])
                color_matrix[row][pix] = "w"

            # binary image
            if r > 240 and g > 240 and b > 240:
                binary_image[row][pix] = np.array(255)
            else:
                binary_image[row][pix] = np.array(0)

    return new_img, binary_image, color_matrix


def show_image(Difficulty):
    original_image, new_image, integer_image, color_matrix = load_image(Difficulty)
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', new_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def show_image(image):
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def print_color_matrix(color_matrix):
    for row in range(len(color_matrix)):
        for pix in range(len(color_matrix[0])):
            print(color_matrix[row][pix], end=" ")
        print()