from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
import cv2 as cv

if __name__ == "__main__":
    original, new, binary, color_matrix = load_image(Difficulty.TEST_SMALL_2)

    detector = ObjectDetector(new, binary, color_matrix)
    detector.scan_image()
    objects = detector.get_objects()

    terminated = False
    while terminated is not True:
        pass



