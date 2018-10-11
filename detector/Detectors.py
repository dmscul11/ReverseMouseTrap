from objects.Object import Object

def boundary_detector(object, label_plane):
    pass

def check_neighborhood(object, label_plane):
    coordinates = object.get_coordinates()
    object_id = object.object_id
    internal_neighbors = []
    external_neighbors = []

    boundaries = []

    for coord in coordinates:
        neighbor = see_4_label_plane(coord[0], coord[1], label_plane) # x, y represenation
        # if this list contains a 0, it is an external boundary
        if 0 in neighbor:
            for n in neighbor:
                if (n != object_id) and (n != 0) and (n not in external_neighbors):
                    external_neighbors.append(n)

            boundaries.append((coord[0], coord[1]))
        else:
            # This gotta be the internal neighbor
            # Fo
            for n in neighbor:
                if n != object_id and (n not in internal_neighbors):
                    internal_neighbors.append(n)

    object.internal_neighbors = internal_neighbors
    object.external_neighbors = external_neighbors
    object.boundaries = boundaries

    # Internal & External Neighbors are mixed
    return internal_neighbors, external_neighbors

def see_4_label_plane(x, y, label_plane):
    try:
        north = label_plane[x][y - 1]
    except:
        north = 0
    try:
        south = label_plane[x][y + 1]
    except:
        south = 0
    try:
        west = label_plane[x - 1][y]
    except:
        west = 0
    try:
        east = label_plane[x + 1][y]
    except:
        east = 0
    # What label that is is [north east south west] clockwise
    neighbor = [north, east, south, west]

    return neighbor

def see_8_label_plane(x, y, label_plane):
    for row in range(x - 1, x + 2):
        for pix in range(y -1, y + 2):
            pass