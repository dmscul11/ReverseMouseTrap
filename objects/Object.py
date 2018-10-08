class Object:
    def __init__(self, object_id):
        self.object_id = object_id

        # Coordinates of all pixels an object currently occupying
        self.coordinates = []
        self.boudaries = []

        # by default
        self.color = "w"

        # An object with collision_lock set to True cannot move further
        self.collision_lock = False

    def set_color(self, color):
        self.color = color

    def insert_coordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def get_coordinates(self):
        return self.coordinates

    def get_color(self):
        return self.color