import os

from detector.ObjectDetector import *
from detector.Detectors import *
from movements.Pivoting import *
from detector.PivotDetector import detect_pivot

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
    img_difficulty = Difficulty.MEDIUM
    original, new, binary, color_matrix = load_image(img_difficulty)

    detector = ObjectDetector(new, binary, color_matrix)
    detector.scan_image()

    objects = detector.get_objects_array()
    objects_dict = detector.get_objects()

    label_plane = detector.get_label_plane()

    update_objects(objects, label_plane)

    for object in objects_dict.values():
        print("Internal Neighbor : ", object.internal_neighbors)
        print("External Neighbor : ", object.external_neighbors)

    # detect_pivot(detector)
    # detector.print_label_plane()

    """
    world = World(objects=objects, original_image=original, aggregated_image=new, binary_image=binary,
                  color_matrix=color_matrix, object_detector=detector)

    while world.terminated is not True:
        world.simulate()
    """

    # Make a video
    # create_movie(img_difficulty.name, len(original[0]), len(original))

