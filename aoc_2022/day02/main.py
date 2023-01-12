from enum import Enum
from util.inputs import parse_input
from outcome import Outcome
from choice import Choice
from time import sleep

def to_outcome(input):
    lookup = {
        "X": Outcome.LOSS,
        "Y": Outcome.DRAW,
        "Z": Outcome.WIN
    }
    return lookup[input]

def to_choice(input):
    lookup = {
        "A": Choice.ROCK,
        "B": Choice.PAPER,
        "C": Choice.SCISSORS,
        "X": Choice.ROCK,
        "Y": Choice.PAPER,
        "Z": Choice.SCISSORS
    }

    return lookup[input]

def calc_outcome(opponent, you):
    return Outcome((you.value-opponent.value)%3)

def parse_function(x): return x.split()

def part1():
    data = parse_input(example=False,function=parse_function)
    total_score = 0
    for round_number, round_data in enumerate(data):
        opponent = to_choice(round_data[0])
        you = to_choice(round_data[1])
        round_outcome = calc_outcome(opponent, you)
        round_score = round_outcome.score() + you.value
        total_score += round_score
        print(f"Round {round_number + 1} Round Score: {round_score:05} Accumulative Score: {total_score:05}", end='\r')
    print(' '*80, end='')
    return total_score

def part2():
    data = parse_input(example=False,function=parse_function)
    total_score = 0
    for round_number, round_data in enumerate(data):
        opponent = to_choice(round_data[0])
        round_outcome = to_outcome(round_data[1])
        you = Choice(((opponent.value-1+round_outcome.value)%3)+1)
        round_score = round_outcome.score()+you.value
        total_score += round_score
        print(f"Round {round_number + 1} Round Score: {round_score:05} Accumulative Score: {total_score:05}", end='\r')
        # print(f'Opponent = {opponent}, desired outcome = {round_outcome}, you pick = {you}')
        # print(f'Score = round outcome({round_outcome.score()}) + pick score({you.value}) = {round_score}')
    print(' '*80, end='')
    return total_score

    
if __name__ == '__main__':
    print("Part 1: running")
    part1_result = part1()
    print(f"\rPart 1: {part1_result}. Expected: 11150")
    print("Part 2: running")
    print(f"\rPart 2: {part2()}. Expected: 8295")
    
