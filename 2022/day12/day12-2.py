file = open('day12.txt')

class Node():
    width = None
    height = None
    count = 0
    def __init__(self, height, x, y, prev_node, prev_line, target):
        self.up, self.down, self.left, self.right = [None,None,None,None]
        self.visited = False
        self.distance = float('inf')
        
        self.height = height
        self.target = target
        
        self.x = x
        self.y = y
        
        self.initUp(prev_line, x)
        self.initLeft(prev_node)
        
        self.id = Node.count
        Node.count += 1
    
    def canMove(self, target):
        return (self.height - target.height) <= 1
        
    def initUp(self, prev_line, x):
        if prev_line != None:     
            if self.canMove(prev_line[x]):
                self.up = prev_line[x]
            prev_line[x].initDown(self)
        
    def initLeft(self, prev_node):
        if prev_node != None:
            if self.canMove(prev_node):
                self.left = prev_node
            prev_node.initRight(self)
        
    def initRight(self, right_node):
        if self.canMove(right_node):
            self.right = right_node
    
    def initDown(self, down_node):
        if self.canMove(down_node):
            self.down = down_node
    
    def neighbourNodes(self):
        return [ node for node in [self.left, self.up, self.right, self.down] if node != None]
    
    def visitableNodes(self):
        return [node for node in self.neighbourNodes() if node.visited == False]
        
    def __str__(self):
        return f"Node {self.id} ({self.x},{self.y}): height {self.height}"
    
    def __repr__(self):
        return f"id:{self.id}"
    
heightmap = []

start = (0, 0)
finish = (0, 0)
y = 0


prev_line = None

for line in [l.strip() for l in file]:
    
    if Node.width == None:
        Node.width = len(line)
    
    x = 0
    prev_node = None
    new_line = []
    for char in line:
        target = False
        if char == 'S':
            start = (x, y)
            char = 'a'
        if char == 'E':
            finish = (x, y)
            target = True
            char = 'z'
        new_node = Node(ord(char)-97, x, y, prev_node, prev_line, target)
        new_line.append(new_node)
        prev_node = new_node
        x += 1
    heightmap.append(new_line)
    prev_line = new_line
    y += 1

Node.height = y

start_node = heightmap[finish[1]][finish[0]]
start_node.distance = 0

stack = [start_node]

print("Searching")
while len(stack) > 0:
    stack.sort(key = lambda x: x.distance, reverse=True)
    current_node = stack.pop()
    for node in current_node.visitableNodes():
        node.distance = min(node.distance, current_node.distance + 1)
        if node not in stack:
            stack.append(node)
    current_node.visited = True
    if current_node.height == 0:
        print(current_node.distance)
        break
