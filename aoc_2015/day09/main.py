from util.inputs import parse_input, fields
from util.graph import Node, Edge
from graph_vis import visualise_graph, random_position, default_config, draw_path, random_path
from random import randint
from util.graph.tsp_graph import GeneticTSPGraph

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

def random_colour():
    return tuple(randint(0,255) for _ in range(3))

def prep_data(data):
    edges = []
    cities = {}

    for (loc1, loc2, distance) in data:
        for loc in (loc1, loc2):
            if loc not in cities:
                cities[loc] = Node(loc, random_position(
                    WINDOW_WIDTH, WINDOW_HEIGHT, 10))
        edges.append(Edge(distance, [cities[loc1], cities[loc2]]))

    return list(cities.values()), edges


def field_func(x):
    try:
        return int(x)
    except ValueError:
        return x


def parse_func(x):
    return fields(x, [0, 2, 4], ' ', field_func)


def left_click(graph:GeneticTSPGraph,screen,screen_size):
    graph.breed_new_generation()


def graph_step(graph: GeneticTSPGraph, screen_size):
    graph.step(screen_size)
    graph.breed_new_generation()


def vis_step(graph: GeneticTSPGraph, surface):
    # if len(graph.current_generation) > 0:
    #     for path in graph.current_generation:
    #         draw_path(surface, path)
    best = graph.best.copy()
    best_in_gen = graph.best_in_generation().copy()
    best.colour = (248, 51, 60 )
    best_in_gen.colour = (97, 158, 109)
    best.line_width = 15
    best_in_gen.line_width = 3
    draw_path(surface,best_in_gen)
    draw_path(surface,best)



def main():

    GENERATION_SIZE = 50
    MAX_ITERATIONS = 1000
    FPS = 120
    
    config = default_config()
    config['window_size'] = (WINDOW_WIDTH,WINDOW_HEIGHT)
    config['step_func'] = graph_step
    config['draw_func'] = vis_step
    config['mouse1_func'] = left_click
    config['node_size'] = 20
    
    
    data = parse_input(function=parse_func)
    cities, edges = prep_data(data)
    paths = [random_path(cities, random_colour(), 5) for _ in range(GENERATION_SIZE)]
    graph = GeneticTSPGraph(cities, edges, GENERATION_SIZE, paths)
    visualise_graph(graph,config, MAX_ITERATIONS,FPS)
    print(f"Best score: {graph._fitness(graph.best)}")
    print(graph.best)
    


if __name__ == '__main__':
    main()
