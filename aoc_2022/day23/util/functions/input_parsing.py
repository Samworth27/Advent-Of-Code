def parse_input(example=False, test_case='example'):
    return [row for row in read_file(example,test_case)]

def read_file(example=False, test_case='example'):
    path = f'./test_cases/tc_{test_case}.txt' if example else './test_cases/input.txt'
    with open(path) as file:
        for line in file:
            yield line.strip('\n')