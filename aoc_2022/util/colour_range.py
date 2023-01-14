import colorsys


def int_colour_value_to_decimal(x):
    if type(x) == int:
        return x/255
    return x

def int_colour_value_to_decimal(x):
    if type(x) == int:
        return x/255
    return x

def hsl_int_to_decimal(colour_tuple):
    h,s,l = colour_tuple
    if type(h) == int:
        h /= 360
    if type(s) == int:
        s /= 100
    if type(l) == int:
        l /= 100
    return (h,s,l)

def rgb_colour_range(rgb1, rgb2, steps):
    rgb1 = tuple(int_colour_value_to_decimal(i) for i in rgb1)
    rgb2 = tuple(int_colour_value_to_decimal(i) for i in rgb2)
        
    colour_range = []
    for i in range(steps + 1):
        t = i / steps
        colour_range.append(interpolate_hsl(colorsys.rgb_to_hsl(rgb1),colorsys.rgb_to_hsl(rgb2),t))
    return [tuple(int(j*255) for j in i) for i in colour_range]

def hsl_colour_range(hsl1, hsl2, steps):
    hsl1 = hsl_int_to_decimal(hsl1)
    hsl2 = hsl_int_to_decimal(hsl2)
        
    colour_range = []
    for i in range(steps + 1):
        t = i / steps
        colour_range.append(interpolate_hsl(hsl1,hsl2,t))
    return [tuple(int(j*255) for j in i) for i in colour_range]
        

def interpolate_hsl(hsl0, hsl1, t):
    h_0, s_0, l_0 = hsl0
    h_1, s_1, l_1 = hsl1

    hue_separation = h_1 - h_0

    # if h_0 > h_1:
    #     h_0, h_1 = h_1, h_0
    #     hue_seperation = -hue_seperation
    #     t = 1 - t
        
    if hue_separation > 0.5:
        h_0 += 1
        h = (h_0 + t * (h_1 - h_0)) % 1
    if hue_separation <= 0.5:
        h = h_0 + t * hue_separation
        
    s = s_0 + t * (s_1 - s_0)
    l = l_0 + t * (l_1 - l_0)
    return colorsys.hls_to_rgb(h,s,l)
        
