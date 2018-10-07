from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
from movements.StringMover import *
import cv2 as cv
import numpy as np

original, new, binary, color_matrix = load_image(Difficulty.MEDIUM)
print(original.shape)
print(new.shape)
print(binary.shape)
print(color_matrix.shape)
print(np.unique(new))
print(np.unique(color_matrix.astype('U13')))

obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
objects = obj_detector.get_objects()

# get string coords
idx = np.nonzero(color_matrix.astype('U13') == 'g')
string_coords = []
for i, e in enumerate(idx[0]):
    string_coords.append((idx[0][i], idx[1][i]))

# find ends of string
edges, front_end, back_end = get_string_ends(string_coords, color_matrix)
width = get_string_width(edges)
print(width)
for e in edges:
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
# show_image(new)
