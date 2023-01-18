from util.vector import Vector
from util.windows import sliding_window

def make_key(node1, node2):
    return tuple(sorted([node1.name, node2.name]))


class Node:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.velocity = Vector(0, 0)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Node[{str(self)}]"
        
    def __hash__(self):
        return hash(self.name)


class Edge:
    def __init__(self, weight, nodes: list[Node, Node]):
        self.weight = weight
        self.nodes = set(nodes)
        
    def __repr__(self):
        return f"{self.nodes}: {self.weight}"


class Graph:
    def __init__(self, nodes, edges):
        self._nodes = {node.name: node for node in nodes}
        self._edges = {make_key(*edge.nodes): edge for edge in edges}
        self._init_frames = 30

    def step(self,window_size):
        visual_factor = 4
        stiffness = 0.7
        dampening = 2
        for edge in self.edges:
            node1, node2 = edge.nodes
            delta = node1.position - node2.position
            force = delta.normal*stiffness*(delta.magnitude - edge.weight * visual_factor)
            node1.velocity -= force
            node2.velocity += force

        for node in self.nodes:
            gravity_delta =  Vector(window_size[0]/2,window_size[1]/2) - node.position
            gravity_direction = gravity_delta.normal
            gravity_magnitude = gravity_delta.magnitude
            gravity_force = gravity_direction * gravity_magnitude
            
            node.velocity += gravity_force
            node.velocity /= (1+dampening)
            node.position += node.velocity

    def add_node(self, new_node):
        if new_node.name in self._nodes:
            return None
        self._nodes[new_node.name] = new_node
        return self._nodes[new_node.name]

    def add_edge(self, new_edge):
        new_key = make_key(*new_edge.nodes)
        if new_key in self._edges:
            return None
        self._edges[new_key] = new_edge
        return self._edges[new_key]
    
    def path_length(self, path):
        length = 0
        path = [*path.nodes]
        node = path.pop(0)
        while len(path) > 0:
            next_node = path.pop(0)
            edge_length = self._edges[make_key(node,next_node)].weight
            length += edge_length
            node = next_node
        return length
    
    def edges_from_path(self,path):
        edges = []
        for node1,node2 in sliding_window(path.nodes,2):
            edges.append(self._edges[make_key(node1,node2)])
        return edges
    
    @property
    def nodes(self):
        return list(self._nodes.values())

    @property
    def edges(self):
        return list(self._edges.values())


class Path:
    def __init__(self, nodes:list, colour:tuple[int,int,int], line_width:int):
        self.nodes = nodes
        self.colour = colour
        self.line_width = line_width
        
    def __len__(self):
        return len(self.nodes)
    
    def __str__(self):
        return str(self.nodes)
    
    def __repr__(self):
        return f"Path[{str(self)}]"
    
    def copy(self):
        return Path([*self.nodes],self.colour,self.line_width)
