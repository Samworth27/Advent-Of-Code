from util.inputs import parse_input, fields
from collections import namedtuple
from os import system
from time import sleep

Instruction = namedtuple('Instruction', ['count', 'source', 'target'])

def print_stacks(stacks):
    
    tallest_stack = max([len(stack) for stack in stacks.values()])
    max_stack_height = sum([len(stack) for stack in stacks.values()])
    rows = []
    for i in range(max_stack_height):
        new_row = []
        for j, row in sorted(stacks.items()):
            new_row.append(row[i] if i < len(row) else ' ' )
        rows.append(new_row)
        
    system('clear')    
    for row in reversed(rows):
        print(' '.join([f"{f'[{i}]' if i != ' ' else '   '}" for i in row]))

    print(' '.join([f" {i+1} " for i in range(len(stacks))]))
        
def crate_input(index):
    return ((index+1)*4)-3


def interpret_line(line):
    return Instruction(*fields(line, [1, 3, 5], lambda x: int(x)))


def move(stacks, count, source, target):

    source_stack = stacks[source]
    target_stack = stacks[target]

    items = source_stack[-count:]
    stacks[source] = source_stack[:-count]
    target_stack.extend(items)
    #


def main(example=False, part2=False, visualise = False):
    rows = 3 if example else 9
    stacks = {i: [] for i in range(1, rows + 1)}
    building = True
    for line in parse_input(example=example):
        if line == '':
            
            if visualise: print_stacks(stacks)
            continue
        if building:
            if line[1] == '1':
                building = False

                continue
            for i in range(1, rows + 1):
                item = line[crate_input(i-1)]
                if item == ' ':
                    continue
                stacks[i].insert(0, item)
            continue
        instruction = interpret_line(line)
        if part2:
            if visualise: sleep(0.1)
            move(stacks, *instruction)
            if visualise: print_stacks(stacks)
        else:
            for i in range(instruction.count):
                if visualise: sleep(0.1)
                move(stacks, 1, instruction.source, instruction.target)
                if visualise: print_stacks(stacks)

    return ''.join([stacks[i][-1] for i in range(1, rows+1)])


if __name__ == '__main__':
    part1 = main(part2=False, visualise=False)
    part2 = main(part2=True, visualise=False)
    print(f"Part 1: result = {part1}, expected DHBJQJCCW")
    print(f"Part 1: result = {part2}, expected WJVRLSJJT")
