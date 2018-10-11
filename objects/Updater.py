from detector.Detectors import *

from threading import Thread

def update_objects(objects_to_update, label_plane):
    # Divide
    object_threads = []
    if type(objects_to_update) == dict:
        for obj in objects_to_update.values():
            object_threads.append(ObjectUpdater(obj, label_plane))
    elif type(objects_to_update) == list:
        for obj in objects_to_update:
            object_threads.append(ObjectUpdater(obj, label_plane))

    for t in object_threads:
        t.start()

class ObjectUpdater(Thread):
    def __init__(self, object, label_plane):
        Thread.__init__(self)
        self.object = object
        self.label_plane = label_plane # Will make this a system-wide global variable or a singleton class

    def run(self):
        check_neighborhood(self.object, self.label_plane)