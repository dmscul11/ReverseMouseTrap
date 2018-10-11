from threading import Thread
class Object:
    def __init__(self, object_id):
        self.object_id = object_id

        # Coordinates of all pixels an object currently occupying
        self.coordinates = []
        self.boundaries = []
        self.internal_neighbors = []
        self.external_neighbors = []
        self.centeroid = (0, 0)

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