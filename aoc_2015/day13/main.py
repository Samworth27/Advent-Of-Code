from aoc_util.inputs import parse_input, fields
from aoc_util.windows import sliding_window
from aoc_util.graph_modules import  GeneticTSPGraph, Path, Node, Edge, make_key, visualise_graph, random_position, random_path, default_config, draw_path

DAY = 13
YEAR = 2015

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

def field_func(x):
    try:
        return int(x)
    except ValueError:
        return x


def parse_func(x):
    data = fields(x.strip('.'), [0, 2, 3, 10], field_func=field_func)
    if data.pop(1) == 'lose':
        data[1] *= -1
    return data

# Use non-directed with the weight of the edges being the combined result of happiness from both people


def prep_data(data):
    nodes = {}
    edges = {}
    for row in data:
        node1_name, weight, node2_name = row
        
        # weights vary from -100 to 100 so move them into a positive range to enable visualisation
        weight *= -1
        weight += 100

        for name in (node1_name, node2_name):
            if name not in nodes:
                nodes[name] = Node(name, random_position(1000, 1000, 5))

        node1 = nodes[node1_name]
        node2 = nodes[node2_name]

        edge_key = make_key(node1, node2)
        if edge_key not in edges:
            edges[edge_key] = Edge(0, [node1, node2])
        edges[edge_key].weight += weight
    return list(nodes.values()), list(edges.values())

def left_click(graph: GeneticTSPGraph, screen, screen_size):
    graph.breed_new_generation()


def graph_step(graph: GeneticTSPGraph, screen_size):
    graph.step(screen_size)
    graph.breed_new_generation()


def vis_step(graph: GeneticTSPGraph, surface, screen_size):
    # if len(graph.current_generation) > 0:
    #     for path in graph.current_generation:
    #         draw_path(surface, path)
    best = graph.best.copy()
    best_in_gen = graph.best_in_generation().copy()
    best.colour = (248, 51, 60)
    best_in_gen.colour = (97, 158, 109)
    best.line_width = 15
    best_in_gen.line_width = 3
    draw_path(surface, best_in_gen)
    draw_path(surface, best)


def part1():
    
    config = default_config()
    config = default_config()
    config['window_size'] = (WINDOW_WIDTH, WINDOW_HEIGHT)
    config['step_func'] = graph_step
    config['draw_func'] = vis_step
    config['mouse1_func'] = left_click
    config['node_size'] = 20
    
    
    data = parse_input((DAY,YEAR), parse_func)
    nodes, edges = prep_data(data)
    graph = GeneticTSPGraph(nodes,edges, 50, [random_path(nodes,(255,0,0),5,True) for i in range(50)],True)
    visualise_graph(graph, config)
    result1 = graph.best, (len(nodes)*200) - graph._fitness(graph.best) 
    print(f"Part 1 result: {result1}")
    return result1[1]


def part2():
    config = default_config()
    config = default_config()
    config['window_size'] = (WINDOW_WIDTH, WINDOW_HEIGHT)
    config['step_func'] = graph_step
    config['draw_func'] = vis_step
    config['mouse1_func'] = left_click
    config['node_size'] = 10
    
    
    data = parse_input((DAY,YEAR), parse_func)
    nodes, edges = prep_data(data)
    me = Node('me',random_position(WINDOW_WIDTH,WINDOW_HEIGHT,20))
    for node2 in nodes:
        edges.append(Edge(200,[me,node2]))
    nodes.append(me)
    graph = GeneticTSPGraph(nodes,edges, 50, [random_path(nodes,(255,0,0),5,True) for i in range(50)],True)
    visualise_graph(graph, config,2000,120)
    result2 = graph.best, ((len(nodes)*200) - graph._fitness(graph.best))
    for i,j in sliding_window(graph.best.nodes,2):
        print(i,j,(graph._edges[make_key(i,j)].weight - 200)*-1)
    print(result2[1])
    return result2[1]

if __name__ == '__main__':
    # result1 = part1()
    result2 = part2()