from .gate import Gate

class BitwiseNOTGate(Gate):
    def __init__(self,source1):
        super().__init__('!',source1,None)
        
    @property
    def value(self):
        if self._value == None:
            self._value = ~self.source1.value
        return self._value