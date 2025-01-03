import math
import numpy as np

class Coords():
    def __init__(self, size):
        self.max_lat = 43.096085  # Top left
        self.min_lat = 42.760639  # Bottom right
        self.min_long = -85.894024  # Top left
        self.max_long = -85.385939  # Bottom right
        self.size = size
        self.latlongs = []

    def fix_coords(self):
        # Applies min-max formula to each coord long/lat, multiplies by size for new matrix coords
        new_coord_arr = []
        for i in self.latlongs:
            new_coord = [0, 0]

            # Basic min/max
            new_coord[0] = math.floor((i[0] - self.min_lat) / (self.max_lat - self.min_lat) * self.size)
            new_coord[1] = math.floor((i[1] - self.min_long) / (self.max_long - self.min_long) * self.size)

            # if the point is between 0 and size
            if 0 <= new_coord[0] <= self.size and 0 <= new_coord[1] <= self.size:
                new_coord_arr.append(new_coord)

        # The lat/lon plane is a flip of the display plane, so call an alignment function and return the result
        aligned_matrix = self.align(new_coord_arr)
        return aligned_matrix

    def to_latlong(self, arr):
        # Does the opposite of the one above it
        latlong_arr = []

        for i in arr:
            new_coord = [0, 0]
            new_coord[0] = ((self.size - i[0]) / self.size) * (self.max_lat - self.min_lat) + self.min_lat
            new_coord[1] = (float(i[1]) / self.size) * (self.max_long - self.min_long) + self.min_long

            latlong_arr.append(new_coord)

        return latlong_arr

    def to_latlong_1D(self, arr):
        latlong_arr = []

        x = (arr[1])
        y = (arr[0])
        x = ((self.size - x) / self.size) * (self.max_lat - self.min_lat) + self.min_lat
        y = (float(y) / self.size) * (self.max_long - self.min_long) + self.min_long
        latlong_arr.append(x)
        latlong_arr.append(y)


        return latlong_arr

    def align(self, matrix):
        # x = y, y = -x
        # % size to account for negative results
        aligned_matrix = [[point[1] % self.size, -point[0] % self.size] for point in matrix]

        return aligned_matrix


# new_debug = Coords(2048)
# new_debug.latlongs = new_debug.to_latlong([[100, 100], [1948, 100], [1948, 1948]])
# print(new_debug.latlongs)

