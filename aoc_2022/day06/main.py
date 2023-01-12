from util.inputs import parse_input
from util.windows import sliding_window
from time import sleep

def indexes(i,required_length, data_length):
    index_0 = max(0,i-20-required_length)
    index_1 = max(0,i+1-required_length)
    index_2 = i + 1
    index_3 = min(data_length,i + 20 + (index_0 + 20 +required_length - index_2))
    return index_0, index_1,index_2, index_3

def main(example=False, required_length = 4, visualise = False):
    data = parse_input(example=example)[0]
    data_length = len(data)
    for i, window in enumerate(sliding_window(data,required_length,fixed = False)):
        if visualise:
            index_0,index_1,index_2,index_3 = indexes(i,required_length,data_length)
            print(f"{data[index_0:index_1]}[{data[index_1:index_2]}]{data[index_2:index_3]}", end='\r')
            sleep(0.001)
          
        if len(set(window)) >= required_length:
            if visualise:
                print('\n',' '*(index_1-index_0-1),''.join(window))
            return i+1
        
if __name__ == '__main__':
    print(f"Example result = {main(example=True)} expected 7")
    print(f"Part 1: Result = {main(example=False)} expected 1848")
    print(f"Part 2: Result = {main(example=False, required_length=14, visualise=True)} expected 2308")