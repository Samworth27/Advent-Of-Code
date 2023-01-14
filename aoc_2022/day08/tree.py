from util.grid import Point, Cardinal

class Tree(Point):
    def __init__(self, position, height, parent_grid):
        self.position = position
        self.height = int(height)
        self.visible_from = {dir: None for dir in Cardinal}
        self.tallest = {dir: None for dir in Cardinal}
        self.view_distance = {dir: None for dir in Cardinal}
        self.grid = parent_grid
        self._is_visible = None
        self._highlight1 = False
        self._highlight2 = False


    def neighbour(self, direction: Cardinal):

        new_pos = super().neighbour(direction)
        return self.grid[new_pos]

    def is_visible(self):
        if self._is_visible == None:
            self.highlight1(True)
            self.grid.record_state()
            for direction in self.tallest:
                if self.visible_from[direction] == None:
                    tallest = self.find_tallest(direction)
                    self.visible_from[direction] = self.height > tallest
            self._is_visible = any(self.visible_from.values())
            self.highlight1(False)
            self.grid.record_state()
        return self._is_visible

    def find_tallest(self, direction: Cardinal):
        node = self.neighbour(direction)
        if node == None:
            return -1
        if self.tallest[direction] == None:
            node.highlight2(True)
            self.tallest[direction] = max(
                node.height, node.find_tallest(direction))
        self.grid.record_state()
        node.highlight2(False)
        return self.tallest[direction]

    def get_view_distance(self, direction):
        node = self.neighbour(direction)
        if node == None:
            return [0 for _ in range(10)]
        if self.view_distance[direction] == None:
            node_distance = node.get_view_distance(direction)
            self.view_distance[direction] = [None for _ in range(10)]
            for view_height in range(10):
                if view_height > node.height:
                    self.view_distance[direction][view_height] = node_distance[view_height] + 1
                else:
                    self.view_distance[direction][view_height] = 1

        return self.view_distance[direction]

    def calculate_vis_score(self):
        score = 1
        for direction in self.view_distance:
            view_distance = self.get_view_distance(direction)[self.height]
            score *= view_distance
        return score
    
    def highlight1(self,value):
        self._highlight1 = value
        self.grid.update_cell(self)
        # if type(value) != bool:
        #     raise TypeError
        # if value:
        #     self.grid._highlight1.add(self.position)
        #     return True
        # if self.position in self.grid._highlight1:
        #     self.grid._highlight1.remove(self.position)
        # return False
    
    def highlight2(self,value):
        self._highlight2 = value
        self.grid.update_cell(self)
        # if type(value) != bool:
        #     raise TypeError
        # if value:
        #     self.grid._highlight2.add(self.position)
        #     return True
        # if self.position in self.grid._highlight2:
        #     self.grid._highlight2.remove(self.position)
        # return False
        


    def __str__(self):
        return f"Tree {self.position, self.height}"

    def __repr__(self):
        return f"Tree {self.position}: Visible {self.is_visible()}"