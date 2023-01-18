import pygame
from util.vector import Vector
from copy import copy
from random import randint, choice, shuffle
from graph import Node, Edge, Path
from util.windows import sliding_window




def default_step_function(graph, window_size):
    graph.step(window_size)
    
def default_draw_function(graph, screen,window_size):
    pass

def default_mouse1_function(graph,screen,screen_size):
    new_node = Node(f"{randint(0,100000)}-{randint(0,100000)}",random_position(screen_size[0],screen_size[1],10))
    graph.add_node(new_node)
    
def default_mouse2_function(graph,screen,screen_size):
    if len(graph.nodes) >= 2:
        node1 = choice(graph.nodes)
        node2 = node1
        while node2 == node1:
            node2 = choice(graph.nodes)
        new_edge = Edge(randint(10,400),[node1,node2])
        graph.add_edge(new_edge)
    
def default_config():
    return copy(_default_config)

def random_path(nodes, colour, line_width):
    random_nodes = [*nodes]
    shuffle(random_nodes)
    return Path(random_nodes,colour,line_width)

def random_position(width, height, node_size):
    return Vector(randint(node_size, width-node_size), randint(node_size, height-node_size))

def draw_path(surface, path:Path):
    for node1,node2 in sliding_window(path.nodes,2):
        pygame.draw.line(surface,path.colour,node1.position.tuple,node2.position.tuple,path.line_width)
        
_default_config = {
    'window_size': (1000, 1000),
    'node_size': 10,
    'step_func':default_step_function,
    'draw_func': default_draw_function,
    'mouse1_func': default_mouse1_function,
    'mouse2_func': default_mouse2_function,
    
}

def visualise_graph(graph, vis_config=default_config(), max_iterations = 1000, fps=30):
    window_width = vis_config['window_size'][0]
    window_height = vis_config['window_size'][1]
    window_size = (window_width,window_height)
    
    node_size = vis_config['node_size']
    step_func = vis_config['step_func']
    draw_func = vis_config['draw_func']
    mouse1_func = vis_config['mouse1_func']
    mouse2_func = vis_config['mouse2_func']
    
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(vis_config['window_size'])
    pygame.display.set_caption("Advent Of Code 2015 - Day 09")
    screen_centre = Vector(500, 500)
    
    for i in range(30):
        graph.step(window_size)

    run = True
    frame = 0
    while run:
        
        frame += 1
        if frame > max_iterations:
            run = False
            break
        
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        mouse1_func(graph,screen,window_size)
                    case 3:
                        mouse2_func(graph,screen,window_size)

        step_func(graph, window_size)

        for edge in graph.edges:
            node1, node2 = edge.nodes
            pygame.draw.line(screen, (50, 50, 50),
                             node1.position.tuple, node2.position.tuple, 1)
        
        draw_func(graph,screen)
        
            
        for node in graph.nodes:
            pygame.draw.circle(screen, (206, 190, 190),
                               node.position.tuple, vis_config['node_size'])

            

        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()
