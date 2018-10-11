from detector.ObjectDetector import ObjectDetector
from loader.ImageLoader import *
from movements.Falling import get_neighbors

def detect_pivot(object_detector):
    objects = object_detector.get_objects()

    for obj in objects.values():
        print(obj)
        # Look for yellow
        if obj.get_color() is "b":
            id = obj.object_id
            neighbors = get_neighbors(object_detector, obj.object_id)
            for n in neighbors:
                if objects[n].get_color() == "y":
                    # If there is an object nearby that is yellow
                    object_detector.get_objects()[id].pivoted = True
                    object_detector.get_objects()[id].pivoted_by = n
                if objects[n].get_color() == "g":
                    object_detector.get_objects()[id].string_attached = True
