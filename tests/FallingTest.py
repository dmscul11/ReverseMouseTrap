from movements.Falling import *

original, new, binary, color_matrix = load_image(Difficulty.TEST_SMALL_2)

obj_detector = NewObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()

clustered = obj_detector.get_objects()

print(check_instability(obj_detector, 1))
