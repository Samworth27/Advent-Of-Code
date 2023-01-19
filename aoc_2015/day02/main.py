from aoc_util.inputs import parse_input, fields


def fields_function(x):
    return tuple(fields(x, None, 'x', int))


def process(width, length, height):

    side1_area = width * length
    side2_area = length * height
    side3_area = width * height

    side1_perimeter = 2 * width + 2 * length
    side2_perimeter = 2 * length + 2 * height
    side3_perimeter = 2 * width + 2 * height

    total_area = 2 * side1_area + 2 * side2_area + 2 * side3_area
    wrap_slack = min(side1_area, side2_area, side3_area)

    ribbon_wrap = min(side1_perimeter, side2_perimeter, side3_perimeter)
    bow = width * length * height

    total_wrapping = total_area  + wrap_slack
    total_ribbon = ribbon_wrap + bow

    return total_wrapping, total_ribbon


def test1():
    for data, (expected1, expected2) in zip(parse_input(True, 'example', fields_function), parse_input(True, 'expected', function=lambda x: tuple(fields(x, None, ' ', int)))):
        result1, result2 = process(*data)
        print(
            f"Part 1 Result: {result1}, expected: {expected1}, match = {result1 == expected1}")
        print(
            f"Part 2 Result: {result2}, expected: {expected2}, match = {result2 == expected2}")


def main():
    results = list(zip(*[process(*data)
                  for data in parse_input(function=fields_function)]))
    results1 = sum(results[0])
    results2 = sum(results[1])

    print(f"Part 1 result: {results1}, Part 2 result: {results2}")


if __name__ == '__main__':
    test1()
    main()
