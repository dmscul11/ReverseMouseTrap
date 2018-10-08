from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector
from movements.Movements import *

original, new, binary, color_matrix = load_image(Difficulty.EASY)

obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()

objects = obj_detector.get_objects()

object_to_move = objects[1]

move_object_right(object_to_move)




