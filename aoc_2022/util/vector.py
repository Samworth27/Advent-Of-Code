from enum import Enum

def complex_xy(x,y):
    return x + y * 1j

class Vector:
    NORTH = None
    EAST = None
    SOUTH = None
    WEST = None
    def __init__(self, x:int|float, y:int|float):
        self._vector = complex_xy(x,y)
        
    def __add__(self,vector2:'Vector') -> 'Vector':
        return Vector.from_complex(self._vector + vector2._vector)
    
    def __sub__(self,vector2:'Vector') -> 'Vector':
        return Vector.from_complex(self._vector - vector2._vector)
    
    def __mul__(self,vector2:'Vector') -> 'Vector':
        return Vector(self.x * vector2.x, self.y * vector2.y)
    
    def __truediv__(self,vector2: 'Vector') -> 'Vector':
        return Vector(self.x / vector2.x, self.y / vector2.y)
    
    def __floordiv__(self,vector2: 'Vector') -> 'Vector':
        return Vector(self.x // vector2.x, self.y // vector2.y)
    
    def from_complex(complex_):
        return Vector(complex_.real, complex_.imag)
    
    def __lt__(self, vector2:'Vector')->bool:
        if self.y < vector2.y: return True
        if self.x < vector2.x: return True
        return False
    
    def __eq__(self, vector2:'Vector') -> bool:
        return self.complex == vector2.complex
    
    def __repr__(self) -> str:
        return f"Vector: {self.x,self.y}"
    
    def __hash__(self):
        return hash(self.complex)
     
    @property
    def complex(self) -> complex:
        return self._vector
        
    @property
    def x(self) -> float:
        return self._vector.real
    
    @x.setter
    def x(self,value):
        self._vector = complex_xy(value, self.y)
    
    @property
    def y(self) -> float:
        return self._vector.imag
    
    @y.setter
    def y(self,value):
        self._vector = complex_xy(self.x, value)

    @property
    def x_int(self):
        return int(self.x)
    
    @property
    def y_int(self):
        return int(self.y)
    
    @property
    def copy(self):
        return Vector(self.x,self.y)
    
Vector.NORTH = Vector(0,-1)
Vector.EAST = Vector(1,0)
Vector.SOUTH = Vector(0,1)
Vector.WEST = Vector(-1,0)
