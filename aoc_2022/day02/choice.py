from enum import Enum
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