from PIL import Image, ImageDraw, ImageFont
from math import floor, ceil

OUTER_MARGIN = 5

class Cell:
    def __init__(self, cell_value, cell_fill, cell_outline):
        self.value = cell_value
        self.fill = cell_fill
        self.outline = cell_outline


def visualise_grid(data, cell_size=11, cell_gap=1, inner_percent=10,colour_mode="RGB",) -> Image:
        
    inner_padding = ceil(cell_size*(inner_percent/2)/100)
    
    font = ImageFont.truetype('FreeMono.ttf', cell_size)
    
    
    if type(cell_size) != int:
        raise TypeError
    
    if cell_size % 2 == 0:
        cell_size += 1
        
    num_cells_x = len(data[0])
    num_cells_y = len(data)

    width = (2*OUTER_MARGIN) + (num_cells_x * cell_size) + ((num_cells_x + 1) * cell_gap) + 1
    height = (2*OUTER_MARGIN) + (num_cells_y * cell_size) + ((num_cells_y + 1) * cell_gap) + 1

    output = Image.new(colour_mode, (width, height), (100,100,100))
    
    draw = ImageDraw.Draw(output)
    # draw.polygon([(0,0),(width-1,0),(width-1,height-1),(0,height-1)],fill=None,outline='black',width=1)
    # Checkerboard for debugging    
    # for x in range(height):
    #     for y in range(width):
    #         draw.point((x,y),fill= 'grey' if ((x+y)%2) else 'white')

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            draw_cell(draw,x,y,cell,cell_size,cell_gap,inner_padding,font)
            
    
    
    return draw, output

def draw_cell(image,x,y,cell,cell_size,cell_gap,inner_padding,font):
    
    
    if cell_size % 2 == 0:
        cell_size += 1
        
    x0 = x * cell_size + (cell_gap * (x+1)) + OUTER_MARGIN
    y0 = y * cell_size + (cell_gap * (y+1)) + OUTER_MARGIN
    x1 = x0 + cell_size - 1
    y1 = y0 + cell_size - 1
    
    x0_inner = x0 + inner_padding
    x1_inner = x1 - inner_padding
    y0_inner = y0 + inner_padding
    y1_inner = y1 - inner_padding

    tl = (x0, y0)
    tl_inner = (x0_inner, y0_inner)
    tr = (x1, y0)
    tr_inner = (x1_inner, y0_inner)
    br = (x1, y1)
    br_inner = (x1_inner, y1_inner)
    bl = (x0, y1)
    bl_inner = (x0_inner, y1_inner)

    image.rectangle(((tl, br)), fill=cell.fill)
    image.text(((x0+x1)/2,(y0+y1)/2),cell.value,'black', anchor='mm', font=font)

    if cell.outline == None:
        return image

    top = [tl, tr, tr_inner, tl_inner]
    right = [tr, br, br_inner, tr_inner]
    bottom = [br, bl, bl_inner, br_inner]
    left = [bl, tl, tl_inner, bl_inner]
    sides = [top, right, bottom, left]

    single_colour = True
    
    if type(cell.outline[0]) == tuple:
        single_colour = False

    for i, points in enumerate(sides):
        image.polygon(
            points, fill=cell.outline if single_colour else cell.outline[i])
        
    if not single_colour:
        image.line([tl, tl_inner], fill='black')
        image.line([tr, tr_inner], fill='black')
        image.line([br, br_inner], fill='black')
        image.line([bl, bl_inner], fill='black')

    image.line([tl_inner,tr_inner,br_inner,bl_inner,tl_inner], fill='black')
    
    return image



def update_grid(image,x,y,cell, cell_size,cell_gap,inner_percent):
    inner_padding = ceil(cell_size*(inner_percent/2)/100)
    font = ImageFont.truetype('FreeMono.ttf', cell_size)
    return draw_cell(image,x,y,cell,cell_size,cell_gap,inner_padding,font)
