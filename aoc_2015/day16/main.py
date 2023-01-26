from enum import Enum
from aoc_util.inputs import parse_input, fields
import re

DAY = 16
YEAR = 2015


class Compounds(Enum):
    children = 0
    cats = 1
    samoyeds = 2
    pomeranians = 3
    akitas = 4
    vizslas = 5
    goldfish = 6
    trees = 7
    cars = 8
    perfumes = 9


MARKERS = [
    (Compounds.children, 3),
    (Compounds.cats, 7),
    (Compounds.samoyeds, 2),
    (Compounds.pomeranians, 3),
    (Compounds.akitas, 0),
    (Compounds.vizslas, 0),
    (Compounds.goldfish, 5),
    (Compounds.trees, 3),
    (Compounds.cars, 2),
    (Compounds.perfumes, 2)

]


class Candidate:
    members = set()

    def __init__(self, name, markers):
        self.name = name
        self.markers = markers
        self.valid = True
        self.members.add(self)

    def check(self, marker):
        compound, count = marker
        if compound in self.markers:
            if self.markers[compound] != count:
                self.valid = False

    def check_2(self, marker):
        compound, count = marker
        if compound in self.markers:
            if compound in [Compounds.cats, Compounds.trees]:
                if self.markers[compound] <= count:
                    self.valid = False
            elif compound in [Compounds.pomeranians, Compounds.goldfish]:
                if self.markers[compound] >= count:
                    self.valid = False
            else:
                if self.markers[compound] != count:
                    self.valid = False

    def reset(self):
        self.valid = True

    @classmethod
    def check_members(cls, marker):
        for member in cls.valid_members:
            member.check(marker)

    @classmethod
    def check_members_2(cls, marker):
        for member in cls.valid_members:
            member.check_2(marker)

    @classmethod
    def reset_all(cls):
        for member in cls.members:
            member.reset()

    @classmethod
    @property
    def valid_members(cls):
        return [member for member in cls.members if member.valid]

    def __str__(self):
        return f"{self.name} valid:{self.valid}"

    def __repr__(self):
        return f"<Candidate {str(self)}"


def fields_function(x: str):
    key, value = x.strip().split(':')
    return Compounds[key], int(value)


def parse_function(x: str):
    name, compounds = re.split(
        r'(?<=Sue \d)\:|(?<=Sue \d\d)\:|(?<=Sue \d\d\d)\:', x)
    return Candidate(name, {k: v for k, v in fields(compounds, split_char=',', field_func=fields_function)})


def part1():
    for marker in MARKERS:
        Candidate.check_members(marker)
        # print(f"{len(Candidate.valid_members)} Candidates remaining")
        if len(Candidate.valid_members) == 1:
            return Candidate.valid_members.pop()


def part2():
    for marker in MARKERS:
        Candidate.check_members_2(marker)
        # print(f"{len(Candidate.valid_members)} Candidates remaining")
        if len(Candidate.valid_members) == 1:
            return Candidate.valid_members.pop()


if __name__ == '__main__':
    parse_input((DAY, YEAR), parse_function)
    print(part1().name)
    Candidate.reset_all()
    print(part2().name)
