from util.functions import process_input, part1_score
from util.test import test_example
from cube import Cube
from instructions import InstructionList

test_cases = {
    'example': 6032,
}


def main():
    map_data, instructions = process_input(example=False,test_case='example_reshaped_2')
    instructions_list = InstructionList(instructions)
    test_map = Cube(map_data)
    test_map.should_print = False
    test_map.should_sleep = False
    test_map.execute_instructions(instructions_list)
    print(part1_score(test_map.player))

    
if __name__ == '__main__':
    main()
