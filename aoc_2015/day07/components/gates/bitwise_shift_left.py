from .gate import Gate

class BitwiseShiftLeftGate(Gate):
    def __init__(self,source1,source2):
        super().__init__('<<',source1,source2)