from loader.ImageLoader import *
from detector.ObjectDetector import ObjectDetector

import matplotlib.pyplot as plt

original, new, binary, color_matrix = load_image(Difficulty.EASY)

obj_detector = ObjectDetector(new, binary, color_matrix)
obj_detector.scan_image()
obj_detector.print_label_plane()

objects = obj_detector.get_objects()
coords = []
for idx in range(1, len(objects)):
    coords.append(objects[idx].get_coordinates())

show_image(new)

for c in coords:
    for pix in c:
        plt.scatter(x=pix[0], y=pix[1], color='b')

plt.show()

print(objects[1].get_color())

