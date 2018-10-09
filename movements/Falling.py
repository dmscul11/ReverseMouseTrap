from detector.ObjectDetector import ObjectDetector
from loader.ImageLoader import *
import operator
import copy


def get_centroid(obj_detector, cluster_id):
    # Given obj_detector and the cluster ID desired, returns centroid

    object_coordinates = obj_detector.get_objects()[cluster_id].coordinates

    x_sum = 0.0
    y_sum = 0.0
    count = 0
    for pixel in object_coordinates:
        x_sum += pixel[0]
        y_sum += pixel[1]
        count += 1

    return round(x_sum / count), round(y_sum / count)


def get_base(obj_detector, cluster_id):
    # Given obj_detector and the cluster ID desired, returns pixels at base of object

    label_plane = obj_detector.get_label_plane()
    object_coordinates = obj_detector.get_objects()[cluster_id].coordinates

    base = []
    for pixel in object_coordinates:
        try:
            if label_plane[pixel[0] + 1][pixel[1]] != cluster_id:
                base.append(pixel)
        except:
            # if bottom edge of label_plane was reached
            base.append(pixel)

    base.sort(key=operator.itemgetter(1))

    return base


def check_instability(obj_detector, cluster_id):
    # Given obj_detector and the cluster ID desired, returns True if object will fall. If it will not fall, it returns
    # point about which the object should pivot or '0' denoting free fall

    if obj_detector.get_objects()[cluster_id].color == "d":
         return False

    label_plane = obj_detector.get_label_plane()
    centroid = get_centroid(obj_detector, cluster_id)
    base = get_base(obj_detector, cluster_id)

    print(base)

    invalid_support = [0, cluster_id]
    left_supported = False
    left_support = base[0]
    right_supported = False
    right_support = base[0]
    # iterate across base
    for pixel in base:
        pixel_supported = False
        # checks if current bottom pixel has a different cluster beneath it
        try:
            if label_plane[pixel[0] + 1][pixel[1]] not in invalid_support or \
               label_plane[pixel[0] + 2][pixel[1]] not in invalid_support:
                pixel_supported = True
        except:
            pixel_supported = True

        if pixel_supported:
            # if center is supported, done
            if pixel[1] == centroid[1]:
                return False
            # else, are we before the center...
            if pixel[1] < centroid[1]:
                left_supported = True
                left_support = pixel
            # ... or are we beyond the center
            if pixel[1] > centroid[1]:
                if not right_support:
                    right_support = pixel
                right_supported = True
            # if both are supported, done
            if left_supported and right_supported:
                return False

    if not (left_supported or right_supported):
        return -1

    if right_support[1] - centroid[1] < centroid[1] - left_support[1]:
        return right_support

    return left_support


def check_neighbor(obj_detector, cluster_1_id, cluster_2_id):
    # Given obj_detector and the cluster IDs to compare, returns whether the objects are adjacent

    object_1_coordinates = obj_detector.get_objects()[cluster_1_id].coordinates
    object_2_coordinates = obj_detector.get_objects()[cluster_2_id].coordinates

    for pixel in object_1_coordinates:
        if any(pix in object_2_coordinates for pix in
               (tuple((pixel[0], pixel[1])), tuple((pixel[0] - 1, pixel[1])), tuple((pixel[0] + 1, pixel[1])),
                tuple((pixel[0], pixel[1] - 1)), tuple((pixel[0], pixel[1] + 1)), tuple((pixel[0] - 2, pixel[1])),
                tuple((pixel[0] + 2, pixel[1])), tuple((pixel[0], pixel[1] - 2)), tuple((pixel[0], pixel[1] + 2)))):
            return True

    return False


def get_neighbors(obj_detector, cluster_id):
    # Given obj_detector and a cluster ID, returns all neighboring clusters (if any)

    neighbors = []
    for cluster in obj_detector.get_objects():
        if check_neighbor(obj_detector, cluster_id, cluster):
            neighbors.append(cluster)

    return neighbors


def free_movement(obj_detector, cluster_id):
    # Given obj_detector and a cluster ID of a valid free blue object, advances its movement by one and returns

    new_obj_detector = copy.deepcopy(obj_detector)
    instability = check_instability(obj_detector, cluster_id)

    # either it is stable (do nothing)
    if not instability:
        return new_obj_detector, []

    new_coordinates = []
    affected_neighbors = get_neighbors(obj_detector, cluster_id)

    # or it is in free fall
    if instability == -1:
        for pixel in new_obj_detector.get_objects()[cluster_id].coordinates:
            new_coordinates.append(tuple((pixel[0] + 10, pixel[1])))

    # or it tips
    else:
        centroid = get_centroid(obj_detector, cluster_id)
        instability = check_instability(obj_detector, cluster_id)

        # tip right
        if centroid[1] > instability[1]:
            for pixel in new_obj_detector.get_objects()[cluster_id].coordinates:
                new_coordinates.append(tuple((pixel[0], pixel[1] + 1)))

        # tip left
        if centroid[1] < instability[1]:
            for pixel in new_obj_detector.get_objects()[cluster_id].coordinates:
                new_coordinates.append(tuple((pixel[0], pixel[1] - 1)))

    if get_neighbors(obj_detector, cluster_id) not in affected_neighbors:
        affected_neighbors.append(get_neighbors(obj_detector, cluster_id))

    setattr(new_obj_detector.get_objects()[cluster_id], "coordinates", new_coordinates)

    return new_obj_detector, affected_neighbors
