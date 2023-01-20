from aoc_util.inputs import parse_input
from aoc_util.vector import Vector

DAY = 3
YEAR = 2015

move_lookup = {
    '^': Vector.NORTH,
    '>': Vector.EAST,
    'v': Vector.SOUTH,
    '<':Vector.WEST
    }
def part1(input):
    position = Vector(0,0)
    visited = set([Vector(0,0)])
    for inst in input:
        position += move_lookup[inst]
        visited.add(position.copy)
    return len(visited)

def part2(input):
    position1 = Vector(0,0)
    position2 = Vector(0,0)
    robot_santa = False
    visited = set([Vector(0,0)])
    for inst in input:
        move = move_lookup[inst]
        if robot_santa:
            position2 += move
            visited.add(position2)
            robot_santa = False
        else:
            position1 += move
            visited.add(position1)
            robot_santa = True
    return len(visited)

def test():
    for data, (expected1, expected2) in zip(parse_input('example'),parse_input('expected',lambda x:x.split())):
        result1 = part1(data)
        result2 = part2(data)
        print(f"Result 1: {result1}, expected: {expected1}, match = {result1 == int(expected1)}")
        print(f"Result 2: {result2}, expected: {expected2}, match = {result2 == int(expected2)}")
    
def main():
    for data in parse_input((DAY,YEAR)):
        result1 = part1(data)
        result2 = part2(data)
        print(f"Part 1 result: {result1}, Part 2 result: {result2}")
    
if __name__ == '__main__':
    test()
    main()