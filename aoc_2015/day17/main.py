import itertools
from aoc_util.inputs import parse_input

containers = parse_input((17,2015),int)
# containers = [20,15,10,5,5]
part1 = sum(sum(sum(j)==150 for j in itertools.combinations(containers,i)) for i in range(1,len(containers)+1))
part2 = list(len([len(j) for j in itertools.combinations(containers,i) if sum(j)==150]) for i in range(1,len(containers)+1))
print(part2)
