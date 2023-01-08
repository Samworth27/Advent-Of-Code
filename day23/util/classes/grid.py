from collections import defaultdict
from enum import Enum
from ..functions.single_use_named_tuple import single_use_named_tuple

VOID = '  '
ELF = '#'  # '\u25C8'
SHADOW = '.'  # '\u25CC'


class Cardinals(Enum):
    North = 0
    South = 1
    West = 2
    East = 3


def calc_bounds(points):
    return single_use_named_tuple('Bounds', **{
        'x_min': int(min(x.real for x in points)),
        'x_max': int(max(x.real for x in points)),
        'y_min': int(min(x.imag for x in points)),
        'y_max': int(max(x.imag for x in points))
    })


def neighbour_positions(centre: complex, direction=None):
    full = [-1, 0, 1]
    match direction:
        case Cardinals.North:
            x_range = full
            y_range = [-1]
        case Cardinals.East:
            x_range = [1]
            y_range = full
        case Cardinals.South:
            x_range = full
            y_range = [1]
        case Cardinals.West:
            x_range = [-1]
            y_range = full
        case _:
            x_range = full
            y_range = full

    return list(set([centre + (x + y*1j) for x in x_range for y in y_range])-set([centre]))


def calc_move(position, direction):
    options = {
        Cardinals.North: 0 - 1j,
        Cardinals.South: 0 + 1j,
        Cardinals.West: -1 + 0j,
        Cardinals.East: 1 + 0j
    }
    return position + options[direction]


class Grid():
    def __init__(self, input):
        self.positions = defaultdict(lambda: str(' '))
        elf_count = 0
        for y, row in enumerate(input):
            for x, value in enumerate(row):
                if value == '#':
                    self.positions[x+y*1j] = elf_count
                    elf_count += 1
        self.bounds = calc_bounds(self.positions)
        self.proposal_order = [Cardinals.North,
                               Cardinals.South, Cardinals.West, Cardinals.East]
        self.proposed_move = {}
        self.proposal_counts = {}
        self.previous = {}
        self.step = 0
        # self.print()
        # print(f"Start State | Score: {self.score()}")

    def run(self, number_of_rounds):
        for _ in range(number_of_rounds):
            if self.run_round():
                return self.step
        return self.score()

    def run_round(self):
        # print(
            # f"*******************\nRound {self.step} Proposal Order {self.proposal_order}")
        self.step += 1
        waiting = self.propose_moves()
        self.make_moves()
        self.bounds = calc_bounds(self.positions)
        # self.print()
        self.reset()
        print(
            f"End Round {self.step} Score: {self.score()} Waiting: {waiting}/{len(self.positions)}\n*******************")
        if waiting == len(self.positions):
            return True
        return False

    def propose_moves(self):
        waiting = 0
        for elf, i in sorted(self.positions.items(), key=lambda x: x[1]):
            if self.has_space(elf):
                waiting += 1
                continue
            proposed_direction = self.propose(elf)
            proposed_position = calc_move(
                elf, proposed_direction) if proposed_direction else None
            # print(f"Elf {i}, proposing to move {proposed_direction.name if proposed_direction else None}, from {elf.real,elf.imag} to {(proposed_position.real,proposed_position.imag) if proposed_position else ''}")
            self.proposed_move[elf] = proposed_position
            if proposed_position in self.proposal_counts:
                self.proposal_counts[proposed_position] += 1
            else:
                self.proposal_counts[proposed_position] = 1
        return waiting

    def make_moves(self):
        for elf, proposed_position in self.proposed_move.items():
            if proposed_position == None:
                continue
            if self.proposal_counts[proposed_position] > 1:
                continue

            self.move(elf, proposed_position)

    def propose(self, elf):
        for direction in self.proposal_order:
            if self.has_space(elf, direction):
                return direction

    def move(self, elf, target_position):

        self.previous[elf] = SHADOW
        self.positions[target_position] = self.positions.pop(elf)

    def rotate_proposal_order(self):
        old = self.proposal_order.pop(0)
        self. proposal_order += [old]

    def reset(self):
        self.rotate_proposal_order()
        self.proposed_move = {}
        self.proposal_counts = {}
        self.previous = {}

    def print(self):
        print("\u253C\u2500\u2500"+"\u253C\u2500\u2500" *
              ((self.bounds.x_max-self.bounds.x_min))+"\u253C")
        for y in range(self.bounds.y_min, self.bounds.y_max+1):
            # print(''.join([self.get_previous(x+y*1j) or f"{self[x + y*1j]:02}" for x in range(min(0,self.bounds.x_min), self.bounds.x_max+1)]))
            print(''.join([f"\u2502{self[x + y*1j]:02}" for x in range(
                self.bounds.x_min, self.bounds.x_max+1)]+['\u2502']))
            print("\u253C\u2500\u2500"+"\u253C\u2500\u2500" *
                  ((self.bounds.x_max-self.bounds.x_min))+"\u253C")

    def has_space(self, position, direction=None):
        # if direction == None:
        #     print([self[p] == VOID for p in neighbour_positions(position, direction)])
        return all([self[p] == VOID for p in neighbour_positions(position, direction)])

    def score(self):
        score = 0
        for y in range(self.bounds.y_min, self.bounds.y_max+1):
            for x in range(self.bounds.x_min, self.bounds.x_max+1):
                if self[x+y*1j] == VOID:
                    score += 1
        return score

    def get_previous(self, value):
        if value in self.previous:
            return self.previous[value]
        else:
            return None

    def __getitem__(self, value):
        default = VOID
        if value in self.positions:
            return self.positions[value]
        else:
            return default
