from util.classes.grid import Grid, neighbour_positions, Cardinals
from util.functions.input_parsing import parse_input

grid = Grid(parse_input(example=False))
print(f"Part 1: {grid.run(20)}")
grid = Grid(parse_input(example=False))
print(f"Part 2: {grid.run(2000)}")
