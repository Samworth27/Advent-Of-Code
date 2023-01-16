from components import Constant, Wire, Gate
from components.gates import BitwiseANDGate, BitwiseNOTGate, BitwiseORGate, BitwiseShiftLeftGate, BitwiseShiftRightGate

instruction_lookup = {
    'NOT': '~',
    'AND': '&',
    'OR': '|',
    'RSHIFT': '>>',
    'LSHIFT': '<<',
}



class Circuit:
    def __init__(self):
        self.components = {}
        self.wires = {}

    def add_connection(self, instruction: tuple):
        match len(instruction):
            case 2:  #pass through
                source_name, destination = instruction
                source = self.get_source(source_name)
                new_component = Wire(destination,self,source)
                self.wires[new_component.name] = new_component
                self.components[destination] = new_component 
                
            case 3: #not
                operator, source_name, destination = instruction
                source = self.get_source(source_name)
                
                new_gate = BitwiseNOTGate(Wire('',self,source))
                self.components[new_gate.id] = new_gate
                
                new_component = Wire(destination,self, new_gate.id)
                self.wires[new_component.name] = new_component
                self.components[destination] = new_component          
            case 4:
                source1_name, operator, source2_name, destination = instruction
                operator = instruction_lookup[operator]
                source1 = self.get_source(source1_name)
                source2 = self.get_source(source2_name)
                new_gate = Gate(operator,Wire('',self,source1),Wire('',self,source2))
                self.components[new_gate.id] = new_gate
                new_component = Wire(destination,self,new_gate.id)
                self.wires[new_component.name] = new_component
                self.components[destination] = new_component 
                

    def get_source(self,source_name):
        try:
            value = int(source_name)
            new_constant = Constant(value)
            self.components[new_constant.id] = new_constant
            return new_constant.id
        except ValueError:
            return source_name
        
    def reset(self):
        for component in self.components.values():
            component.reset()
        
    
    def get_value(self, component_name):
        return self.components[component_name].value
