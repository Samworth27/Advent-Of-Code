from .component import Component

class Constant(Component):
    def __init__(self,value):
        super().__init__()
        self.value = value