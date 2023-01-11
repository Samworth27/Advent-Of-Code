from enum import Enum
from collections import defaultdict


class MapTiles(Enum):
    void = '.'
    tile = '\u25CC'
    wall = '\u25C6'

class PlayerTiles(Enum):
    up = '\u25B3'
    right = '\u25B7'
    down = '\u25BD'
    left = '\u25C1'

class PathTiles(Enum):
    up = '\u25B5'
    right = '\u25B9'
    down = '\u25BF'
    left = '\u25C3'
    
class InstructionTypes(Enum):
    move = 0
    turn = 1
    
class Rotations(Enum):
    left = 0
    right = 1
    reversed = 2
    none = 3
    
class Point():
    def __init__(self, location,point):
        self.location = location
        self.key = point
        self.value = point.value

    def __repr__(self):
        return f"Point: ({int(self.location.real)}, {int(self.location.imag)})"
    
class CubePoint():
    def __init__(self, location,point,face = ' '):
        self.location = location
        self.key = point
        self.value = point.value
        self.face = face
    
    def __repr__(self):
        return f"Point: ({int(self.location.real)}, {int(self.location.imag)})"