from util.inputs import parse_input
from visibility_grid import VisGrid
from visualisation import create_visualisation
import numpy as np
from random import random,getrandbits


def gen_test_case(width, height):
    n_width = 10/width 
    c_width = width/2
    dist_func = lambda x:(width - abs(c_width - x)-c_width)*n_width
    horizontals = np.array([[random() * dist_func(x) if getrandbits(1) else random()*5 for x in range(width)] for y in range(height)]).reshape(height,width)
    verticals = np.array([[random() * dist_func(x)if getrandbits(1) else random()*5 for x in range(height)] for y in range(width)]).reshape(height,width)

    output = np.clip((horizontals + verticals),0,9).astype(int)
    print(output)
    return output


def record():
    # grid = VisGrid(parse_input(example=True), (100, 5, 20))
    test_case = gen_test_case(20,20)
    print(test_case)
    grid = VisGrid(test_case, (25, 5, 20))
    grid.start_recording(record_video=True)
    grid.record_state()
    grid.count_visible()
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
