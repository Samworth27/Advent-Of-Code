from util.inputs import parse_input, fields
from file_structure import FileStructure

def build_fs(example=False):
    fs = FileStructure()
    for line in parse_input(example=example):
        print(line)
        fields_ = fields(line)
        if fields_[0] == '$':
            if fields_[1] == 'cd':
                fs.cd(fields_[2])
                print(fs.pwd())
            if fields_[1] == 'ls':
                
                continue
        else:
            if fields_[0] == 'dir':
                fs.mkdir(fields_[1])
            else:
                fs.mkfile(int(fields_[0]),fields_[1])
    fs.cd(' ')
    fs.cmd('clear')
    return fs

def run_terminal(file_structure):
    while True:
        prompt = fields(input(f"{file_structure.pwd()}$ "))
        if len(prompt) == 0:
            continue
        if file_structure.cmd(*prompt):
            break   

if __name__ == '__main__':
    test = build_fs(example=True)
    print(f"Example... input 'exit' to continue to real input")
    # run_terminal(test)
    
    real = build_fs(example=False)
    print(f"Input help for help")
    run_terminal(real)
          
    
    
# file = open('day07.txt')

# root = FsNode('root')
# current_node = root

# debug_counter = 0
# debug_limit = 20

# wanted_dir = []
# wanted_dir_sizes = []
# desired_size = 100000

# clear()
# for line in file:
#     # if debug_counter < debug_limit:
#     #     debug_counter += 1
#     # else:
#     #     break
#     instruction = line.strip().split()

#     root.display_tree()

#     if instruction[0] == '$':
#         match instruction[1]:
#             case 'cd':
#                 if instruction[2] == '..':
#                     if current_node.size < desired_size:
#                         wanted_dir.append(current_node)
#                         wanted_dir_sizes.append(current_node.size)
#                 current_node = current_node.cd(instruction[2])
#             case 'ls':
#                 # print(current_node)
#                 pass
#     else:
#         if instruction[0] == 'dir':
#             current_node.create_dir(instruction[1])
#         else:
#             current_node.create_file(instruction[1], instruction[0])
#     # time.sleep(0.001)
#     clear()

# print(f'part 1 answer: {sum(wanted_dir_sizes)}')

# space_available = 70000000
# space_required = 30000000
# space_remaining = space_available - root.size
# target = space_required - space_remaining
# print(f'space remaining = {space_remaining}')
# print(f'additional space required = { target}')


# def calc_diff(node):
#     return node.size - target


# def search_tree(node, closest_match):
#     print(f'searching {node.dir_name}')

#     print(calc_diff(node), calc_diff(closest_match))
#     if calc_diff(node) < calc_diff(closest_match):
#         closest_match = node
#         print("New best")

#     for child in node.children:
#         print(f'evaluating {child}')
#         if child.size > target:
#             closest_child = search_tree(child, closest_match)
#             if calc_diff(closest_child) < calc_diff(closest_match):
#                 closest_match = closest_child
#                 print("new_best")

#     return closest_match


# closest_match = search_tree(root, root)
# print(
#     f'Closest Match is {closest_match} with a size of {closest_match.size} and a difference of {calc_diff(closest_match)}')
