from movements.Falling import *

class Reasoner:
    def __init__(self):
        pass

    def check_stability_of_all_objects(self, object_detector, objects):
        unstable_objects = []
        centeroids = []

        for cluster_id in objects.keys():
            stability = check_instability(obj_detector=object_detector, cluster_id=cluster_id)
            if stability == False: # Stable
                pass
            elif stability == -1: # Unstable
                unstable_objects.append(cluster_id)
            elif stability == -1:
                pass
            else:
                # Centeroid
                centeroids.append((cluster_id, stability))

        return unstable_objects, centeroids

    def check_free_movement(self, object_detector, objects):
        for cluster_id in objects.keys():
            new_object_detector, affected_neighbors = free_movement(object_detector, cluster_id)
            print(new_object_detector, " ", affected_neighbors)