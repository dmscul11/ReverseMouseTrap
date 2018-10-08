from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
from detector.NewObjectDetector import NewObjectDetector
from world.World import World
import cv2 as cv


if __name__ == "__main__":
    original, new, binary, color_matrix = load_image(Difficulty.MEDIUM)

    # detector = ObjectDetector(new, binary, color_matrix)
    detector = NewObjectDetector(new, binary, color_matrix)
    detector.scan_image()
    objects = detector.get_objects()

    print_color_matrix(color_matrix)
    #detector.print_label_plane()

    show_image(new)

    world = World(objects=objects, original_image=original, aggregated_image=new, binary_image=binary,
                  color_matrix=color_matrix)

    while world.terminated is not True:
        world.simulate()



