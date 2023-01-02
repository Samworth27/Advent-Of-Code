import os
import copy
from collections import namedtuple
import time


class Shape():
    Bounds = namedtuple('BoundsBox', ['x1', 'x2', 'y1', 'y2'])

    def __init__(self, name, array=[[]]):
        self.name = name
        self.array = array
        self.x = 0
        self.y = 0
        self.height = len(array)
        self.width = len(array[0])
        # print(f"{self.name}: {self.bounds()}")
        # print(f"w:{self.width} h:{self.height}")
        # input(self)

    def lookup(self, x, y):
        return [*reversed(self.array)][y - self.y][x-self.x]

    def trackedCopy(self, x, y):
        tc = copy.copy(self)
        tc.x = x
        tc.y = y
        return tc

    def bounds(self):
        return Shape.Bounds(self.x, self.x + (self.width - 1), self.y, self.y + (self.height - 1))

    def __str__(self):
        return ''.join('\n'.join([str(y) for y in self.array]))

    def __repr__(self):
        return self.name


class Sequence():

    def __init__(self, input):
        last = None
        self.values = [i for i in input]
        self.pointer = 0

    def next(self):
        self.pointer = (self.pointer + 1) % len(self.values)
        return self.val()

    def prev(self):
        self.pointer = (self.pointer + len(self.values) - 1) % len(self.values)
        return self.val()

    def val(self):
        return self.values[self.pointer]


class Chamber():

    SteadyRock = namedtuple('SteadyRock', ['shape', 'jet', 'env'])
    HeightsPair = namedtuple('HeightsPair', ['id', 'height'])

    def __init__(self, shapes, move_sequence):
        self.rows = []
        self.shapes = [*shapes]
        self.shape_index = 0
        self.current_shape = Shape('none')
        self.sequence = move_sequence
        self.heights = []
        self.rock_record = {}

    def dropRock(self, debug, debug_count):
        falling = True
        while falling:
            falling, rock = self.step(debug=debug, debug_count=debug_count)
        return rock
    
    def dropRocks(self, count, debug=False):
        rock_n = 0
        while rock_n < count:
            rock = self.dropRock(debug,rock_n)

            if self.cycleExists(rock):
                cycle_start = rock_n
                cycle_start_height = self.getHighestRock()
                start_rock = self.rock_record[rock]
                cycle_length = start_rock[-1].id - start_rock[-2].id
                cycle_height = start_rock[-1].height - start_rock[-2].height
                
                print(f"cycle detected at after {cycle_start} rocks at a height of {cycle_start_height}")
                
                rocks_remaining = count - cycle_start
                cycles_remaining = rocks_remaining//cycle_length
                leftover_rocks = rocks_remaining%cycle_length
                cycles_total_height = cycle_height*cycles_remaining
                
                print(f"{rocks_remaining} rocks remaining")
                print(
                    f"{cycles_remaining} full cycles and {leftover_rocks} rocks remaining")
                print(f"{cycle_start_height + cycles_total_height}")
                break
            else:
                if rock in self.rock_record:
                    self.rock_record[rock].append(
                        self.HeightsPair(rock_n, self.getHighestRock()))
                else:
                    self.rock_record[rock] = [
                        self.HeightsPair(rock_n, self.getHighestRock())]
            rock_n += 1
        else:
            return self.getHighestRock()
        
        # reset rock cycle
        # for i in range(cycle_length-1):
        #     self.dropRock(False,i)
            
        leftover_start_height = self.getHighestRock()
        for rock in range(leftover_rocks - 1):
            print(rock, self.getHighestRock())
            falling = True
            while falling:
                falling, rock = self.step()
        leftover_height = self.getHighestRock() - leftover_start_height
        print(f"leftover height = {leftover_height}")
        return(cycle_start_height + cycles_total_height + leftover_height)
        
    def cycleExists(self, rock):
        if rock in self.rock_record:
            if len(self.rock_record[rock]) >= 2:
                return True
        return False

    def step(self, display=False, debug=False, debug_count=0):
        if debug:
            os.system('clear')
            clearing = 'none'
            print('*'*40)
            print(f"Rock number {debug_count}\n")
            self.displayRows(clearing=clearing)
        else:
            clearing = 'both'
        falling = True
        if self.sequence.val() == '>':
            if debug:
                print(f"Move Right (valid = {self.validPosition('right')}\n")
            if self.validPosition('right'):
                self.current_shape.x += 1
        else:
            if debug:
                print(f"Move Left (valid = {self.validPosition('left')}\n")
            if self.validPosition('left'):
                self.current_shape.x -= 1

        if display or debug:
            self.displayRows(clearing=clearing)
        if debug:
            print(f"Move Down (valid = {self.validPosition('down')}\n")
        if self.validPosition('down'):
            self.current_shape.y -= 1
        else:
            self.setRock()
            falling = False

        if display or debug:
            self.displayRows(clearing=clearing)

        if debug:
            print('*'*40)
            input("Enter to continue")
            os.system('clear')

        rock = Chamber.SteadyRock(
            self.current_shape.name, self.sequence.val(), self.env_state(50))
        self.sequence.next()
        return (falling, rock)

    def validPosition(self, direction):
        test_x = 0
        test_y = 0

        match direction:
            case 'left':
                test_x = -1
            case 'right':
                test_x = 1
            case 'down':
                test_y = -1
            case 'up':
                test_y = 1

        test_x += self.current_shape.x
        test_y += self.current_shape.y

        test_bounds = Shape.Bounds(
            test_x, test_x + self.current_shape.width, test_y, test_y + self.current_shape.height)

        # Is future position in the grid
        if test_bounds.y1 < 0:
            return False
        if test_bounds.x1 < 0 or test_bounds.x2 > 7:
            return False

        # Is the future position clear of all obstacles
        if test_bounds.y1 > self.getHighestRock():
            return True

        # test future position by each co-ordinate pair
        shape_bounds = self.current_shape.bounds()
        for shape_y, test_y in zip([*range(shape_bounds.y1, shape_bounds.y2+1)], [*range(test_bounds.y1, test_bounds.y2+1)]):
            for shape_x, test_x in zip([*range(shape_bounds.x1, shape_bounds.x2+1)], [*range(test_bounds.x1, test_bounds.x2+1)]):
                if self.current_shape.lookup(shape_x, shape_y) == 2 and self.lookup(test_x, test_y) == 1:
                    return False

        return True

    def addNextShape(self):
        next_shape = self.getNextShape()
        start_x = 2
        start_y = self.getHighestRock() + 3
        self.current_shape = next_shape.trackedCopy(start_x, start_y)
        req_rows = -(len(self.rows) - self.current_shape.bounds().y2 - 2)
        if req_rows > 0:
            self.addBlankRow(req_rows)

    def lookup(self, x, y, include_shape=False):
        shape_xr = range(self.current_shape.x,
                         self.current_shape.x + self.current_shape.width)
        shape_yr = range(self.current_shape.y,
                         self.current_shape.y + self.current_shape.height)
        if y in shape_yr and x in shape_xr and include_shape:
            return max(self.rows[y][x], self.current_shape.lookup(x, y))
        return self.rows[y][x]

    # utils
    def setRock(self):
        bounds = self.current_shape.bounds()
        for y in range(bounds.y1, bounds.y2+1):
            for x in range(bounds.x1, bounds.x2+1):
                self.rows[y][x] = max(self.current_shape.lookup(
                    x, y) - 1, self.lookup(x, y))
        self.addNextShape()
        self.heights.append(self.getHighestRock())
        # self.displayRows(all = True)

    def getHighestRock(self):
        for y in range(len(self.rows)-1, 0-1, -1):
            if 1 in self.rows[y]:
                return y + 1
        return 0

    def getNextShape(self):
        shape = self.shapes[self.shape_index]
        self.shape_index = (self.shape_index + 1) % len(self.shapes)
        return shape
    
    def prevShape(self):
        self.shape_index = (self.shape_index + 1) % len(self.shapes)

    def addBlankRow(self, number=1):
        for _ in range(number):
            self.rows.append([0, 0, 0, 0, 0, 0, 0])

    def env_state(self, n_rows):
        h = self.getHighestRock()
        return tuple(int(''.join([str(x) for x in y]), 2) for y in self.rows[h-n_rows:h])

    # Visualisation
    def displayRows(self, all=False, clearing='both'):
        if clearing == 'both' or clearing == 'start':
            os.system('clear')
        shape_bounds = self.current_shape.bounds()
        if all:
            start = 0
            finish = len(self.rows)-2
        else:
            start = max(0, shape_bounds.y1 - 5)
            finish = min(len(self.rows)-2, shape_bounds.y2 + 2)
        screen = ''
        if start != 0:
            screen += '      0123456\n'
        if start not in range(len(self.rows)) or finish not in range(len(self.rows)):
            return IndexError
        for i in range(finish+1, start-1, -1):
            screen += f"{i:04} {self.rowString(i)}\n"
        if start == 0:
            screen += '     +-------+\n'
            screen += '      0123456\n'
        screen += '\n'
        print(screen)
        time.sleep(0.1)
        if clearing == 'both' or clearing == 'end':
            os.system('clear')

    def rowString(self, y):
        return ''.join(['|', *[self.interpretInt(self.lookup(x, y, include_shape=True)) for x in range(len(self.rows[y]))], '|'])

    def interpretInt(self, input):
        values = {0: '.', 1: '#', 2: '@'}
        return values[input]


def interpretString(input):
    fields = input.strip().split(':')
    name = fields.pop(0).strip()
    array = [[int(x) for x in y.strip().split(' ')] for y in fields]
    return Shape(name, array)


shapes_list = [interpretString(i) for i in open('day17-shapes.txt')]
seq_input = open('day17.txt').read().strip()

seq = Sequence(seq_input)

chamber = Chamber(shapes_list, seq)
chamber.addNextShape()
answer = chamber.dropRocks(2022, debug=False)


shapes_list = [interpretString(i) for i in open('day17-shapes.txt')]
seq_input = open('day17.txt').read().strip()

seq = Sequence(seq_input)

chamber = Chamber(shapes_list, seq)
chamber.addNextShape()
answer = chamber.dropRocks(1000000000000, debug=False)
print(answer)