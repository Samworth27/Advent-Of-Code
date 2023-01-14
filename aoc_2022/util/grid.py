from collections import namedtuple
from enum import Enum
from util.vector import Vector

Bounds = namedtuple('Bounds', ['x_min', 'x_max', 'y_min', 'y_max'])

class Cardinal(Enum):
    north = Vector.NORTH
    east = Vector.EAST
    south = Vector.SOUTH
    west = Vector.WEST

class Point:
    def __init__(self, position, value):
        self.position = position
        self.value = value
        
    def neighbour(self,direction:Cardinal):
        return self.position + direction.value

    def __repr__(self):
        return f"Point {self.position}"

    def __str__(self):
        return str({self.position})


class Grid:
    def __init__(self, input, PointClass=Point, point_args = None, default_return=None):
        self.default = default_return
        self._points = {}
        self.initialise_points(input, PointClass, point_args)
        self.last_bounds_hash = self._key_hash
        self.last_array_hash = self._key_hash
        self._bounds = self._calculate_bounds()
        self._array = self._build_array()

    def initialise_points(self, input, PointClass, point_args):
        for y, row in enumerate(input):
            for x, point_value in enumerate(row):
                vector = Vector(x, y)
                point = PointClass(vector, point_value, *point_args) if point_args else PointClass(vector, point_value)
                self[vector] = point

    def __setitem__(self, position, value):
        self._points[position] = value

    def __getitem__(self, position):
        if position in self._points:
            return self._points[position]
        else:
            return self.default

    def _calculate_bounds(self, points=None):
        if points is None:
            points = self._points
        return Bounds(
            x_min=int(min(vector.x for vector in points)),
            x_max=int(max(vector.x for vector in points)),
            y_min=int(min(vector.y for vector in points)),
            y_max=int(max(vector.y for vector in points))
        )

    def _build_array(self):
        x_min, x_max, y_min, y_max = self.bounds
        _array = [[self[Vector(x, y)] for x in range(
            x_min, x_max+1)] for y in range(y_min, y_max+1)]
        return _array

    @property
    def _key_hash(self):
        return hash(tuple(sorted(self._points.keys())))

    @property
    def bounds(self):
        if self._key_hash != self.last_bounds_hash:
            self._bounds = self._calculate_bounds()
            self.last_bounds_hash = self._key_hash
        return self._bounds

    @property
    def array(self) -> list[list[Point]]:
        if self._key_hash != self.last_array_hash:
            self._array = self._build_array()
            self.last_array_hash = self._key_hash
        return self._array
    
    def __iter__(self):
        x0, x1, y0, y1 = self.bounds
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                yield self[Vector(x,y)]
