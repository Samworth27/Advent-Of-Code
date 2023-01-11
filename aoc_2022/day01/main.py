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


if __name__ == "__main__":

    def parse_function(x): return 'end_elf' if x == '' else int(x)

    test_data = parse_input(example=True, function=parse_function)
    test_results = sum(calorie_finder(test_data, 1))
    print(f"Advent of Code - 2022 - Day 01")
    print(f"\nTest Answer: {test_results}. Expected {24000}\n")
    
    # Part 1
    p1_start = perf_counter()
    p1_data = parse_input(example=False, function=parse_function)
    p1_parse_complete = perf_counter()
    p1_results = sum(calorie_finder(p1_data,1))
    p1_complete = perf_counter()
    p1_total_time = p1_complete - p1_start
    p1_interval_1 = p1_parse_complete - p1_start
    p1_interval_2 = p1_complete - p1_parse_complete
    print(f"Part 1 Complete:\n\tTotal Time: {p1_total_time}\n\tParsing Time: {p1_interval_1}\n\tProcessing Time: {p1_interval_2}")
    print(f"Results: {p1_results}. Expected 72718\n")
    
    # Part 2
    p2_start = perf_counter()
    p2_data = parse_input(example=False, function=parse_function)
    p2_parse_complete = perf_counter()
    p2_results = sum(calorie_finder(p2_data,3))
    p2_complete = perf_counter()
    p2_total_time = p2_complete - p2_start
    p2_interval_1 = p2_parse_complete - p2_start
    p2_interval_2 = p2_complete - p2_parse_complete
    print(f"Part 2 Complete:\n\tTotal Time: {p2_total_time}\n\tParsing Time: {p2_interval_1}\n\tProcessing Time: {p2_interval_2}")
    print(f"Results: {p2_results}. Expected 213089")
    
