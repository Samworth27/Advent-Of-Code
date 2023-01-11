_lookup = {
        -2: '=',
        -1: '-',
        0: '0',
        1: '1',
        2: '2',
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2': 2
}

def snafu_carry(base5_array):
    index = len(base5_array) - 1
    while index >= 0:
        digit = base5_array[index]
        if digit >= 3:
            if index == 0:
                base5_array.insert(0,0)
                index += 1
            base5_array[index] -= 5
            base5_array[index-1] += 1
        index -= 1
    return base5_array


def base10_snafu(base10_number):
 
    base5_array = []
    while base10_number > 0:
        digit = base10_number % 5
        base5_array.insert(0,digit)
        base10_number //= 5
    base5_array = snafu_carry(base5_array)
    return ''.join([_lookup[digit] for digit in base5_array])

def snafu_base10(snafu_number):
    snafu_as_array = [_lookup[char]for char in reversed(snafu_number)]
    values = [digit * (5 ** position) for position, digit in enumerate(snafu_as_array)]
    return sum(values)