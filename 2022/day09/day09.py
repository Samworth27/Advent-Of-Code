import os
import time
file = open('day09.txt')


def clear():
    os.system('clear')

class Canvas():
    def __init__(self, width, height, x_offset, y_offset, disabled = False):
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.origin = [self.x_offset, self.y_offset]
        self.objects = []
        self.disabled = disabled
        
    def addObject(self, object):
      self.objects.append(object)
      
    def draw(self):
      if self.disabled:
        return 
      clear()
      dis_map = [['.' for _ in range(self.width)] for _ in range(self.height)]
      dis_map[self.y_offset][self.x_offset] = '*'
      for object in reversed(self.objects):
        dis_x = (object.x + self.width + self.x_offset)%self.width
        dis_y = (object.y*-1+self.y_offset + self.height)%self.height
        dis_map[dis_y][dis_x] = str(object.symbol)
      for row in dis_map:
          print(' '.join(row))
      # time.sleep(0.01)
      # input("press enter to continue")

class Head():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tail = None
        self.symbol = 'H'

    def move(self, dir):
        match dir:
            case 'U':
                self.y += 1
            case 'D':
                self.y -= 1
            case 'R':
                self.x += 1
            case 'L':
                self.x -= 1
        canvas.draw()
        self.tail.move()


class Tail():
    def __init__(self, head, position):
        self.x = 0
        self.y = 0
        self.last_x = 0
        self.last_y = 0
        self.position = position
        self.head = head
        self.head.tail = self
        self.visited = []
        self.tail = None
        self.symbol = str(position)

    def __str__(self):
        return f"tail number {self.position} at {self.x,self.y}"

    def move(self):
        self.last_x = self.x
        self.last_y = self.y
        x_dist = self.head.x - self.x
        y_dist = self.head.y - self.y
        manhattan_dist = abs(x_dist) + abs(y_dist)
        if manhattan_dist > 2:
          if abs(x_dist) == abs(y_dist):
            self.x += int(x_dist/2)
            self.y += int(y_dist/2)
          elif abs(x_dist) > abs(y_dist):
            self.x += int(x_dist/2)
            self.y += int(y_dist)
          else:
            self.x += int(x_dist)
            self.y += int(y_dist/2)
          
        elif manhattan_dist > 1:
          if abs(x_dist) != abs(y_dist):
            self.x += int(x_dist/2)
            self.y += int(y_dist/2)

        if ((self.x, self.y)not in self.visited):
            self.visited.append((self.x, self.y))
        if self.x != self.last_x or self.y != self.last_y:
          canvas.draw()
        if self.tail:
            self.tail.move()


debug_count = 0
debug_limit = 20

canvas = Canvas(26,21,11,15)

head = Head()
canvas.addObject(head)
# tail = Tail(head, 1)
tails = []
prev_tail = head
for i in range(1, 10):
    new_tail = Tail(prev_tail, i)
    canvas.addObject(new_tail)
    tails.append(new_tail)
    prev_tail = tails[-1]


for line in file:

    dir, dis = line.strip().split(' ')
    for _ in range(int(dis)):
        head.move(dir)


print(len(tails[-1].visited))
