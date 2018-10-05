from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector

import matplotlib.pyplot as plt

original, new, binary, color_matrix = load_image(Difficulty.HARD)

obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
obj_detector.print_label_plane()

objects = obj_detector.get_objects()
coord = objects[2].get_coordinates()

show_image(binary)

for c in coord:
    plt.scatter(c[0], c[1])

plt.show()

print(coord)
print(objects[1].get_color())

