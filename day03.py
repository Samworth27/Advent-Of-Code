file = open('./day03.txt')


def item_pri(item):
    pri = ord(item)-96
    if pri < 0:
        pri += 58
    return pri


total = 0

for line in file:
    contents = line.strip()
    centerpoint = int((len(contents))/2)
    comp1 = set(contents[:centerpoint])
    comp2 = set(contents[centerpoint:])
    for item in comp1:
        if item in comp2:
            pri = item_pri(item)
            total += pri
            break

print(f'part 1 total: {total}')

file = open('./day03.txt')
total = 0
while (True):
    bag1 = set(file.readline().strip())
    if not bag1:
        print(bag1)
        break
    bag2 = set(file.readline().strip())
    bag3 = set(file.readline().strip())
    for item in bag1:
        if item in bag2:
            if item in bag3:
                print(item, item_pri(item))
                pri = item_pri(item)
                total += pri
                break

print(f'part 2 total: {total}')
