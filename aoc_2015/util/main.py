from util.inputs import parse_input

def part1(input):
    pass

def part2(input):
    pass

def test():
    for data, expected in zip(parse_input(True,'example'),parse_input(True,'expected')):
        print(data)
        result = None
        print(f"Result: {result}, expected: {expected}, match = {result == expected}")
    
def main():
    data = parse_input
    result1 = None
    result2 = None
    print(f"Part 1 result: {result1}, Part 2 result: {result2}")
    
if __name__ == '__main__':
    test()
    main()