from util.inputs import parse_input
from util.heap import MaxHeap
from time import perf_counter, sleep


def calorie_finder(input, return_top_n=3, verbose = True):
    heap = MaxHeap()
    current_elf_total = 0
    for elf, row in enumerate(input):
        if row == 'end_elf':
            heap.insert(current_elf_total)
            # if verbose: print(f"Elf {elf:03}: {current_elf_total:05}", end='\r')
            current_elf_total = 0
            continue
        current_elf_total += row
    return [heap.remove_max() for i in range(return_top_n)]

def main(part1=True, expected_result = ''):
    start = perf_counter()
    
    # Collect data from input file
    data = parse_input(example=False, function=parse_function)
    parse_complete = perf_counter()
    # Run Calculate the sum of the largest n elves
    results = sum(calorie_finder(data,1 if part1 else 3))
    
    complete = perf_counter()
    total_time = complete - start
    interval_1 = parse_complete - start
    interval_2 = complete - parse_complete
    print(f"Part {1 if part1 else 2} Complete:\n\tTotal Time: {total_time}\n\tParsing Time: {interval_1}\n\tProcessing Time: {interval_2}")
    print(f"Results: {results}. Expected {expected_result}\n")
    
if __name__ == "__main__":

    def parse_function(x): return 'end_elf' if x == '' else int(x)

    test_data = parse_input(example=True, function=parse_function)
    test_results = sum(calorie_finder(test_data, 1))
    print(f"Advent of Code - 2022 - Day 01")
    print(f"\nTest Answer: {test_results}. Expected {24000}\n")
    
    # Part 1
    main(part1 = True, expected_result='72718')
    
    # Part 2
    main(part1 = False, expected_result='213089')

    
