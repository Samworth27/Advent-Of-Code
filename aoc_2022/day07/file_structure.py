from fs_node import FsNode, NodeType
import os

def clear():
    os.system('clear')
    
class FileStructure():
    def __init__(self):
        self._root = FsNode('/', NodeType.root)
        # self._root._nodes['..'] = self._root
        self._current_node: FsNode = self._root
    
    def cmd(self,cmd,*args):
        match cmd:
            case 'cd':
                if len(args) == 0:
                    args = [' ']
                self.cd(*args)
            case 'ls':
                self.ls()
            case 'mkdir':
                self.mkdir(*args)
            case 'mkfile':
                self.mkfile(*args)
            case 'pwd':
                print(self.pwd())
            case 'sml_dirs':
                self.small_dirs(*args)
            case 'find_space':
                self.find_space(*args)
            case 'help':
                self.help(*args)
            case 'clear':
                clear()
            case 'exit':
                return True
            case 'part1':
                self.cd(' ')
                self.small_dirs(100000)
                print("Expected value: 1611433")
            case 'part2':
                self.cd(' ')
                self.find_space(30000000)
                print("Expected value: 2086088")
            
    def cd(self,name):
        if name == ' ':
            self._current_node = self._root
            return None
        if name == '/':
            return None
        if name not in self._current_node.nodes:
            print(f"Directory '{name}' not found")
            input(self.ls())
            return None
        if self._current_node[name].type == NodeType.file:
            return None
        self._current_node = self._current_node[name]
        
    def ls(self):
        if len(self._current_node.children) == 0:
            print(f"━━ {f'{self._current_node.name} ':╌<13} (dir, size={self._current_node.size})", end='')
            return None
        print(f"┏━ {f'{self._current_node.name} ':╌<13} (dir, size={self._current_node.size})", end='')
        for child in self._current_node.children.values():
            print(f"\n┣{'━'*4} {f'{child.name} ':╌<10} ({child.type.name} size={child.size})", end='\r')
        print(f"┗{'━'*4} {f'{child.name} ':╌<10} ({child.type.name} size={child.size})")
        
    def mkdir(self, name: str):
        new_folder = FsNode(name, NodeType.dir, self._current_node)
        self._current_node[name] = new_folder
        

    def mkfile(self, size, name):
        new_file = FsNode(name,NodeType.file,self._current_node,size)
        self._current_node[name] = new_file
        self._update(self._current_node)
        
    def pwd(self, node=None):
        path = []
        if node == None:
            node = self._current_node
        while node.type != NodeType.root:
            path.append(node.name)
            node = node.parent
        path.append('~')
        return '/'.join(reversed(path))
    
    def small_dirs(self,limit, node = None):
        limit = int(limit)
        if node == None:
            node = self._current_node
        results = []
        if node.size <= limit:
            print(f"Node at {self.pwd(node)} is less than or equal to {limit}")
            results.append(node.size)
        for child_dir in node.children_dir.values():
            results.extend(self.small_dirs(limit, child_dir))
        if node == self._current_node:
            print(f"\nSum of all directories less than or equal to {limit} is {sum(results)}")
        return results
    
    def find_space(self, req_space, node = None):
        req_space = int(req_space)
        disk_size = 70000000
        available_space = disk_size - self._root.size
        target = req_space - available_space
        if node == None:
            print(f"Available Space: {available_space}")
            print(f"Deletion Target: {target}")
        if available_space > req_space:
            print("Space is already available")
            return None
        if node == None:
            node = self._current_node
            if node.size < target:
                print("No directories larger than required space found in the current directory")
                return None
        closest = node
        for child_dir in node.children_dir.values():
            child_closest = self.find_space(req_space, node = child_dir)
            if child_closest.size > target:
                if child_closest.size < closest.size:
                    print(f"Directory at {self.pwd(child_closest)} is a new candidate with size of {child_closest.size}")
                    closest = child_closest

        if node  == self._current_node:
            print(f"\nSmallest directory larger than the required space is located at {self.pwd(closest)} and has size of {closest.size}")
        return closest
        
            
    
    def help(self, cmd = None):
        lookup = {
            'cd': "cd [dir] \t\t\t- Changes directory",
            'ls': "ls \t\t\t- List items",
            'mkdir': "mkdir [name] \t\t- Creates new directory",
            'mkfile': "mkfile [size] [name] \t- Creates new file",
            'pwd': "pwd \t\t\t- Prints current path",
            'sml_dirs': "sml_dirs [limit] \t- Returns the sum of all child directories \n\t\t\t\tthat are below the limit in size. \n\t\t\t\tRun from root with a limit of 100000 for part 1 answer",
            'find_space': "find_space [space_required] - Finds the smallest directory larger then the space required\n\t\t\t\tRun from root with a value of 30000000 for the answer to part 2",
            'help': "help [command:optional] - Prints help to screen",
            'clear': "clear \t\t\t - Clears the terminal screen",
            'exit': "exit \t\t\t - Exits the program",
            'part1': 'part1 \t\t\t - Moves to root and runs sml_dirs with the parameters for part 1',
            'part2': 'part2 \t\t\t - Moves to root and runs find_space with the parameters for part 2'
        }
        if cmd == None:
            for line in lookup.values():
                print(line)
            return None
        print(lookup[cmd])
    

        

    
    def _update(self, node):
        node.size = sum([child.size for child in node.children.values()])
        if node.type is not NodeType.root:
            self._update(node.parent)
        
    def __repr__(self):
        return f""