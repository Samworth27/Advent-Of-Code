from collections import namedtuple
from enum import Enum
from util.vector import Vector

Bounds = namedtuple('Bounds', ['x_min', 'x_max', 'y_min', 'y_max'])


class Point:
    def __init__(self, position, draw_value):
        self.position = position
        self.draw_value = draw_value

    def __repr__(self):
        return f"Point {self.draw_value} {self.position}"

    def __str__(self):
        return str(self.draw_value)


class Grid:
    def __init__(self, input, default=None):
        self.default = default
        self._points = {}
        self.initialise_points(input)
        self._bounds = self._calculate_bounds()
        self._bounds_hash = self._key_hash

    def initialise_points(self, input):
        for y, row in enumerate(input):
            for x, point_value in enumerate(row):
                vector = Vector(x, y)
                self[vector] = Point(vector, point_value)

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

    @property
    def _key_hash(self):
        return hash(tuple(sorted(self._points.keys())))

    @property
    def bounds(self):
        if self._key_hash != self._bounds_hash:
            self._bounds = self._calculate_bounds()
        return self._bounds

    @property
    def array(self) -> list[list[Point]]:
        x_min, x_max, y_min, y_max = self.bounds
        _array = [[self[Vector(x, y)] for x in range(x_min, x_max+1)]
                  for y in range(y_min, y_max+1)]
        return _array
