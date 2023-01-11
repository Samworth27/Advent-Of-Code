from collections import namedtuple
from copy import copy

Number = namedtuple('Number', ['id', 'val'])


def read_file(example=False):
    path = "example.txt" if example else "input.txt"
    with open(path) as file:
        return [Number(id, 811589153*int(value.strip())) for id, value in enumerate(file)]


class CircularList():
    def __init__(self, input, index_item):
        self.values = copy(input)
        self.index_item = index_item

    def __getitem__(self, index):
        return self.values[self.c_index(index)]

    def __setitem__(self, index, value):
        self.values[self.c_index(index)] = value

    def move_left(self, index):
        self[index], self[index-1] = self[index-1], self[index]

    def move_right(self, index):
        self[index], self[index+1] = self[index+1], self[index]

    def move_left_n_times(self, item, n):
        index = self.index(item)
        holding = self.pop(index)
        target = index+n
        self.insert(target,holding)
            
    def move_right_n_times(self, item, n):
        index = self.index(item)
        holding = self.pop(index)
        target = index+n
        self.insert(target,holding)

    def shift(self,inst):
        id, val = inst
        if val < 0:
            self.move_left_n_times(inst,val)
        elif val > 0:
            self.move_right_n_times(inst,val)
        # print(self)
     
    def c_index(self, index):
        return (index + len(self)) % len(self)

    def index(self, item):
        return self.values.index(item)
    
    def zero_reference(self,index):
        start_index = self.index(self.index_item)
        return self[self.c_index(start_index+index)].val
    
    def pop(self,index = -1):
        return self.values.pop(self.c_index(index))
    
    def insert(self,index,value):
        self.values.insert(self.c_index(index),value)

    def __len__(self):
        return len(self.values)
    
    def __repr__(self):
        return str([x.val for x in self.values])


def mix(c_list, instructions):
    for iteration, inst in enumerate(instructions):
        example.shift(inst)
        if iteration % 1 == 0: print(f"[{iteration}/{len(instructions)}]")

example_list = read_file()

index_item = example_list[[x.val for x in example_list].index(0)]

example = CircularList(example_list,index_item)

for _ in range(10):
    mix(example,example_list)

answer = [example.zero_reference(1000),example.zero_reference(2000), example.zero_reference(3000)]
print(sum(answer))
