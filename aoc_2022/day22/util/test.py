from util.functions import process_input, part1_score
from grid import Grid
from instructions import InstructionList

def test_example(test,expected):
    test_map_data, test_instructions = process_input(example=True, test_case=test)

    test_map_board = Grid(test_map_data)
    test_map_board.should_print = False
    test_instruction_list = InstructionList(test_instructions)
    test_map_board.execute_instructions(test_instruction_list)
    print(
        f"Password = {part1_score(test_map_board.player)} Matches Example: {part1_score(test_map_board.player) == expected}")