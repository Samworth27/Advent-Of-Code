from collections import namedtuple
from copy import copy

Number = namedtuple('Number',['id','val'])

def read_file(example=False):
    path = "example.txt" if example else "input.txt"
    with open(path) as file:
        return [Number(id,int(value.strip())) for id, value in enumerate(file)]




class EncryptedFile():
    def __init__(self, input):
        self.instructions = input
        self.output = copy(input)
        self.length = len(self.instructions)
        
    def mix(self):
        # print([x.val for x in self.output])
        for instruction in self.instructions:
            if instruction.val == 0:
                self.key_start = instruction
                
            source_index = self.output.index(instruction)
            target_index = ((source_index + instruction.val - (1 if instruction.val < 0 else -1 if source_index + instruction.val > self.length else 0))+self.length) % self.length
            # print(instruction, source_index,target_index)
            holding = self.output.pop(source_index)
            self.output.insert(target_index,holding)
            # print([x.val for x in self.output])
        # print([x.val for x in self.output])  
    def get_key(self, index):
        start_index = self.output.index(self.key_start)
        target = (start_index + index + self.length)%self.length
        return self.output[target].val
    
    

example_input = read_file(example=True)
example = EncryptedFile(example_input)
example.mix()
example_answer = [example.get_key(1000),example.get_key(2000),example.get_key(3000)]
print(example_answer, sum(example_answer))

part1_input = read_file()
part1 = EncryptedFile(part1_input)
part1.mix()
part1_answer = [part1.get_key(1000),part1.get_key(2000),part1.get_key(3000)]
print(part1_answer, sum(part1_answer))