from objects.Object import Object
import math

def check_neighborhood(object, label_plane):
    from world.World import World
    coordinates = object.get_coordinates()
    object_id = object.object_id
    internal_neighbors = []
    external_neighbors = []

    boundaries = []

    pivot_found = False

    for coord in coordinates:
        neighbor = see_8_label_plane(coord[0], coord[1], label_plane) # x, y represenation
        # if this list contains a 0, it is an external boundary
        if 0 in neighbor:
            for n in neighbor:
                if (n != object_id) and (n != 0) and (n not in external_neighbors):
                    external_neighbors.append(n)
                    object.point_of_impact = coord

            # Boundary detection it can provide some boundary not all
            boundaries.append((coord[0], coord[1]))
        else:
            # This gotta be the internal neighbor
            for n in neighbor:
                if n != 0:
                    if (n != object_id) and (n not in internal_neighbors) and World.get_instance().objects_dict[n].color == ("y" or "g"):
                        internal_neighbors.append(n)

    object.internal_neighbors = internal_neighbors
    object.external_neighbors = external_neighbors

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
            object.upper_object = n
            object.point_of_impact = bound
        if s != 0 and s != object_id:
            object.bottom_object = s
            bottom_countered = True
            object.unstable = False
            object.point_of_impact = bound

        if bottom_countered == False:
            object.unstable = True

    object.boundaries = boundaries

def check_pixel_occupation(object):
    object.pixel_occupation = len(object.coordinates)
    return True

def check_centeroid(object):
    centeroid = None
    if object.pixel_occupation < 2:
        try:
            object.centeroid = object.get_coordinates()[0]
            centeroid = object.get_coordinates()[0]
            return centeroid
        except:
            object.centeroid = (0, 0)
            centeroid = (0, 0)
            return centeroid
    else:
        list_len = len(object.get_coordinates())

        # Simplified method
        middle = math.floor(list_len / 2)
        object.centeroid = object.get_coordinates()[middle]
        centeroid = object.centeroid
        return centeroid

def get_centroid(cluster_id):
    from world.World import World
    object_coordinates = World.get_instance().objects_dict[cluster_id].coordinates

    x_sum = 0.0
    y_sum = 0.0
    count = 0
    for pixel in object_coordinates:
        x_sum += pixel[0]
        y_sum += pixel[1]
        count += 1

    try:
        centeroid = (round(x_sum / count), round(y_sum / count))
    except:
        centeroid = check_centeroid(World.get_instance().objects_dict[cluster_id])

    World.get_instance().objects_dict[cluster_id].centeroid = centeroid

def detect_pivot(object):
    from world.World import World
    # Look for yellow
    objects = World.get_instance().objects_dict
    if object.get_color() is "b":
        internal_neighbors = object.internal_neighbors
        for n in internal_neighbors:
            if objects[n].color == "y":
                object.pivoted = True
                object.pivoted_by = n
        for n in object.external_neighbors:
            if objects[n].color == "g":
                object.string_attached = True

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
    neighbor = []
    for row in range(x - 1, x + 2):
        for pix in range(y -1, y + 2):
            try:
                neighbor.append(label_plane[row][pix])
            except:
                neighbor.append(0) # Image Boundary

    return neighbor

