from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
import cv2 as cv

original, new, binary, color_matrix = load_image(Difficulty.TEST_SMALL_2)

obj_detector = ObjectDetector(new, binary)