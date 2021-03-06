from objects.Object import Object
import math


def check_neighborhood(obj, label_plane):
    coordinates = obj.get_coordinates()
    object_id = obj.object_id
    internal_neighbors = []
    external_neighbors = []

    boundaries = []
    for coord in coordinates:
        neighbor = see_4_label_plane(coord[0], coord[1], label_plane)  # x, y representation

        # if this list contains a 0, it is an external boundary
        if 0 in neighbor:
            for n in neighbor:
                if (n != object_id) and (n != 0) and (n not in external_neighbors):
                    external_neighbors.append(n)
                    obj.point_of_impact = coord
                    
            # Boundary detection
            # Boundary detection it can provide some boundary not all
            boundaries.append((coord[0], coord[1]))
        else:
            # This gotta be the internal neighbor
            for n in neighbor:
                if n != object_id and (n not in internal_neighbors):
                    internal_neighbors.append(n)

    obj.internal_neighbors = internal_neighbors
    obj.external_neighbors = external_neighbors
    obj.boundaries = boundaries
    # Base Detection. Only look at the last element # Or Boundaries?
    bottom_countered = False
    for bound in boundaries:
        # See neighbor returns ids of surrounding objects in clockwise ordering
        # Upper object will be shown in the north direction
        neighbor = see_4_label_plane(bound[0], bound[1], label_plane)
        #North
        n = neighbor[0]
        #East
        e = neighbor[1]
        #South
        s = neighbor[2]
        #West
        w = neighbor[3]

        if n != 0 and n != object_id:
            obj.upper_object = n
            obj.point_of_impact = bound
        if s != 0 and s != object_id:
            obj.bottom_object = s
            bottom_countered = True
            obj.unstable = False
            obj.point_of_impact = bound

        if bottom_countered == False:
            obj.unstable = True

    obj.internal_neighbors = internal_neighbors
    obj.external_neighbors = external_neighbors
    obj.boundaries = boundaries

    # Internal & External Neighbors are mixed
    return internal_neighbors, external_neighbors

def check_pixel_occupation(object):
    object.pixel_occupation = len(object.coordinates)

    return True

def check_centroid(object):
    if object.pixel_occupation < 2:
        object.centroid = object.get_coordinates()[0]
    else:
        list_len = len(object.get_coordinates())

        # Simplified method
        middle = math.floor(list_len / 2)
        object.centroid = object.get_coordinates()[middle]

    return True

def detect_pivot(object):
    from world.World import World
    # Look for yellow
    objects = World.get_instance().objects_dict
    if object.get_color() is "b":
        id = object.object_id
        internal_neighbors = object.internal_neighbors
        for n in internal_neighbors:
            # print(n)
            if objects[n].color == "y":
                object.pivoted = True
                object.pivoted_by = n

    return True

def see_4_label_plane(row, col, label_plane):
    try:
        north = label_plane[row - 1][col]
    except:
        north = 0
    try:
        south = label_plane[row + 1][col]
    except:
        south = 0
    try:
        west = label_plane[row][col - 1]
    except:
        west = 0
    try:
        east = label_plane[row][col + 1]
    except:
        east = 0

    # What label that is is [north east south west] clockwise
    neighbor = [north, east, south, west]

    return neighbor

def see_8_label_plane(x, y, label_plane):
    # Not implemented
    for row in range(x - 1, x + 2):
        for pix in range(y -1, y + 2):
            pass
