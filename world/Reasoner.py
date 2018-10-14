
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
        if slope > -0.5 and slope < 0.5: # / like this. might tip left
            # Assume stable
            return False
        elif slope >= 0.5:
            return (True, "right")
        elif slope <= -0.5:
            return (True, "left")


def calculate_centroid_slope(object_1, object_2):
    obj_1_centeroid = object_1.centeroid
    obj_2_centeroid = object_2.centeroid
    try:
        slope = (obj_2_centeroid[0] - obj_1_centeroid[0]) / (obj_2_centeroid[1] - obj_1_centeroid[1])
    except:
        pass

def calculate_slope(point_1, point_2):
    try:
        slope = (point_1[1] - point_2[1]) / (point_1[0] - point_2[0])
        slope = abs(slope)
        print(slope)
        return slope
    except:
        pass