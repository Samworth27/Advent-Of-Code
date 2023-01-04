
def read_file(example=False):
    path = 'example.txt' if example else 'input.txt'
    with open(path) as file:
        for line in file:
            yield line.strip().split(' ')

def process_input(fields:list):
    name = fields[0][:4]
    job = fields[1:]
    if len(job) == 1:
        job[0] = int(job[0])
    return (name,tuple(job))

class Monkey():
    instances = {}
    def __init__(self,name,job):
        self.name = name
        self.job = job
        if len(job) == 1:
            self.yell = self.yell_number
        else:
            self.yell = self.yell_operation
        self.add_self(self)
    
    def yell_number(self):
        return self.job[0]
    
    def yell_operation(self):
        monkey1 = self.get_instance(self.job[0])
        monkey2 = self.get_instance(self.job[2])
        return self.operation(monkey1.yell(),self.job[1], monkey2.yell())
    

    
    def __repr__(self) -> str:
        return f"Monkey: {self.name} job: {self.job}"
    @staticmethod
    def operation(value1,operator,value2):
        match operator:
            case '+':
                return value1 + value2
            case '-':
                return value1 - value2
            case '*':
                return value1 * value2
            case '/':
                if value2 == 0: raise ZeroDivisionError
                return value1 / value2
    
    @classmethod
    def get_instance(cls,instance_key):
        return cls.instances[instance_key]    
    
    @classmethod
    def add_self(cls, instance):
        cls.instances[instance.name] = instance

def main():
    for monkey in read_file():
        Monkey(*process_input(monkey))
    print(Monkey.get_instance('root').yell())

if __name__ == '__main__':
    main()