import math


class Operation():
    def __init__(self, operator, x):
        self.operator = operator
        if x == 'old':
            self.x = 'old'
        else:
            self.x = int(x)

    def calc(self, old):
        if self.x == 'old':
            x = old
        else:
            x = self.x

        match self.operator:
            case '+':
                return old + x
            case '*':
                return old * x

    def __str__(self):
        return f"new = old {self.operator} {self.x}"


class Test():
    def __init__(self, x, true_target, false_target):
        self.x = x
        self.true_target = true_target
        self.false_target = false_target

    def runTest(self, item_value):
        if item_value % self.x == 0:
            return self.true_target
        else:
            return self.false_target

    def __str__(self):
        return f"if divisible by {self.x} goto {self.true_target} else goto {self.false_target}"


class Item():
    count = 0
    lcm = 0

    def getID():
        id = Item.count
        Item.count += 1
        return id

    def __init__(self, init_worry_value):
        self.worry_value = init_worry_value
        self.id = Item.getID()

    def increase(self, x):
        self.worry_value += x
        return self.worry_value

    def decrease(self):
        self.worry_value = self.worry_value % Item.lcm
        return self.worry_value

    def __str__(self):
        return f"Item {self.id}[{self.worry_value}]"

    def __repr__(self) -> str:
        return str(self)


class Monkey():
    count = 0

    def getID():
        id = Monkey.count
        Monkey.count += 1
        return id

    def __init__(self, items: list, operation, test, monkeys):
        self.id = Monkey.getID()
        self.items = items
        self.operation = operation
        self.test = test
        self.monkeys = monkeys
        self.inspect_count = 0

    def takeTurn(self):
        while len(self.items) > 0:
            item = self.items[0]
            target = self.inspect_item(item)
            self.pass_item(target)

    def inspect_item(self, item):
        self.inspect_count += 1
        item.worry_value = self.operation.calc(item.worry_value)
        item.decrease()
        return self.test.runTest(item.worry_value)

    def pass_item(self, target):
        item = self.items.pop(0)
        self.monkeys[target].receive_item(item)

    def receive_item(self, item):
        self.items.append(item)

    def __str__(self):
        return f"Monkey {self.id}[{self.inspect_count}]: {self.items}"

    def __repr__(self) -> str:
        return f"\n{self}"


file = open('day11.txt')

monkeys = []
items = []
lcm_ints = []

for i in range(8):
    file.readline()
    items = [Item(int(i))
             for i in file.readline().strip().split(':')[1].split(',')]
    # operation
    operation_str = file.readline().strip().split(' ')[-2:]
    operation = Operation(operation_str[0], operation_str[1])
    # test line 1
    test_str = [int(file.readline().strip().split(' ')[-1]) for _ in range(3)]
    test = Test(test_str[0], test_str[1], test_str[2])
    lcm_ints.append(test_str[0])
    monkeys.append(Monkey(items, operation, test, monkeys))
    file.readline()

lcm = math.lcm(*lcm_ints)
Item.lcm = lcm

for i in range(10000):
    if i % 100 == 0:
        print(f"round {i}") 
    for monkey in monkeys:
        monkey.takeTurn()


max_count = [0, 0]
for monkey in monkeys:
    if monkey.inspect_count > min(max_count):
        if monkey.inspect_count > max(max_count):
            max_count.insert(0, monkey.inspect_count)
        else:
            max_count.insert(1, monkey.inspect_count)
        max_count.pop()

print(max_count[0]*max_count[1])
