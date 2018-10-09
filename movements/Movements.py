def move_object_right(object):
    for idx in range(len(object.coordinates)):
        x = object.coordinates[idx][0]
        y = object.coordinates[idx][1] + 1

        object.coordinates.remove((x, y - 1))
        object.coordinates.insert(idx, (x, y))

def move_object_left(object):
    for idx in range(len(object.coordinates)):
        x = object.coordinates[idx][0]
        y = object.coordinates[idx][1] - 1

        object.coordinates.remove((x, y + 1))
        object.coordinates.insert(idx, (x, y))

def move_object_up(object):
    for idx in range(len(object.coordinates)):
        x = object.coordinates[idx][0] - 1
        y = object.coordinates[idx][1]

        object.coordinates.remove((x + 1, y))
        object.coordinates.insert(idx, (x, y))

def move_object_down(object):
    for idx in range(len(object.coordinates)):
        x = object.coordinates[idx][0] + 1
        y = object.coordinates[idx][1]

        object.coordinates.remove((x - 1, y))
        object.coordinates.insert(idx, (x, y))