file = open('day10.txt')

tick = 0
x = 1
score = 0
waiting = False
addx = 0

def calcSpritePos(x):
    sprite_position = ['.' for _ in range(40)]
    sprite_position[x] = '#'
    if x >= 1:
      sprite_position[x-1] = "#"
    if x <= 38:
      sprite_position[x+1] = '#'
    return sprite_position

display_line = ''
sprite_pos = calcSpritePos(x)

while tick <= 240:
    if tick%40 == 0:
      print(display_line)
      display_line = ""
      
    display_line += sprite_pos[tick%40]
    
    
  
  
    if waiting == False:
        line = file.readline().strip().split(' ')
        if len(line) == 2:
            addx = int(line[1])
            # print(f"\nAddX {addx}")
            waiting = True
    else:
        # print("\nwaiting")
        # print(f"adding {addx}")
        x += addx
        waiting = False

    # print(f"\ntick: {tick}\n{x = }\n{addx = }/{waiting = }\n{score = }")
    # input("press enter to continue")
    sprite_pos = calcSpritePos(x)
    tick += 1
