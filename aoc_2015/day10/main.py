from util.inputs import parse_input
import re

def look_and_say(input):
    groups = re.findall(r"((.)\2+)|(\d)", input)
    output = ''
    for group in groups:
        if group[0] != '':
            output += f"{len(group[0])}{group[1]}"
        else:
            output += f"1{group[2]}"
    return output
        

def test():
    for data, expected in zip(parse_input(True,'example'),parse_input(True,'expected')):
        result = look_and_say(data)
        print(f"Result: {result}, expected: {expected}, match = {result == expected}")
    
def look_and_say_n(input,steps):
    
    for i in range(steps):
        input = look_and_say(input)
        
    return input

def main():
    data = parse_input()[0]
    result1 = len(look_and_say_n(data,40))
    result2 = len(look_and_say_n(data,50))
    print(f"Part 1 result: {result1}, Part 2 result: {result2}")
    
if __name__ == '__main__':
    # test()
    main()