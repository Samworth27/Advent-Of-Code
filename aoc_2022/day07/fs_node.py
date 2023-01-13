from enum import Enum

class NodeType(Enum):
    root = 0
    dir = 1
    file = 2

class FsNode():
    def __init__(self, dir_name, type_, parent=None, size=0) -> None:
        self.name = dir_name
        self.type = type_
        self.size = size
        if parent == None:
            parent = self
        self._nodes = {'..': parent}
        
    @property
    def nodes(self):
        return list(self._nodes.keys())
    
    @property
    def parent(self):
        return self._nodes['..']
    
    @property
    def children(self):
        return {key:node for key,node in self._nodes.items() if key != '..'}
    
    @property
    def children_dir(self):
        return {key:node for key,node in self._nodes.items() if key != '..' and node.type == NodeType.dir}
    def __getitem__(self, node):
        if node in self.nodes:
            return self._nodes[node]
    
    def __setitem__(self, node, value):
        self._nodes[node] = value

    def __str__(self):
        return f"{self.name} ({self.type.name}{f', size={self.size}' if self.size > 0 else ''})"
    
    def __repr__(self):
        return f"Node [{self.name}]"

    def update_parent(self, size):
        if self.parent:
            self.parent.size += size
            self.parent.update_parent(size)