from aoc_util.inputs import parse_input
from aoc_util.windows import sliding_window

def is_vowel(char):
    return char in ('a', 'e', 'i', 'o', 'u')

def double(char1, char2):
    return char1 == char2

def invalid(char1, char2):
    return char1+char2 in ('ab', 'cd', 'pq', 'xy')

def is_palindrome(char1,char2,char3):
    return char1 == char3


def string_nice1(input):
    vowel_count = 0
    contains_double = False

    for i, (char1, char2)in enumerate(sliding_window(input, 2)):
        if invalid(char1, char2):
            return False
        if double(char1,char2):
            contains_double = True
        vowel_count += is_vowel(char1)
        if i == len(input) - 2:
            vowel_count += is_vowel(char2)
            
    return contains_double and vowel_count >= 3 
        
def string_nice2(input):
    contains_palindrome = 0
    contains_pairs = 0
    pairs = set()
    for i, (char1, char2, char3)in enumerate(sliding_window(input, 3)):
        contains_palindrome += is_palindrome(char1,char2,char3)
        pair1 = (char1,char2)
        pair2 = (char2,char3)
        contains_pairs += pair2 in pairs
        pairs.add(pair1)
        if contains_palindrome and contains_pairs:
            return True
    return False
        


def test():
    for data, (expected1, expected2) in zip(parse_input(True, 'example'), parse_input(True, 'expected', lambda x: tuple(y=='True' for y in x.split()))):
        result1 = string_nice1(data)
        print(f"Part 1 result: {result1}, expected: {expected1}, match = {result1 == expected1}")
        result2 = string_nice2(data)
        print(f"Part 2 result: {result2}, expected: {expected2}, match = {result2 == expected2}\n")


def main():
    data = parse_input()
    result1 = sum(string_nice1(string_) for string_ in data)
    result2 = sum(string_nice2(string_) for string_ in data)
    print(f"Part 1 result: {result1}, Part 2 result: {result2}")


if __name__ == '__main__':
    test()
    main()
