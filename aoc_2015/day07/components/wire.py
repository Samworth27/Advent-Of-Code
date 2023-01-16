from .component import Component

class Wire(Component):
    def __init__(self,name,circuit,source:str):
        super().__init__()
        self.circuit = circuit
        self.name = name
        self._source = source
    
    @property
    def source(self):
        return self.circuit.components[self._source]
    
    @property
    def value(self):
        # if self._value == None:
        self._value = self.source.value
        self.unsign()
        return self._value
    
    def __repr__(self):
        return f"Wire {self.name}: {self.value}"