from util.colour_range import hsl_colour_range
from util.visualise_grid import Cell, visualise_grid
import numpy as np
import cv2

GOOD = (0, 200, 50)
BAD = (255, 0, 0)
HIGH1 = (255, 133, 82)
HIGH2 = (233, 215, 88)
fill_lookup = hsl_colour_range((84, 30, 40), (108, 40, 50), 10)

def pick_colour(point):
    if point[1]:
        return HIGH1
    if point[2]:
        return HIGH2
    if point[3] == None:
        return None
    if point[3] == True:
        return GOOD
    if point[3] == False:
        return BAD
    return None

def prep_point(point):
    # four_sides = tuple(
    #     GOOD if dir else BAD for dir in point.visible_from.values())
    single_border =  pick_colour((None,point._highlight1,point._highlight2,point._is_visible))
    return Cell('', fill_lookup[point.height], single_border)

def prep_point_2(*point):
    border = pick_colour(point)
    return Cell('',fill_lookup[point[0]], border)

def create_visualisation(history, cell_size):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    first_frame = visualise_grid(history[0],cell_size)
    first_frame.save('./.output/start.png')
    first_frame = np.array(first_frame)[:,:,::-1]
    width, height, _ = first_frame.shape
    video = cv2.VideoWriter('output.avi',fourcc,10,(width, height))
    video.write(first_frame)
    for i, state in enumerate(history):
        print(f"Processing frame {i}/ {len(history)}")
        image = visualise_grid(state, cell_size)
        image.save(f"./.output/{i}.png")
        frame = np.array(image)[:,:,::-1]
        video.write(frame)
    cv2.destroyAllWindows
    video.release()
