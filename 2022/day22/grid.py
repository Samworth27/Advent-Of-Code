from util.classes import MapTiles, Point, InstructionTypes
from util.functions import clear_terminal
from player import Player
from collections import defaultdict
from time import sleep

MOVE = InstructionTypes.move
TURN = InstructionTypes.turn

class Grid():
    def __init__(self,map_data):
        self._grid_data = defaultdict(lambda: None)
        for y, row in enumerate(map_data):
            for x, point in enumerate(row):
                self._grid_data[x + 1j*y] = Point(x + 1j*y,point)
        self.calc_bounds()   
        self.path = defaultdict(lambda: None)
        self.player = Player(self, self.start_point())
        self.should_print = True
        self.should_sleep = True
        
    def execute_instructions(self,instruction_list):
        for iteration, instruction in enumerate(instruction_list):
            # print(f"{iteration + 1}/ {len(instruction_list)}")
            if instruction.type == TURN:
                self.player.rotate(instruction.direction)
            if instruction.type == MOVE:
                self.player.move(instruction.distance)  
        return self.player.location

    def calc_bounds(self):
        points = self._grid_data.keys()
        # print(points)
        self.bounds = {
            'x_min':int(min(x.real for x in points)),
            'x_max':int(max(x.real for x in points)),
            'y_min':int(min(x.imag for x in points)),
            'y_max':int(max(x.imag for x in points))
        }
    
    def start_point(self):
        for x in self.all_cols():
            if self._grid_data[x+0j].key == MapTiles.tile:
                return x+0j
    
    def all_rows(self):
        for y in range(self.bounds['y_min'],self.bounds['y_max']+1):
            yield y
            
    def all_cols(self):
        for x in range(self.bounds['x_min'], self.bounds['x_max']+1):
            yield x
    
    def all_points(self):
        for x in self.all_cols():
            for y in self.all_rows():
                yield x,y
        
    def print(self, clear_before=False):
        if clear_before: clear_terminal()
        
        for y in self.all_rows():
            row = []
            for x in self.all_cols():
                point = x + 1j *y
                grid_value = self.player.direction.value if self.player.location == point else self.path[point] and self.path[point].value or self._grid_data[point] and self._grid_data[point].value
                row += [grid_value]
            print (''.join(row))
        if self.should_sleep: sleep(0.1)
            
            
    def print_player_scan(self):
        print(''.join([x.value for x in [*reversed(self.player.scan(rearwards=True)),*self.player.scan()]]))
        
    def __getitem__(self,key):
        return self._grid_data[key]