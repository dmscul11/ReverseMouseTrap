from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
from movements.StringMover import *
import cv2 as cv
import numpy as np


# read in image
original, new, binary, color_matrix = load_image(Difficulty.EASY)
print(np.unique(color_matrix.astype('U13')))

# detect objects
obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
objects = obj_detector.get_objects()

# move pivot
show_image(new)


# test plotting for edge finding
breaking
for e in front_end:
    new[e[0], e[1], :] = [0., 0., 0.]
    new[e[0]+1, e[1], :] = [0., 0., 0.]
    new[e[0]-1, e[1], :] = [0., 0., 0.]
    new[e[0], e[1]+1, :] = [0., 0., 0.]
    new[e[0], e[1]-1, :] = [0., 0., 0.]
    new[e[0]+1, e[1]+1, :] = [0., 0., 0.]
    new[e[0]+1, e[1]-1, :] = [0., 0., 0.]
    new[e[0]-1, e[1]-1, :] = [0., 0., 0.]
    new[e[0]-1, e[1]+1, :] = [0., 0., 0.]
    new[e[0]+2, e[1], :] = [0., 0., 0.]
    new[e[0]-2, e[1], :] = [0., 0., 0.]
    new[e[0], e[1]+2, :] = [0., 0., 0.]
    new[e[0], e[1]-2,:] = [0., 0., 0.]
    new[e[0]+2, e[1]+2, :] = [0., 0., 0.]
    new[e[0]+2, e[1]-2, :] = [0., 0., 0.]
    new[e[0]-2, e[1]-2, :] = [0., 0., 0.]
    new[e[0]-2, e[1]+2, :] = [0., 0., 0.]
show_image(new)
