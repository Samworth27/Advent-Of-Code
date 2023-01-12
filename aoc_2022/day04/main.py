from util.inputs import parse_input
from os import system
from time import sleep


def process(pair):
    return tuple(tuple(int(section) for section in elf.split('-')) for elf in pair.split(','))
    # output = []
    # pair = file_string.split(',')
    # for section in pair:
    #   range = [int(i) for i in section.split('-')]

    #   output.append(range)

    # return output


def sort_ranges(range1, range2):
    if range1 == range2:
        return range1, range2
    r1_low, r1_high = range1
    r2_low, r2_high = range2
    if r1_low < r2_low:
        return range1, range2
    if r1_low == r2_low and r1_high > r2_high:
        return range1, range2
    return range2, range1


def contains(range_low, range_high):
    r1_low, r1_high = range_low
    r2_low, r2_high = range_high
    return r2_high <= r1_high and r2_low <= r1_high


def overlap(range_low, range_high):
    r1_low, r1_high = range_low
    r2_low, r2_high = range_high
    return r2_low <= r1_high

def print_range(range_):
    low, high = range_
    left_buffer = low
    centre_buffer = high-left_buffer-len(str(low))
    print(f"{' '*left_buffer}{low}{'-'*centre_buffer}{high if centre_buffer >= 0 else ''}")

def main(example=False, part1=True, part2=True, verbose=0):
    if verbose > 1:
        system('clear')
    if part1:
        contained_count = 0
    if part2:
        overlap_count = 0
    for i, pair in enumerate(parse_input(example=example, function=process)):
        lower, upper = sort_ranges(*pair)
        if verbose > 0:
            print('*'*101)
            print(f"  Pair {i}  ".center(101))
            if verbose > 1:
                sleep(0.1)
            print_range(upper)
            print_range(lower)
        if verbose > 1:
            sleep(0.3)
        if not overlap(lower, upper):
            if verbose > 1:
                system('clear')
            continue
        if part2:
            overlap_count += 1
            if verbose > 0:
                print('Ranges overlap'.center(101))
                
        if part1 and contains(lower, upper):
            contained_count += 1
            if verbose > 0:
                print('One range is fully contained in another'.center(101))
        if verbose > 0:
            print('*'*101)
        if verbose > 1:
            sleep(1)
        if verbose > 1:
            system('clear')
    
    if part1 and part2:
        return contained_count, overlap_count
    if part1: return contained_count
    if part2: return overlap_count
    return 'Why run this at all?'


if __name__ == '__main__':
    
    part1_example, part2_example = main(example=True)
    print(f"\nExample data:\n\tPart 1: Result = {part1_example}, expected 2\n\tPart 2: Result = {part2_example}, expected 4")
    
    part1, part2 = main()
    print(f"\nPuzzle data:\n\tPart 1: Result = {part1}, expected 496\n\tPart 2: Result = {part2}, expected 847")