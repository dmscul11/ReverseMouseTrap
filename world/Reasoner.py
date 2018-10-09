from movements.Falling import check_instability

class Reasoner:
    def __init__(self):
        pass

    def check_stability_of_all_objects(self, object_detector, objects):
        unstable_objects = []
        centeroids = []

        for cluster_id in objects.keys():
            stability = check_instability(obj_detector=object_detector, cluster_id=cluster_id)
            print(stability)
            if stability == False: # Stable
                pass
            elif stability == True: # Unstable
                unstable_objects.append(cluster_id)
            elif stability == -1:
                pass
            else:
                # Centeroid
                centeroids.append((cluster_id, stability))

        return unstable_objects, centeroids