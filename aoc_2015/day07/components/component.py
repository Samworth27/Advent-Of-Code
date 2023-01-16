class Component:
    count = 0  
    def __init__(self):
        self.id = self.get_id()
        self._value = None
        
    def reset(self):
        self._value = None
        
    def unsign(self):
        if self._value < 0:
            self._value = self._value + (1 << 16)
        
    @classmethod
    def get_id(cls):
        new_id = f"{cls.__name__}{cls.count}"
        cls.count += 1
        return new_id
    
    def __repr__(self):
        return f"{self.id} {self.value}"