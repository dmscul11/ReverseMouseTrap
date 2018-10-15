from detector.Detectors import *

import time
from threading import Thread

__update_counter = 0

def update_objects(objects_to_update, label_plane):
    # Divide
    global __update_counter

    object_threads = []
    if type(objects_to_update) == dict:
        for obj in objects_to_update.values():
            object_threads.append(ObjectUpdater(obj, label_plane))
    elif type(objects_to_update) == list:
        for obj in objects_to_update:
            object_threads.append(ObjectUpdater(obj, label_plane))

    for t in object_threads:
        t.start()

    # These methods needs interaction with other objects.
    # Running sequentially
    if __update_counter < 3:
        if type(objects_to_update) == dict:
            for obj in objects_to_update.values():
                detect_pivot(obj)
        elif type(objects_to_update) == list:
            for obj in objects_to_update:
                detect_pivot(obj)
        __update_counter += 1
    else:
        __update_counter += 1
        pass

class ObjectUpdater(Thread):
    def __init__(self, object, label_plane):
        Thread.__init__(self)
        self.object = object
        self.label_plane = label_plane # Will make this a system-wide global variable or a singleton class

    def run(self):
        check_neighborhood(self.object, self.label_plane)
        check_pixel_occupation(self.object)
        check_centeroid(self.object)