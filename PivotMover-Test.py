from loader.ImageLoader import *
from detector.NewObjectDetector import NewObjectDetector
from movements.StringMover import *
from movements.Pivoting import *
import cv2 as cv
import numpy as np


# read in image
original, new, binary, color_matrix = load_image(Difficulty.TEST)
print(np.unique(color_matrix.astype('U13')))

# detect objects
obj_detector = NewObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
objects = obj_detector.get_objects()

# get pivot lever 14, (15) and pivot 17
# move pivot random times
for i in range(10):
    new_image, new_lever, new_center = rotate_pivot(obj_detector, new, 4, 5, 'counterclockwise')
    new = np.array(new_image)
    obj_detector.get_objects()[4].coordinates = list(new_lever)
    obj_detector.get_objects()[5].coordinates = list(new_center)
show_image(new)