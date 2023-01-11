# Part 1

# file = open('./day01.txt')
# max_cal = 0
# counting = True
# while(counting):
#   elf_total = 0
#   counting_elf = True
#   while (counting_elf):  
#     data = file.readline()
    
#     if not data:
#       counting = False
#       break
    
#     stripped_data = data.strip()
#     if (stripped_data == ""):
#       counting_elf = False
#       break
#     # print(f"'{stripped_data}'")
#     elf_total += int(stripped_data)
  
#   if(elf_total > max_cal):
#     max_cal = elf_total
    
#   print(f'elf total = {elf_total}, elf max = {max_cal}')
  
# Part 2

file = open('./day01.txt')
top_3 = [0,0,0]
counting = True
while(counting):
  elf_total = 0
  counting_elf = True
  while (counting_elf):  
    data = file.readline()
    
    if not data:
      counting = False
      break
    
    stripped_data = data.strip()
    if (stripped_data == ""):
      counting_elf = False
      break
    # print(f"'{stripped_data}'")
    elf_total += int(stripped_data)
  
  if(elf_total > min(top_3)):
    print("New top 3")
    top_3.append(elf_total)
    top_3.sort(reverse=True)
    top_3.pop()
    
  print(f'elf total = {elf_total}, elf max = {top_3}')
  
print(f"top three = {sum(top_3)}")