
class Object:
    def __init__(self, object_id):
        self.object_id = object_id
        self.coordinates = []
        # by default
        self.color = "w"

    def set_color(self, color):
        self.color = color

    def insert_coordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def get_coordinates(self):
        return self.coordinates

    def get_color(self):
        return self.color