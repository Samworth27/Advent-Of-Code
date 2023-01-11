from dataclasses import dataclass, field, asdict, astuple
from enum import Enum
from copy import deepcopy





class Resource(Enum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3


ORE = Resource.ore
CLAY = Resource.clay
OBSIDIAN = Resource.obsidian
GEODE = Resource.geode


@dataclass
class ResourceTracker():
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __getitem__(self, key):
        if key == ORE:
            return self.ore
        if key == CLAY:
            return self.clay
        if key == OBSIDIAN:
            return self.obsidian
        if key == GEODE:
            return self.geode

    def __setitem__(self, key, value):
        if key == ORE:
            self.ore = value
        if key == CLAY:
            self.clay = value
        if key == OBSIDIAN:
            self.obsidian = value
        if key == GEODE:
            self.geode = value

    def __add__(value1, value2):
        return ResourceTracker(value1.ore + value2.ore, value1.clay + value2.clay, value1.obsidian + value2.obsidian, value1.geode + value2.geode)

    def __sub__(value1, value2):
        return ResourceTracker(value1.ore - value2.ore, value1.clay - value2.clay, value1.obsidian - value2.obsidian, value1.geode - value2.geode)


@dataclass
class Blueprint():
    id: int
    costs: dict
    max_costs: dict


@dataclass
class State():
    blueprintID: str
    max_step: int
    step: int = 0
    best: int = 0
    building: Resource = None
    inventory: ResourceTracker = field(
        default_factory=lambda: ResourceTracker(0, 0, 0, 0))
    robots: ResourceTracker = field(
        default_factory=lambda: ResourceTracker(1, 0, 0, 0))
    path: list = field(default_factory=list)

    def start_build(self, robot_type: Resource, robot_costs: dict):
        if robot_type:
            self.inventory -= robot_costs[robot_type]
        self.building = robot_type
        return robot_type
    

    def finish_build(self):
        if self.building:
            self.robots[self.building] += 1
        return self.building

    def gather_resources(self):
        self.inventory += self.robots


    def build_options(self, max_costs: dict):
        filter = {
            ORE: self.robots.ore < max_costs.ore,
            CLAY: self.robots.clay < max_costs.clay,
            OBSIDIAN: self.robots.obsidian < max_costs.obsidian and self.robots.clay > 1,
            GEODE: self.robots.obsidian > 1
        }
        return reversed([k for k, v in filter.items() if v])
    
    
    def hypothetical_best(self):
        geodes = self.inventory.geode
        geode_bots = self.robots.geode
        time_remaining = self.max_step - self.step
        best = int(geodes + (time_remaining*geode_bots) +
                (time_remaining*(time_remaining-1))/2)
        return best

    def copy(self):
        return deepcopy(self)
