import os
from collections import namedtuple
from pyvis.network import Network

pathNode = namedtuple('pathNode', ('room', 'time'))


def clearDisplay():
    os.system('clear')

def initGraph(file):
    graph_edges = {}
    rates = {}
    valves = set()
    
    for line in file:
        input = [i.strip() for i in line.split(' ')]
        name = input[1]
        rate = int(input[4][5:-1])
        node_edges = [i.strip(',') for i in input[9:]]
        graph_edges[name] = node_edges
        rates[name] = rate
        if rate > 0:
            valves.add(name)
        
    return graph_edges, rates, valves

def floydWarshall(edges, filter_nodes = None):
        
    distances = {x:{y:float('inf') for y in edges} for x in edges}
    
    for node, node_edges in edges.items():
        for node2 in node_edges:
            distances[node][node2] = 1
        distances[node][node] = 0
        
    for k in edges:
        for i in edges:
            for j in edges:
                ij = distances[i][j]
                ik = distances[i][k]
                kj = distances[k][j]
                
                if ij > ik + kj:

                    distances[i][j] = ik + kj

    
    output = {x:{y:distances[x][y] for y in filter_nodes} for x in filter_nodes} or distances

    return output

def dfsPart1(node, valves, time, path = []):
    if path == []:
        path = [pathNode(node,time)]
   
    if len(valves) == 0:
        time = 0

    if time < 0:
        path.pop()
        time = 0
    
    if time == 0:
            
        relief = 0
        for i in path:
            relief += i.time * rates[i.room]
        return relief, path

    best_score = 0
    best_path = []
    
    for i in valves:
        new_time = time - (distance[node][i] + 1)
        new_path = [*path, pathNode(i,new_time)]
        
        new_valves = valves - {i}
        
        bs,bp = dfsPart1(i, new_valves, new_time, new_path)
        if bs > best_score:
            best_score = bs
            best_path = bp

    return best_score, best_path

def dfsPart2(human_path, node, valves, time, path = []):
    if path == []:
        path = [pathNode(node,time)]
   
    if len(valves) == 0:
        time = 0

    if time < 0:
        path.pop()
        time = 0
    
    if time == 0:
            
        relief = 0
        hp = {p.room: p.time for p in human_path}
        ep = {p.room: p.time for p in path}
        rooms = set([*hp,*ep])
        
        for i in rooms:
            if i in hp and i in ep:
                relief += max(hp[i],ep[i]) * rates[i]
            elif i in hp:
                relief += hp[i] * rates[i]
            else:
                relief += ep[i] * rates[i]
        return relief, path

    best_score = 0
    best_path = []
    
    for i in valves:
        new_time = time - (distance[node][i] + 1)
        new_path = [*path, pathNode(i,new_time)]
        
        new_valves = valves - {i}
        
        bs,bp = dfsPart2(human_path,i, new_valves, new_time, new_path)
        if bs > best_score:
            best_score = bs
            best_path = bp

    return best_score, best_path
        



edges, rates, valves = initGraph(open('day16.txt'))
print("Calculating min distances")
distance = floydWarshall(edges,['AA',*valves])
print("Calculating Part 1")
part1_score, part1_path = dfsPart1('AA', valves, 30)
print(f"part 1 : {part1_score}")

print("Calculating Part 2")
print("Calculating human path")
human_score, human_path = dfsPart1('AA', valves, 26)

print(f"part 2 human score: {human_score} path: {human_path}")
print("Calculating Elephant Path")
total_score, elephant_path = dfsPart2(human_path, 'AA', valves, 26 )
print(f"Best score: {total_score}, elephant_path {elephant_path}")





g = Network()
for n in edges:
    highlight = rates[n] > 0 or n == 'AA'
    g.add_node(n,size=20 if highlight else 10, color = 'green' if highlight else 'red')
    
for n1, n1_edges in edges.items():
    for n2 in n1_edges:
        g.add_edge(n1,n2,weight=1)
    


# g.toggle_physics(True)
# g.show('day16.html')