from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
from world.World import World
import cv2 as cv

if __name__ == "__main__":
    original, new, binary, color_matrix = load_image(Difficulty.TEST_SMALL_2)

    detector = ObjectDetector(new, binary, color_matrix)
    detector.scan_image()
    objects = detector.get_objects()

    show_image(new)

    world = World(objects=objects, original_image=original, aggregated_image=new, binary_image=binary,
                  color_matrix=color_matrix)

    while world.terminated is not True:
        world.simulate()



