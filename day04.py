def process(file_string):
  output = []
  pair = file_string.split(',')
  for section in pair:
    range = [int(i) for i in section.split('-')]
    
    output.append(range)
    
  return output
    
  

file = open('./day04.txt')
line_number = 1
contained_count = 0
overlap_count = 0

for line in file:
  elf1, elf2 = process(line)
  if(elf1[0] < elf2[0]):
    lower = elf1
    upper = elf2
  elif(elf1[0] > elf2[0]):
    lower = elf2
    upper = elf1
  else:
    if(elf1[1] > elf2[1]):
      lower = elf1
      upper = elf2
    else:
      lower = elf2
      upper = elf1
  
  
  hit = False
  
  if(lower[1] >= upper[1]):
    contained_count += 1
    print(f'{line_number:4}: {lower[0]:2} ... [{upper[0]:2}...{upper[1]:2}] ... {lower[1]} ** {contained_count = }')
    hit = True
    
  if(lower[1]>=upper[0]):
    overlap_count += 1
    print(f'{line_number:4}: {lower[0]:2} ... [{upper[0]:2}...{upper[1]:2}] ... {lower[1]} ## {overlap_count = }')
    hit = True
    
  if not hit:
    print(f'{line_number:4}: {lower[0]:2} ... [{upper[0]:2}...{upper[1]:2}] ... {lower[1]}')
    
  line_number += 1
      
print(f'{contained_count = }')
print(f'{overlap_count = }')