from util.functions import process_input, part1_score
from util.test import test_example
from grid import Grid
from instructions import InstructionList

test_cases = {
    'example': 6032,
    '1': 1041,
    '2': 1045,
    '3': 1045,
    '4': 1043,
    '5': 1047,
    '6': 1036
}


def main():

    for test,expected_value in test_cases.items():
        test_example(test,expected_value)


    map_data, instructions = process_input(example=False)
    map_board = Grid(map_data)
    instruction_list = InstructionList(instructions)
    map_board.should_sleep = False
    map_board.should_print = False
    map_board.execute_instructions(instruction_list)
    map_board.print()
    print(part1_score(map_board.player))
    
    
if __name__ == '__main__':
    main()
