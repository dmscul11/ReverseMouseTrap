def move_object_right(object):
    for idx in range(len(object.coordinates)):
        object.coordinates[idx] = (object.coordinates[idx][0] + 1, object.coordinates[idx][0] + 1)