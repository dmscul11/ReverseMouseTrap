from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
from detector.NewObjectDetector import NewObjectDetector
from world.World import World
import cv2 as cv
import sys

if __name__ == "__main__":
    original, new, binary, color_matrix = load_image(Difficulty.TEST_SMALL_2)

    detector = NewObjectDetector(new, binary, color_matrix)
    detector.scan_image()

    objects = detector.get_objects()
    # detector.print_label_plane()

    world = World(objects=objects, original_image=original, aggregated_image=new, binary_image=binary,
                  color_matrix=color_matrix, object_detector=detector)

    while world.terminated is not True:
        world.simulate()



