import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from aoc_util.inputs import parse_input, fields

DAY=15
YEAR=2015

properties = parse_input((DAY,YEAR),lambda x: fields(x,[2,4,6,8],' ',lambda y:int(y.strip(','))))
properties_with_calories = parse_input((DAY,YEAR),lambda x: fields(x,[2,4,6,8,10],' ',lambda y:int(y.strip(','))))

def recipe_score(ingredient_counts, ingredients):
    running_totals = [0 for _ in range(len(ingredients[0]))]
    for i,ingredient in enumerate(ingredients):
        for j, property in enumerate(ingredient):
            running_totals[j] += ingredient_counts[i]*property
    running_totals = [max(0,x) for x in running_totals]
    score = 1
    for i in range(4):
        score *= running_totals[i]
    if len(running_totals) == 4:
        return score
    else:
        return score, running_totals[-1]



def candidates(total_required, dimensions):
    grid = np.mgrid[[range(0,total_required+1) for _ in range(dimensions)]]
    options = np.where(sum(grid)==total_required)
    for candidate in zip(*options):
        yield candidate
    
def recipes_with_calories(required_n_calories):
    for candidate in candidates(100,4):
        score, calories = recipe_score(candidate,properties_with_calories)
        if calories == required_n_calories:
            yield score
        

def part1():
    scores = [recipe_score(candidate,properties) for candidate in candidates(100,4)]
    print(max(scores))

def part2():
    print(max(recipes_with_calories(500)))
    
if __name__ == '__main__':
    part1()
    part2()

# data = list(zip(*candidates(TOTAL,4)))

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(xs=data[0],ys=data[1],zs=data[2],alpha=scores)
# plt.show()