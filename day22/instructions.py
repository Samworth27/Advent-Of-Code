from dataclasses import dataclass
from util.classes import PlayerTiles, InstructionTypes

@dataclass
class Instruction():
    type:InstructionTypes
    direction: str = None
    distance: int = 0

class InstructionList():
    def __init__(self,str_input):
        
        distance = True
        self.instructions = []
        self.index = 0
        
        dist_temp = ''
        for char in str_input:
            if char in ['L','R']:
                self.instructions.append(Instruction(InstructionTypes.move,distance = int(dist_temp)))
                self.instructions.append(Instruction(InstructionTypes.turn,direction = char))
                dist_temp = ''
            else:
                dist_temp += char
        if dist_temp != '':
            self.instructions.append(Instruction(InstructionTypes.move,distance = int(dist_temp)))
                
    def __len__(self):
        return len(self.instructions)
                
    
    def __iter__(self):
        for instruction in self.instructions:
            yield instruction
