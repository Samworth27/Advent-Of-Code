from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from time import sleep




def preprocess(file):
    def preproccessLine(line):
        return [tuple(int(i) for i in step.strip().split(',')) for step in line.strip().split('->')]
    
    def processLine(line):
        vertex1 = None
        rocks = set()
        for vertex2 in line:
            if vertex1 == None:
                vertex1 = vertex2
                continue
            x1, y1 = vertex1
            x2, y2 = vertex2
            xr = range(min(x1,x2),max(x1,x2)+1)
            yr = range(min(y1,y2),max(y1,y2)+1)
            rocks.update([(x,y) for x in xr for y in yr])
            vertex1 = vertex2
        return rocks
            
        
    def minAndMax(elements):
        return (min(elements), max(elements))
    
    cave_map = set()
    
    rocks = [preproccessLine(line) for line in file]      
    
    for line in rocks:
        cave_map.update(processLine(line))
    
    rocks_flattened = [vertex for line in rocks for vertex in line]
    # x_range = minAndMax([vertex[0] for vertex in rocks_flattened])
    y_range = (0, max([vertex[1] for vertex in rocks_flattened]))
    x_range = (500-y_range[1]-2,500+y_range[1]+2)
    
    
    return cave_map, x_range, y_range

def drawMap(rock_map, sand_map, sand, x_range, y_range):
    def getPointValue(x,y):
        rock_colour = 1 #(100,100,100,1)
        sand_colour = 2 #(200,200,200,1)
        air_colour =  0 #(0,0,0,1)
        if (x,y) == sand or (x,y) in sand_map:
            return sand_colour
        elif (x,y) in rock_map:
            return rock_colour
        else:
            return air_colour
        
        
    xr = range(0, x_range[1]+1)
    yr = range(0, y_range[1]+3)
    return [[getPointValue(x,y) for x in xr] for y in yr]


def dropSand(rock_map, sand_map, y_limit):
    def nextStep(sand, rock_map, sand_map):
        sandx, sandy = sand
        
        down = (sandx, sandy+1)
        left = (sandx-1, sandy+1)
        right = (sandx+1, sandy+1)
        
        if down not in rock_map and down not in sand_map and sandy < y_limit+1:
            return down
        elif left not in rock_map and left not in sand_map and sandy < y_limit+1:
            return left
        elif right not in rock_map and right not in sand_map and sandy < y_limit+1:
            return right
        else:
            return sand
                
    sand = (500,0)
    
    while True:


        sand_next = nextStep(sand, rock_map, sand_map)
        if sand_next == (500,0):
            return set()
        if sand_next == sand:
            new_sand_map = sand_map.copy()
            new_sand_map.add(sand)
            return new_sand_map
        sand = sand_next
    

def updateGraph(plot,data):
    plot.set_data([x[300:700] for x in data])
    fig.canvas.flush_events()
 
file = open('day14.txt')
rocks, x_range, y_range = preprocess(file)
   
plt.ion()
fig, ax = plt.subplots()
plt.figure(figsize = (10,10))
plt.register_cmap(cmap=LinearSegmentedColormap.from_list(name='sand',colors=[[0.0,0.0,0.0,1.0],[1.0,0.0,0.0,1.0],[194.0,178.0,128.0,1.0]]))
plot = plt.imshow(drawMap(rocks, set(),(0,0), x_range, y_range), interpolation='nearest', cmap='sand',vmin=0,vmax=2)
plt.show()
updateGraph(plot,drawMap(rocks, set(),(0,0), x_range, y_range))

sand_map = set(())
sand = 0
while True:
    print(f"\n\nsand particle {sand}")
    sand_map = dropSand(rocks, sand_map, y_range[1])
    if len(sand_map) == 0:
        break
    if sand % 100 == 0:
        updateGraph(plot,drawMap(rocks, sand_map, sand, x_range, y_range))
    sand += 1
    

