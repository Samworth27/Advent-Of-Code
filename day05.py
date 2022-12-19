file = open('./day05.txt')

stacks = [[] for _ in range(9)]

mode = 'build'
for line in file:
  print('\n',line)
  
  match mode:
    case 'build':
      layer = []
      for i in range(0,9):
        id = line[((i+1)*4)-3]
        if id.isdigit():
          # file.readline()
          mode = 'move'
          file.readline()
          print("Build Complete")
          break
        else:
          layer.append(id)
          print(f'stack {i} = {id}')
          if id != ' ':
            stacks[i].insert(0,id)
    case 'move':
      comd = line.strip().split(' ')
      print(comd)
      count = int(comd[1])
      source = int(comd[3])-1
      dest = int(comd[5])-1
      print(stacks[source])
      items = stacks[source][-count:]
      print(items)
      stacks[source] = stacks[source][:-count]
      stacks[dest].extend(items)
    

for stack in stacks:
  print(stack[-1])