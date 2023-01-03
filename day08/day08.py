file = open('day08.txt')


class Tree():
    def __init__(self, x, y, height, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.height = height
        self.visible = False
        self.tallest = {
            'north': None,
            'east': None,
            'south': None,
            'west': None
        }
        self.view_distance = {
            'north': None,
            'east': None,
            'south': None,
            'west': None
        }

    def __str__(self) -> str:
        return f"Tree: ({self.x},{self.y})[{self.height}]"

    def __repr__(self) -> str:
        return str(self)

    def getNeighbour(self, direction):
        x = self.x
        y = self.y
        match direction:
            case 'north':
                if self.y == 0:
                    return None
                y -= 1
            case 'south':
                if self.y == self.grid.y_max:
                    return None
                y += 1
            case 'west':
                if self.x == 0:
                    return None
                x -= 1

            case 'east':
                if self.x == self.grid.x_max:
                    return None
                x += 1
        return self.grid.getTree(x, y)

    def isVisible(self):
        for direction in self.tallest:
            if self.height > self.getTallest(direction):
                self.visible = True
        return self.visible

    def getTallest(self, direction):
        node = self.getNeighbour(direction)
        if node == None:
            return -1
        if self.tallest[direction] == None:
            self.grid.calculations += 1
            self.tallest[direction] = max(
                node.height, node.getTallest(direction))

        return self.tallest[direction]

    def getViewDistance(self, direction):
        node = self.getNeighbour(direction)
        if node == None:
            return [0 for _ in range(10)]
        if self.view_distance[direction] == None:
            node_distance = node.getViewDistance(direction)
            self.view_distance[direction] = [None for _ in range(10)]
            for view_height in range(10):
                if view_height > node.height:
                    self.view_distance[direction][view_height] = node_distance[view_height] + 1
                else:
                    self.view_distance[direction][view_height] = 1
                    
        return self.view_distance[direction]
                
                
    def calcVisScore(self):
        score = 1
        for direction in self.view_distance:
            view_distance = self.getViewDistance(direction)[self.height]
            print(view_distance)
            score *= view_distance
            
        return score


class VisGrid():
    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.grid = []
        self.calculations = 0

    def getTree(self, x, y):
        return self.grid[y][x]


height = [[int(i) for i in line.strip()]for line in file.readlines()]
vis = VisGrid(len(height[0])-1, len(height)-1)
vis.grid = [[Tree(x, y, height[y][x], vis)
             for x in range(len(height[0]))] for y in range(len(height))]


visible = 0
best_score = 0
for row in vis.grid:
    for node in row:
        if node.isVisible():
            visible += 1
        vis_score = node.calcVisScore()
        print(f"{[node.x,node.y]}, score:{vis_score}")
        if vis_score > best_score:
            best_score = vis_score

print(best_score)
