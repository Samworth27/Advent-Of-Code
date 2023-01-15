import colorsys


def rgb_int_to_dec(colour_tuple):
    return tuple(i/255 for i in colour_tuple)


def rgb_dec_to_int(colour_tuple):
    return tuple(int(round(i*255)) for i in colour_tuple)


def hsl_dec_to_int(colour_tuple):
    h, s, l = colour_tuple
    h = int(round(h*360))
    s = int(round(s*100))
    l = int(round(l*100))
    return (h, s, l)


def hsl_int_to_dec(colour_tuple):
    h, s, l = colour_tuple
    h /= 360
    s /= 100
    l /= 100
    return (h, s, l)


def rgb_to_hsl(rgb):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return (h, s, l)


def hsl_to_rgb(hsl):
    h, s, l = hsl
    return colorsys.hls_to_rgb(h, l, s)


def rgb_colour_range(rgb1, rgb2, steps):
    rgb1 = tuple(rgb_int_to_dec(i) for i in rgb1)
    rgb2 = tuple(rgb_int_to_dec(i) for i in rgb2)

    colour_range = []
    for i in range(steps + 1):
        t = i / steps
        colour_range.append(interpolate_hsl(
            colorsys.rgb_to_hsl(rgb1), colorsys.rgb_to_hsl(rgb2), t))
    return [tuple(int(j*255) for j in i) for i in colour_range]


def hsl_colour_range(hsl1, hsl2, steps, return_RGB=False):
    
    hsl1 = hsl_int_to_dec(hsl1)
    hsl2 = hsl_int_to_dec(hsl2)
    
    colour_range = []
    for i in range(steps + 1):
        t = i / steps
        colour_range.append(interpolate_hsl(hsl1,hsl2,t))
    if return_RGB:
        colour_range = [rgb_dec_to_int(hsl_to_rgb(i)) for i in colour_range]
    else:
        colour_range = [hsl_dec_to_int(i) for i in colour_range]
    return colour_range


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
    return (h,s,l)
