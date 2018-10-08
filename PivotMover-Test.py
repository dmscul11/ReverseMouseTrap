from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
from movements.StringMover import *
from movements.Pivoting import *
import cv2 as cv
import numpy as np


# read in image
original, new, binary, color_matrix = load_image(Difficulty.EASY)
print(np.unique(color_matrix.astype('U13')))

# detect objects
obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
objects = obj_detector.get_objects()

# get pivot lever 14, (15) and pivot 17
# move pivot random times
for i in range(10):
    new_image, new_lever, new_center = rotate_pivot(obj_detector, new, 14, 17, 'counterclockwise')
    new = np.array(new_image)
    obj_detector.get_objects()[14].coordinates = list(new_lever)
    obj_detector.get_objects()[17].coordinates = list(new_center)
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
