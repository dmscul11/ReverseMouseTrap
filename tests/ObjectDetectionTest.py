from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector

original, new, binary, color_matrix = load_image(Difficulty.TEST_SMALL_2)

obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
obj_detector.print_label_plane()

objects = obj_detector.get_objects()
coord = objects[1].get_coordinates()
print(coord)
print(objects[1].get_color())

