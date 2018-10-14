
def will_fall(obj):
    if obj.color == "b" and not obj.pivoted and len(obj.external_neighbors) == 0:
        # Then it can fall.
        # object.print_properties()
        return True
    else:
        return False


def will_tip(obj):
    from world.World import World
    if obj.color == "b" and not obj.pivoted and len(obj.external_neighbors) > 0:
        # Determine a direction of tipping
        # Compare centroid coordinates' slope
        for target in obj.external_neighbors:
            calculate_centroid_slope(obj, World.get_instance().objects_dict[target])
            
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
    obj_1_centroid = object_1.centroid
    obj_2_centroid = object_2.centroid
    try:
        slope = (obj_2_centeroid[0] - obj_1_centeroid[0]) / (obj_2_centeroid[1] - obj_1_centeroid[1])
    except:
        return 0
