from threading import Thread

class Object:
    def __init__(self, object_id):
        self.object_id = object_id

        # Coordinates of all pixels an object currently occupying
        self.coordinates = []
        self.boundaries = []
        self.internal_neighbors = []
        self.external_neighbors = []
        self.centeroid = None

        self.pixel_occupation = 0

        # by default
        self.color = "w"

        # An object with collision_lock set to True cannot move further
        self.collision_lock = False
        self.unstable = False
        self.pivoted = False
        self.string_attached = False

        self.pivoted_by = 0
        self.front_end = []
        self.back_end = []
        self.width = 0
        #
        self.upper_object = None
        self.bottom_object = None
        self.point_of_impact = None

    def object_post_processing(self):
        self.size = len(self.coordinates)

    def set_color(self, color):
        self.color = color

    def insert_coordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def get_coordinates(self):
        return self.coordinates

    def get_color(self):
        return self.color

    def get_size(self):
        return self.size

    def print_properties(self):
        print(" ======================================== ")
        print("Object ID : ", self.object_id, "  Color : ", self.color, "  Pivoted : ", self.pivoted, "  Pivoted by : ", self.pivoted_by, "  String Attached : ", self.string_attached)
        print("Front end : ", self.front_end, "  Back end : ", self.back_end, "  Unstable : ", self.unstable, "  pixel occupation : ", self.pixel_occupation)
        print("Center Coordinate : ", self.centeroid, "  Internal Neighbors : ", self.internal_neighbors, "  External Neighbors : ", self.external_neighbors)
        print("Point of Impact: ", self.point_of_impact)