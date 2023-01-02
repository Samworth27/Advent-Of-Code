from enum import Enum
from copy import copy, deepcopy


# class Resource(Enum):
#     ore = 0
#     clay = 1
#     obsidian = 2
#     geode = 3


# class Draw():
#     class Line():
#         hr = '\u2500'
#         vr = '\u2502'
#         both = '\u253C'

#     class Corner():
#         tl = '\u250C'
#         tr = '\u2510'
#         bl = '\u2514'
#         br = '\u2518'

#     class T():
#         left = '\u251C'
#         right = '\u2524'
#         top = '\u252C'
#         bottom = '\u2534'


# class ResourceContainer():

#     def __init__(self, initial_geode_amount=0, initial_obsidian_amount=0, initial_clay_amount=0, initial_ore_amount=0):
#         self._inventory = {
#             Resource.geode: initial_geode_amount,
#             Resource.obsidian: initial_obsidian_amount,
#             Resource.clay: initial_clay_amount,
#             Resource.ore: initial_ore_amount
#         }

#     def __setitem__(self, resource, value):
#         self._inventory[resource] = value

#     def __getitem__(self, resource):
#         return self._inventory[resource]

#     def keys(self):
#         return self._inventory.keys()

#     def values(self):
#         return self._inventory.values()

#     def items(self):
#         return zip(self.keys(),self.values())

#     def __repr__(self):
#         # return str(self._inventory)
#         inventory_string = '\n'.join(
#             [f"\t{key.name}: {value}" for key, value in self._inventory.items()])
#         return (f"{inventory_string}\n")

#     def __add__(self, value2):
#         return ResourceContainer(*[x+y for x, y in zip(self._inventory.values(), value2._inventory.values())])

#     def __sub__(self, value2):
#         return ResourceContainer(*[x-y for x, y in zip(self._inventory.values(), value2._inventory.values())])


# class RobotFactory():
#     def __init__(self, id, geode_robot_cost, obsidian_robot_cost, clay_robot_cost, ore_robot_cost):
#         self.id = id
#         self.robot_costs = ResourceContainer(
#             geode_robot_cost, obsidian_robot_cost, clay_robot_cost, ore_robot_cost)
#         self.resources = ResourceContainer()
#         self.robots = ResourceContainer(initial_ore_amount=1)
#         self.building = None
#         self.max_production = self.calculate_max_production()

#     def calculate_max_production(self):
#         production_max = ResourceContainer()
#         for resource_type in self.resources.keys():
#             max_cost = 0
#             for robot_type in self.robot_costs.values():
#                 max_cost = max(robot_type[resource_type], max_cost)
#             production_max[resource_type] = max_cost
#         return production_max

#     def at_max_production(self, resource_type):
#         if resource_type == None or resource_type == Resource.geode: return False
#         return self.robots[resource_type] >= self.max_production[resource_type]

#     def start_build(self, robot_type):
#         if robot_type:
#             self.building = robot_type
#             self.resources -= self.robot_costs[robot_type]

#     def finish_build(self):
#         if self.building:
#             self.robots[self.building] = self.robots[self.building]+1
#             self.building = None

#     def buildable_amount(self,robot_type):
#         cost = self.robot_costs[robot_type]
#         return min([self.resources[r]//cost[r] for r in self.resources.keys() if cost[r] > 0])

#     def can_build(self, robot_type):
#         return self.buildable_amount(robot_type) > 0

#     def build_options(self):
#         options = [robot_type for robot_type in self.robot_costs.keys() if self.can_build(robot_type)]+[None]
#         return options

#     def collect_resources(self):
#         self.resources += self.robots

#     def hypothetical_best(self, time_remaining):
#         geodes = self.resources[Resource.geode]
#         geode_bots = self.robots[Resource.geode]
#         best = geodes + (time_remaining*geode_bots)+(time_remaining*(time_remaining-1))/2
#         return best


#     def costs_repr(self):
#         return ''.join([f"{robot.name} robot:\n {cost}" for robot, cost in self.robot_costs.items()])

#     def __repr__(self):

#         titles = f"{'type':>20}{Draw.Line.vr}{'inventory':>19}{Draw.Line.vr}{'robots':>19}{Draw.Line.vr}\n{Draw.Line.hr*20}{Draw.Line.both}{Draw.Line.hr*19}{Draw.Line.both}{Draw.Line.hr*19}{Draw.T.right}"
#         lines = '\n'.join([f"{name.name: >20}{Draw.Line.vr}{resource:>19}{Draw.Line.vr}{robot:>19}{Draw.Line.vr}" for name,
#                           resource, robot in zip(self.resources.keys(), self.resources.values(), self.robots.values())])
#         return f"Factory {self.id}\n{titles}\n{lines}"

#         # return f"Robot Factory {self.id}\nResources:\n{self.resources}\nRobots:\n{self.robots}"


# def read_file(example=False) -> dict[RobotFactory]:
#     path = 'day19-example.txt' if example else 'day19.txt'
#     blueprints = {}
#     with open(path)as file:
#         for line in file:
#             fields = line.strip().split(' ')
#             id = int(fields[1][0:-1])
#             ore_robot_cost = ResourceContainer(initial_ore_amount=int(fields[6]))
#             clay_robot_cost = ResourceContainer(initial_ore_amount=int(fields[12]))
#             obsidian_robot_cost = ResourceContainer(
#                 initial_ore_amount=int(fields[18]), initial_clay_amount=int(fields[21]))
#             geode_robot_cost = ResourceContainer(
#                 initial_ore_amount=int(fields[27]), initial_obsidian_amount=int(fields[30]))
#             blueprints[id] = RobotFactory(
#                 id, geode_robot_cost, obsidian_robot_cost, clay_robot_cost, ore_robot_cost)
#     return blueprints


# i = 0
# def best_path(factory:RobotFactory, step = 24, path=[(None,"0/0")], record  = (0,0), waits = 0):
#     global i

#     best,earliest_geode = record

#     if factory.resources[Resource.geode] == 1 and step > earliest_geode:
#         earliest_geode = max(step,earliest_geode)

#     if step == 1:
#         factory.collect_resources()
#         # print(f"\nstep: {24 - step},geodes: {factory.resources[Resource.geode]}, {best=}, {earliest_geode=}, {waits=}, \n{path}")
#         return (factory.resources[Resource.geode],earliest_geode)

#     factory.collect_resources()
#     factory.finish_build()
#     step = step - 1

#     if i % 10000 == 0:
#         print(f"{i}\nstep: {24 - step},geodes: {factory.resources[Resource.geode]}, {best=}, {earliest_geode=}, {waits=}, \n{[i[0] for i in path]}\n{[i[1] for i in path]}")

#     i += 1


#     build_options = factory.build_options()
#     for option_index,robot_type in enumerate(build_options):

#         if robot_type == None and len(build_options) > 1:
#             waits = waits + 1
#         else:
#             waits = 0

#         if waits > 1:
#             continue
#         new_factory = deepcopy(factory)
#         if factory.hypothetical_best(step) >= best and not factory.at_max_production(robot_type):
#             new_factory.start_build(robot_type)
#             option_string = f"{option_index+1}/{len(build_options)}"
#             new_best, new_earliest = best_path(new_factory, step = step, path=[*path,(robot_type.name,option_string) if robot_type else (robot_type,option_string)], record = (best,earliest_geode), waits=waits)
#             best = max(best, new_best)
#             earliest_geode = max(earliest_geode, new_earliest)
#     return best, earliest_geode
#     # start build


class Resource(Enum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3


def read_file(example=False):
    path = 'day19-example.txt' if example else 'day19.txt'
    blueprints = {}
    with open(path)as file:
        for line in file:
            fields = line.strip().split(' ')
            id = int(fields[1][0:-1])
            robot_costs = {
                'ore': [int(fields[6]), 0, 0, 0],
                'clay': [int(fields[12]), 0, 0, 0],
                'obsidian': [int(fields[18]), int(fields[21]), 0, 0],
                'geode': [int(fields[27]), 0, int(fields[30]), 0],
            }
            blueprints[id] = robot_costs
    return blueprints


start_state = {
    'blueprint': 0,
    'resources': [0, 0, 0, 0],
    'robots': [1, 0, 0, 0],
    'building': None,
    'step': 23,
    'path': [None],
    'best': 0,
    'previous_state': None
}


def start_build(state, robot_type, robot_costs):
    new_state = deepcopy(state)
    if robot_type:
        new_state['resources'] = [x-y for x,
                              y in zip(new_state['resources'], robot_costs[robot_type])]
    new_state['building'] = robot_type
    return new_state


def finish_build(state):
    new_state = deepcopy(state)
    if new_state['building']:
        robot_type = Resource[new_state['building']]
        new_state['robots'][robot_type.value] += 1
        # new_state['building'] = None
    return new_state


def gather_resources(state):
    new_state = deepcopy(state)
    new_state['resources'] = [x+y for x,
                              y in zip(new_state['resources'], new_state['robots'])]
    return new_state


def hypothetical_best(state):
    geodes = state['resources'][Resource.geode.value]
    geode_bots = state['robots'][Resource.geode.value]
    time_remaining = state['step']
    best = int(geodes + (time_remaining*geode_bots) +
               (time_remaining*(time_remaining-1))/2)
    return best


def affordable(available_resources, robot_cost):
    return all([a_r >= r_c for a_r, r_c in zip(available_resources, robot_cost)])


def get_options(state, robot_costs):
    options = [robot_type for robot_type, cost in robot_costs.items(
    ) if affordable(state['resources'], cost)]
    if len(options) < 4:
        options += [None]
    return options

max_costs_memo = {}

def max_costs(state, robot_costs):
    blueprintID = state['blueprint']
    if blueprintID not in max_costs_memo:
        max_costs_memo[blueprintID] = [int(max(a,b,c,d)) for a,b,c,d in zip(*robot_costs.values())]
    return max_costs_memo[blueprintID]

def limit_storage(state,robot_costs):
    for max_cost, current_storage in zip(max_costs(state, robot_costs)[:3], state['resources'][:3]):
        if current_storage >= max_cost:
           return True
       
    return False
      
def limit_production(state, robot_costs):
    for max_cost, current_production in zip(max_costs(state, robot_costs)[:3], state['robots'][:3]):
        if current_production >= max_cost:
           return True
       
    return False

def limit_waiting(option,options, state):
    print(option == None, not all(state['path'][-5:]),len(options) > 1)
    if option == None and not all(state['path'][-5:]) and len(options) > 1:
        return True
    return False


pruned = 0

def prune(option,options, state, robot_costs):
    global pruned
    if hypothetical_best(state) < state['best']:
        pruned += 1
        return True
    if limit_storage(state,robot_costs):
        if option is not None:
            pruned += 1
            return True
    if limit_production(state,robot_costs):
        if len(options) > 1:
            pruned += 1
            return True
    # if limit_waiting(option,options,state):
    #     print(option,options)
    #     return True
    return False

iterations = 0

def best_path(state, robot_costs, paths = []):
    global iterations
    iterations += 1
    state = gather_resources(state)
    # print(iterations,pruned, pruned/(pruned+iterations)*100)
    if state['step'] == 0:
        print(state['resources'][Resource.geode.value], state['best'], state['path'])
        print(iterations,pruned, pruned/(pruned+iterations)*100)
        paths.append(state)
        return state['resources'][Resource.geode.value]
    # gather resources

    # Finish Build
    state = finish_build(state)

    state['previous_state'] = deepcopy(state)

    options = get_options(state, robot_costs)

    best = state['best']

    for robot_type in options:
        new_state = start_build(state, robot_type, robot_costs)
        if prune(robot_type,options, new_state, robot_costs):
            continue
        new_state['path'] = new_state['path'] + [robot_type]
        new_state['step'] = new_state['step'] - 1
        new_state['best'] = best
        best = max(best, best_path(state=new_state, robot_costs=robot_costs,paths = paths))

    state['best'] = best
    return best

def get_replay_frames(state):
    frame = state
    frames = [copy(frame)]
    frames[0]['previous_state'] = None
    while frame['previous_state']:
        frames.append(copy(frame['previous_state']))
        frames[-1]['previous_state'] = None
        frame = frame['previous_state']
    return frames

def replay(frames):
    for frame in reversed(frames):
        print(f"== Minute {24-frame['step']}")
        if frame['building']:
            print(f"Building {frame['building']} robot")
        for i, robot in enumerate(frame['robots']):
            if robot > 0:
                print(f"{robot} {Resource(i).name}-collecting robot collects {robot} ore; you now have {frame['resources'][i]} {Resource(i).name}")
            
            
        input("enter to continue")

def main():
    test = read_file(True)
    paths = []
    print(best_path(start_state, test[1],paths))
    
    # replay(get_replay_frames(paths[1]))


if __name__ == '__main__':
    main()
