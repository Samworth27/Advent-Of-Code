from util.classes import MapTiles, PathTiles, PlayerTiles, Rotations

UP = PlayerTiles.up
RIGHT = PlayerTiles.right
DOWN = PlayerTiles.down
LEFT = PlayerTiles.left

FORWARDS = {
    UP: 0 -1j,
    RIGHT: 1 + 0j,
    DOWN: 0 +1j,
    LEFT: -1 + 0j
}


class Player():
    def __init__(self, grid, location):
        self.location = location
        self.grid = grid
        self.direction = RIGHT
        self.grid.path[self.location] = PathTiles[self.direction.name]
        self.current_face = grid.start_face()
        
    def rotate(self, move_direction):
        if move_direction == 'R':
            self.direction = {
                RIGHT:DOWN,
                DOWN:LEFT,
                LEFT:UP,
                UP:RIGHT
            }[self.direction]
        if move_direction == 'L':
            self.direction = {
                RIGHT:UP,
                DOWN:RIGHT,
                LEFT:DOWN,
                UP:LEFT
            }[self.direction]
        self.grid.path[self.location] = PathTiles[self.direction.name]
        if self.grid.should_print: self.grid.print(True)
    
    def scan(self, rearwards = False):
        forward_motion = FORWARDS[self.direction]
        scan_result = [self.grid._grid_data[self.location]] if rearwards else []
        last_point = self.location
        while True:
            next_point = last_point + forward_motion if not rearwards else last_point - forward_motion
            point_value = self.grid._grid_data[next_point]
            if point_value == None or point_value.key == MapTiles.void: break
            scan_result.append(point_value)
            last_point = next_point
        return scan_result
    
    def move(self,distance):
        scan = self.scan() 
        for step in range(distance):
            forward_motion = FORWARDS[self.direction]
            next_position = self.location+forward_motion
            next_point = self.grid[next_position]
            if self.point_on_face(next_position):
                if next_point.key == MapTiles.tile:
                    self.location = next_point.location
            else:
                self.wrap()
            self.grid.path[self.location] = PathTiles[self.direction.name]
            if self.grid.should_print: self.grid.print(True)
            
    def wrap(self):
        target_edge = self.current_face[self.direction.name]
        target_face = target_edge.destination_face
        
        # calculate new local face position
        target_local_position = self.edge_transition(target_edge)
        target_global_position = self.local_to_global(target_face,target_local_position)
        
        # self.grid.print(bounds = self.current_face.bounds)
        # print(f"Current Location:\n\tFace: {self.current_face}\n\tEdge: {self.direction.name}\n\tglobal pos: {self.location},\n\tlocal pos: {self.global_to_local(self.location, self.current_face)}")
        # print(f"Target Location:\n\tFace: {target_face}\n\tEdge: {target_edge.destination_edge}\n\tglobal pos: {target_global_position},\n\tlocal pos: {target_local_position}")
        print(f"Face {self.current_face.id}.{self.direction.name} [{self.global_to_local(self.location, self.current_face)}] to Face {target_face.id}.{target_edge.destination_edge}[{target_local_position}] turning {target_edge.rotation.name}")
        # input(f"enter to continue")
        
        next_point = self.grid[target_global_position]
        print(f"Next position: {target_global_position} Next point: {next_point}")
        if next_point.key == MapTiles.tile:
            self.location = target_global_position
            self.current_face = target_face
            if target_edge.rotation == Rotations.right:
                self.rotate('R')
            elif target_edge.rotation == Rotations.left:
                self.rotate('L')
            elif target_edge.rotation == Rotations.reversed:
                self.rotate('R')
                self.rotate('R')
    

    def edge_transition(self,target_edge):
        width = self.grid.face_width - 1
        state = (self.direction,target_edge.destination_edge)
        current_local_position = self.global_to_local(self.location, self.current_face)
        if state in [(UP,'up'), (DOWN,'down')]:
            target_local_position = (width - current_local_position.real) + current_local_position.imag*1j
        if state in [(RIGHT,'right') , (LEFT,'left')]:
            target_local_position = current_local_position.real + ((width * 1j) - current_local_position.imag*1j)
        if state in [(UP,'down') , (DOWN,'up')]:
            target_local_position = current_local_position.real + ((width * 1j) - current_local_position.imag*1j)
        if state in [(LEFT,'right') , (RIGHT,'left')]:
            target_local_position = (width - current_local_position.real) + current_local_position.imag*1j
            
        if state in [(RIGHT,'up')]:
            target_local_position = (width - current_local_position.imag) + 0j
        if state in [(LEFT, 'up')]:
            target_local_position = (current_local_position.imag) + 0j
        if state in [(RIGHT,'down')]:
            target_local_position = (current_local_position.imag) + (width * 1j)
        if state in [(LEFT,'down')]:
            target_local_position = (width-current_local_position.imag) + (width * 1j)
        
        if state in [(UP,'right')]:
            target_local_position = width + (width-current_local_position.real)*1j
        if state in [(UP,'left')]:
            target_local_position = 0 + (current_local_position.real)*1j
        if state in [(DOWN,'right')]:
            target_local_position = width + (current_local_position.real)*1j
        if state in [(DOWN,'left')]:
            target_local_position = 0 + (width - current_local_position.real)*1j  
            
        return target_local_position
            
    def point_on_face(self,point:complex):
        x:int = point.real
        y:int = point.imag
        face_bounds = self.current_face.bounds
        if x in range(face_bounds.x_min,face_bounds.x_max+1):
            if y in range(face_bounds.y_min,face_bounds.y_max+1):
                return True
        return False
    @staticmethod
    def global_to_local(global_point: complex,face)->complex:
        bounds = face.bounds
        return global_point - bounds.x_min - 1j*bounds.y_min
    
    @staticmethod
    def local_to_global(face, local_point: complex)->complex:
        bounds = face.bounds
        return local_point + bounds.x_min + 1j*bounds.y_min

        
        