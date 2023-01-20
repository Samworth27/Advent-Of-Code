from aoc_util.inputs import parse_input, fields
from aoc_util.graph_modules import Graph, Node, Edge, make_key, visualise_graph, random_position

DAY = 13
YEAR = 2015

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




def main():
    data = parse_input((DAY,YEAR), parse_func)
    nodes, edges = prep_data(data)
    graph = Graph(nodes,edges)
    visualise_graph(graph)
    result1 = None
    result2 = None
    print(f"Part 1 result: {result1}, Part 2 result: {result2}")


if __name__ == '__main__':
    main()
