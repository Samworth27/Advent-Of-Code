from util.inputs import parse_input, fields
from graph import Graph, Node, Edge, Path, make_key
from graph_vis import visualise_graph, random_position, default_config, draw_path, random_path
from random import choice, choices, randint, random

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


def build_short_edges_first(nodes, edges):
    sorted_edges = sorted(edges, key=lambda x: x.weight)
    remaining_nodes = set(nodes)
    node1, node2 = sorted_edges.pop(0).nodes

    new_path = [node1, node2]
    remaining_nodes -= {node1, node2}
    while len(new_path) < len(nodes):
        if len(sorted_edges) > 0:
            node1, node2 = sorted_edges.pop(0).nodes
            if new_path[0] in (node1, node2):
                if new_path[0] == node1 and new_path[-1] != node2:
                    if node2 in remaining_nodes and node2:
                        new_path.insert(0, node2)
                        remaining_nodes -= {node2}
                elif new_path[0] == node2 and new_path[-1] != node1:
                    if node1 in remaining_nodes:
                        new_path.insert(0, node1)
                        remaining_nodes -= {node1}
            elif new_path[-1] in (node1, node2):
                if new_path[-1] == node1 and new_path[0] != node2:
                    if node2 in remaining_nodes:
                        new_path.append(node2)
                        remaining_nodes -= {node2}
                elif new_path[-1] == node2 and new_path[-1] != node1:
                    if node1 in remaining_nodes:
                        new_path.append(node1)
                        remaining_nodes -= {node1}
            else:
                node = choice([*remaining_nodes])
                new_path.append(node)
                remaining_nodes -= {node}
        else:
            node = choice([*remaining_nodes])
            new_path.append(node)
            remaining_nodes -= {node}
    return new_path
#


class TSPGraph(Graph):
    def __init__(self, nodes, edges):
        super().__init__(nodes, edges)

        self.best_path = None
        self.displayed_paths = []


class GeneticTSPGraph(TSPGraph):
    def __init__(self, nodes, edges, generation_size, start_generation:list[Path]):
        super().__init__(nodes, edges)
        self.generation_size = generation_size
        self.current_generation = [*start_generation]
        self.best = self.best_in_generation()

    def best_in_generation(self):
        return min(self.current_generation,key=lambda x:self._fitness(x))
    
    def breed_new_generation(self):
        new_generation = []
        fitness_weights = self._fitness_weights()
        for i in range(self.generation_size-1):
            parent1, parent2 = choices(self.current_generation,fitness_weights,k=2)
            new_generation.append(self.mutate(self.cross_over(parent1,parent2)))
        self.current_generation = new_generation
        if self._fitness(self.best_in_generation()) < self._fitness(self.best):
            self.best = self.best_in_generation()
            
    def _fitness_weights(self):
        max_fitness = self._max_fitness()
        return [self._fitness(x)/max_fitness for x in self.current_generation]
    
    def _fitness(self, path):
        fitness = self.path_length(path)
        return fitness
    
    def _max_fitness(self):
        return max(self._fitness(x) for x in self.current_generation)
    
    def mutate(self,path):
        new_path = path.copy()
        times = randint(0,5)
        for i in range(times):
            if random() < 0.25:
                index1,index2 = choices(list(range(0,len(new_path)-1)),k=2)
                new_path.nodes[index1],new_path.nodes[index2] = new_path.nodes[index2], new_path.nodes[index1]
            else:
                new_path.nodes.append(new_path.nodes.pop(0))
        return new_path

    def cross_over(self, parent1: Path, parent2: Path):
        all_edges = [
            *self.edges_from_path(parent1), *self.edges_from_path(parent2)]
        colour = tuple((a+b)/2 for a,b in zip(parent1.colour,parent2.colour))
        line_width = (parent1.line_width + parent2.line_width)//2
        return Path(build_short_edges_first(parent1.nodes, all_edges),colour,line_width)

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
    best.colour = (0,100,255)
    best_in_gen.colour = (255,0,255)
    draw_path(surface,best_in_gen)
    draw_path(surface,best)



def main():

    GENERATION_SIZE = 30
    MAX_ITERATIONS = 50
    FPS = 2
    
    config = default_config()
    config['window_size'] = (WINDOW_WIDTH,WINDOW_HEIGHT)
    config['step_func'] = graph_step
    config['draw_func'] = vis_step
    config['mouse1_func'] = left_click
    
    
    data = parse_input(function=parse_func)
    cities, edges = prep_data(data)
    paths = [random_path(cities, random_colour(), 5) for _ in range(GENERATION_SIZE)]
    graph = GeneticTSPGraph(cities, edges, GENERATION_SIZE, paths)
    visualise_graph(graph,config, MAX_ITERATIONS,FPS)
    print(f"Best score: {graph._fitness(graph.best)}")
    print(graph.best)
    


if __name__ == '__main__':
    main()
