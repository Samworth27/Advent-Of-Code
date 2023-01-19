from aoc_util.inputs import parse_input
from aoc_util.windows import sliding_window
import re

DISALLOWED_CHARACTERS = set(['i', 'o', 'l'])


def contains_disallowed(string):
    return len(set(string).intersection(DISALLOWED_CHARACTERS)) > 0


def number_of_pairs(string):
    matches = re.findall(r"(\w)\1{1}", string)
    return len(matches)


def has_straight(string, straight_length):
    for char1, char2, char3 in sliding_window(string, straight_length):
        char1_int, char2_int, char3_int = ord(char1), ord(char2), ord(char3)
        if char2_int - char1_int == 1 and char3_int - char2_int == 1:
            return True
    return False


def valid(string):
    if contains_disallowed(string):
        return False
    if number_of_pairs(string) < 2:
        return False
    return has_straight(string, 3)


def increment_string(string):
    digit_array = [ord(char)-97 for char in string]
    digit_array[-1] += 1
    for i, val in enumerate(reversed(digit_array)):
        i = len(digit_array)-1-i
        if val >= 26:
            digit_array[i] = 0
            if i == 0:
                digit_array.insert(0, 0)
            else:
                digit_array[i-1] += 1
    return ''.join(chr(digit+97) for digit in digit_array)


def increment_password(current_password):
    candidate = increment_string(current_password)
    while not valid(candidate):
        candidate = increment_string(candidate)
    return candidate


def main():
    result1 = increment_password('vzbxkghb')
    result2 = increment_password(result1)
    print(f"Part 1 result: {result1}, Part 2 result: {result2}")


if __name__ == '__main__':
    main()
