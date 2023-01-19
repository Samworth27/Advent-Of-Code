from aoc_util.inputs import parse_input
from hashlib import md5


def process(input:str):
    five = '00000'
    six = '000000'
    five_at = None
    i = 0
    while True: 
        first_five = md5((input + str(i)).encode("utf-8")).hexdigest()[:5]
        if first_five == five:
            five_at = i
            print(f"Five found at {i}")
            break
        i += 1
    while True: 
        first_six = md5((input + str(i)).encode("utf-8")).hexdigest()[:6]
        if first_six == six:
            print(f"Six found at {i}")
            return(five_at, i)
        i += 1

def test():
    for data, expected1 in zip(parse_input(True,'example'),parse_input(True,'expected')):
        result1, result2 = process(data)
        print(f"Part 1 result: {result1}, expected: {expected1}, match = {result1 == int(expected1)}")
    
def main():
    for data in parse_input():
        result1,result2 = process(data)
        print(f"Part 1 result: {result1}, Part 2 result: {result2}")
    
if __name__ == '__main__':
    test()
    main()