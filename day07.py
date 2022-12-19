import os
import time

def clear():
  os.system('clear')

class node():
    def __init__(self, dir_name) -> None:
        self.dir_name = dir_name
        self.type = 'directory'
        self.size = 0
        self.children = []
        self.parent = None
        self.depth = 1

    def __str__(self):
      return f'Directory {self.dir_name} with {len(self.children)} children\n'
    
    def __repr__(self):
      return str(self)
    
    def select_dir(self, dir_name):
        for child in self.children:
            if child.dir_name == dir_name:
                return child
        return self.create_dir(dir_name)
      
    def create_dir(self,dir_name):
      new_node = node(dir_name)
      new_node.parent = self
      new_node.depth = self.depth + 1
      self.children.append(new_node)
      return new_node
    
    def create_file(self,dir_name,size):
      new_node = node(dir_name)
      new_node.parent = self
      new_node.size = int(size)
      new_node.depth = self.depth + 1
      new_node.type = 'file'
      self.children.append(new_node)
      new_node.update_parent(int(size))
      return new_node
      
    def update_parent(self, size):   
      if self.parent:
        self.parent.size += size
        self.parent.update_parent(size)
      

    def cd(self, dir_name):
        if dir_name == '..':
            return self.parent
        else:
            return current_node.select_dir(dir_name)
          
    def display_tree(self):
      print(f'{" "*(self.depth-1)} {self.dir_name} [size: {self.size}]')
      for child in self.children:
        child.display_tree()


file = open('day07.txt')

root = node('root')
current_node = root

debug_counter = 0
debug_limit = 20

wanted_dir = []
wanted_dir_sizes = []
desired_size = 100000

clear()
for line in file:
    # if debug_counter < debug_limit:
    #     debug_counter += 1
    # else:
    #     break
    instruction = line.strip().split()

    root.display_tree()

    if instruction[0] == '$':
        match instruction[1]:
            case 'cd':
                if instruction[2] == '..':
                  if current_node.size < desired_size:
                    wanted_dir.append(current_node)
                    wanted_dir_sizes.append(current_node.size)
                current_node = current_node.cd(instruction[2])
            case 'ls':
                # print(current_node)
                pass
    else:
      if instruction[0] == 'dir':
        current_node.create_dir(instruction[1])
      else:
        current_node.create_file(instruction[1], instruction[0])
    # time.sleep(0.001)
    clear()

print(f'part 1 answer: {sum(wanted_dir_sizes)}')

space_available = 70000000
space_required = 30000000
space_remaining = space_available - root.size
target = space_required - space_remaining
print(f'space remaining = {space_remaining}')
print(f'additional space required = { target}')


def calc_diff(node):
  return node.size - target

def search_tree(node, closest_match):
  print(f'searching {node.dir_name}')
  
  print(calc_diff(node), calc_diff(closest_match))
  if calc_diff(node) < calc_diff(closest_match):
    closest_match = node
    print("New best")
  
  for child in node.children:
    print(f'evaluating {child}')
    if child.size > target:
      closest_child = search_tree(child, closest_match)
      if calc_diff(closest_child) < calc_diff(closest_match):
        closest_match = closest_child
        print("new_best")
  
  return closest_match
    

closest_match = search_tree(root, root)
print(f'Closest Match is {closest_match} with a size of {closest_match.size} and a difference of {calc_diff(closest_match)}')