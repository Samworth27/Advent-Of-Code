import random

file = open('day16-example.txt')


class Valve():
    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.on = False
        self.tunnels = []

    def accessible_valves(self):
        return [i.other_valve(self) for i in self.tunnels]
    
    def valve_accessible(self, valve):
        for tunnel in self.tunnels:
            if tunnel.other_valve(self) == valve:
                return True
        return False

    def link_valve(self, valve):
        if not self.valve_accessible(valve):
            new_tunnel = Tunnel(self, valve)
            self.tunnels.append(new_tunnel)
            valve.tunnels.append(new_tunnel)

    def __repr__(self):
        return f"{self.name}({self.flow_rate})[{'on' if self.on else 'off'}]"


class Tunnel():
    def __init__(self, valve1, valve2):
        self.valve1 = valve1
        self.valve2 = valve2

    def other_valve(self, entry):
        if entry == self.valve1:
            return self.valve2
        else:
            return self.valve1
    def __repr__(self):
        return (f"{self.valve1.name} -> {self.valve2.name}")

valves = {}
tunnels_to_create = []
for line in file:
    valve_string, tunnel_string = line.strip().split(';')
    valve_name, flow_string = [valve_string.strip().split(' ')[i]
                               for i in [1, -1]]
    flow_rate = int(flow_string.split('=')[-1])
    valves[valve_name] = Valve(valve_name, flow_rate)
    tunnel_connections = [i.strip(',')
                          for i in tunnel_string.strip().split(' ')[4:]]
    tunnels_to_create.append(
        (valve_name, tunnel_connections))


for tunnel_tuple in tunnels_to_create:
    valve1 = tunnel_tuple[0]
    for valve2 in tunnel_tuple[1]:
        valves[valve1].link_valve(valves[valve2])

def randomMove(valve):
    return random.choice(valve.tunnels).other_valve(valve)

def openValve(valve):
    valve.on = True
    return valve
    
def getPressureRelief():
    return sum([valves[i].flow_rate for i in valves if valves[i].on])

def takeAction(random_action=True):
    if random_action:
        if current_valve.on:
            action = randomMove
        else:
            action = random.choice([randomMove,openValve])
    
    return action(current_valve)
        

time = 0
pressure = 0

current_valve = valves['AA']

while time <= 30:
    print(current_valve)
    pressure += getPressureRelief()
    time += 1
    current_valve = takeAction(random_action=True)
    
print(pressure)