from aoc_util.inputs import parse_input, fields
from aoc_util.vector import Vector
import pygame
import numpy as np
from random import randint, choice, shuffle, random
import math 
from aoc_util.windows import sliding_window
WINDOW_SIZE = (1000,1000)
NODE_WIDTH = 30

def random_position():
    return Vector(randint(2*NODE_WIDTH,WINDOW_SIZE[0]-(2*NODE_WIDTH)),randint(2*NODE_WIDTH,WINDOW_SIZE[1]-(2*NODE_WIDTH)))

def field_func(x):
    try:
        return int(x)
    except ValueError:
        return x

def make_key(city1, city2):
    return tuple(sorted([city1, city2]))

def build_distance_lookup(data):
    lookup = {}
    all_cities = set()
    for (loc1, loc2, distance) in data:
        lookup[make_key(loc1, loc2)] = distance
        all_cities.update(set([loc1, loc2]))
    return lookup, all_cities

def path_length(path, distances):
    path = [*path]
    node = path.pop(0)
    length = 0
    while len(path) > 0:
        next_node = path.pop(0)
        length += distances[make_key(node,next_node)]
        node = next_node
    return length

def initial_guess(cities, distances):
    sorted_dist = [i[0] for i in sorted(distances.items(),key=lambda x:x[1])]
    nodes = {node.name: node for node in cities}
    city1,city2 = sorted_dist.pop(0)
    cities_list = [nodes[city1],nodes[city2]]
    del nodes[city1]
    del nodes[city2]
    
    while len(nodes) > 0:

        city1,city2 = sorted_dist.pop(0)
        
        if cities_list[0].name in (city1,city2):
            if cities_list[0].name == city1 and cities_list[-1].name != city2:
                if city2 in nodes and city2:
                    cities_list.insert(0,nodes[city2])
                    del nodes[city2]
            elif cities_list[0].name == city2 and cities_list[-1].name != city1:
                if city1 in nodes:
                    cities_list.insert(0,nodes[city1])
                    del nodes[city1]
        elif cities_list[-1].name in (city1,city2):
            if cities_list[-1].name == city1 and cities_list[0].name != city2:
                if city2 in nodes:
                    cities_list.append(nodes[city2])
                    del nodes[city2]
            elif cities_list[-1].name == city2 and cities_list[-1].name != city1:
                if city1 in nodes:
                    cities_list.append(nodes[city1])
                    del nodes[city1]
        else:
            sorted_dist.append((city1,city2))
        
    return cities_list

def swap_vertices(path):
    index0 = 0
    index1 = 0
    path = [*path]
    while(index0 == index1):
        index0 = randint(0,len(path)-1)
        index1 = randint(0,len(path)-1)
    path[index0],path[index1] = path[index1], path[index0]
    return path

def path_names(path):
    return [node.name for node in path]

class Node:
    def __init__(self,name, position):
        self.name = name
        self.connections = set()
        self.position = position
        self.velocity = Vector(0,0)
        self.acceleration = Vector(0,0)
        
    def add_node(self,node):
        if len(self.connections) < 2 and len(node.connections) < 2:
            self.connections.add(node)
            node.connections.add(self)
            
            

def main(distances:dict, cities:set, longest=False):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Advent Of Code 2015 - Day 09")
    screen_centre = Vector(500, 500)

    run = True
    
    print_event = pygame.USEREVENT+1
    
    nodes = {Node(city, random_position()) for city in cities}
    
    area = WINDOW_SIZE[0] * WINDOW_SIZE[1]
    k = math.sqrt(area/len(nodes))/2
    t = 500
    
    def fa(z):
        return (z*z)/k
    def fr(z): 
        if z == 0:
            return 0
        return (k*k)/z
    
    while t > 0.01:
        for node in nodes:
            
            node.velocity = Vector(0,0)
            
            gravity_delta = screen_centre - node.position
            gravity_direction = gravity_delta.normal
            gravity_magnitude = fa(gravity_delta.magnitude)
            gravity_force = gravity_direction * gravity_magnitude
            
            node.velocity += gravity_force
            
            
            for node2 in (nodes-{node}):
                delta = node.position - node2.position
                node.velocity += delta.normal * fr(delta.magnitude)
                
                delta = node.position - node2.position
                # node.velocity -= (delta.normal*fa(delta.magnitude))
                node.velocity += (delta.normal*fa(distances[make_key(node.name,node2.name)])*2)
                
        for node in nodes:
            node.position += node.velocity.normal * min(node.velocity.magnitude,t)
        t = t*0.9
    
    guess = initial_guess(nodes, distances)
    current_guess = guess
    next_guess = guess
    best_guess = guess
    
    temp = 1000
    pygame.time.set_timer(pygame.K_SPACE,100)
    print(path_names(guess))
    while run:
        screen.fill('black')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.K_SPACE:
                print(f"Temperature: {round(temp,1)} swap P: {round(swap_prob,2)}")
                print(f"Current length of global best path:{path_length(path_names(best_guess),distances)}")
                print(f"Current length of local best: {local_length} error from global best:{local_err}")
                print(f"length of current iteration: {next_length} error from global best{next_err}")
                
            # if event.type == pygame.MOUSEBUTTONUP:
        next_guess = swap_vertices(next_guess)
        temp = temp/(1+0.05*t)
        global_length = path_length(path_names(best_guess),distances)
        local_length = path_length(path_names(current_guess),distances)
        next_length = path_length(path_names(next_guess),distances)
        local_err = local_length  #- global_length
        next_err = next_length #- global_length
        if longest:
            if next_length > global_length:
                best_guess = next_guess
        else:
            if next_length < global_length:
                best_guess = next_guess

        if longest:
            swap_prob = min(1,math.exp((next_err - local_err)/ temp))
            if next_err > local_err:
                current_guess = next_guess
            else:
                if swap_prob > random():
                    current_guess = next_guess
        else:
            swap_prob = min(1,math.exp((local_err-next_err)/ temp))
            if next_err < local_err:
                current_guess = next_guess
            else:
                if swap_prob > random():
                    current_guess = next_guess


        
        print([node.name for node in best_guess],global_length)

        
        
        
        
        
        # Draw best guess
        for node1,node2 in sliding_window(best_guess,2):
            pygame.draw.line(screen,(0,255,0),node1.position.tuple,node2.position.tuple,5)
        
        # Draw local best guess
        for node1,node2 in sliding_window(current_guess,2):
            pygame.draw.line(screen,(0,0,255),node1.position.tuple,node2.position.tuple,5)

        # Draw guess
        for node1,node2 in sliding_window(next_guess,2):
            pygame.draw.line(screen,(255,0,0),node1.position.tuple,node2.position.tuple)
        
        for node in nodes:
            pygame.draw.circle(screen,(255,0,0),node.position.tuple,NODE_WIDTH)

        pygame.display.flip()
        
        clock.tick(120)
        
        
        
        
        if temp < 0.1:
            run = False
    pygame.quit()
    return global_length



if __name__ == '__main__':
    distances, cities = build_distance_lookup(parse_input(
        function=lambda x: fields(x, [0, 2, 4], field_func=field_func)))
    
    print(path_length(['Norrath','Faerun','Straylight','Tristram','AlphaCentauri','Snowdin','Arbre','Tambi'],distances))
    # part1 = main(distances, cities)
    # part2 = main(distances, cities, True)
