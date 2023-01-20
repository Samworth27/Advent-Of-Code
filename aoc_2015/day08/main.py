from aoc_util.inputs import parse_input, fields
import re

DAY = 8
YEAR = 2015

def part1(input):
    a,b = string_lengths(input)
    return a - b

def part2(input):
    a,b = string_lengths2(input)
    return b - a

def replace(match_obj):
    if match_obj.group(1) is not None:
        return match_obj.group(1)[-1]
    if match_obj.group(2) is not None:
        return '*'
    
def replace2(match_obj):
    if match_obj.group(1) is not None:
        return f"\\{match_obj.group(1)}"
    
def string_lengths(input):
    string_len = len(input)
    input = re.sub(r"(\\[\",\\])|(\\x[0-9a-f][0-9a-f])", replace, input[1:-1])
    memory_length = len(input)
    return string_len, memory_length

def string_lengths2(input):
    string_len = len(input)
    input = re.sub(r"([\\\"])", replace2, input)
    input = '"'+input+'"'
    encoded_length = len(input)
    return string_len, encoded_length


def test():
    def parse_function(x): return tuple(fields(x, field_func=int))
    for data, expected in zip(parse_input('example'), parse_input('expected',parse_function)):
        print(data)
        result1 = string_lengths(data)
        result2 = string_lengths2(data)
        print(f"Result: {result1}, expected: {expected}, match = {result1 == expected}")
        print(f"Results 2: {result2}")
    data = parse_input('example')
    result1 = sum(part1(x) for x in data)
    result2 = sum(part2(x) for x in data)
    print(f"Test Part 1 result: {result1}, Part 2 result: {result2}")


def main():
    data = parse_input((DAY,YEAR))
    result1 = sum(part1(x) for x in data)
    result2 = sum(part2(x) for x in data)
    print(f"Part 1 result: {result1}, Part 2 result: {result2}")


if __name__ == '__main__':
    test()
    main()
