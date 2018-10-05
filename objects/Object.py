
class Object:
    coordinates = []
    # by default
    color = "w"

    def __init__(self, object_id):
        self.object_id = object_id
        pass

    def set_color(self, color):
        self.color = color

    def insert_coordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def get_coordinates(self):
        return self.coordinates

    def get_color(self):
        return self.color