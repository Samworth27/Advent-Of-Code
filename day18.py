from collections import namedtuple
from os import system
from dataclasses import dataclass

AIR = '\u2591'
LAVA = '\u2588'

blocks = namedtuple('blocks',['air','lava'])(AIR,LAVA)
    

RED = '91'
YELLOW = '93'
CYAN = '96'

BUFFER = 2

Point3 = namedtuple('Point3', ['x', 'y', 'z'])

def colour_text(input,colour):
    return f"\033[{colour}m{input}\033[00m"
    

class Droplet():
    def __init__(self, points):
        x_min, x_max = min_max([point.x for point in points])
        y_min, y_max = min_max([point.y for point in points])
        z_min, z_max = min_max([point.z for point in points])
        
        self.points = points
        
        self._space = [[[AIR for x in range(x_max+BUFFER)] for y in range(
            y_max+BUFFER)] for z in range(z_max+BUFFER)]
        
        for point in points:
            self.set_point(point.x, point.y, point.z, LAVA)

    def set_point(self, x, y, z, value):
        try:
            self._space[z][y][x] = value
            return True
        except IndexError:
            return False

    def get_point(self, x, y, z, default=None):
        if x < 0 or y < 0 or z < 0:
            return default
        try:
            return self._space[z][y][x]
        except IndexError:
            return default
        
    def _point_visible_faces(self, point, outside_air = None):
        visibility = {}
        for label, neighbour_point in neighbour_points(point).items():
            if outside_air:
                visibility[label] = self.get_point(*neighbour_point, AIR) == AIR and neighbour_point in outside_air
            else:
                visibility[label] = self.get_point(*neighbour_point, AIR) == AIR
                
        return sum(visibility.values())
    
    def surface_area(self):
        surface_area = 0
        for point in self.points:
            surface_area += self._point_visible_faces(point)
        return surface_area
    
    def exterior_surface_area(self):
        outside_points = []
        visited = []
        start_node = Point3(0,0,0)
        queue = [start_node]
        global blocks
        while len(queue) > 0:
            node = queue.pop(0)
            node_neigbours = neighbour_points(node).values()
            for point in [i for i in node_neigbours if i not in visited]:
                match self.get_point(*point, None):
                    case blocks.air:
                        visited.append(point)
                        queue.append(point)
                    case blocks.lava:
                        visited.append(point)
                        if point not in outside_points: outside_points.append(point)
                    case _:
                        pass
        
        surface_area = 0
        for point in outside_points:
            surface_area += self._point_visible_faces(point, visited)
        return surface_area
                        
                    
    
    def get_slice(self,z):
        z_slice = self._space[z]
        return z_slice
        
    def draw_slice(self,z:int, highlight:Point3 = None) -> list:
        z_slice = self.get_slice(z)
        slice_repr = ''
        for y, col in enumerate(z_slice):
            col_repr = ''
            for x, val in enumerate(col):
                colour = YELLOW if Point3(x,y,z) == highlight else RED if val == LAVA else CYAN
                col_repr += colour_text(val,colour)
            slice_repr += col_repr + '\n'
        
        return slice_repr
    
    def draw(self):
        for z, z_slice in enumerate(reversed(self._space)):
            system('clear')
            print(f"Layer {z}\n")
            print(self.draw_slice(z))
            input("Enter to view next slice")
            


def min_max(x: list):
    return min(x), max(x)


def neighbour_points(point):
    return {
        'up': Point3(point.x, point.y, point.z+1),
        'down': Point3(point.x, point.y, point.z-1),
        'right': Point3(point.x,point.y+1,point.z),
        'left': Point3(point.x,point.y-1,point.z),
        'forward': Point3(point.x+1, point.y, point.z),
        'backwards':Point3(point.x-1, point.y, point.z)
    }

def process_file(path:str):
    with open(path) as file:
        points = []
        for line in file:
            points.append(Point3(*[int(i)+BUFFER for i in line.strip().split(',')]))
    return points
def main():
    


    part1_example = Droplet(process_file('day18-example.txt'))
    print(f"Part 1 example passes test: {part1_example.surface_area() == 64}")
    
    part1 = Droplet(process_file('day18.txt'))
    # part1.draw()
    print(f"Part 1 answer: {part1.surface_area()}")
    
    print(f"Part 2 example passes test: {part1_example.exterior_surface_area() == 58} answer {part1_example.exterior_surface_area()}")
    print(f"Part 2 answer: {part1.exterior_surface_area()}")

if __name__ == '__main__':
    main()
