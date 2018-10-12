

def will_fall(object):
    if object.color == "b" and object.pivoted == False and len(object.external_neighbors) == 0:
        # Then it can fall.
        # object.print_properties()
        return True
    else:
        return False

def will_tip(object):
    from world.World import World
    if object.color == "b" and object.pivoted == False and len(object.external_neighbors) > 0:
        # Determine a direction of tipping
        # Compare centeroid coordinates' slope
        for target in object.external_neighbors:
            calculate_centroid_slope(object, World.get_instance().objects_dict[target])

        return True
    else:
        return False

def calculate_centroid_slope(object_1, object_2):
    obj_1_centeroid = object_1.centeroid
    obj_2_centeroid = object_2.centeroid
    try:
        slope = (obj_2_centeroid[0] - obj_1_centeroid[0]) / (obj_2_centeroid[1] - obj_1_centeroid[1])
        print(slope)
    except:
        pass