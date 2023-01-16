from ..component import Component


class Gate(Component):
    count = 0

    def __init__(self, operator, source1, source2):
        super().__init__()
        self.operator = operator
        self.source1 = source1
        self.source2 = source2

    @property
    def value(self):
        if self._value == None:
            self._value = eval(
                f"{self.source1.value} {self.operator} {self.source2.value}")
            self.unsign()
        return self._value
