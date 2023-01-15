from util.inputs import parse_input
from visibility_grid import VisGrid
from visualisation import create_visualisation
import numpy as np
from random import random,getrandbits
from math import pi, sin, radians, degrees

def gen_test_case(width, height):
    horizontal_func = lambda x:sin((1/(width-1))*pi*x)*5
    vertical_func = lambda y:sin((1/(height-1))*pi*y)*5
    walk = lambda : (random() - 0.5) * 2 
    horizontals = np.array([[random() * horizontal_func(x) + walk() for x in range(width)] for y in range(height)]).reshape(height,width)
    verticals = np.rot90(np.array([[random() * vertical_func(y) + walk() for y in range(height)] for x in range(width)]))
    output = np.clip((horizontals+verticals),0,9).astype(int)
    return output


def record():
    # grid = VisGrid(parse_input(example=True), (100, 5, 20))
    test_case = gen_test_case(20,20)
    grid = VisGrid(test_case, (20, 1, 20))
    grid.start_recording(record_video=True)
    grid.sleep(60)
    grid.count_visible()
    grid.sleep(60)
    grid.stop_recording()


def main():
    grid = VisGrid(parse_input())
    print(f"Part 1: result = {grid.count_visible()}, expected value: 1840")
    print(
        f"Part 2: result = {grid.highest_vis_score()}, expected value: 405769")


if __name__ == '__main__':
    # main()
    record()
    # gen_test_case(10, 10)
