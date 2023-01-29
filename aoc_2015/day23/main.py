from aoc_util.inputs import parse_input, fields

DAY = 23
YEAR = 2015

class Instruction:
    members = dict()
    def __init__(self,opcode,operation):
        self.opcode = opcode
        self.operation = operation
        self.members[opcode] = self
        
    def __str__(self):
        return f"{self.opcode}"
    
    def __repr__(self):
        return f"<Instruction [{self.opcode}]>"
        
    @classmethod
    def get(cls,inst):
        return cls.members[inst]

def half_operation(computer,register):
    computer[register] //= 2
    jump_operation(computer,1)

def triple_operation(computer,register):
    computer[register] *= 3
    jump_operation(computer,1)
    
def increment_operation(computer,register):
    computer[register] += 1
    jump_operation(computer,1)
    
def jump_operation(computer,offset):
    offset = int(offset)
    new_pointer = computer.pointer + offset
    if new_pointer < 0 or new_pointer >= len(computer.instructions):
        computer.running = False
        print("Program terminating: Invalid Pointer")
        return False
    computer.pointer = new_pointer
    return True

def even(int_):
    return int_ % 2 == 0

def jump_even_operation(computer,register,offset):
    if even(computer[register]):
        jump_operation(computer,offset)
    else:
        jump_operation(computer,1)
        
def jump_one_operation(computer,register,offset):
    if computer[register] == 1:
        jump_operation(computer,offset)
    else:
        jump_operation(computer,1)

half = Instruction('hlf', half_operation)
triple = Instruction('tpl', triple_operation)
increment = Instruction('inc',increment_operation)
jump = Instruction('jmp',jump_operation)
jump_if_even = Instruction('jie', jump_even_operation)
jump_if_one = Instruction('jio',jump_one_operation)

class Computer:
    def __init__(self,n_registers:int,instructions:list[Instruction,list[str]]):
        self.registers = [0 for _ in range(n_registers)]
        self.instructions = instructions
        self.pointer = 0
        self.running = False
        
    def execute(self):
        instruction, args = self.instructions[self.pointer]
        instruction.operation(self,*args)
        # print(f"[{self.pointer}]{instruction} {', '.join([str(a) for a in args])} {self}")
        
    def run_program(self):
        self.running = True
        while(self.running):
            self.execute()
        return self.registers
            
    def __getitem__(self,register):
        if type(register) == str:
            register = ord(register.lower())-97
        
        if register < len(self.registers) and register >= 0:
            return self.registers[register]
        else:
            raise IndexError(f"The register {register} does not exist")
    
    def __setitem__(self,register, value):
        if type(register) == str:
            register = ord(register.lower())-97
        if register < len(self.registers) and register >= 0:
            self.registers[register] = value
        else:
            raise IndexError(f"The register {register} does not exist")
        
    def __str__(self):
        return ''.join([f"[REG {i}|{reg}]" for i,reg in enumerate(self.registers)])
    
def fields_(x):
    return [y.strip(',') for y in fields(x)]   

def build_program(example=False):
    return [(Instruction.get(inst),args) for inst,*args in parse_input('example' if example else (DAY,YEAR),fields_)]
    
def part1():
    program = build_program()
    computer = Computer(2,program)
    return computer.run_program()
    
def part2():
    program = build_program()
    computer = Computer(2,program)
    computer[0] = 1
    return computer.run_program()
    
def main():
    part1_result = part1()
    part2_result = part2()
    print(part1_result[1])
    print(part2_result[1])
    
if __name__ == '__main__':
    main()