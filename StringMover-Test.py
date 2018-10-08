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

# get string coords (Since not found in objects)
idx = np.nonzero(color_matrix.astype('U13') == 'g')
string_coords = []
for i, e in enumerate(idx[0]):
    string_coords.append((idx[0][i], idx[1][i]))

# find ends of string and width done once per string
edges, front_end, back_end = get_string_ends(string_coords, color_matrix)
width = get_string_width(edges)

# move string a certain number of times because a certain object moved
# set to move string up 50 iterations
pull_end = end_check(objects[1], string_coords, front_end, back_end)
for i in range(50):
    image, new_string, new_front_end, new_back_end = pull_string(new, string_coords, pull_end, front_end, 'up', back_end, width)
    new = np.array(image)
    string_coords = list(new_string)
    front_end = list(new_front_end)
    back_end = list(new_back_end)
show_image(image)


# test plotting for edge finding
stoping
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
