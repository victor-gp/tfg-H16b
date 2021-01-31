from math import ceil, floor
from numpy import arange
from itertools import product


class DiscretePlane:
    def __init__(self, x_min, x_max, x_resolution, y_min, y_max, y_resolution):
        self.x_axis = DiscreteAxis(x_min, x_max, x_resolution)
        self.y_axis = DiscreteAxis(y_min, y_max, y_resolution)

    # project (x, y) into the coordinates relative to the plane's (implicit) matrix
    def projection_coordinates(self, x, y):
        x_coord = self.x_axis.projection_coordinate(x)
        y_coord = self.y_axis.projection_coordinate(y)

        if x_coord is None or y_coord is None: return None
        else: return x_coord, y_coord

    # dimension of the matrix represented by the plane
    def dimension(self):
        return self.x_axis.projection_dimension, self.y_axis.projection_dimension


    # all the points in the plane
    def range(self):
        x_range = self.x_axis.range()
        y_range = self.y_axis.range()
        return product(x_range, y_range)

    def extent(self):
        x_min, x_max = self.x_axis.extent()
        y_min, y_max = self.y_axis.extent()

        return x_min, x_max, y_min, y_max

    def projection_resolution(self):
        return self.x_axis.projection_resolution(), self.y_axis.projection_resolution()


    def to_dict(self):
        return {
            '__discrete_plane__': True,
            'x_min': self.x_axis.min,
            'x_max': self.x_axis.max,
            'x_scan_resolution': self.x_axis.scan_resolution,
            'x_projection_dimension': self.x_axis.projection_dimension,
            'y_min': self.y_axis.min,
            'y_max': self.y_axis.max,
            'y_scan_resolution': self.y_axis.scan_resolution,
            'y_projection_dimension': self.y_axis.projection_dimension
        }

    @classmethod
    def from_dict(cls, dict):
        if '__discrete_plane__' not in dict:
            raise RuntimeError('not a DiscretePlane dict')

        restored_plane = cls.__new__(cls)
        restored_plane.x_axis = DiscreteAxis.restore(
            dict['x_min'], dict['x_max'],
            dict['x_scan_resolution'], dict['x_projection_dimension']
        )
        restored_plane.y_axis = DiscreteAxis.restore(
            dict['y_min'], dict['y_max'],
            dict['y_scan_resolution'], dict['y_projection_dimension']
        )

        return restored_plane


class DiscreteAxis:
    def __init__(self, min, max, resolution):
        self.min = min
        self.max = max
        self.scan_resolution = resolution
        self.projection_dimension = DiscreteAxis.projection_dimension(min, max, resolution)


    def projection_coordinate(self, point):
        relative_position = (point - self.min) / (self.max - self.min)
        float_coordinate = relative_position * self.projection_dimension

        if float_coordinate < 0: return None
        if float_coordinate >= self.projection_dimension: return None

        return floor(float_coordinate)

    @staticmethod
    def projection_dimension(min, max, orientative_resolution):
        dimension_float = (max - min) / orientative_resolution
        return ceil(dimension_float)
        # actual resolution >= orientative resolution


    def range(self):
        # max + resolution so max is included in the range
        range_max = self.max + self.scan_resolution
        return arange(self.min, range_max, self.scan_resolution)

    def extent(self):
        return self.min, self.max

    def projection_resolution(self):
        return (self.max - self.min) / self.projection_dimension


    @classmethod
    def restore(cls, min, max, scan_resolution, projection_dimension):
        restored_axis = cls.__new__(cls)
        restored_axis.min = min
        restored_axis.max = max
        restored_axis.scan_resolution = scan_resolution
        restored_axis.projection_dimension = projection_dimension

        return restored_axis
