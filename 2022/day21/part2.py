
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
    if name == 'root':
        job[1] = '='
    return (name,tuple(job))

class Monkey():
    instances = {}
    human_path = {}
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

    def display_yell(self):
        monkey1 = self.get_instance(self.job[0])
        monkey2 = self.get_instance(self.job[2])
        print(monkey1.yell(), self.job[1],monkey2.yell())
    
    
    def swap_values_order(self,operator,b,target):
        match operator:
            case '+': return ('+',b,target)
            case '-': return ('-',b,-target)
            case '*': return ('*',b,target)
            case '/': return ('*',1/b,1/target)
            case '=': return ('=',b,target)
        
    def target_solver(self,operator,b,target):
        match operator:
            case '=': return b
            case '+': return target-b
            case '-': return target+b
            case '*': return target/b
            case '/': return target*b
    
    def make_equal(self,target=None):
        if self.name == 'humn':
            self.job = tuple([int(target)])
            return int(target)
        
        human_left, human_right = self.contains_human(self)
        monkey1 = self.get_instance(self.job[0])
        monkey2 = self.get_instance(self.job[2])
        human_side = monkey1 if human_left else monkey2
        other_side = monkey2 if human_left else monkey1
        # target_job = (operator, other_value, target) used like: *human* (operation) other = target
        if human_left:
            # print(f"H {self.job[1]} {monkey2.name}")
            target_job = (self.job[1],monkey2.yell(),target)
        if human_right:
            # print(f"{monkey1.name}{[monkey1.yell()]} {self.job[1]} H = T[{target}]")
            target_job = self.swap_values_order(self.job[1],monkey1.yell(),target)
        new_target = round(self.target_solver(*target_job))
        # print(f"name: {self.name} target: {target} target_job:{target_job} = {new_target}")
        
        
        return human_side.make_equal(new_target)
        
        
    
    def __repr__(self) -> str:
        return f"Monkey: {self.name} job: {self.job}"
    
    @classmethod
    def contains_human(cls,instance):
        if instance.name not in cls.human_path:
            if instance.name == 'humn': 
                cls.human_path[instance.name] = tuple([True])
            elif instance.yell == instance.yell_number: 
                cls.human_path[instance.name] = tuple([False, False])
            else:
                monkey1 = instance.get_instance(instance.job[0])
                monkey2 = instance.get_instance(instance.job[2])
                cls.human_path[instance.name] = tuple([any(cls.contains_human(monkey1)), any(cls.contains_human(monkey2))])
        return cls.human_path[instance.name]
    
    @staticmethod
    def inverse_operator(operator):
        options = {
            '+':'-',
            '-':'+',
            '*':'/',
            '/':'*',
            '=':'='
        }
        return options[operator]
        
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
            case '=':
                return value1 == value2
    
    @classmethod
    def get_instance(cls,instance_key):
        return cls.instances[instance_key]    
    
    @classmethod
    def add_self(cls, instance):
        cls.instances[instance.name] = instance

def main():
    for monkey in read_file(example=False):
        Monkey(*process_input(monkey))
    root = Monkey.get_instance('root')
    human = Monkey.get_instance('humn')
    print(root.make_equal())
    

if __name__ == '__main__':
    main()