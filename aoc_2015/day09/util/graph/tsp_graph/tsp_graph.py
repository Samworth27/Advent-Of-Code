from ..graph import Graph, Path
from random import choice, choices, randint, random

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