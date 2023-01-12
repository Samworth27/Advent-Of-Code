from enum import Enum
class Outcome(Enum):
    def __str__(self):
        return self.name.title()
      
    def score(self):
      return ((self.value + 1)%3)*3
    WIN = 1
    DRAW = 0
    LOSS = 2
