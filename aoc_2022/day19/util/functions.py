from util.classes import Resource, Blueprint, ResourceTracker, State
from dataclasses import astuple, asdict


def read_file(example=False):
    path = 'day19-example.txt' if example else 'day19.txt'
    blueprints = {}
    with open(path)as file:
        for line in file:
            fields = line.strip().split(' ')
            id = int(fields[1][0:-1])
            robot_costs = [ResourceTracker(int(fields[6]), 0, 0, 0),
                           ResourceTracker(int(fields[12]), 0, 0, 0),
                           ResourceTracker(
                               int(fields[18]), int(fields[21]), 0, 0),
                           ResourceTracker(
                               int(fields[27]), 0, int(fields[30]), 0),
                           ]
            flat_costs = [astuple(x) for x in robot_costs]
            max_costs = [int(max(a, b, c, d))
                         for a, b, c, d in zip(*flat_costs)]
            blueprints[id] = Blueprint(id, ResourceTracker(
                *robot_costs), ResourceTracker(*max_costs))
    return blueprints


def prepare_state(blueprint, max_steps):
    return State(blueprint.id, max_step=max_steps)

def affordable(available_resources, robot_cost):
    return all([a_r >= r_c for a_r, r_c in zip(astuple(available_resources), astuple(robot_cost))])

def is_vowel(char: str):
    return char in ['a', 'e', 'i', 'o', 'u']


def first_char(string: str):
    return string[0]


def debug_start_build(robot_type, robot_costs):
    if robot_type is None:
        return None
    cost_string = ' and '.join(
        [f"{value} {key}" for key, value in asdict(robot_costs[robot_type]).items() if value > 0])

    a_or_an = f"a{'n' if is_vowel(first_char(robot_type.name)) else ''}"
    print(
        f"Spend {cost_string} to start building {a_or_an} {robot_type.name}-collecting robot.")


def debug_gather(state):
    print('\n'.join([f"{value} {key}-collecting robot{'s' if value>1 else ''} collects {value} {key}; you now have {state.inventory[Resource[key]]} {key}" for key,
          value in asdict(state.robots).items() if value > 0]))


def debug_finish_build(state, robot_type):
    if robot_type is not None:
        print(
            f"The new {robot_type.name}-collecting robot is ready; you now have {state.robots[robot_type]} of them")
