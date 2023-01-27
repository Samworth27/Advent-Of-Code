import math

memo = {}

def factorise(n):
    if n not in memo:
        factors = set()
        limit = math.ceil(math.sqrt(n))
        for i in range(1,limit+1):
            if i in factors:
                break
            if n%i == 0:
                factors.add(i)
                factors.add(n//i)
        memo[n] = factors
    return memo[n]

def gifts(house):
    return sum(factorise(house))*10

def gifts2(house):
    return sum([f*11 for f in factorise(house) if f*50 >= house])

def part1():
    i = 1
    while True:
        g = gifts(i)
        print(f"house {i}, gifts: {g}", end='\r')
        if g >= 34000000:
            break
        i += 1
    print(f"\nPart 1 result: {i}")
    
def part2():
    i = 1
    while True:
        g = gifts2(i)
        print(f"house {i}, gifts: {g}", end='\r')
        if g >= 34000000:
            break
        i += 1
    print(f"\nPart2 result: {i}")


if __name__ == '__main__':
    part1()
    part2()