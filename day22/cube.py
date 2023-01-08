from util.classes import MapTiles, CubePoint, InstructionTypes, Rotations
from util.functions import clear_terminal
from player import Player
from collections import defaultdict
from time import sleep
from collections import namedtuple

MOVE = InstructionTypes.move
TURN = InstructionTypes.turn


Bounds = namedtuple('Bounds', ['x_min', 'x_max', 'y_min', 'y_max'])


class Edge():
    def __init__(self, destination_face, destination_edge, travel_rotation):
        self.rotation = travel_rotation
        self.destination_face = destination_face
        self.destination_edge = destination_edge
    
    def __repr__(self):
        return f"{self.destination_face.id}.{self.destination_edge}"


class Face():
    def __init__(self, id, face_bounds: Bounds):
        self.id = id
        self.bounds = face_bounds
        self.up: Edge = None
        self.right: Edge = None
        self.down: Edge = None
        self.left: Edge = None
        
    def __repr__(self):
        return f"Face {self.id}: (top: {self.up} right: {self.right} bottom: {self.down} left:{self.left})"
        
        
    def __getitem__(self,edge):
        if edge in ['up','right','down','left']:
            return self.__getattribute__(edge)
        
    def __setitem__(self,edge,value):
        if edge in ['up','right','down','left']:
            self.__setattr__(edge,value)


def join_faces(face1,edge1,face2,edge2,rotation_f1_f2):
    face1[edge1] = Edge(face2,edge2,rotation_f1_f2)
    rotation_options = {
        Rotations.left: Rotations.right,
        Rotations.right: Rotations.left,
        Rotations.reversed: Rotations.reversed,
        Rotations.none: Rotations.none
    }
    face2[edge2] = Edge(face1,edge1,rotation_options[rotation_f1_f2])
    
def cube_assembler(faces:list[Face], example=False):
    if example:
        # face 0
        join_faces(faces[0],'up',faces[1], 'up', Rotations.reversed)
        join_faces(faces[0], 'right', faces[5], 'right', Rotations.reversed)
        join_faces(faces[0], 'down', faces[3], 'up', Rotations.none)
        join_faces(faces[0], 'left', faces[2], 'up', Rotations.reversed)
        
        # faces[1].up => faces[0]
        join_faces(faces[1],'right', faces[2], 'left', Rotations.none)
        join_faces(faces[1],'down', faces[4], 'down', Rotations.reversed)
        join_faces(faces[1],'left', faces[5], 'down',Rotations.left)
        
        # faces[2].up => faces[0]
        join_faces(faces[2],'right',faces[3],'left',Rotations.none)
        join_faces(faces[2],'down',faces[4], 'left', Rotations.left)
        # faces[2].left => faces[1]
        
        # faces[3].up => faces[0]
        join_faces(faces[3],'right', faces[5],'up', Rotations.right)
        join_faces(faces[3],'down',faces[4],'up', Rotations.none)
        # faces[3].left => faces[2]
        
        # faces[4].up => faces[3]
        join_faces(faces[4],'right',faces[5],'left',Rotations.none)
        # faces[4].down => faces[1]
        # faces[4].left
        
        # faces[5].up => faces[3]
        # faces[5].right => faces[0]
        # faces[5].down => faces[1]
        # faces[5].left => faces[4]
    else:
        join_faces(faces[0],'up',faces[5],'left',Rotations.right)
        join_faces(faces[0], 'right', faces[1],'left', Rotations.none)
        join_faces(faces[0],'down', faces[2],'up', Rotations.none)
        join_faces(faces[0],'left', faces[3], 'left', Rotations.reversed)
        
        join_faces(faces[1],'up', faces[5], 'down', Rotations.none)
        join_faces(faces[1], 'right', faces[4], 'right', Rotations.reversed)
        join_faces(faces[1],'down', faces[2], 'right', Rotations.right)
        # join_faces(faces[1],'left'
        
        # join_faces(faces[2],'up'
        # join_faces(faces[2], 'right'
        join_faces(faces[2],'down', faces[4],'up',Rotations.none)
        join_faces(faces[2],'left', faces[3],'up', Rotations.left)
        
        # join_faces(faces[3],'up'
        join_faces(faces[3], 'right', faces[4],'left',Rotations.none)
        join_faces(faces[3],'down', faces[5],'up',Rotations.none)
        # join_faces(faces[3],'left'
        
        # join_faces(faces[4],'up'
        # join_faces(faces[4], 'right'
        join_faces(faces[4],'down', faces[5], 'right',Rotations.right)
        # join_faces(faces[4],'left'
        
        # join_faces(faces[5],'up'
        # join_faces(faces[5], 'right'
        # join_faces(faces[5],'down'
        # join_faces(faces[5],'left'
    return faces


    

class Cube():
    def __init__(self, map_data, example = False):
        self._grid_data = defaultdict(lambda: None)
        for y, row in enumerate(map_data):
            for x, point in enumerate(row):
                self._grid_data[x + 1j*y] = CubePoint(x + 1j*y, point)
        self.calc_bounds()
        self.face_width = 4 if len(map_data) < 50 else 50
        print(self.face_width)
        self.path = defaultdict(lambda: None)
        self._faces= []

        self.should_print = True
        self.should_sleep = True

        for y in range(0, self.bounds.y_max+1, self.face_width):
            for x in range(0, self.bounds.x_max+1, self.face_width):
                selection = Bounds(x, x+self.face_width-1, y, y+self.face_width-1)
                if not self.contains_any_void(selection):
                    self._faces.append(Face(len(self._faces),selection))
        
        self._faces = cube_assembler(self._faces, example=example)
        
        self.player = Player(self, self.start_point())

    def execute_instructions(self, instruction_list):
        for iteration, instruction in enumerate(instruction_list):
            # print(f"{iteration + 1}/ {len(instruction_list)}")
            if instruction.type == TURN:
                self.player.rotate(instruction.direction)
            if instruction.type == MOVE:
                self.player.move(instruction.distance)
        return self.player.location

    def calc_bounds(self):
        points = self._grid_data.keys()
        self.bounds = Bounds(
            int(min(x.real for x in points)),
            int(max(x.real for x in points)),
            int(min(x.imag for x in points)),
            int(max(x.imag for x in points))
        )

    def start_point(self):
        for x in self.all_cols():
            if self._grid_data[x+0j].key == MapTiles.tile:
                return x+0j
    
    def start_face(self):
        return self._faces[0]

    def all_rows(self):
        for y in range(self.bounds.y_min, self.bounds.y_max+1):
            yield y

    def all_cols(self):
        for x in range(self.bounds.x_min, self.bounds.x_max+1):
            yield x

    def all_points(self):
        for x in self.all_cols():
            for y in self.all_rows():
                yield x, y
                
    def contains_any_void(self,selection):
        for y in range(selection.y_min, selection.y_max + 1):
            for x in range(selection.x_min, selection.x_max + 1):
                if self._grid_data[x + 1j*y].key == MapTiles.void:
                    return True
        return False
                    
    def print(self, clear_before=False, bounds=None):
        if bounds == None:
            bounds = self.bounds
        if clear_before:
            clear_terminal()

        for y in range(bounds.y_min, bounds.y_max + 1):
            row = []
            if y % self.face_width == 0:
                print('\u2500'*(self.bounds.y_max - self.bounds.y_min))
            for x in range(bounds.x_min, bounds.x_max+1):
                if x % self.face_width == 0:
                    row.append('\u2502')
                point = x + 1j * y
                grid_value = self.player.direction.value if self.player.location == point else self.path[
                    point] and self.path[point].value or self._grid_data[point] and self._grid_data[point].value
                row += [grid_value]
            print(''.join(row))
        if self.should_sleep:
            sleep(0.1)

    def print_faces(self, clear_before=False):
        if clear_before:
            clear_terminal()

        for i,face in enumerate(self._faces):
            print(f"Face {i}")
            self.print(clear_before = clear_before, bounds=face.bounds)

    def print_player_scan(self):
        print(''.join([x.value for x in [
              *reversed(self.player.scan(rearwards=True)), *self.player.scan()]]))

    def __getitem__(self, key):
        return self._grid_data[key]
