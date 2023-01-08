from os import system
from util.classes import MapTiles, PlayerTiles, PathTiles

def read_file(example=False, test_case='example'):
    path = f'./test_cases/tc_{test_case}.txt' if example else './test_cases/input.txt'
    with open(path) as file:
        for line in file:
            yield line.strip('\n')
            
def clear_terminal():
    system('clear')
    
def process_input(example=False, test_case='example'):
    lines = list(read_file(example=example,test_case=test_case))
    map = []
    instructions = lines[-1]
    map_width = max([len(row) for row in lines[:-2]])
    for line in lines[:-2]:
        char_values = {' ': MapTiles.void,
                       '.': MapTiles.tile,
                       '#': MapTiles.wall}

        extra_void = map_width - len(line)
        map.append([*[char_values[char]
                    for char in line], *[MapTiles.void]*extra_void])
    
    return map, instructions

def part1_score(player):
    row_score = (player.location.imag+1) * 1000
    col_score = (player.location.real+1) * 4
    direction_score = {
        PlayerTiles.right:0,
        PlayerTiles.down:1,
        PlayerTiles.left:2,
        PlayerTiles.up:3
    }[player.direction]
    
    return int(row_score + col_score + direction_score)