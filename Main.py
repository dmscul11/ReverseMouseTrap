from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
import cv2 as cv
import numpy as np

original, new, binary, color_matrix = load_image(Difficulty.MEDIUM)
print(original.shape)
print(new.shape)
print(binary.shape)
print(color_matrix.shape)
print(np.unique(new))
print(np.unique(color_matrix))

obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
objects = obj_detector.get_objects()

print(type(objects))
for o in objects:
    print('\n' + str(o) + ':')
    print(len(objects[o].get_coordinates()))
    print(objects[o].get_color())
