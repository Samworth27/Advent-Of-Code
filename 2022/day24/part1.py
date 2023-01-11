from util.grid import Grid, Point
from util.vector import Vector
from util.input_parsing import parse_input
from enum import Enum

import curses
from curses import wrapper


from time import perf_counter, perf_counter_ns, sleep


def print_array(array):
    draw_lookup = {
        Tiles.wall: '\u2593',
        Tiles.ground: ' ',
        Tiles.blizzard_north: '\u25B3',
        Tiles.blizzard_east: '\u25B7',
        Tiles.blizzard_south: '\u25BD',
        Tiles.blizzard_west: '\u25C1',
        Tiles.expedition: 'E'
    }

    for y, row in enumerate(array):
        # for x, point in enumerate(row):
        # print((x,y),point)
        _row = [draw_lookup[x.draw_value] if x.draw_value in draw_lookup else str(
            x.draw_value) for x in row]
        print(''.join(_row))
    print('')


def curses_print_array(screen, array):
    draw_lookup = {
        Tiles.wall: ('\u2588',3),
        Tiles.ground: (' ',0),
        Tiles.blizzard_north: ('\u2591',1),
        Tiles.blizzard_east: ('\u2591',1),
        Tiles.blizzard_south: ('\u2591',1),
        Tiles.blizzard_west: ('\u2591',1),
        2: ('\u2592',1),
        3: ('\u2593',1),
        4: ('\u2593',1),
        Tiles.expedition: ('\u25CF',2)
    }

    for y, row in enumerate(array):
        for x, point in enumerate(row):
            char, colour = draw_lookup[point.draw_value] if point.draw_value in draw_lookup else str(
                point.draw_value)
            screen.addch(y, x, char, curses.color_pair(colour))
    screen.refresh(0, 0, 0, 0, len(array), len(array[0]))


class Tiles(Enum):
    wall = '#'
    ground = '.'
    blizzard_north = '^'
    blizzard_east = '>'
    blizzard_south = 'v'
    blizzard_west = '<'
    expedition = 'E'


class Cardinals(Enum):
    north = Vector.NORTH
    east = Vector.EAST
    south = Vector.SOUTH
    west = Vector.WEST


class Expedition:
    def __init__(self, position: Vector, step):
        self.position = position
        self.step = step
        self.draw_value = Tiles.expedition

        self.path = []

    def __repr__(self):
        return f"Expedition: pos {(self.position.x,self.position.y)} step:{self.step}"


class Blizzard:
    instance_count = 0

    def __init__(self, position: Vector, direction: Cardinals, draw_value: str):
        self.id = self.get_id()
        self.position = position
        self.direction = direction
        self.draw_value = draw_value

    def move(self, bounds):
        x_min, x_max, y_min, y_max = bounds
        x_min += 1
        x_max -= 1
        y_min += 1
        target_position = self.position + self.direction.value
        width = x_max - x_min + 1
        height = y_max - y_min
        self.position = Vector(((target_position.x_int - 1) %
                               width)+1, ((target_position.y_int - 1) % height)+1)

    def __repr__(self):
        return f"Blizzard {self.id} Position: {self.position} Direction: {self.direction}"

    def __str__(self):
        return f"Blizzard {self.id} {self.position} {self.direction}"

    @classmethod
    def get_id(cls):
        id = cls.instance_count
        cls.instance_count += 1
        return id


class BlizzardMap(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._step = 0
        self._stage = 0
        self.initialise_blizzards()
        self._expeditions = {self._step: {
            self.expedition_start(): Expedition(self.expedition_start(), self._step)}}
        self._goal = self.expedition_goal()
        self._answers = []

    # Initialisation Methods

    def initialise_blizzards(self):
        self._blizzards: list[Blizzard] = []
        direction_lookup = {
            Tiles.blizzard_north: Cardinals.north,
            Tiles.blizzard_east: Cardinals.east,
            Tiles.blizzard_south: Cardinals.south,
            Tiles.blizzard_west: Cardinals.west
        }
        for row in super().array:
            for point in row:
                point.draw_value = Tiles(point.draw_value)
                if point.draw_value not in direction_lookup.keys():
                    continue
                new_blizzard = Blizzard(
                    position=point.position,
                    direction=direction_lookup[point.draw_value],
                    draw_value=point.draw_value)
                self._blizzards.append(new_blizzard)
                self[point.position] = Point(
                    position=point.position, draw_value=Tiles.ground)

    def expedition_start(self):
        for x, point in enumerate(super().array[0]):
            if point.draw_value == Tiles.ground:
                return Vector(x, 0)

    def expedition_goal(self):
        for x, point in enumerate(super().array[-1]):
            if point.draw_value == Tiles.ground:
                return Vector(x, self.bounds.y_max)

    # Main Methods
    def run_solver(self, limit=1000):
        for i in range(limit):
            if self.step():
                return self._step

    def step(self):
        step_start = perf_counter()
        self.move_all_blizzards_once()
        self.move_expeditions()
        step_end = perf_counter()
        # print(f"Step {self._step} completed in {step_end-step_start} {len(self._expeditions[self._step])} expeditions")
        fastest = self.expedition_finished()
        if fastest:
            self._answers.append(self._step)
            match self._stage:
                case 0:
                    self._expeditions[self._step + 1] = {fastest.position: fastest}
                    self._goal = self.expedition_start()
                    self._stage = 1
                
                case 1:
                    self._expeditions[self._step + 1 ] = {fastest.position: fastest}
                    self._goal = self.expedition_goal()
                    self._stage = 2
                
                case 2:
                    return True
        self._step += 1
            

    def move_all_blizzards_once(self):
        bounds = super().bounds
        for blizzard in self._blizzards:
            blizzard.move(bounds)

    def move_expeditions(self):
        points = self.points
        for expedition in self._expeditions[self._step].values():
            moved = False
            for direction in Cardinals:
                candidate = expedition.position + direction.value
                if candidate not in points.keys():
                    # print(f"{direction}: {candidate} Not in Bounds")
                    continue
                if points[candidate].draw_value != Tiles.ground:
                    # print(f"{direction}: {candidate} {points[candidate].draw_value} not open ground")
                    continue
                # print(f'{direction}: {candidate} Valid')
                self.add_expedition(candidate)
                moved = True
            # include current position
            if points[expedition.position].draw_value == Tiles.ground:
                # print(f"{Expedition} Stayed Still")
                self.add_expedition(expedition.position.copy)

    def expedition_finished(self):
        for expedition in self._expeditions[self._step].keys():
            if expedition == self._goal:
                return self._expeditions[self._step][expedition]

    def in_bounds(self, point):
        if point.x < self.bounds.x_min and point.x > self.bounds.x_max:
            return False
        if point.y < self.bounds.y_min and point.y > self.bounds.y_max:
            return False
        return True

    def add_expedition(self, position):
        if self._step + 1 not in self._expeditions.keys():
            self._expeditions[self._step + 1] = dict()
        self._expeditions[self._step + 1][position] = Expedition(position, self._step+1)

    @property
    def array(self):
        blank_map = super().array
        for blizzard in self._blizzards:
            pos = blizzard.position
            point = blank_map[pos.y_int][pos.x_int]
            # print(blizzard.id,point.position,type(point),type(point) == Blizzard)
            if type(point) == Blizzard:
                blank_map[pos.y_int][pos.x_int] = Point(pos, 2)
            elif type(point) == Point and type(point.draw_value) == int:
                blank_map[pos.y_int][pos.x_int].draw_value += 1
            else:
                blank_map[pos.y_int][pos.x_int] = blizzard
        for expedition in self._expeditions[self._step].values():
            blank_map[expedition.position.y_int][expedition.position.x_int] = expedition

        return blank_map

    @property
    def points(self):
        _points = {**self._points}
        for blizzard in self._blizzards:
            _points[blizzard.position] = blizzard
        return _points
    
    @property
    def answer(self):
        return '\n'.join([f"Stage: {stage} took {time - (self._answers[stage-1] if stage > 1 else 0)} minutes. Total time: {time} minutes" for stage, time in enumerate(self._answers)])

def curses_main(screen: curses.window):
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    pad = curses.newpad(300, 300)
    curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_MAGENTA,curses.COLOR_BLACK)

    test = BlizzardMap(parse_input(example=False))
    screen.getkey()
    curses_print_array(pad,test.array)
    for _ in range(1000):
        if test.step():
            screen.clear()
            screen.addstr(test.answer)
            screen.getkey()
            break
        # screen.getkey()
        curses_print_array(pad,test.array)
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    print(test._step)


def main():
    test = BlizzardMap(parse_input(example=False))
    print(test.run_solver(1000))


if __name__ == '__main__':
    wrapper(curses_main)
    # main()
