from aoc_util.inputs import parse_input, fields
import pygame
from random import getrandbits
import numpy as np


DAY = 6
YEAR = 2015

WINDOW_SIZE = (1000, 1000)

ON = 1
OFF = 0


def show_frame(image):
    
    screen = pygame.display.get_surface()
    screen.fill((0,0,0))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    # while 1:
    #     event = pygame.event.wait()
    #     if event.type == pygame.QUIT:
    #         raise SystemExit
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         break


def main(data:list, part1=True):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Advent Of Code 2015 - Day 06")

    run = True
    # array = np.random.random((1000,1000))
    array = np.zeros((1000,1000))
    surface = pygame.surfarray.make_surface(array)
    show_frame(surface)
    screen.fill((0,0,0))
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if len(data) == 0:
            break
        inst, (x0, y0), (x1, y1) = data.pop(0)
        inst_from = (x0, y0)
        inst_to = (x1, y1)
        if inst == 'on':
            if part1:
                array[y0:y1+1, x0:x1+1] = ON
            else:
                array[y0:y1+1, x0:x1+1] += 1
        if inst == 'off':
            if part1:
                array[y0:y1+1, x0:x1+1] = OFF
            else:
                array[y0:y1+1, x0:x1+1] -= 1
                mask = array[y0:y1+1, x0:x1+1] < 0
                array[y0:y1+1, x0:x1+1][mask] = 0
        if inst == 'toggle':
            if part1:
                array[y0:y1+1, x0:x1+1] = array[y0:y1+1, x0:x1+1] == 0
            else:
                array[y0:y1+1, x0:x1+1] += 2
            
        surface = pygame.surfarray.make_surface(array)
        show_frame(surface)

        pygame.display.flip()
        clock.tick(120)
        
    return int(sum(sum(array)))

    pygame.quit()


def parse_function(line):
    _fields = fields(line)
    if len(_fields) == 5:
        del _fields[0]
    _fields[1] = tuple(int(x) for x in _fields[1].split(','))
    _fields[3] = tuple(int(x) for x in _fields[3].split(','))

    del _fields[2]

    return tuple(_fields)

if __name__ == '__main__':

    data = parse_input((DAY,YEAR),parse_function)
    print(f"Part 1 result = {main(data)}")
    data = parse_input((DAY,YEAR),parse_function)
    print(f"Part 2 result = {main(data, part1=False)}")
