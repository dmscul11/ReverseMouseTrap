def move_object_right(object):
    for idx in range(len(object.coordinates)):
        x = object.coordinates[idx][0] + 2
        y = object.coordinates[idx][1] + 2

        coord = object.get_coordinates()
        coord.insert(idx, (x, y))