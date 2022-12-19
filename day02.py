from enum import Enum


class Outcome(Enum):
    def __str__(self):
        return self.name.title()
      
    def score(self):
      return ((self.value + 1)%3)*3
    WIN = 1
    DRAW = 0
    LOSS = 2


class Choice(Enum):
    def __gt__(self, b):
        return 1 == (self.value - b.value) % 3

    def __lt__(self, b):
        return 2 == (self.value - b.value) % 3

    def __str__(self):
        return self.name.title()

    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def to_outcome(input):
    options = {
        "X": Outcome.LOSS,
        "Y": Outcome.DRAW,
        "Z": Outcome.WIN
    }
    return options[input]


def to_choice(input):
    options = {
        "A": Choice.ROCK,
        "B": Choice.PAPER,
        "C": Choice.SCISSORS,
        "X": Choice.ROCK,
        "Y": Choice.PAPER,
        "Z": Choice.SCISSORS
    }

    return options[input]


def calc_outcome(opponent, you):
    # if you > opponent:
    #     return Outcome.WIN
    # if you < opponent:
    #     return Outcome.LOSS
    # return Outcome.DRAW
    return Outcome((you.value-opponent.value)%3)


file = open('./day02.txt')

part_1_total = 0
part_2_total = 0

temp_counter = 0
temp_counter_limit = 15

while (True):
    # Testing Counter
    # if (temp_counter > temp_counter_limit):
    #     break
    # else:
    #     temp_counter += 1

    # Main Loop
    game_round = file.readline().strip().split(' ')
    print(game_round)
    if (game_round == ['']):
        break

    #  Part 1
    opponent = to_choice(game_round[0])
    you = to_choice(game_round[1])
    round_outcome = calc_outcome(opponent, you)
    round_score = round_outcome.score()+you.value
    # print(f'Opponent = {opponent}, you = {you}, round_outcome = {round_outcome}')
    part_1_total += round_score

    # Part 2
    opponent = to_choice(game_round[0])
    round_outcome = to_outcome(game_round[1])
    you = Choice(((opponent.value-1+round_outcome.value)%3)+1)
    round_score = round_outcome.score()+you.value
    
    print(f'Opponent = {opponent}, desired outcome = {round_outcome}, you pick = {you}')
    print(f'Score = round outcome({round_outcome.score()}) + pick score({you.value}) = {round_score}')
    part_2_total += round_score

print(f'Part 1 Total: {part_1_total}')
print(f'Part 2 Total: {part_2_total}')
