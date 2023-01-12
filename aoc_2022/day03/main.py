from util.inputs import parse_input
from util.sliding_window import sliding_window

def lookup_priority(item):
    return (ord(item)-96)%58

def part2_window_function(rucksacks:list[set]):
    r1, r2, r3 = rucksacks
    return r1.intersection(r2).intersection(r3).pop()

def split(list_: list | str):
    centrepoint = len(list_)//2
    return (list_[:centrepoint],list_[centrepoint:])
    
    
    
def part1(example=False):
    score = 0
    for rucksack in parse_input(example=example):
        c1,c2 = split(rucksack) # c1, c2 represent compartments
        common_value = set(c1).intersection(set(c2)).pop()
        score += lookup_priority(common_value)
    return score
        
def part2(example=False):
    data = parse_input(example=example)
    return sum([lookup_priority(common_value) for common_value in sliding_window(data,3,part2_window_function,lambda x: set(x))])
    # score = 0
    # for common_value in sliding_window(data,3, part2_window_function,lambda x: set(x)):
    #     score += lookup_priority(common_value)
    # return score

if __name__ == '__main__':
    print(f"Part 1 example = {part1(example=True)}. Expected value is 157")
    print(f"Part 1 = {part1()}. Expected value is 7428")
    print(f"Part 2 example = {part2(example=True)}. Expected value is 70")
    print(f"Part 2 = {part2()}. Expected value is 2650")
    