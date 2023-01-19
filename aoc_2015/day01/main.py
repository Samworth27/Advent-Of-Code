from aoc_util.inputs import parse_input

def part1(input:str):
    floor_ = 0
    basement = None
    for i, inst in enumerate(input):
        if inst == '(': floor_ += 1
        if inst == ')': floor_ -= 1
        if floor_ == -1 and not basement:
            basement = i + 1
            
    return floor_, basement
    

def test():
    for data, expected_result in zip(parse_input(True,'example'),parse_input(True,'example_expected',int)):
        result, basement = part1(data)
        print(f"Result: {result}, expected: {expected_result}, match = {result == expected_result}")
    
def main():
    for data in parse_input():
        result, first_visit = part1(data)
        print(f"Part 1 result: {result}, Part 2 result: {first_visit}")
        return part1(data)
    
if __name__ == '__main__':
    test()
    main()