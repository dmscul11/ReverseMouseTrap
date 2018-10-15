import os

from detector.ObjectDetector import *
from detector.Detectors import *
from movements.Pivoting import *

from objects.Updater import update_objects
from world.World import World
import cv2 as cv
import sys

def create_movie(image_name, frame_width, frame_height):
    # YEAH !!!
    movie_output_path = os.path.join(os.path.dirname(__file__), "MOVIE_OUTPUT")
    try:
        os.mkdir(movie_output_path)
    except:
        pass

    movie_name = os.path.join(movie_output_path, image_name + ".avi")
    vid = cv.VideoWriter(movie_name, -1, 30, (frame_width, frame_height))

    img_path = os.path.join(os.path.dirname(__file__), "world", "render_files")
    file_list = sorted(os.listdir(img_path))

    for f in file_list:
        img = cv.imread(os.path.join(img_path, f))
        vid.write(img)

    cv.destroyAllWindows()
    vid.release()

if __name__ == "__main__":
    img_difficulty = Difficulty.EASY
    original, new, binary, color_matrix = load_image(img_difficulty)

    detector = ObjectDetector(new, binary, color_matrix)
    detector.scan_image()

    # All we need to supply to the world
    objects = detector.get_objects_array()
    objects_dict = detector.get_objects()
    label_plane = detector.get_label_plane()

    # detector.print_label_plane()

    world = World.get_instance()
    world.create_world(objects=objects, objects_dict=objects_dict, label_plane=label_plane)

    # Discover properties of objects
    update_objects(world.objects, world.label_plane) # Internal update

    while world.terminated is not True:
        world.simulate()

    # Make a video
    create_movie(img_difficulty.name, len(original[0]), len(original))


