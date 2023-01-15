import numpy as np
from random import random
from math import pi, sin
from util.inputs import parse_input
from visibility_grid import VisGrid

def gen_test_case(width, height):
    horizontal_func = lambda x:sin((1/(width-1))*pi*x)*5
    vertical_func = lambda y:sin((1/(height-1))*pi*y)*5
    walk = lambda : (random() - 0.5) * 2 
    horizontals = np.array([[random() * horizontal_func(x) + walk() for x in range(width)] for y in range(height)]).reshape(height,width)
    verticals = np.rot90(np.array([[random() * vertical_func(y) + walk() for y in range(height)] for x in range(width)]))
    output = np.clip((horizontals+verticals),0,9).astype(int)
    return output


def record(example = True, width = 0, height = 0):
    # grid = VisGrid(parse_input(example=True), (100, 5, 20))
    test_case = gen_test_case(10,7)
    grid = VisGrid(test_case, (10, 3, 40))
    grid.start_recording(record_video=True)
    grid.sleep(60)
    grid.count_visible()
    grid.sleep(60)
    grid.stop_recording()
    
if __name__ == '__main__':
    record()