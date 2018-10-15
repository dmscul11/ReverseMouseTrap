
def will_fall(object):
    if object.color == "b" and object.pivoted == False and object.unstable == True:
        # Then it can fall.
        # object.print_properties()
        return True
    else:
        return False

def will_tip(object):
    from world.World import World
    if object.color == "b" and object.pivoted == False and object.unstable == False and object.point_of_impact != None:
        # Determine a direction of tipping
        slope = calculate_slope(object.centeroid, object.point_of_impact)
        if slope > -0.2 and slope < 0.2: # / like this. might tip left
            # Assume stable
            return False
        elif slope >= 0.2:
            return (True, "right")
        elif slope <= -0.2:
            return (True, "left")

def will_tilt(object):
    from world.World import World
    if object.pivoted:
        # Determine a direction of tilting
        for neighbor in object.external_neighbors:
            poi = object.point_of_impact
            center = object.centeroid

            if poi[1] > center[1]:
                return (True, "clockwise")
            elif poi[1] < center[1]:
                return (True, "counterclockwise")

def calculate_centroid_slope(object_1, object_2):
    obj_1_centeroid = object_1.centeroid
    obj_2_centeroid = object_2.centeroid
    try:
        slope = (obj_2_centeroid[0] - obj_1_centeroid[0]) / (obj_2_centeroid[1] - obj_1_centeroid[1])
    except:
        pass


def calculate_slope(point_1, point_2):
    try:
        slope = (point_1[1] - point_2[1]) / (point_2[0] - point_1[0])
        return slope
    except:
        return 0