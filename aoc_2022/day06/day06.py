file = open('day06.txt')
message = file.readline()
req_length = 14
print(message)


for i in range(len(message)-3):
  subset = message[i:i+req_length]
  u_count = len(set(subset))
  print(f'subset: {subset}, unique chars = {u_count}')
  if u_count == req_length:
    print(i+req_length)
    break