color_bgr_dict = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'red': (0, 0, 255),
    'deep_red': (0, 0, 200),
    'orange': (0, 165, 255),
    'yellow': (0, 255, 255),
    'purple': (128, 0, 128),
    'pink': (203, 192, 255),
    'brown': (42, 42, 165),
    'gray': (128, 128, 128),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'cyan': (255, 255, 0),
    'magenta': (255, 0, 255),
}


def get_color_bgr(color):
    if not color: 
        return (0, 0, 200)  
    
    bgr = color_bgr_dict.get(color.lower(), (0, 0, 200))
    return bgr

